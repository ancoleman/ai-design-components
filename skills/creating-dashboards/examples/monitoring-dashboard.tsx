import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Cpu, HardDrive, Wifi } from 'lucide-react';

/**
 * System Monitoring Dashboard
 *
 * Real-time infrastructure monitoring with:
 * - Gauge widgets for CPU, memory, disk
 * - Live request rate chart (SSE updates)
 * - Alert indicators for threshold breaches
 * - Color-coded health status
 */

interface GaugeProps {
  title: string;
  value: number;
  max: number;
  unit: string;
  icon: React.ReactNode;
}

function Gauge({ title, value, max, unit, icon }: GaugeProps) {
  const percentage = (value / max) * 100;
  const color =
    percentage >= 90 ? '#ef4444' :
    percentage >= 70 ? '#f59e0b' :
    '#10b981';

  return (
    <div style={{
      backgroundColor: '#fff',
      border: '1px solid #e2e8f0',
      borderRadius: '12px',
      padding: '24px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
        <div style={{ color: '#64748b' }}>{icon}</div>
        <span style={{ fontSize: '14px', fontWeight: 500, color: '#64748b' }}>{title}</span>
      </div>

      <div style={{ position: 'relative', width: '100%', height: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {/* Gauge background */}
        <svg width="100%" height="100%" viewBox="0 0 200 120">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="12"
            strokeLinecap="round"
          />
          {/* Value arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={`${percentage * 2.5} 251`}
          />
        </svg>

        <div style={{ position: 'absolute', textAlign: 'center' }}>
          <div style={{ fontSize: '32px', fontWeight: 700, color }}>
            {value.toFixed(1)}
            <span style={{ fontSize: '20px', color: '#64748b' }}>{unit}</span>
          </div>
          <div style={{ fontSize: '14px', color: '#94a3b8' }}>
            of {max}{unit}
          </div>
        </div>
      </div>
    </div>
  );
}

export function MonitoringDashboard() {
  const [metricsData, setMetricsData] = useState([
    { time: '10:00', requests: 1200 },
    { time: '10:05', requests: 1350 },
    { time: '10:10', requests: 1180 },
    { time: '10:15', requests: 1420 },
    { time: '10:20', requests: 1560 },
    { time: '10:25', requests: 1380 },
  ]);

  // Simulate real-time updates (replace with actual SSE)
  useEffect(() => {
    const interval = setInterval(() => {
      setMetricsData((prev) => {
        const newData = [...prev.slice(1)];
        const lastTime = prev[prev.length - 1].time;
        const [hours, minutes] = lastTime.split(':').map(Number);
        const newMinutes = (minutes + 5) % 60;
        const newTime = `${hours}:${newMinutes.toString().padStart(2, '0')}`;

        newData.push({
          time: newTime,
          requests: Math.floor(1000 + Math.random() * 600),
        });

        return newData;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '24px', backgroundColor: '#f8fafc', minHeight: '100vh' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '30px', fontWeight: 700, color: '#0f172a' }}>
          System Monitoring
        </h1>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 16px',
          backgroundColor: '#10b981',
          borderRadius: '8px',
          color: '#fff',
          fontSize: '14px',
          fontWeight: 600,
        }}>
          <div style={{ width: '8px', height: '8px', backgroundColor: '#fff', borderRadius: '50%' }} />
          All Systems Operational
        </div>
      </div>

      {/* Gauge Widgets */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '16px',
        marginBottom: '24px',
      }}>
        <Gauge
          title="CPU Usage"
          value={45.2}
          max={100}
          unit="%"
          icon={<Cpu size={20} />}
        />
        <Gauge
          title="Memory Usage"
          value={68.5}
          max={100}
          unit="%"
          icon={<HardDrive size={20} />}
        />
        <Gauge
          title="Disk Usage"
          value={52.3}
          max={100}
          unit="%"
          icon={<HardDrive size={20} />}
        />
        <Gauge
          title="Network I/O"
          value={234}
          max={1000}
          unit=" Mbps"
          icon={<Wifi size={20} />}
        />
      </div>

      {/* Request Rate Chart */}
      <div style={{
        backgroundColor: '#fff',
        border: '1px solid #e2e8f0',
        borderRadius: '12px',
        padding: '24px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Activity size={20} color="#64748b" />
          <h2 style={{ fontSize: '18px', fontWeight: 600, color: '#0f172a', margin: 0 }}>
            Request Rate (Real-time)
          </h2>
          <div style={{
            marginLeft: 'auto',
            padding: '4px 12px',
            backgroundColor: '#eff6ff',
            borderRadius: '6px',
            fontSize: '12px',
            color: '#3b82f6',
            fontWeight: 600,
          }}>
            LIVE
          </div>
        </div>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={metricsData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="time" stroke="#64748b" />
            <YAxis stroke="#64748b" label={{ value: 'Requests', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
              }}
            />
            <Line
              type="monotone"
              dataKey="requests"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default MonitoringDashboard;
