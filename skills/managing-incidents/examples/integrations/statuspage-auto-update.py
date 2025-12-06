#!/usr/bin/env python3
"""
Statuspage.io Auto-Update Integration

Automatically posts status page updates from incident Slack channel messages.
Monitors incident channels and posts updates to Statuspage.io when Communications Lead posts updates.

Dependencies:
    pip install slack-sdk requests

Configuration:
    Set environment variables:
    - SLACK_BOT_TOKEN: Slack bot token
    - STATUSPAGE_API_KEY: Statuspage.io API key
    - STATUSPAGE_PAGE_ID: Statuspage.io page ID

Usage:
    python statuspage-auto-update.py
"""

import os
import re
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
import requests

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
STATUSPAGE_API_KEY = os.environ.get("STATUSPAGE_API_KEY")
STATUSPAGE_PAGE_ID = os.environ.get("STATUSPAGE_PAGE_ID")

STATUSPAGE_API_BASE = f"https://api.statuspage.io/v1/pages/{STATUSPAGE_PAGE_ID}"


def parse_status_update(message_text: str) -> Optional[dict]:
    """
    Parse status update message from Slack.

    Expected format:
        [TIMESTAMP] Update #N - [Status]

        Current Status: [status]
        Issue: [description]
        Impact: [impact]
        Progress: [progress]
        ETA: [eta]

    Args:
        message_text: Slack message text

    Returns:
        Parsed update dict or None if not a valid status update
    """
    # Check if message matches status update format
    if not re.match(r"\d{2}:\d{2}.*Update #\d+", message_text):
        return None

    lines = message_text.split("\n")

    # Extract status
    status_line = [l for l in lines if l.startswith("Current Status:")]
    if not status_line:
        return None

    status_text = status_line[0].split(":", 1)[1].strip()

    # Map status to Statuspage.io status
    status_mapping = {
        "Investigating": "investigating",
        "Identified": "identified",
        "Monitoring": "monitoring",
        "Resolved": "resolved"
    }

    status = status_mapping.get(status_text, "investigating")

    # Extract issue description
    issue_line = [l for l in lines if l.startswith("Issue:")]
    issue = issue_line[0].split(":", 1)[1].strip() if issue_line else "Service disruption"

    # Extract impact
    impact_line = [l for l in lines if l.startswith("Impact:")]
    impact = impact_line[0].split(":", 1)[1].strip() if impact_line else "Under investigation"

    # Combine into status message
    message = f"{issue}\n\nImpact: {impact}"

    return {
        "status": status,
        "message": message
    }


def get_or_create_incident(name: str) -> str:
    """
    Get existing incident or create new one on Statuspage.io.

    Args:
        name: Incident name (from Slack channel name)

    Returns:
        Incident ID
    """
    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    # Check for unresolved incidents
    response = requests.get(
        f"{STATUSPAGE_API_BASE}/incidents/unresolved",
        headers=headers
    )

    if response.status_code == 200:
        incidents = response.json()
        # Find incident matching name
        for incident in incidents:
            if name.lower() in incident.get("name", "").lower():
                return incident["id"]

    # Create new incident
    incident_data = {
        "incident": {
            "name": name,
            "status": "investigating",
            "impact_override": "major",
            "body": "We are investigating reports of service disruption.",
            "components": {},  # Auto-detect or configure
            "component_ids": []
        }
    }

    response = requests.post(
        f"{STATUSPAGE_API_BASE}/incidents",
        headers=headers,
        json=incident_data
    )

    if response.status_code == 201:
        return response.json()["id"]

    raise Exception(f"Failed to create incident: {response.text}")


def update_statuspage(incident_id: str, status: str, message: str):
    """
    Post update to Statuspage.io incident.

    Args:
        incident_id: Statuspage incident ID
        status: Incident status (investigating, identified, monitoring, resolved)
        message: Update message
    """
    headers = {
        "Authorization": f"OAuth {STATUSPAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    update_data = {
        "incident_update": {
            "body": message,
            "status": status
        }
    }

    response = requests.patch(
        f"{STATUSPAGE_API_BASE}/incidents/{incident_id}",
        headers=headers,
        json=update_data
    )

    if response.status_code == 200:
        print(f"✅ Status page updated: {status}")
    else:
        print(f"❌ Failed to update status page: {response.text}")


def handle_slack_message(client: SocketModeClient, req: SocketModeRequest):
    """
    Handle Slack message events.

    Monitors incident channels for status updates from Communications Lead
    and automatically posts to Statuspage.io.
    """
    if req.type == "events_api":
        # Acknowledge request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        event = req.payload["event"]

        # Only process messages in incident channels
        if event.get("type") == "message" and "incident-" in event.get("channel_name", ""):
            message_text = event.get("text", "")

            # Parse status update
            update = parse_status_update(message_text)
            if not update:
                return

            # Get or create Statuspage incident
            channel_name = event.get("channel_name", "")
            incident_title = channel_name.replace("incident-", "").replace("-", " ").title()

            try:
                incident_id = get_or_create_incident(incident_title)
                update_statuspage(incident_id, update["status"], update["message"])

                # React to message to confirm posted
                slack_client = WebClient(token=SLACK_BOT_TOKEN)
                slack_client.reactions_add(
                    channel=event["channel"],
                    timestamp=event["ts"],
                    name="white_check_mark"
                )

            except Exception as e:
                print(f"Error updating status page: {e}")


def main():
    """
    Start Slack event listener for automatic status page updates.
    """
    if not all([SLACK_APP_TOKEN, STATUSPAGE_API_KEY, STATUSPAGE_PAGE_ID]):
        print("Error: Missing required environment variables")
        print("Required: SLACK_APP_TOKEN, STATUSPAGE_API_KEY, STATUSPAGE_PAGE_ID")
        return

    client = SocketModeClient(
        app_token=SLACK_APP_TOKEN,
        web_client=WebClient(token=SLACK_BOT_TOKEN)
    )

    client.socket_mode_request_listeners.append(handle_slack_message)

    print("🚀 Statuspage auto-update bot started")
    print("Monitoring incident channels for status updates...")

    client.connect()

    # Keep running
    from slack_sdk.socket_mode.builtin import SocketModeClient
    import time
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
