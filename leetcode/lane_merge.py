from dataclasses import dataclass
from typing import List, Literal, Tuple, Optional

Lane = Literal["A", "B"]
MergedEvent = Tuple[float, Lane, int]  # (merge_time, lane, idx_within_lane)


def other(l: Lane) -> Lane:
    return "B" if l == "A" else "A"


@dataclass
class LaneMerge:
    lane_a: List[float]
    lane_b: List[float]
    min_gap: float = 1.0
    start_turn: Lane = "A"
    epsilon: float = 1e-9

    def merge(self) -> List[MergedEvent]:
        i, j = 0, 0
        last_time = float("-inf")
        turn: Lane = self.start_turn
        out: List[MergedEvent] = []

        while i < len(self.lane_a) or j < len(self.lane_b):
            tA: Optional[float] = None
            tB: Optional[float] = None

            if i < len(self.lane_a):
                tA = max(self.lane_a[i], last_time + self.min_gap)
            if j < len(self.lane_b):
                tB = max(self.lane_b[j], last_time + self.min_gap)

            # Only A left
            if tA is not None and tB is None:
                last_time = tA
                out.append((last_time, "A", i))
                i += 1
                turn = other("A")
                continue

            # Only B left
            if tB is not None and tA is None:
                last_time = tB
                out.append((last_time, "B", j))
                j += 1
                turn = other("B")
                continue

            # Both candidates exist
            assert tA is not None and tB is not None
            if abs(tA - tB) <= self.epsilon:
                # Exact (or near) tie: use turn, then flip for next tie
                if turn == "A":
                    last_time = tA
                    out.append((last_time, "A", i))
                    i += 1
                    turn = other("A")
                else:
                    last_time = tB
                    out.append((last_time, "B", j))
                    j += 1
                    turn = other("B")
            elif tA < tB:
                last_time = tA
                out.append((last_time, "A", i))
                i += 1
                # Flip so next tie favors the other lane than who just merged
                turn = other("A")
            else:
                last_time = tB
                out.append((last_time, "B", j))
                j += 1
                turn = other("B")

        return out


# --- Quick tests / sanity checks ---
if __name__ == "__main__":
    # 1) Equal arrivals -> strict zipper starting with A
    sim = LaneMerge(lane_a=[0, 1, 2], lane_b=[0, 1, 2], min_gap=0.0, start_turn="A")
    merged = sim.merge()
    assert [(lane, idx) for _, lane, idx in merged] == [
        ("A", 0),
        ("B", 0),
        ("A", 1),
        ("B", 1),
        ("A", 2),
        ("B", 2),
    ]

    # 2) Unequal arrivals -> earliest goes first; ties alternate relative to last merged
    sim = LaneMerge(
        lane_a=[0.0, 0.2, 0.4], lane_b=[0.05, 0.25, 0.45], min_gap=0.0, start_turn="B"
    )
    merged = sim.merge()
    assert [lane for _, lane, _ in merged][:4] == ["A", "B", "A", "B"]

    # 3) Safety gap enforced (min_gap = 1.0); all cars queued at t=0
    sim = LaneMerge(lane_a=[0, 0, 0], lane_b=[0, 0, 0], min_gap=1.0, start_turn="A")
    merged = sim.merge()
    times = [t for t, _, _ in merged]
    assert all(abs(times[k] - k) < 1e-9 for k in range(6))  # 0,1,2,3,4,5

    # 4) Empty lane edge case
    sim = LaneMerge(lane_a=[0, 0.5], lane_b=[], min_gap=0.3)
    merged = sim.merge()
    assert [(lane, idx) for _, lane, idx in merged] == [("A", 0), ("A", 1)]

    # 5) Tight arrivals where gap stretches later cars (min_gap=0.5)
    sim = LaneMerge(lane_a=[0.0, 0.1], lane_b=[0.0, 0.1], min_gap=0.5, start_turn="A")
    merged = sim.merge()
    expected = [
        (0.0, "A", 0),
        (0.5, "B", 0),
        (1.0, "A", 1),
        (1.5, "B", 1),
    ]
    for (t1, l1, i1), (t2, l2, i2) in zip(merged, expected):
        assert l1 == l2 and i1 == i2 and abs(t1 - t2) < 1e-9

    print("All lane-merge tests passed ✅")
