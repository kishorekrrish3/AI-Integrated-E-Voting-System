"""
Data Structures Module
Implements custom HashTable, Trie, and SegmentTree from scratch
"""

class HashTable:
    """Custom Hash Table implementation with chaining for collision resolution"""

    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.collision_count = 0

    def _hash(self, key):
        """Generate hash value for a key"""
        return hash(str(key)) % self.size

    def insert(self, key, value):
        """Insert or update key-value pair"""
        index = self._hash(key)

        # Check if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        # Track collisions
        if len(self.table[index]) > 0:
            self.collision_count += 1

        self.table[index].append((key, value))
        self.count += 1

    def get(self, key):
        """Retrieve value by key"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                self.count -= 1
                return True
        return False

    def contains(self, key):
        """Check if key exists"""
        return self.get(key) is not None

    def get_all(self):
        """Return all key-value pairs as dictionary"""
        result = {}
        for bucket in self.table:
            for key, value in bucket:
                result[key] = value
        return result

    def get_load_factor(self):
        """Calculate load factor (items per bucket)"""
        return self.count / self.size if self.size > 0 else 0

    def get_stats(self):
        """Get hash table statistics"""
        bucket_sizes = [len(bucket) for bucket in self.table]
        max_chain_length = max(bucket_sizes) if bucket_sizes else 0
        empty_buckets = sum(1 for size in bucket_sizes if size == 0)

        return {
            'total_items': self.count,
            'table_size': self.size,
            'load_factor': self.get_load_factor(),
            'collisions': self.collision_count,
            'max_chain_length': max_chain_length,
            'empty_buckets': empty_buckets,
            'utilization': ((self.size - empty_buckets) / self.size * 100) if self.size > 0 else 0
        }

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return self.get_all()

    def from_dict(self, data):
        """Load from dictionary"""
        for key, value in data.items():
            self.insert(key, value)


class TrieNode:
    """Node for Trie data structure"""

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data = None


class Trie:
    """Prefix Tree for efficient candidate name search and autocomplete"""

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word, data=None):
        """Insert word into Trie with optional associated data"""
        node = self.root
        word = word.lower()

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end_of_word:
            self.word_count += 1
        node.is_end_of_word = True
        node.data = data

    def search(self, word):
        """Search for exact word in Trie"""
        node = self._find_node(word.lower())
        return node.data if node and node.is_end_of_word else None

    def starts_with(self, prefix):
        """Find all words starting with prefix"""
        node = self._find_node(prefix.lower())
        if not node:
            return []

        results = []
        self._collect_words(node, prefix.lower(), results)
        return results

    def _find_node(self, prefix):
        """Find node corresponding to prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node, prefix, results):
        """Recursively collect all words from node"""
        if node.is_end_of_word:
            results.append({'word': prefix, 'data': node.data})

        for char, child_node in node.children.items():
            self._collect_words(child_node, prefix + char, results)

    def get_stats(self):
        """Get Trie statistics"""
        return {
            'total_words': self.word_count,
            'max_depth': self._get_max_depth(self.root, 0)
        }

    def _get_max_depth(self, node, depth):
        """Calculate maximum depth of Trie"""
        if not node.children:
            return depth
        return max(self._get_max_depth(child, depth + 1) for child in node.children.values())


class SegmentTree:
    """Segment Tree for range query operations (demo structure)"""

    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        if arr:
            self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        """Build segment tree from array"""
        if start == end:
            self.tree[node] = arr[start]
            return

        mid = (start + end) // 2
        self._build(arr, 2 * node + 1, start, mid)
        self._build(arr, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, left, right):
        """Query sum in range [left, right]"""
        if self.n == 0:
            return 0
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        """Recursive range query"""
        if right < start or left > end:
            return 0
        if left <= start and end <= right:
            return self.tree[node]

        mid = (start + end) // 2
        left_sum = self._query(2 * node + 1, start, mid, left, right)
        right_sum = self._query(2 * node + 2, mid + 1, end, left, right)
        return left_sum + right_sum

    def update(self, index, value):
        """Update value at index"""
        if self.n == 0:
            return
        self._update(0, 0, self.n - 1, index, value)

    def _update(self, node, start, end, index, value):
        """Recursive update"""
        if start == end:
            self.tree[node] = value
            return

        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node + 1, start, mid, index, value)
        else:
            self._update(2 * node + 2, mid + 1, end, index, value)

        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
