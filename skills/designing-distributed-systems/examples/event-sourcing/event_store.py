"""
Event Sourcing Pattern

Demonstrates: Event store with replay and snapshots

Dependencies:
    - Python 3.7+

Usage:
    python event_store.py
"""

from datetime import datetime
from typing import List, Dict, Any

class Event:
    """Immutable event"""

    def __init__(self, aggregate_id: str, event_type: str, data: Dict, version: int):
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.data = data
        self.version = version
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return f"Event({self.event_type}, v{self.version}, {self.data})"


class EventStore:
    """Event store with replay capability"""

    def __init__(self):
        self.events = {}  # aggregate_id -> [events]
        self.snapshots = {}  # aggregate_id -> snapshot

    def append(self, aggregate_id: str, event: Event):
        """Append event to store"""
        if aggregate_id not in self.events:
            self.events[aggregate_id] = []
        self.events[aggregate_id].append(event)
        print(f"Appended: {event}")

    def get_events(self, aggregate_id: str, from_version=0):
        """Get events for aggregate starting from version"""
        events = self.events.get(aggregate_id, [])
        return [e for e in events if e.version >= from_version]

    def replay(self, aggregate_id: str):
        """Replay events to rebuild current state"""
        events = self.get_events(aggregate_id)
        state = {}

        for event in events:
            state = self._apply_event(state, event)

        return state

    def _apply_event(self, state: Dict, event: Event) -> Dict:
        """Apply event to state"""
        if event.event_type == 'AccountCreated':
            state['account_id'] = event.aggregate_id
            state['balance'] = event.data['initial_balance']
            state['status'] = 'active'

        elif event.event_type == 'MoneyDeposited':
            state['balance'] += event.data['amount']

        elif event.event_type == 'MoneyWithdrawn':
            state['balance'] -= event.data['amount']

        elif event.event_type == 'AccountClosed':
            state['status'] = 'closed'

        return state

    def create_snapshot(self, aggregate_id: str):
        """Create snapshot of current state"""
        state = self.replay(aggregate_id)
        version = len(self.events[aggregate_id])
        self.snapshots[aggregate_id] = {
            'state': state,
            'version': version,
            'timestamp': datetime.utcnow()
        }
        print(f"Snapshot created at version {version}")


if __name__ == "__main__":
    print("Event Sourcing Pattern Demo\n")

    event_store = EventStore()

    # Create account
    print("Creating account...")
    event_store.append('account-123', Event(
        aggregate_id='account-123',
        event_type='AccountCreated',
        data={'initial_balance': 1000},
        version=1
    ))

    # Deposit
    print("\nDeposit $500...")
    event_store.append('account-123', Event(
        aggregate_id='account-123',
        event_type='MoneyDeposited',
        data={'amount': 500},
        version=2
    ))

    # Withdraw
    print("\nWithdraw $200...")
    event_store.append('account-123', Event(
        aggregate_id='account-123',
        event_type='MoneyWithdrawn',
        data={'amount': 200},
        version=3
    ))

    # Replay to get current state
    print("\nReplaying events to get current state...")
    current_state = event_store.replay('account-123')
    print(f"Current state: {current_state}")

    # More transactions
    print("\nDeposit $1000...")
    event_store.append('account-123', Event(
        aggregate_id='account-123',
        event_type='MoneyDeposited',
        data={'amount': 1000},
        version=4
    ))

    print("\nReplaying events again...")
    current_state = event_store.replay('account-123')
    print(f"Current state: {current_state}")

    # Demonstrate time travel
    print("\nTime travel: Get state at version 2...")
    events_v2 = event_store.get_events('account-123', from_version=0)[:2]
    state_v2 = {}
    for event in events_v2:
        state_v2 = event_store._apply_event(state_v2, event)
    print(f"State at v2: {state_v2}")
