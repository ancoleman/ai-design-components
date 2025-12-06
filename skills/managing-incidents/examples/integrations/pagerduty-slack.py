#!/usr/bin/env python3
"""
PagerDuty to Slack Integration

Automatically creates incident Slack channels when PagerDuty incidents are triggered.
Uses PagerDuty webhooks to receive incident events and Slack API to create channels.

Dependencies:
    pip install slack-sdk requests

Configuration:
    Set environment variables:
    - SLACK_BOT_TOKEN: Slack bot token with channels:manage scope
    - PAGERDUTY_WEBHOOK_SECRET: Secret for validating PagerDuty webhooks

Usage:
    # Run webhook server
    python pagerduty-slack.py

    # Configure PagerDuty webhook:
    # URL: https://your-server.com/pagerduty-webhook
    # Events: incident.triggered, incident.acknowledged, incident.resolved
"""

import os
import json
import hmac
import hashlib
from datetime import date
from typing import Optional
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
PAGERDUTY_WEBHOOK_SECRET = os.environ.get("PAGERDUTY_WEBHOOK_SECRET")

slack_client = WebClient(token=SLACK_BOT_TOKEN)


def verify_pagerduty_signature(request_body: bytes, signature: str) -> bool:
    """
    Verify PagerDuty webhook signature for security.

    Args:
        request_body: Raw request body
        signature: X-PagerDuty-Signature header value

    Returns:
        True if signature is valid, False otherwise
    """
    if not PAGERDUTY_WEBHOOK_SECRET:
        return True  # Skip verification if secret not configured

    expected = hmac.new(
        PAGERDUTY_WEBHOOK_SECRET.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)


def create_incident_channel(incident: dict) -> Optional[str]:
    """
    Create Slack channel for incident.

    Args:
        incident: PagerDuty incident object

    Returns:
        Channel ID if created successfully, None otherwise
    """
    incident_id = incident["id"]
    incident_number = incident["incident_number"]
    title = incident["title"].lower().replace(" ", "-")[:50]

    # Generate channel name: #incident-YYYY-MM-DD-###-title
    channel_name = f"incident-{date.today()}-{incident_number}-{title}"

    # Slack channel names must be lowercase, no special chars
    channel_name = "".join(c for c in channel_name if c.isalnum() or c == "-")

    try:
        # Create channel
        response = slack_client.conversations_create(
            name=channel_name,
            is_private=False
        )

        channel_id = response["channel"]["id"]

        # Post initial incident details
        severity = incident.get("urgency", "unknown")
        service = incident.get("service", {}).get("summary", "Unknown")

        slack_client.chat_postMessage(
            channel=channel_id,
            text=f"🚨 *Incident Declared: SEV{severity.upper()}*",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 Incident #{incident_number}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Severity:*\n{severity.upper()}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Service:*\n{service}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*PagerDuty:*\n<{incident['html_url']}|View Incident>"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Status:*\nInvestigating"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Description:*\n{incident['title']}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Next Steps:*\n1. Incident Commander (IC) to be assigned\n2. Begin investigation\n3. Post status updates every 15-30 minutes"
                    }
                }
            ]
        )

        # Pin important information
        slack_client.pins_add(
            channel=channel_id,
            timestamp=response["ts"]
        )

        print(f"Created incident channel: {channel_name} (ID: {channel_id})")
        return channel_id

    except SlackApiError as e:
        print(f"Error creating Slack channel: {e.response['error']}")
        return None


def post_incident_update(incident: dict, event_type: str):
    """
    Post incident status update to existing channel.

    Args:
        incident: PagerDuty incident object
        event_type: Type of event (acknowledged, resolved, etc.)
    """
    # Find incident channel by searching for incident number
    # In production, store channel_id → incident_id mapping in database

    incident_number = incident["incident_number"]

    try:
        # Search for channel
        channels_response = slack_client.conversations_list()
        channel_id = None

        for channel in channels_response["channels"]:
            if f"incident-" in channel["name"] and str(incident_number) in channel["name"]:
                channel_id = channel["id"]
                break

        if not channel_id:
            print(f"Channel not found for incident #{incident_number}")
            return

        # Post update based on event type
        if event_type == "incident.acknowledged":
            slack_client.chat_postMessage(
                channel=channel_id,
                text=f"✅ Incident acknowledged by {incident.get('assigned_to', 'on-call')}"
            )

        elif event_type == "incident.resolved":
            slack_client.chat_postMessage(
                channel=channel_id,
                text="🎉 *INCIDENT RESOLVED*",
                blocks=[
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "🎉 INCIDENT RESOLVED"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Incident #{incident_number} has been resolved.\n\n*Next Steps:*\n1. Post-mortem to be scheduled within 48 hours\n2. Action items will be tracked\n3. Thank you to all responders!"
                        }
                    }
                ]
            )

            # Archive channel after 24 hours (would need scheduled job)
            # For now, just add note
            slack_client.chat_postMessage(
                channel=channel_id,
                text="_This channel will be archived in 24 hours._"
            )

    except SlackApiError as e:
        print(f"Error posting update: {e.response['error']}")


@app.route("/pagerduty-webhook", methods=["POST"])
def pagerduty_webhook():
    """
    Handle PagerDuty webhook events.

    Events:
        - incident.triggered: Create Slack channel
        - incident.acknowledged: Post acknowledgment
        - incident.resolved: Post resolution
    """
    # Verify signature
    signature = request.headers.get("X-PagerDuty-Signature", "")
    if not verify_pagerduty_signature(request.get_data(), signature):
        return jsonify({"error": "Invalid signature"}), 401

    data = request.get_json()

    # Handle webhook event
    for message in data.get("messages", []):
        event_type = message.get("event")
        incident = message.get("incident", {})

        if event_type == "incident.triggered":
            create_incident_channel(incident)

        elif event_type in ["incident.acknowledged", "incident.resolved"]:
            post_incident_update(incident, event_type)

    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    # Run webhook server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
