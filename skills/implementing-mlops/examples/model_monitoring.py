"""
Model Monitoring Example

Demonstrates model monitoring patterns including:
- Data drift detection
- Prediction drift detection
- Model performance degradation alerts
- Feature importance monitoring
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from scipy import stats
from sklearn.ensemble import IsolationForest
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Drift Detection
# =============================================================================

@dataclass
class DriftResult:
    """Result of drift detection analysis."""
    feature_name: str
    drift_detected: bool
    drift_score: float
    p_value: Optional[float]
    method: str
    threshold: float
    details: Dict


class DataDriftDetector:
    """
    Detect data drift between reference and production distributions.

    Supports multiple detection methods:
    - KS Test (Kolmogorov-Smirnov): Continuous features
    - Chi-Square Test: Categorical features
    - PSI (Population Stability Index): Distribution shift
    """

    def __init__(
        self,
        reference_data: pd.DataFrame,
        ks_threshold: float = 0.05,
        psi_threshold: float = 0.2,
    ):
        self.reference_data = reference_data
        self.ks_threshold = ks_threshold
        self.psi_threshold = psi_threshold
        self._compute_reference_stats()

    def _compute_reference_stats(self):
        """Pre-compute reference distribution statistics."""
        self.reference_stats = {}
        for col in self.reference_data.columns:
            self.reference_stats[col] = {
                "mean": self.reference_data[col].mean(),
                "std": self.reference_data[col].std(),
                "min": self.reference_data[col].min(),
                "max": self.reference_data[col].max(),
                "quantiles": self.reference_data[col].quantile([0.25, 0.5, 0.75]).to_dict(),
            }

    def ks_test(self, feature: str, production_data: pd.Series) -> DriftResult:
        """
        Kolmogorov-Smirnov test for continuous feature drift.

        Returns True if distributions are significantly different.
        """
        reference = self.reference_data[feature].dropna()
        production = production_data.dropna()

        statistic, p_value = stats.ks_2samp(reference, production)
        drift_detected = p_value < self.ks_threshold

        return DriftResult(
            feature_name=feature,
            drift_detected=drift_detected,
            drift_score=statistic,
            p_value=p_value,
            method="ks_test",
            threshold=self.ks_threshold,
            details={
                "reference_mean": float(reference.mean()),
                "production_mean": float(production.mean()),
                "reference_std": float(reference.std()),
                "production_std": float(production.std()),
            }
        )

    def calculate_psi(
        self,
        feature: str,
        production_data: pd.Series,
        n_bins: int = 10
    ) -> DriftResult:
        """
        Population Stability Index for distribution shift.

        PSI Interpretation:
        - < 0.1: No significant change
        - 0.1 - 0.2: Moderate change, investigate
        - > 0.2: Significant change, action required
        """
        reference = self.reference_data[feature].dropna()
        production = production_data.dropna()

        # Create bins from reference data
        bins = np.percentile(reference, np.linspace(0, 100, n_bins + 1))
        bins[0] = -np.inf
        bins[-1] = np.inf

        # Calculate proportions
        ref_counts = np.histogram(reference, bins=bins)[0]
        prod_counts = np.histogram(production, bins=bins)[0]

        # Avoid division by zero
        ref_props = (ref_counts + 1) / (len(reference) + n_bins)
        prod_props = (prod_counts + 1) / (len(production) + n_bins)

        # Calculate PSI
        psi = np.sum((prod_props - ref_props) * np.log(prod_props / ref_props))
        drift_detected = psi > self.psi_threshold

        return DriftResult(
            feature_name=feature,
            drift_detected=drift_detected,
            drift_score=psi,
            p_value=None,
            method="psi",
            threshold=self.psi_threshold,
            details={
                "reference_bins": ref_props.tolist(),
                "production_bins": prod_props.tolist(),
                "interpretation": self._interpret_psi(psi),
            }
        )

    def _interpret_psi(self, psi: float) -> str:
        if psi < 0.1:
            return "No significant change"
        elif psi < 0.2:
            return "Moderate change - investigate"
        else:
            return "Significant change - action required"

    def detect_all_features(
        self,
        production_data: pd.DataFrame,
        method: str = "ks_test"
    ) -> List[DriftResult]:
        """Run drift detection on all features."""
        results = []
        for feature in self.reference_data.columns:
            if feature in production_data.columns:
                if method == "ks_test":
                    result = self.ks_test(feature, production_data[feature])
                elif method == "psi":
                    result = self.calculate_psi(feature, production_data[feature])
                else:
                    raise ValueError(f"Unknown method: {method}")
                results.append(result)
        return results


# =============================================================================
# Prediction Monitoring
# =============================================================================

class PredictionMonitor:
    """
    Monitor model predictions for anomalies and drift.

    Tracks:
    - Prediction distribution changes
    - Confidence score degradation
    - Anomalous prediction patterns
    """

    def __init__(
        self,
        reference_predictions: np.ndarray,
        reference_probabilities: np.ndarray,
        contamination: float = 0.05,
    ):
        self.reference_predictions = reference_predictions
        self.reference_probabilities = reference_probabilities
        self.contamination = contamination

        # Fit anomaly detector on reference probabilities
        self.anomaly_detector = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.anomaly_detector.fit(reference_probabilities.reshape(-1, 1))

        # Store reference statistics
        self.ref_pred_dist = np.bincount(reference_predictions) / len(reference_predictions)
        self.ref_prob_mean = reference_probabilities.mean()
        self.ref_prob_std = reference_probabilities.std()

    def check_prediction_distribution(
        self,
        production_predictions: np.ndarray,
        threshold: float = 0.1
    ) -> Dict:
        """Check if prediction class distribution has shifted."""
        prod_dist = np.bincount(
            production_predictions,
            minlength=len(self.ref_pred_dist)
        ) / len(production_predictions)

        # Calculate distribution shift
        shift = np.abs(prod_dist - self.ref_pred_dist).sum() / 2

        return {
            "distribution_shift": float(shift),
            "drift_detected": shift > threshold,
            "reference_distribution": self.ref_pred_dist.tolist(),
            "production_distribution": prod_dist.tolist(),
        }

    def check_confidence_degradation(
        self,
        production_probabilities: np.ndarray,
        z_threshold: float = 2.0
    ) -> Dict:
        """Detect if model confidence has degraded."""
        prod_mean = production_probabilities.mean()
        prod_std = production_probabilities.std()

        # Z-score for mean shift
        z_score = abs(prod_mean - self.ref_prob_mean) / self.ref_prob_std

        return {
            "mean_shift_z_score": float(z_score),
            "confidence_degraded": z_score > z_threshold,
            "reference_mean": float(self.ref_prob_mean),
            "production_mean": float(prod_mean),
            "reference_std": float(self.ref_prob_std),
            "production_std": float(prod_std),
        }

    def detect_anomalous_predictions(
        self,
        probabilities: np.ndarray
    ) -> Dict:
        """Flag anomalous prediction confidence scores."""
        anomaly_labels = self.anomaly_detector.predict(probabilities.reshape(-1, 1))
        anomaly_indices = np.where(anomaly_labels == -1)[0]

        return {
            "num_anomalies": len(anomaly_indices),
            "anomaly_rate": len(anomaly_indices) / len(probabilities),
            "anomaly_indices": anomaly_indices.tolist()[:100],  # Limit output
            "anomaly_values": probabilities[anomaly_indices][:100].tolist(),
        }


# =============================================================================
# Performance Monitoring
# =============================================================================

class PerformanceMonitor:
    """
    Track model performance over time with alerting.

    Monitors:
    - Accuracy, precision, recall, F1
    - Performance degradation trends
    - Threshold violations
    """

    def __init__(
        self,
        baseline_metrics: Dict[str, float],
        alert_thresholds: Dict[str, float],
    ):
        self.baseline_metrics = baseline_metrics
        self.alert_thresholds = alert_thresholds
        self.metrics_history: List[Dict] = []

    def log_metrics(
        self,
        metrics: Dict[str, float],
        timestamp: Optional[datetime] = None
    ):
        """Log metrics with timestamp."""
        if timestamp is None:
            timestamp = datetime.now()

        entry = {
            "timestamp": timestamp.isoformat(),
            "metrics": metrics,
            "alerts": self._check_alerts(metrics),
        }
        self.metrics_history.append(entry)

        # Log alerts
        for alert in entry["alerts"]:
            logger.warning(f"ALERT: {alert}")

        return entry

    def _check_alerts(self, metrics: Dict[str, float]) -> List[str]:
        """Check if any metrics violate thresholds."""
        alerts = []
        for metric, value in metrics.items():
            if metric in self.alert_thresholds:
                threshold = self.alert_thresholds[metric]
                baseline = self.baseline_metrics.get(metric, threshold)

                # Alert if performance dropped below threshold
                if value < threshold:
                    drop = ((baseline - value) / baseline) * 100
                    alerts.append(
                        f"{metric} dropped to {value:.4f} "
                        f"(baseline: {baseline:.4f}, threshold: {threshold:.4f}, "
                        f"drop: {drop:.1f}%)"
                    )
        return alerts

    def get_performance_trend(
        self,
        metric: str,
        window_size: int = 7
    ) -> Dict:
        """Analyze performance trend for a metric."""
        if len(self.metrics_history) < window_size:
            return {"error": "Insufficient history"}

        recent_values = [
            entry["metrics"].get(metric, 0)
            for entry in self.metrics_history[-window_size:]
        ]

        # Simple linear regression for trend
        x = np.arange(len(recent_values))
        slope, intercept = np.polyfit(x, recent_values, 1)

        return {
            "metric": metric,
            "current_value": recent_values[-1],
            "mean": float(np.mean(recent_values)),
            "std": float(np.std(recent_values)),
            "trend_slope": float(slope),
            "trend_direction": "improving" if slope > 0 else "degrading",
            "values": recent_values,
        }

    def generate_report(self) -> Dict:
        """Generate comprehensive monitoring report."""
        if not self.metrics_history:
            return {"error": "No metrics logged"}

        latest = self.metrics_history[-1]

        # Aggregate alerts
        all_alerts = []
        for entry in self.metrics_history[-7:]:
            all_alerts.extend(entry["alerts"])

        return {
            "report_timestamp": datetime.now().isoformat(),
            "latest_metrics": latest["metrics"],
            "baseline_metrics": self.baseline_metrics,
            "active_alerts": latest["alerts"],
            "alerts_last_7_entries": all_alerts,
            "total_entries": len(self.metrics_history),
        }


# =============================================================================
# Alerting Integration
# =============================================================================

class AlertManager:
    """Manage and dispatch monitoring alerts."""

    def __init__(self, alert_config: Dict):
        self.config = alert_config
        self.alert_history: List[Dict] = []

    def send_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        details: Dict,
    ):
        """Send alert to configured channels."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "severity": severity,
            "message": message,
            "details": details,
        }

        self.alert_history.append(alert)

        # Log alert
        logger.warning(f"[{severity.upper()}] {alert_type}: {message}")

        # In production, send to:
        # - Slack/Teams webhook
        # - PagerDuty
        # - Email
        # - Prometheus Alertmanager

        return alert

    def check_and_alert(
        self,
        drift_results: List[DriftResult],
        prediction_metrics: Dict,
        performance_metrics: Dict,
    ):
        """Analyze all monitoring results and send appropriate alerts."""

        # Check for data drift
        drifted_features = [r for r in drift_results if r.drift_detected]
        if len(drifted_features) > 0:
            self.send_alert(
                alert_type="data_drift",
                severity="warning" if len(drifted_features) < 3 else "critical",
                message=f"Data drift detected in {len(drifted_features)} features",
                details={
                    "features": [r.feature_name for r in drifted_features],
                    "scores": {r.feature_name: r.drift_score for r in drifted_features},
                }
            )

        # Check for prediction drift
        if prediction_metrics.get("drift_detected"):
            self.send_alert(
                alert_type="prediction_drift",
                severity="warning",
                message="Prediction distribution has shifted",
                details=prediction_metrics,
            )

        # Check for performance degradation
        if prediction_metrics.get("confidence_degraded"):
            self.send_alert(
                alert_type="confidence_degradation",
                severity="critical",
                message="Model confidence has degraded significantly",
                details=prediction_metrics,
            )


