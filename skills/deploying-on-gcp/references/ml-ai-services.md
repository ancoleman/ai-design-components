# GCP ML/AI Services Reference

Patterns for Vertex AI, AutoML, and pre-trained AI services.

## Table of Contents

1. [Vertex AI](#vertex-ai)
2. [AutoML](#automl)
3. [Pre-trained APIs](#pre-trained-apis)
4. [TPUs](#tpus)

---

## Vertex AI

### Custom Training Job

```python
from google.cloud import aiplatform

aiplatform.init(
    project='project-id',
    location='us-central1',
    staging_bucket='gs://my-bucket'
)

# Create custom training job
job = aiplatform.CustomTrainingJob(
    display_name='custom-training-job',
    script_path='train.py',
    container_uri='gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest',
    requirements=['pandas==2.0.0', 'scikit-learn==1.3.0'],
    model_serving_container_image_uri='gcr.io/cloud-aiplatform/prediction/pytorch-gpu.1-13:latest',
)

# Run training
model = job.run(
    dataset=dataset,
    replica_count=1,
    machine_type='n1-standard-8',
    accelerator_type='NVIDIA_TESLA_V100',
    accelerator_count=1,
    model_display_name='my-model',
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
)

# Deploy model
endpoint = model.deploy(
    deployed_model_display_name='deployed-model',
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=10,
    accelerator_type='NVIDIA_TESLA_T4',
    accelerator_count=1,
)

# Make prediction
prediction = endpoint.predict(instances=[[5.1, 3.5, 1.4, 0.2]])
```

### Vertex AI Pipelines

```python
from kfp.v2 import dsl
from kfp.v2.dsl import component, pipeline

@component(base_image='python:3.9')
def preprocess_data(input_path: str, output_path: str):
    import pandas as pd
    df = pd.read_csv(input_path)
    # Preprocessing logic
    df.to_csv(output_path, index=False)

@component(base_image='gcr.io/cloud-aiplatform/training/pytorch-gpu.1-13:latest')
def train_model(data_path: str, model_path: str):
    # Training logic
    pass

@pipeline(name='ml-pipeline')
def ml_pipeline(input_path: str):
    preprocess_task = preprocess_data(input_path=input_path, output_path='/tmp/processed.csv')
    train_task = train_model(data_path=preprocess_task.output, model_path='/tmp/model')

# Compile and run
from kfp.v2 import compiler
compiler.Compiler().compile(pipeline_func=ml_pipeline, package_path='pipeline.json')

from google.cloud import aiplatform
aiplatform.PipelineJob(
    display_name='ml-pipeline-run',
    template_path='pipeline.json',
    parameter_values={'input_path': 'gs://bucket/data.csv'}
).run()
```

---

## AutoML

### AutoML Tables (Structured Data)

```python
from google.cloud import aiplatform

# Create dataset
dataset = aiplatform.TabularDataset.create(
    display_name='sales-predictions',
    gcs_source='gs://bucket/sales_data.csv',
)

# Train AutoML model
job = aiplatform.AutoMLTabularTrainingJob(
    display_name='automl-sales-job',
    optimization_prediction_type='regression',
    optimization_objective='minimize-rmse',
)

model = job.run(
    dataset=dataset,
    target_column='sales_amount',
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
    model_display_name='sales-prediction-model',
    budget_milli_node_hours=8000,  # 8 hours
)
```

### AutoML Vision

```python
# Create image dataset
dataset = aiplatform.ImageDataset.create(
    display_name='product-classification',
    gcs_source='gs://bucket/images.csv',  # CSV with image paths and labels
)

# Train image classification model
job = aiplatform.AutoMLImageTrainingJob(
    display_name='automl-image-job',
    prediction_type='classification',
    multi_label=False,
)

model = job.run(
    dataset=dataset,
    model_display_name='product-classifier',
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
    budget_milli_node_hours=20000,  # 20 hours
)

# Deploy and predict
endpoint = model.deploy(machine_type='n1-standard-4')
prediction = endpoint.predict(instances=[{'content': 'gs://bucket/test_image.jpg'}])
```

---

## Pre-trained APIs

### Vision API

```python
from google.cloud import vision

client = vision.ImageAnnotatorClient()

# Image from GCS
image = vision.Image()
image.source.image_uri = 'gs://bucket/image.jpg'

# Or from local file
with open('image.jpg', 'rb') as f:
    content = f.read()
image = vision.Image(content=content)

# Label detection
response = client.label_detection(image=image)
for label in response.label_annotations:
    print(f'{label.description}: {label.score}')

# Text detection (OCR)
response = client.text_detection(image=image)
print(response.full_text_annotation.text)

# Face detection
response = client.face_detection(image=image)
for face in response.face_annotations:
    print(f'Joy: {face.joy_likelihood}')
    print(f'Sorrow: {face.sorrow_likelihood}')

# Object localization
response = client.object_localization(image=image)
for obj in response.localized_object_annotations:
    print(f'{obj.name}: {obj.score}')
```

### Natural Language API

```python
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

text = "Google Cloud Platform provides powerful AI services."
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Sentiment analysis
sentiment = client.analyze_sentiment(document=document).document_sentiment
print(f'Sentiment score: {sentiment.score}')
print(f'Sentiment magnitude: {sentiment.magnitude}')

# Entity extraction
response = client.analyze_entities(document=document)
for entity in response.entities:
    print(f'{entity.name}: {entity.type_}')

# Syntax analysis
response = client.analyze_syntax(document=document)
for token in response.tokens:
    print(f'{token.text.content}: {token.part_of_speech.tag}')
```

### Translation API

```python
from google.cloud import translate_v2

client = translate_v2.Client()

# Translate text
result = client.translate('Hello, world!', target_language='es')
print(result['translatedText'])  # "¡Hola Mundo!"

# Detect language
result = client.detect_language('Bonjour')
print(result['language'])  # 'fr'

# Get supported languages
languages = client.get_languages()
for language in languages:
    print(f'{language["name"]}: {language["language"]}')
```

### Speech-to-Text

```python
from google.cloud import speech

client = speech.SpeechClient()

# Audio from GCS
audio = speech.RecognitionAudio(uri='gs://bucket/audio.wav')

# Or from local file
with open('audio.wav', 'rb') as f:
    content = f.read()
audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
    enable_automatic_punctuation=True,
)

# Synchronous recognition (< 60 seconds)
response = client.recognize(config=config, audio=audio)
for result in response.results:
    print(result.alternatives[0].transcript)

# Long audio recognition
operation = client.long_running_recognize(config=config, audio=audio)
response = operation.result(timeout=300)
```

---

## TPUs

### Cloud TPU Configuration

```hcl
resource "google_tpu_node" "tpu" {
  name               = "ml-tpu"
  zone               = "us-central1-a"
  accelerator_type   = "v3-8"  # 8 cores
  tensorflow_version = "2.12.0"
  network            = google_compute_network.main.id
  cidr_block         = "10.0.0.0/29"

  scheduling_config {
    preemptible = false
  }

  labels = {
    environment = "production"
  }
}
```

### TPU Training Example

```python
import tensorflow as tf

# TPU initialization
resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='ml-tpu')
tf.config.experimental_connect_to_cluster(resolver)
tf.tpu.experimental.initialize_tpu_system(resolver)
strategy = tf.distribute.TPUStrategy(resolver)

# Model training with TPU
with strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

# Train on TPU
model.fit(train_dataset, epochs=10, validation_data=val_dataset)
```

## Service Selection Guide

| Task | Expertise Level | Service | Cost |
|------|-----------------|---------|------|
| **Image classification** | Low | AutoML Vision | $$ |
| **Image classification** | High | Custom Vertex AI | $$$ |
| **Object detection** | Low | Vision API | $ |
| **Text classification** | Low | AutoML Natural Language | $$ |
| **Text classification** | High | Custom Vertex AI | $$$ |
| **Sentiment analysis** | Any | Natural Language API | $ |
| **Translation** | Any | Translation API | $ |
| **Speech recognition** | Any | Speech-to-Text API | $ |
| **Custom ML model** | High | Vertex AI Training | $$$-$$$$ |
| **Large model training** | High | Vertex AI with TPUs | $$$$-$$$$$ |

## Best Practices

- Start with pre-trained APIs for standard tasks
- Use AutoML for custom models with limited ML expertise
- Use Vertex AI custom training for advanced use cases
- Enable Vertex AI Model Monitoring for production models
- Use Feature Store for reusable features
- Implement ML pipelines for reproducibility
- Use TPUs for large-scale transformer model training
- Monitor prediction costs and latency
