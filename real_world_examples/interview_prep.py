from __future__ import annotations
from typing import List, Tuple, Dict, Set, Iterable, Optional, Callable
from collections import defaultdict, deque
import heapq, hashlib, base64, dataclasses, time


# ============================================================
# 2) Content-Addressed Chunk Manifest
# ============================================================


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def build_manifest(s: str, c: int) -> Tuple[Set[str], List[str]]:
    """Part A — unique object set and ordered manifest (hex digests)."""
    objects=set(); manifest=[]
    bs = s.encode()
    for i in range(0, len(bs), c):
        chunk = bs[i:i+c]
        h = sha256_hex(chunk)
        objects.add(h)
        manifest.append(h)
    return objects, manifest

def to_store_for_idempotency(s: str, c: int, already: Set[str]) -> Set[str]:
    """Part B — only hashes not yet stored."""
    objs, _ = build_manifest(s, c)
    return objs - already

def resume_missing_indices(manifest: List[str], stored: Set[str]) -> List[int]:
    """Part C — indices whose hash not stored (upload in order)."""
    return [i for i,h in enumerate(manifest) if h not in stored]

# ------------------------------------------------------------
# demo:
# objs, man = build_manifest("ABABA", 2)
# print(len(objs), man)
# print(to_store_for_idempotency("ABABA", 2, already=set(list(objs)[:1])))
# print(resume_missing_indices(man, stored=set()))


# ============================================================
# 5) Rate Limiting & Resiliency Primitives
# ============================================================

class SlidingWindowCounter:
    """Part A — limit N in window W (ms). O(1) amortized per call."""
    def __init__(self, N:int, W_ms:int):
        self.N=N; self.W=W_ms
        self.qs: Dict[str, deque] = defaultdict(deque)

    def allow(self, key:str, now_ms:int) -> Tuple[bool,int,int]:
        q = self.qs[key]
        cutoff = now_ms - self.W
        while q and q[0] <= cutoff:
            q.popleft()
        if len(q) < self.N:
            q.append(now_ms)
            remaining = self.N - len(q)
            reset = self.W if len(q)==0 else self.W - (now_ms - q[0])
            return True, remaining, reset
        else:
            reset = self.W - (now_ms - q[0])
            return False, 0, max(reset,0)

class TokenBucket:
    """Part B — (capacity C, refill R tokens/sec)."""
    @dataclasses.dataclass
    class State:
        tokens: float
        last_ms: int
    def __init__(self, C:int, R_per_sec:float):
        self.C=float(C); self.R=R_per_sec
        self.state: Dict[str, TokenBucket.State] = {}
    def allow(self, key:str, now_ms:int) -> Tuple[bool,int,int]:
        st = self.state.get(key)
        if not st:
            st = TokenBucket.State(tokens=self.C, last_ms=now_ms)
            self.state[key]=st
        # refill
        delta = (now_ms - st.last_ms)/1000.0
        st.tokens = min(self.C, st.tokens + delta*self.R)
        st.last_ms = now_ms
        if st.tokens >= 1.0:
            st.tokens -= 1.0
            remaining = int(st.tokens)
            time_to_full = int(((self.C - st.tokens)/self.R)*1000) if self.R>0 else 0
            return True, remaining, time_to_full
        else:
            needed = 1.0 - st.tokens
            wait_ms = int((needed/self.R)*1000) if self.R>0 else 10**9
            return False, int(st.tokens), wait_ms

class CircuitBreaker:
    """Part C — Closed -> Open -> HalfOpen with cooldown & trial cap."""
    @dataclasses.dataclass
    class S:
        state: str = "Closed"           # Closed | Open | HalfOpen
        fails: int = 0
        opened_at: int = 0
        trials: int = 0

    def __init__(self, F:int, cooldown_ms:int, H:int):
        self.F=F; self.cooldown=cooldown_ms; self.H=H
        self.st: Dict[str, CircuitBreaker.S] = defaultdict(CircuitBreaker.S)

    def call(self, key:str, now_ms:int, fn:Callable[[], object]):
        s = self.st[key]
        # transitions on entry
        if s.state=="Open":
            if now_ms - s.opened_at >= self.cooldown:
                s.state="HalfOpen"; s.trials=0
            else:
                raise RuntimeError("circuit open (fail fast)")
        try:
            if s.state=="HalfOpen":
                if s.trials>=self.H:
                    raise RuntimeError("half-open trial limit reached")
                s.trials += 1
            # execute
            res = fn()
            # on success
            s.state="Closed"; s.fails=0; s.trials=0
            return res
        except Exception as e:
            # on failure
            s.fails += 1
            if s.state=="HalfOpen" or (s.state=="Closed" and s.fails>=self.F):
                s.state="Open"; s.opened_at=now_ms; s.trials=0
            raise
