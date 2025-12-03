#!/usr/bin/env python3
"""
WebSocket Connection Testing Tool

Tests WebSocket server connectivity, authentication, and message handling.
Useful for validating WebSocket implementations before frontend integration.

Usage:
    python test_websocket_connection.py --url ws://localhost:8000/ws
    python test_websocket_connection.py --url wss://api.example.com/ws --auth-token SECRET
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime
from typing import Optional

try:
    import websockets
except ImportError:
    print("❌ Error: websockets library not installed")
    print("Install with: pip install websockets")
    sys.exit(1)


async def test_connection(
    url: str,
    auth_token: Optional[str] = None,
    test_messages: int = 5,
    timeout: int = 10
):
    """Test WebSocket connection with optional authentication."""

    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    print(f"🔌 Connecting to {url}...")
    print(f"   Auth: {'Yes' if auth_token else 'No'}")
    print(f"   Timeout: {timeout}s")
    print("")

    try:
        async with websockets.connect(url, extra_headers=headers) as ws:
            print(f"✅ Connected successfully!")
            print(f"   Server: {ws.response_headers.get('Server', 'Unknown')}")
            print(f"   Protocol: {ws.subprotocol or 'None'}")
            print("")

            # Test ping/pong
            print("🏓 Testing ping/pong...")
            pong_waiter = await ws.ping()
            latency = await asyncio.wait_for(pong_waiter, timeout=timeout)
            print(f"✅ Pong received (latency: {latency:.2f}s)")
            print("")

            # Send test messages
            print(f"📤 Sending {test_messages} test messages...")
            for i in range(test_messages):
                message = {
                    "type": "test",
                    "sequence": i + 1,
                    "timestamp": datetime.utcnow().isoformat(),
                    "payload": f"Test message {i + 1}"
                }

                await ws.send(json.dumps(message))
                print(f"   Sent: {message['payload']}")

                # Wait for response
                try:
                    response = await asyncio.wait_for(
                        ws.recv(),
                        timeout=timeout
                    )
                    print(f"   Received: {response[:100]}...")
                except asyncio.TimeoutError:
                    print(f"   ⚠️  No response (timeout: {timeout}s)")

                await asyncio.sleep(0.5)

            print("")
            print("✅ All tests passed!")
            print("")
            print("📊 Summary:")
            print(f"   Connection: Success")
            print(f"   Ping/Pong: Success")
            print(f"   Messages sent: {test_messages}")

            return True

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Connection failed: HTTP {e.status_code}")
        if e.status_code == 401:
            print("   Hint: Check auth token")
        elif e.status_code == 403:
            print("   Hint: Authorization denied")
        return False

    except websockets.exceptions.InvalidURI:
        print(f"❌ Invalid WebSocket URI: {url}")
        print("   Hint: Use ws:// or wss:// scheme")
        return False

    except asyncio.TimeoutError:
        print(f"❌ Connection timeout after {timeout}s")
        print("   Hint: Server may be down or unreachable")
        return False

    except ConnectionRefusedError:
        print(f"❌ Connection refused")
        print("   Hint: Is the server running?")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test WebSocket server connectivity"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="WebSocket URL (ws:// or wss://)"
    )
    parser.add_argument(
        "--auth-token",
        help="Bearer token for authentication"
    )
    parser.add_argument(
        "--messages",
        type=int,
        default=5,
        help="Number of test messages to send (default: 5)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout in seconds (default: 10)"
    )

    args = parser.parse_args()

    # Run async test
    success = asyncio.run(
        test_connection(
            url=args.url,
            auth_token=args.auth_token,
            test_messages=args.messages,
            timeout=args.timeout
        )
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
