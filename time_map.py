from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)  # key -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        entries = self.store[key]
        i = bisect.bisect_right(entries, (timestamp, chr(127)))  # find upper bound
        if i == 0:
            return ""
        
        value = entries[i - 1][1]
        return "" if value is None else value

    def delete(self, key: str, timestamp: int) -> None:
        # Mark as deleted by storing (timestamp, None)
        self.store[key].append((timestamp, None))