# =============================================================================
# Usage Example
# =============================================================================

def main():
    """Demonstrate model monitoring pipeline."""
    np.random.seed(42)

    # Generate reference data (from training)
    n_samples = 1000
    reference_features = pd.DataFrame({
        "feature_1": np.random.normal(0, 1, n_samples),
        "feature_2": np.random.normal(5, 2, n_samples),
        "feature_3": np.random.exponential(2, n_samples),
    })
    reference_predictions = np.random.randint(0, 2, n_samples)
    reference_probabilities = np.random.beta(5, 2, n_samples)

    # Initialize monitors
    drift_detector = DataDriftDetector(reference_features)
    prediction_monitor = PredictionMonitor(
        reference_predictions,
        reference_probabilities
    )
    performance_monitor = PerformanceMonitor(
        baseline_metrics={"accuracy": 0.95, "f1": 0.93, "precision": 0.94},
        alert_thresholds={"accuracy": 0.90, "f1": 0.88, "precision": 0.88}
    )
    alert_manager = AlertManager({})

    # Simulate production data with drift
    production_features = pd.DataFrame({
        "feature_1": np.random.normal(0.5, 1.2, n_samples),  # Mean shifted
        "feature_2": np.random.normal(5, 2, n_samples),       # No change
        "feature_3": np.random.exponential(3, n_samples),     # Distribution changed
    })
    production_predictions = np.random.randint(0, 2, n_samples)
    production_probabilities = np.random.beta(4, 3, n_samples)  # Degraded

    # Run drift detection
    print("=" * 60)
    print("Data Drift Detection")
    print("=" * 60)
    drift_results = drift_detector.detect_all_features(production_features)
    for result in drift_results:
        status = "DRIFT" if result.drift_detected else "OK"
        print(f"  {result.feature_name}: {status} (score={result.drift_score:.4f})")

    # Run prediction monitoring
    print("\n" + "=" * 60)
    print("Prediction Monitoring")
    print("=" * 60)
    pred_dist = prediction_monitor.check_prediction_distribution(production_predictions)
    print(f"  Distribution shift: {pred_dist['distribution_shift']:.4f}")

    conf_check = prediction_monitor.check_confidence_degradation(production_probabilities)
    print(f"  Confidence z-score: {conf_check['mean_shift_z_score']:.4f}")
    print(f"  Degraded: {conf_check['confidence_degraded']}")

    # Log performance metrics
    print("\n" + "=" * 60)
    print("Performance Monitoring")
    print("=" * 60)
    performance_monitor.log_metrics({
        "accuracy": 0.91,
        "f1": 0.89,
        "precision": 0.90
    })
    report = performance_monitor.generate_report()
    print(f"  Current accuracy: {report['latest_metrics']['accuracy']}")
    print(f"  Alerts: {report['active_alerts']}")

    # Send alerts
    print("\n" + "=" * 60)
    print("Alert Summary")
    print("=" * 60)
    alert_manager.check_and_alert(drift_results, conf_check, report)
    print(f"  Total alerts sent: {len(alert_manager.alert_history)}")


if __name__ == "__main__":
    main()
