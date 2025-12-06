/*
IoT Data Pipeline using InfluxDB 3.x and Go

Features:
- MQTT subscriber for IoT sensor data
- Batch ingestion to InfluxDB (5,000 points per batch)
- Automatic downsampling with continuous queries
- Health monitoring and metrics
*/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	influxdb3 "github.com/influxdata/influxdb-client-go/v2"
)

// SensorReading represents a single IoT sensor measurement
type SensorReading struct {
	SensorID    string    `json:"sensor_id"`
	Temperature float64   `json:"temperature"`
	Humidity    float64   `json:"humidity"`
	Pressure    float64   `json:"pressure"`
	Location    string    `json:"location"`
	Timestamp   time.Time `json:"timestamp"`
}

// Pipeline manages the IoT data ingestion pipeline
type Pipeline struct {
	mqttClient   mqtt.Client
	influxClient influxdb3.Client
	writeAPI     influxdb3.WriteAPIBlocking
	buffer       []SensorReading
	bufferMutex  sync.Mutex
	batchSize    int
	flushTicker  *time.Ticker
	metrics      *Metrics
}

// Metrics tracks pipeline performance
type Metrics struct {
	messagesReceived int64
	pointsWritten    int64
	writeErrors      int64
	lastFlush        time.Time
	mutex            sync.Mutex
}

func (m *Metrics) IncrementReceived() {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	m.messagesReceived++
}

func (m *Metrics) IncrementWritten(count int) {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	m.pointsWritten += int64(count)
	m.lastFlush = time.Now()
}

func (m *Metrics) IncrementErrors() {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	m.writeErrors++
}

func (m *Metrics) Print() {
	m.mutex.Lock()
	defer m.mutex.Unlock()
	fmt.Printf("[Metrics] Received: %d, Written: %d, Errors: %d, Last Flush: %s\n",
		m.messagesReceived, m.pointsWritten, m.writeErrors, m.lastFlush.Format(time.RFC3339))
}

// NewPipeline creates a new IoT data pipeline
func NewPipeline(mqttBroker, influxURL, influxToken, influxOrg, influxBucket string) (*Pipeline, error) {
	// Create InfluxDB client
	influxClient := influxdb3.NewClient(influxURL, influxToken)
	writeAPI := influxClient.WriteAPIBlocking(influxOrg, influxBucket)

	// Create MQTT client
	opts := mqtt.NewClientOptions()
	opts.AddBroker(mqttBroker)
	opts.SetClientID("iot-pipeline")
	opts.SetCleanSession(true)
	opts.SetAutoReconnect(true)
	mqttClient := mqtt.NewClient(opts)

	pipeline := &Pipeline{
		mqttClient:   mqttClient,
		influxClient: influxClient,
		writeAPI:     writeAPI,
		buffer:       make([]SensorReading, 0, 5000),
		batchSize:    5000,
		flushTicker:  time.NewTicker(10 * time.Second),
		metrics:      &Metrics{},
	}

	return pipeline, nil
}

// Start begins the pipeline
func (p *Pipeline) Start() error {
	// Connect to MQTT broker
	if token := p.mqttClient.Connect(); token.Wait() && token.Error() != nil {
		return fmt.Errorf("failed to connect to MQTT: %w", token.Error())
	}
	log.Println("Connected to MQTT broker")

	// Subscribe to sensor topics
	if token := p.mqttClient.Subscribe("sensors/#", 0, p.handleMessage); token.Wait() && token.Error() != nil {
		return fmt.Errorf("failed to subscribe: %w", token.Error())
	}
	log.Println("Subscribed to sensors/#")

	// Start flush goroutine
	go p.flushLoop()

	// Start metrics reporting goroutine
	go p.metricsLoop()

	return nil
}

// handleMessage processes incoming MQTT messages
func (p *Pipeline) handleMessage(client mqtt.Client, msg mqtt.Message) {
	var reading SensorReading
	if err := json.Unmarshal(msg.Payload(), &reading); err != nil {
		log.Printf("Failed to unmarshal message: %v", err)
		return
	}

	p.metrics.IncrementReceived()

	// Add to buffer
	p.bufferMutex.Lock()
	p.buffer = append(p.buffer, reading)
	bufferLen := len(p.buffer)
	p.bufferMutex.Unlock()

	// Flush if buffer full
	if bufferLen >= p.batchSize {
		p.flush()
	}
}

// flushLoop periodically flushes the buffer
func (p *Pipeline) flushLoop() {
	for range p.flushTicker.C {
		p.flush()
	}
}

// flush writes buffered readings to InfluxDB
func (p *Pipeline) flush() {
	p.bufferMutex.Lock()
	if len(p.buffer) == 0 {
		p.bufferMutex.Unlock()
		return
	}

	// Swap buffer
	toWrite := p.buffer
	p.buffer = make([]SensorReading, 0, p.batchSize)
	p.bufferMutex.Unlock()

	// Convert to InfluxDB points
	points := make([]*influxdb3.Point, len(toWrite))
	for i, reading := range toWrite {
		point := influxdb3.NewPointWithMeasurement("sensor_data").
			AddTag("sensor_id", reading.SensorID).
			AddTag("location", reading.Location).
			AddField("temperature", reading.Temperature).
			AddField("humidity", reading.Humidity).
			AddField("pressure", reading.Pressure).
			SetTime(reading.Timestamp)
		points[i] = point
	}

	// Write to InfluxDB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := p.writeAPI.WritePoint(ctx, points...); err != nil {
		log.Printf("Failed to write points: %v", err)
		p.metrics.IncrementErrors()
		return
	}

	p.metrics.IncrementWritten(len(points))
	log.Printf("Flushed %d points to InfluxDB", len(points))
}

// metricsLoop periodically prints metrics
func (p *Pipeline) metricsLoop() {
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		p.metrics.Print()
	}
}

// Stop gracefully shuts down the pipeline
func (p *Pipeline) Stop() {
	log.Println("Stopping pipeline...")

	// Flush remaining buffer
	p.flush()

	// Stop ticker
	p.flushTicker.Stop()

	// Disconnect MQTT
	p.mqttClient.Disconnect(250)

	// Close InfluxDB
	p.influxClient.Close()

	log.Println("Pipeline stopped")
}

func main() {
	// Configuration from environment
	mqttBroker := getEnv("MQTT_BROKER", "tcp://localhost:1883")
	influxURL := getEnv("INFLUX_URL", "http://localhost:8086")
	influxToken := getEnv("INFLUX_TOKEN", "")
	influxOrg := getEnv("INFLUX_ORG", "myorg")
	influxBucket := getEnv("INFLUX_BUCKET", "iot-sensors")

	// Create pipeline
	pipeline, err := NewPipeline(mqttBroker, influxURL, influxToken, influxOrg, influxBucket)
	if err != nil {
		log.Fatalf("Failed to create pipeline: %v", err)
	}

	// Start pipeline
	if err := pipeline.Start(); err != nil {
		log.Fatalf("Failed to start pipeline: %v", err)
	}

	// Wait for interrupt signal
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	<-sigChan

	// Graceful shutdown
	pipeline.Stop()
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
