#!/usr/bin/env python3
"""
Post-Mortem Auto-Generator

Automatically generates post-mortem documents from incident data.
Pulls timeline from Slack, metrics from monitoring, and creates pre-filled post-mortem.

Dependencies:
    pip install slack-sdk google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Configuration:
    Set environment variables:
    - SLACK_BOT_TOKEN: Slack bot token
    - GOOGLE_CREDENTIALS_PATH: Path to Google service account credentials

Usage:
    python postmortem-generator.py --incident-channel incident-2025-12-03-api-outage
"""

import os
import argparse
from datetime import datetime
from typing import List, Dict
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
GOOGLE_CREDS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials.json")
POSTMORTEM_TEMPLATE_ID = os.environ.get("POSTMORTEM_TEMPLATE_ID")  # Google Doc template

slack_client = WebClient(token=SLACK_BOT_TOKEN)


def get_incident_timeline(channel_name: str) -> List[Dict]:
    """
    Extract incident timeline from Slack channel history.

    Args:
        channel_name: Name of incident Slack channel

    Returns:
        List of timeline events with timestamps and messages
    """
    try:
        # Find channel by name
        channels = slack_client.conversations_list()
        channel_id = None

        for channel in channels["channels"]:
            if channel["name"] == channel_name:
                channel_id = channel["id"]
                break

        if not channel_id:
            raise ValueError(f"Channel not found: {channel_name}")

        # Get channel history
        history = slack_client.conversations_history(channel=channel_id, limit=1000)

        timeline = []
        for message in reversed(history["messages"]):
            # Skip bot messages and reactions
            if message.get("subtype") in ["bot_message", "message_replied"]:
                continue

            timestamp = datetime.fromtimestamp(float(message["ts"]))
            user_id = message.get("user", "system")

            # Get user name
            user_name = "System"
            if user_id != "system":
                try:
                    user_info = slack_client.users_info(user=user_id)
                    user_name = user_info["user"]["real_name"]
                except:
                    user_name = user_id

            timeline.append({
                "time": timestamp.strftime("%H:%M"),
                "event": message.get("text", ""),
                "actor": user_name
            })

        return timeline

    except SlackApiError as e:
        print(f"Error fetching Slack history: {e.response['error']}")
        return []


def extract_incident_metadata(channel_name: str) -> Dict:
    """
    Extract incident metadata from channel name and pinned messages.

    Args:
        channel_name: Incident channel name

    Returns:
        Dict with incident ID, severity, date, etc.
    """
    # Parse channel name: incident-YYYY-MM-DD-###-title
    parts = channel_name.replace("incident-", "").split("-")

    incident_date = f"{parts[0]}-{parts[1]}-{parts[2]}" if len(parts) >= 3 else "Unknown"

    return {
        "incident_id": f"INC-{incident_date}-001",
        "date": incident_date,
        "severity": "SEV1",  # Default, can be extracted from pinned message
        "channel_name": channel_name
    }


def create_postmortem_document(incident_data: Dict, timeline: List[Dict]) -> str:
    """
    Create Google Doc from post-mortem template with incident data.

    Args:
        incident_data: Incident metadata
        timeline: Timeline events

    Returns:
        URL of created Google Doc
    """
    # Authenticate with Google
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDS_PATH,
        scopes=["https://www.googleapis.com/auth/documents",
                "https://www.googleapis.com/auth/drive"]
    )

    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # Copy template
    if POSTMORTEM_TEMPLATE_ID:
        file_metadata = {
            "name": f"Post-Mortem: {incident_data['incident_id']}",
            "parents": []  # Configure folder ID if needed
        }
        copied_file = drive_service.files().copy(
            fileId=POSTMORTEM_TEMPLATE_ID,
            body=file_metadata
        ).execute()

        doc_id = copied_file["id"]

    else:
        # Create new document
        doc = docs_service.documents().create(body={
            "title": f"Post-Mortem: {incident_data['incident_id']}"
        }).execute()

        doc_id = doc["documentId"]

    # Populate document with incident data
    requests = []

    # Insert incident summary
    requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": f"""Post-Mortem: {incident_data['incident_id']}

Incident ID: {incident_data['incident_id']}
Severity: {incident_data['severity']}
Date: {incident_data['date']}
Status: Draft

## Timeline

"""
        }
    })

    # Insert timeline
    timeline_text = "\n".join([
        f"{event['time']} - {event['event']} (@{event['actor']})"
        for event in timeline
    ])

    requests.append({
        "insertText": {
            "location": {"index": 200},  # After summary
            "text": timeline_text + "\n\n"
        }
    })

    # Execute batch update
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()

    # Get shareable link
    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

    print(f"✅ Post-mortem document created: {doc_url}")
    return doc_url


def schedule_postmortem_meeting(incident_data: Dict, doc_url: str):
    """
    Schedule post-mortem meeting in Google Calendar (placeholder).

    Args:
        incident_data: Incident metadata
        doc_url: URL to post-mortem document
    """
    # In production, use Google Calendar API to create meeting
    print(f"📅 Reminder: Schedule post-mortem meeting within 48 hours")
    print(f"   Suggested attendees: IC, SMEs, stakeholders")
    print(f"   Document: {doc_url}")


def main():
    """Generate post-mortem from incident Slack channel."""
    parser = argparse.ArgumentParser(description="Generate post-mortem document")
    parser.add_argument(
        "--incident-channel",
        required=True,
        help="Incident Slack channel name (e.g., incident-2025-12-03-api-outage)"
    )
    args = parser.parse_args()

    print(f"🔍 Fetching incident data from #{args.incident_channel}...")

    # Extract incident metadata
    incident_data = extract_incident_metadata(args.incident_channel)

    # Get incident timeline from Slack
    timeline = get_incident_timeline(args.incident_channel)

    if not timeline:
        print("❌ Failed to fetch incident timeline")
        return

    print(f"✅ Extracted {len(timeline)} timeline events")

    # Create post-mortem document
    doc_url = create_postmortem_document(incident_data, timeline)

    # Schedule post-mortem meeting
    schedule_postmortem_meeting(incident_data, doc_url)

    print("\n✅ Post-mortem generation complete!")
    print(f"   Document: {doc_url}")
    print(f"   Next steps:")
    print(f"   1. Review and complete sections: Root Cause, Impact, What Went Well/Wrong")
    print(f"   2. Schedule post-mortem meeting (within 48 hours)")
    print(f"   3. Define action items with owners and due dates")


if __name__ == "__main__":
    main()
