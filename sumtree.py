import numpy as np

class SumTree:
    def __init__(self, capacity):
        self.capacity = capacity  # 最大容量
        self.tree = np.zeros(2 * capacity - 1)  # 二叉樹陣列
        self.data = np.zeros(capacity, dtype=object)  # 儲存數據的陣列
        self.size = 0
        self.write = 0

    def _propagate(self, idx, change):
        """向上更新樹節點"""
        parent = (idx - 1) // 2
        self.tree[parent] += change

        if parent != 0:
            self._propagate(parent, change)

    def _retrieve(self, idx, s):
        """根據隨機數 s 查找樣本"""
        left = 2 * idx + 1
        right = left + 1

        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    def total_priority(self):
        """返回根節點的總優先級"""
        return self.tree[0]

    def add(self, priority, data):
        """添加數據及其對應的優先級"""
        idx = self.write + self.capacity - 1
        self.data[self.write] = data
        self.update(idx, priority)

        self.write += 1
        if self.write >= self.capacity:
            self.write = 0

        if self.size < self.capacity:
            self.size += 1

    def update(self, idx, priority):
        """更新樣本的優先級"""
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        self._propagate(idx, change)

    def get(self, s):
        """根據隨機數 s 返回樣本"""
        idx = self._retrieve(0, s)
        data_idx = idx - self.capacity + 1
        return (idx, self.tree[idx], self.data[data_idx])
