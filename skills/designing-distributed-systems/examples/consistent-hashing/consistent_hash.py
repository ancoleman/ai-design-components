"""
Consistent Hashing Implementation

Demonstrates: Consistent hashing with virtual nodes for even distribution

Dependencies:
    - Python 3.7+
    - No external dependencies (uses standard library)

Usage:
    python consistent_hash.py
"""

import hashlib
import bisect

class ConsistentHash:
    """Consistent hashing implementation with virtual nodes"""
    
    def __init__(self, nodes=None, replicas=150):
        """
        Initialize consistent hash ring
        
        Args:
            nodes: List of physical node identifiers
            replicas: Number of virtual nodes per physical node (default: 150)
        """
        self.replicas = replicas
        self.ring = {}  # hash -> physical node
        self.sorted_keys = []
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def _hash(self, key):
        """Hash function returning integer"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        """Add physical node with virtual replicas to the ring"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            self.ring[hash_val] = node
            bisect.insort(self.sorted_keys, hash_val)
        print(f"Added node '{node}' with {self.replicas} virtual nodes")
    
    def remove_node(self, node):
        """Remove physical node and its virtual replicas from the ring"""
        for i in range(self.replicas):
            virtual_key = f"{node}:{i}"
            hash_val = self._hash(virtual_key)
            if hash_val in self.ring:
                del self.ring[hash_val]
                self.sorted_keys.remove(hash_val)
        print(f"Removed node '{node}' and its virtual nodes")
    
    def get_node(self, key):
        """Find physical node responsible for key"""
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Binary search for first node >= hash_val
        idx = bisect.bisect(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0  # Wrap around to first node
        
        return self.ring[self.sorted_keys[idx]]
    
    def get_nodes(self, key, n=3):
        """Get N physical nodes for replication"""
        if not self.ring or n > len(set(self.ring.values())):
            return []
        
        hash_val = self._hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val)
        
        nodes = []
        seen = set()
        
        while len(nodes) < n:
            if idx >= len(self.sorted_keys):
                idx = 0
            
            node = self.ring[self.sorted_keys[idx]]
            if node not in seen:
                nodes.append(node)
                seen.add(node)
            
            idx += 1
        
        return nodes
    
    def distribution(self):
        """Analyze key distribution across nodes"""
        node_counts = {}
        test_keys = [f"key{i}" for i in range(10000)]
        
        for key in test_keys:
            node = self.get_node(key)
            node_counts[node] = node_counts.get(node, 0) + 1
        
        return node_counts


if __name__ == "__main__":
    # Create consistent hash ring with 4 nodes
    ch = ConsistentHash(['node1', 'node2', 'node3', 'node4'])
    
    # Test key assignments
    print("\nKey assignments:")
    test_keys = ['user123', 'user456', 'user789', 'product100']
    for key in test_keys:
        node = ch.get_node(key)
        replicas = ch.get_nodes(key, n=3)
        print(f"  {key} → {node} (replicas: {replicas})")
    
    # Check distribution
    print("\nInitial distribution (10,000 keys):")
    dist = ch.distribution()
    for node, count in sorted(dist.items()):
        percentage = (count / 10000) * 100
        print(f"  {node}: {count} keys ({percentage:.2f}%)")
    
    # Add new node and check redistribution
    print("\nAdding node5...")
    ch.add_node('node5')
    
    print("\nDistribution after adding node5:")
    dist = ch.distribution()
    for node, count in sorted(dist.items()):
        percentage = (count / 10000) * 100
        print(f"  {node}: {count} keys ({percentage:.2f}%)")
    
    # Remove node and check redistribution
    print("\nRemoving node2...")
    ch.remove_node('node2')
    
    print("\nDistribution after removing node2:")
    dist = ch.distribution()
    for node, count in sorted(dist.items()):
        percentage = (count / 10000) * 100
        print(f"  {node}: {count} keys ({percentage:.2f}%)")
