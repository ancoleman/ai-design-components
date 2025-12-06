# Model Governance and Compliance

Establish governance frameworks for model risk management, regulatory compliance, and responsible AI practices.

## Table of Contents

- [Overview](#overview)
- [Model Cards](#model-cards)
- [Bias Detection and Fairness](#bias-detection-and-fairness)
- [Audit Trails](#audit-trails)
- [Model Approval Workflows](#model-approval-workflows)
- [Regulatory Compliance](#regulatory-compliance)
- [Responsible AI Practices](#responsible-ai-practices)
- [Implementation Examples](#implementation-examples)

## Overview

Model governance ensures ML systems are transparent, accountable, fair, and compliant with regulations. Critical for regulated industries (finance, healthcare, government) and high-stakes applications.

### Governance Components

```
Model Governance Framework
    |
    ├─ Documentation (Model Cards)
    |  └─ Purpose, performance, limitations, ethical considerations
    |
    ├─ Fairness & Bias (Fairness Metrics)
    |  └─ Demographic parity, equalized odds, bias mitigation
    |
    ├─ Audit Trails (Version Control)
    |  └─ Who trained, approved, deployed models
    |
    ├─ Approval Workflows (Stage Gates)
    |  └─ Testing → Staging → Production approval
    |
    ├─ Compliance (Regulations)
    |  └─ EU AI Act, Model Risk Management (SR 11-7), GDPR
    |
    └─ Monitoring (Ongoing)
       └─ Performance degradation, drift, fairness shifts
```

## Model Cards

Standardized documentation for model transparency and accountability.

### Model Card Template

Based on Google's Model Card Toolkit and Microsoft's approach.

```markdown
# Model Card: Fraud Detection Model v2.1

## Model Details

**Developer:** Risk Analytics Team
**Model Date:** 2023-06-01
**Model Version:** v2.1.0
**Model Type:** Gradient Boosting Classifier (XGBoost)
**Training Dataset:** Transactions 2022-01-01 to 2023-05-01 (10M samples)

**Contact:** ml-team@company.com
**License:** Internal Use Only

## Intended Use

**Primary Use Case:**
Real-time fraud detection for credit card transactions.

**Intended Users:**
- Risk management team (monitoring alerts)
- Customer service (investigating flagged transactions)
- Automated systems (blocking high-risk transactions)

**Out-of-Scope Uses:**
- NOT for credit scoring or lending decisions
- NOT for employee monitoring
- NOT for insurance underwriting

## Factors

**Relevant Factors:**
- Transaction amount ($0 - $10,000 range)
- Merchant category (online retail, gas stations, restaurants, etc.)
- Geographic location (domestic vs international)
- Time of day and day of week
- User purchase history

**Evaluation Factors:**
- Demographics: Age groups, geographic regions
- Transaction types: Card-present vs card-not-present
- Merchant risk levels: High-risk vs low-risk categories

## Metrics

**Model Performance:**
- Precision: 0.87 (87% of flagged transactions are actual fraud)
- Recall: 0.82 (82% of fraud cases detected)
- F1-Score: 0.84
- AUC-ROC: 0.94

**Decision Threshold:**
- Probability > 0.75: Block transaction automatically
- Probability 0.50-0.75: Flag for manual review
- Probability < 0.50: Allow transaction

**False Positive Rate:** 0.3% (3 in 1,000 legitimate transactions flagged)
**False Negative Rate:** 18% (18 in 100 fraud cases missed)

## Evaluation Data

**Dataset:** 2M transactions (May 2023, held-out test set)
**Data Collection:** Production transaction logs
**Preprocessing:** Same as training (feature engineering, scaling)

**Limitations:**
- Test set from same time period as training (may not capture future fraud patterns)
- Geographic bias: 85% US transactions, limited international coverage

## Training Data

**Dataset Size:** 10M transactions (Jan 2022 - May 2023)
**Positive Class:** 1.2% fraud (120K fraud cases)
**Negative Class:** 98.8% legitimate (9.88M legitimate)

**Data Sources:**
- Transaction logs (card networks)
- Merchant database (category, risk scores)
- User profiles (purchase history, account age)

**Preprocessing:**
- Feature engineering: 45 derived features
- Balancing: SMOTE upsampling of minority class (fraud)
- Train/val/test split: 70% / 15% / 15%

## Ethical Considerations

**Fairness:**
- Model evaluated for demographic parity across age groups and geographic regions
- No statistically significant differences in false positive rates across protected groups
- Monthly monitoring to detect fairness drift

**Privacy:**
- Model does not use sensitive attributes (race, religion, political affiliation)
- User data encrypted in transit and at rest
- GDPR-compliant: Right to explanation implemented via SHAP

**Risks:**
- False positives: Legitimate transactions blocked (customer friction)
- False negatives: Fraud cases missed (financial loss)
- Bias risk: Model may learn patterns correlated with demographics

## Caveats and Recommendations

**Limitations:**
1. **Temporal Drift:** Fraud patterns evolve rapidly (monthly retraining recommended)
2. **Geographic Coverage:** Trained primarily on US transactions (limited international)
3. **Novel Fraud:** Zero-day fraud attacks not in training data may be missed
4. **Data Quality:** Model performance degrades if input features missing or corrupt

**Recommendations:**
1. Monitor false positive rate (target: <0.5%)
2. Retrain monthly on recent data to capture evolving fraud patterns
3. Human review for transactions in [0.50, 0.75] probability range
4. Implement feedback loop: Analysts label flagged transactions → retrain

**Usage Guidelines:**
- Always provide explanation to users when transaction blocked
- Offer appeal process for false positives
- Combine with rule-based systems for comprehensive coverage
```

### Model Card Automation

```python
# generate_model_card.py
from model_card_toolkit import ModelCardToolkit
import mlflow

def generate_model_card(model_uri, output_path):
    """Auto-generate model card from MLflow metadata."""

    # Load model metadata
    model = mlflow.sklearn.load_model(model_uri)
    run = mlflow.get_run(model.metadata.run_id)

    # Initialize Model Card Toolkit
    mct = ModelCardToolkit()

    # Create model card
    model_card = mct.scaffold_assets()

    # Populate from MLflow
    model_card.model_details.name = run.data.tags['model_name']
    model_card.model_details.version = run.data.tags['model_version']
    model_card.model_details.description = run.data.tags['description']

    # Performance metrics
    model_card.quantitative_analysis.performance_metrics = [
        {'type': 'precision', 'value': run.data.metrics['precision']},
        {'type': 'recall', 'value': run.data.metrics['recall']},
        {'type': 'f1_score', 'value': run.data.metrics['f1']},
    ]

    # Fairness metrics
    model_card.quantitative_analysis.fairness_metrics = [
        {
            'type': 'demographic_parity',
            'slice': 'age_group',
            'value': run.data.metrics['demographic_parity_age']
        }
    ]

    # Export
    mct.update_model_card(model_card)
    mct.export_format(output_path=output_path, format='html')

    print(f"Model card saved to {output_path}")
```

## Bias Detection and Fairness

Measure and mitigate algorithmic bias to ensure equitable outcomes.

### Fairness Metrics

**1. Demographic Parity (Statistical Parity)**

Equal positive rate across groups.

```
P(ŷ = 1 | A = a) = P(ŷ = 1 | A = b)

Where:
- ŷ = prediction
- A = protected attribute (e.g., age group)
- a, b = different values of A
```

**Example:**
- Loan approval rate: 30% for age group 18-25, 30% for age group 55-65
- Demographic parity satisfied if rates equal across all age groups

**2. Equalized Odds**

Equal true positive rate AND false positive rate across groups.

```
P(ŷ = 1 | y = 1, A = a) = P(ŷ = 1 | y = 1, A = b)  (TPR)
P(ŷ = 1 | y = 0, A = a) = P(ŷ = 1 | y = 0, A = b)  (FPR)
```

**Example:**
- Fraud detection: 85% recall for urban users, 85% recall for rural users
- AND 2% false positive rate for both groups

**3. Equal Opportunity**

Equal true positive rate across groups (subset of equalized odds).

```
P(ŷ = 1 | y = 1, A = a) = P(ŷ = 1 | y = 1, A = b)
```

**Example:**
- Disease detection: 90% recall for all age groups

**4. Calibration**

Predicted probabilities match actual outcomes across groups.

```
P(y = 1 | ŷ = p, A = a) = P(y = 1 | ŷ = p, A = b) = p
```

**Example:**
- When model predicts 70% fraud probability, 70% of cases are actually fraud (for all groups)

### Bias Detection with Fairlearn

```python
# bias_detection.py
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

def evaluate_fairness(y_true, y_pred, sensitive_features):
    """
    Evaluate model fairness across sensitive attributes.

    Args:
        y_true: Ground truth labels
        y_pred: Model predictions
        sensitive_features: DataFrame with protected attributes (age_group, region, etc.)

    Returns:
        Fairness metrics report
    """

    # Overall metrics
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred)
    }

    # Metrics by group
    metric_frame = MetricFrame(
        metrics={
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score,
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_features
    )

    # Fairness metrics
    demographic_parity = demographic_parity_difference(
        y_true, y_pred, sensitive_features=sensitive_features['age_group']
    )

    equalized_odds = equalized_odds_difference(
        y_true, y_pred, sensitive_features=sensitive_features['age_group']
    )

    # Report
    report = {
        'overall_metrics': metrics,
        'metrics_by_group': metric_frame.by_group.to_dict(),
        'demographic_parity_difference': demographic_parity,
        'equalized_odds_difference': equalized_odds,
    }

    # Check thresholds
    if abs(demographic_parity) > 0.1:
        report['warning'] = f"Demographic parity violation: {demographic_parity:.3f} (threshold: 0.1)"

    if abs(equalized_odds) > 0.1:
        report['warning'] = f"Equalized odds violation: {equalized_odds:.3f} (threshold: 0.1)"

    return report

# Example usage
sensitive_features = pd.DataFrame({
    'age_group': ['18-25', '26-40', '41-55', '56+'] * 250,
    'region': ['urban', 'rural'] * 500
})

fairness_report = evaluate_fairness(y_test, y_pred, sensitive_features)
print(fairness_report)
```

### Bias Mitigation Techniques

**1. Preprocessing: Reweighting**

Adjust training sample weights to balance groups.

```python
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.ensemble import RandomForestClassifier

# Constraint: Demographic parity
constraint = DemographicParity()

# Train fair model
mitigator = ExponentiatedGradient(
    estimator=RandomForestClassifier(),
    constraints=constraint
)

mitigator.fit(X_train, y_train, sensitive_features=sensitive_train['age_group'])

# Predict
y_pred = mitigator.predict(X_test)
```

**2. In-Processing: Adversarial Debiasing**

Train model to predict label while adversary tries to predict sensitive attribute.

```python
# Adversarial debiasing (using AIF360)
from aif360.algorithms.inprocessing import AdversarialDebiasing
import tensorflow as tf

# Debias during training
debiased_model = AdversarialDebiasing(
    unprivileged_groups=[{'age_group': 0}],
    privileged_groups=[{'age_group': 1}],
    scope_name='debiased_classifier',
    sess=tf.Session()
)

debiased_model.fit(dataset_train)
predictions = debiased_model.predict(dataset_test)
```

**3. Post-Processing: Threshold Optimization**

Adjust decision thresholds per group to satisfy fairness constraints.

```python
from fairlearn.postprocessing import ThresholdOptimizer

# Optimize thresholds for equalized odds
postprocessor = ThresholdOptimizer(
    estimator=trained_model,
    constraints='equalized_odds',
    predict_method='predict_proba'
)

postprocessor.fit(X_train, y_train, sensitive_features=sensitive_train['age_group'])

# Fair predictions
y_pred_fair = postprocessor.predict(X_test, sensitive_features=sensitive_test['age_group'])
```

## Audit Trails

Track all model lifecycle events for compliance and accountability.

### Audit Log Components

```python
# audit_logger.py
import json
from datetime import datetime
from enum import Enum

class ModelEvent(Enum):
    TRAINING_STARTED = "training_started"
    TRAINING_COMPLETED = "training_completed"
    MODEL_REGISTERED = "model_registered"
    MODEL_PROMOTED_STAGING = "model_promoted_staging"
    MODEL_PROMOTED_PRODUCTION = "model_promoted_production"
    MODEL_DEPLOYED = "model_deployed"
    MODEL_PREDICTION = "model_prediction"
    MODEL_ROLLBACK = "model_rollback"
    MODEL_ARCHIVED = "model_archived"

class AuditLogger:
    """Log model lifecycle events for audit trail."""

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def log_event(self, event_type, model_name, model_version,
                  user, metadata=None):
        """
        Log model event.

        Args:
            event_type: ModelEvent enum
            model_name: Name of model
            model_version: Version (e.g., "v2.1.0")
            user: User who triggered event
            metadata: Additional context (dict)
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type.value,
            'model_name': model_name,
            'model_version': model_version,
            'user': user,
            'metadata': metadata or {}
        }

        # Append to audit log
        with open(self.log_file_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Also send to SIEM (Splunk, ELK, etc.)
        self._send_to_siem(log_entry)

    def _send_to_siem(self, log_entry):
        """Send audit log to SIEM for compliance monitoring."""
        # Send to Splunk HTTP Event Collector
        import requests
        requests.post(
            'https://splunk.company.com:8088/services/collector',
            headers={'Authorization': 'Splunk <token>'},
            json={'event': log_entry, 'sourcetype': 'ml_audit_log'}
        )

# Usage
audit_logger = AuditLogger('/var/log/ml_audit.jsonl')

# Log training
audit_logger.log_event(
    event_type=ModelEvent.TRAINING_STARTED,
    model_name='fraud_detection',
    model_version='v2.1.0',
    user='data-scientist@company.com',
    metadata={
        'training_data': 's3://ml-data/train.parquet',
        'hyperparameters': {'n_estimators': 100, 'max_depth': 10}
    }
)

# Log promotion to production
audit_logger.log_event(
    event_type=ModelEvent.PROMOTED_PRODUCTION,
    model_name='fraud_detection',
    model_version='v2.1.0',
    user='ml-engineer@company.com',
    metadata={
        'approved_by': 'risk-manager@company.com',
        'approval_date': '2023-06-15',
        'test_accuracy': 0.94
    }
)
```

### Prediction Logging

Log individual predictions for compliance audits (GDPR right to explanation).

```python
# prediction_logger.py
import json
from datetime import datetime

class PredictionLogger:
    """Log predictions for audit trail and right to explanation."""

    def log_prediction(self, model_version, input_data, prediction,
                       probability, explanation=None):
        """
        Log prediction with explanation.

        Args:
            model_version: Version of model used
            input_data: Input features (dict)
            prediction: Model prediction
            probability: Prediction probability
            explanation: SHAP values or feature importance (dict)
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'model_version': model_version,
            'input': input_data,
            'prediction': prediction,
            'probability': probability,
            'explanation': explanation
        }

        # Store in database for GDPR compliance
        self._store_in_database(log_entry)

    def get_prediction_history(self, user_id, days=90):
        """Retrieve prediction history for user (GDPR right to access)."""
        # Query database
        return self._query_database(user_id, days)

# Usage
logger = PredictionLogger()

# Log prediction with SHAP explanation
logger.log_prediction(
    model_version='v2.1.0',
    input_data={'transaction_amount': 500, 'merchant_category': 'online_retail'},
    prediction=1,  # Fraud
    probability=0.87,
    explanation={
        'transaction_amount': 0.35,  # SHAP value (contribution to prediction)
        'merchant_category': 0.28,
        'time_of_day': 0.12
    }
)
```

## Model Approval Workflows

Stage-gate process for model promotion from development to production.

### Approval Stages

```
Development → Testing → Staging → Production
    |           |         |           |
    |           |         |           └─ Approver: VP Engineering + Risk Manager
    |           |         └─ Approver: ML Engineering Lead
    |           └─ Approver: Data Science Lead
    └─ No approval needed
```

### MLflow Model Registry Approval Workflow

```python
# approval_workflow.py
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

def promote_model(model_name, version, stage, approver_email):
    """
    Promote model to stage with approval.

    Args:
        model_name: Name of registered model
        version: Model version to promote
        stage: Target stage ("Staging", "Production")
        approver_email: Email of person approving
    """

    # Check model meets requirements
    model_version = client.get_model_version(model_name, version)

    # Validation checks
    checks = validate_model_for_promotion(model_name, version, stage)

    if not checks['passed']:
        raise ValueError(f"Model validation failed: {checks['failures']}")

    # Promote model
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=stage,
        archive_existing_versions=True  # Archive current production model
    )

    # Log approval to audit trail
    audit_logger.log_event(
        event_type=ModelEvent.MODEL_PROMOTED_PRODUCTION if stage == "Production" else ModelEvent.MODEL_PROMOTED_STAGING,
        model_name=model_name,
        model_version=f"v{version}",
        user=approver_email,
        metadata={'checks': checks}
    )

    print(f"Model {model_name} v{version} promoted to {stage} by {approver_email}")

def validate_model_for_promotion(model_name, version, stage):
    """
    Validate model meets requirements for stage promotion.

    Returns:
        dict with validation results
    """
    checks = {'passed': True, 'failures': []}

    # Get model metrics
    model_version = client.get_model_version(model_name, version)
    run = client.get_run(model_version.run_id)

    # Check accuracy threshold
    accuracy = run.data.metrics.get('accuracy', 0)
    if accuracy < 0.85:
        checks['passed'] = False
        checks['failures'].append(f"Accuracy {accuracy:.3f} below threshold 0.85")

    # Check fairness
    demographic_parity = run.data.metrics.get('demographic_parity_difference', 1.0)
    if abs(demographic_parity) > 0.1:
        checks['passed'] = False
        checks['failures'].append(f"Demographic parity violation: {demographic_parity:.3f}")

    # Check model card exists
    if not model_version.description or len(model_version.description) < 100:
        checks['passed'] = False
        checks['failures'].append("Model card missing or incomplete")

    # Production-specific checks
    if stage == "Production":
        # Check load test results
        load_test_passed = run.data.tags.get('load_test_passed', 'false') == 'true'
        if not load_test_passed:
            checks['passed'] = False
            checks['failures'].append("Load test not passed")

        # Check security scan
        security_scan = run.data.tags.get('security_scan_passed', 'false') == 'true'
        if not security_scan:
            checks['passed'] = False
            checks['failures'].append("Security scan not passed")

    return checks

# Example: Promote to production with approval
promote_model(
    model_name='fraud_detection',
    version=5,
    stage='Production',
    approver_email='risk-manager@company.com'
)
```

### Automated Approval for Staging

```python
# auto_promote_staging.py
import mlflow

def auto_promote_to_staging(model_name, version):
    """
    Automatically promote model to Staging if validation passes.

    Used in CI/CD pipeline after training.
    """
    checks = validate_model_for_promotion(model_name, version, "Staging")

    if checks['passed']:
        promote_model(model_name, version, "Staging", "ci-cd-bot@company.com")
        print(f"✓ Model auto-promoted to Staging")
    else:
        print(f"✗ Model validation failed: {checks['failures']}")
        raise ValueError("Model not ready for Staging")
```

## Regulatory Compliance

Navigate regulatory requirements for AI/ML systems.

### EU AI Act (2024)

**Risk Categories:**
- **Unacceptable Risk:** Banned (social scoring, real-time biometric surveillance)
- **High Risk:** Strict requirements (healthcare, critical infrastructure, employment)
- **Limited Risk:** Transparency obligations (chatbots must disclose they're AI)
- **Minimal Risk:** No obligations (spam filters)

**High-Risk AI System Requirements:**
1. **Risk Management System:** Identify and mitigate risks throughout lifecycle
2. **Data Governance:** High-quality, representative training data
3. **Documentation:** Technical documentation and instructions for use
4. **Transparency:** Users informed about AI system capabilities and limitations
5. **Human Oversight:** Human intervention possible
6. **Accuracy, Robustness, Cybersecurity:** Meet performance standards

**MLOps Implementation:**
```python
# EU AI Act compliance checklist
eu_ai_act_compliance = {
    'risk_classification': 'High Risk (Credit Scoring)',
    'risk_management': {
        'risk_assessment_completed': True,
        'mitigation_measures': ['Bias testing', 'Fairness constraints', 'Human review for edge cases']
    },
    'data_governance': {
        'training_data_documented': True,
        'data_quality_checks': True,
        'representativeness_validated': True
    },
    'documentation': {
        'technical_documentation': 'Model card available',
        'instructions_for_use': 'User guide provided',
        'model_card_url': 'https://internal.company.com/model-cards/credit-scoring-v2'
    },
    'transparency': {
        'users_informed': True,
        'explanation_available': True  # SHAP explanations
    },
    'human_oversight': {
        'human_review_available': True,
        'override_mechanism': True
    },
    'accuracy_robustness': {
        'accuracy': 0.92,
        'fairness_tested': True,
        'adversarial_robustness_tested': True
    }
}
```

### Model Risk Management (SR 11-7) - Banking

US Federal Reserve guidance for banking institutions.

**Requirements:**
1. **Model Validation:** Independent review of models
2. **Model Inventory:** Centralized registry of all models
3. **Risk Tiering:** Classify models by risk level
4. **Ongoing Monitoring:** Performance tracking
5. **Documentation:** Development, validation, and use

**Implementation:**
```python
# SR 11-7 model inventory
model_inventory = {
    'model_name': 'Credit Risk Model',
    'model_id': 'CR-2023-001',
    'risk_tier': 'Tier 1 (High Risk)',
    'model_owner': 'credit-risk-team@bank.com',
    'model_validator': 'model-validation-group@bank.com',
    'validation_date': '2023-06-01',
    'validation_status': 'Approved',
    'next_validation_date': '2024-06-01',
    'documentation': {
        'model_development_document': 'https://docs/CR-2023-001-dev.pdf',
        'validation_report': 'https://docs/CR-2023-001-validation.pdf',
        'user_guide': 'https://docs/CR-2023-001-user-guide.pdf'
    },
    'limitations': [
        'Not validated for loans >$1M',
        'Limited data for emerging markets',
        'Performance degrades in recession scenarios'
    ],
    'monitoring': {
        'frequency': 'Monthly',
        'metrics': ['AUC-ROC', 'Default rate', 'Fairness metrics'],
        'alert_thresholds': {'auc_drop': 0.05, 'default_rate_change': 0.10}
    }
}
```

### GDPR (General Data Protection Regulation)

**Right to Explanation (Article 22):**
Individuals have right to explanation for automated decisions.

```python
# GDPR-compliant prediction with explanation
import shap

def predict_with_explanation(model, input_data):
    """
    Make prediction with SHAP explanation (GDPR compliant).
    """
    # Prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # SHAP explanation
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_data)

    # Format explanation (human-readable)
    feature_contributions = {
        feature: float(shap_value)
        for feature, shap_value in zip(input_data.columns, shap_values[0])
    }

    # Sort by absolute contribution
    sorted_features = sorted(
        feature_contributions.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    explanation_text = "Top factors influencing decision:\n"
    for feature, contribution in sorted_features[:5]:
        direction = "increased" if contribution > 0 else "decreased"
        explanation_text += f"- {feature}: {direction} likelihood by {abs(contribution):.2f}\n"

    return {
        'prediction': int(prediction),
        'probability': float(probability),
        'explanation': explanation_text,
        'feature_contributions': feature_contributions
    }

# User requests explanation
result = predict_with_explanation(model, user_data)
print(result['explanation'])
```

## Responsible AI Practices

### Explainability

Make model decisions interpretable.

**SHAP (SHapley Additive exPlanations):**
```python
import shap
import matplotlib.pyplot as plt

# Train model
model = xgboost.XGBClassifier().fit(X_train, y_train)

# SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot (feature importance)
shap.summary_plot(shap_values, X_test)

# Force plot (individual prediction)
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### Privacy-Preserving ML

**Differential Privacy:**
```python
# Differentially private training (TensorFlow Privacy)
from tensorflow_privacy.privacy.optimizers.dp_optimizer_keras import DPKerasAdamOptimizer

optimizer = DPKerasAdamOptimizer(
    l2_norm_clip=1.0,          # Gradient clipping
    noise_multiplier=0.5,      # Noise added to gradients
    num_microbatches=1,
    learning_rate=0.001
)

model.compile(optimizer=optimizer, loss='binary_crossentropy')
model.fit(X_train, y_train, epochs=10)
```

**Federated Learning:**
Train model on decentralized data without data leaving devices.

```python
# TensorFlow Federated (conceptual)
import tensorflow_federated as tff

# Define federated model
def model_fn():
    return tff.learning.from_keras_model(
        keras_model=create_keras_model(),
        input_spec=input_spec,
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=[tf.keras.metrics.Accuracy()]
    )

# Federated training process
iterative_process = tff.learning.build_federated_averaging_process(model_fn)

# Train on federated data (data never leaves devices)
state = iterative_process.initialize()
for round_num in range(100):
    state, metrics = iterative_process.next(state, federated_train_data)
    print(f'Round {round_num}: {metrics}')
```

## Implementation Examples

### Example 1: Complete Governance Pipeline

```python
# governance_pipeline.py
from datetime import datetime

class GovernancePipeline:
    """End-to-end governance for model lifecycle."""

    def __init__(self, model_name, model_version):
        self.model_name = model_name
        self.model_version = model_version
        self.audit_logger = AuditLogger('/var/log/ml_audit.jsonl')

    def train_model_with_governance(self, X_train, y_train, sensitive_features):
        """Train model with governance checks."""

        # 1. Log training start
        self.audit_logger.log_event(
            ModelEvent.TRAINING_STARTED,
            self.model_name,
            self.model_version,
            user=get_current_user()
        )

        # 2. Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # 3. Evaluate fairness
        fairness_report = evaluate_fairness(y_train, model.predict(X_train), sensitive_features)

        if fairness_report.get('warning'):
            print(f"⚠️  {fairness_report['warning']}")
            # Optionally: Trigger bias mitigation

        # 4. Generate model card
        generate_model_card(model, fairness_report, output_path=f'model_cards/{self.model_name}_{self.model_version}.html')

        # 5. Register model with metadata
        mlflow.sklearn.log_model(
            model,
            'model',
            registered_model_name=self.model_name,
            metadata={
                'version': self.model_version,
                'fairness_report': fairness_report,
                'model_card_url': f'model_cards/{self.model_name}_{self.model_version}.html'
            }
        )

        # 6. Log training completion
        self.audit_logger.log_event(
            ModelEvent.TRAINING_COMPLETED,
            self.model_name,
            self.model_version,
            user=get_current_user(),
            metadata={'fairness': fairness_report}
        )

        return model

    def deploy_with_approval(self, model, approver_email):
        """Deploy model after approval."""

        # 1. Validate model
        checks = validate_model_for_promotion(self.model_name, self.model_version, "Production")

        if not checks['passed']:
            raise ValueError(f"Model validation failed: {checks['failures']}")

        # 2. Get approval
        approved = request_approval(approver_email, self.model_name, self.model_version)

        if not approved:
            raise ValueError("Deployment not approved")

        # 3. Deploy
        deploy_model(model, self.model_name, self.model_version)

        # 4. Log deployment
        self.audit_logger.log_event(
            ModelEvent.MODEL_DEPLOYED,
            self.model_name,
            self.model_version,
            user=approver_email
        )

        print(f"✓ Model deployed to production")

# Usage
pipeline = GovernancePipeline('fraud_detection', 'v2.1.0')
model = pipeline.train_model_with_governance(X_train, y_train, sensitive_features)
pipeline.deploy_with_approval(model, approver_email='risk-manager@company.com')
```
