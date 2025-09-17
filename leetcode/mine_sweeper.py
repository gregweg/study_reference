from collections import deque
from dataclasses import dataclass, field
from typing import Set, Tuple, Iterable, List

Coord = Tuple[int, int]


@dataclass
class MineSweeper:
    rows: int
    cols: int
    mines: Set[Coord]  # {(r,c), ...}
    revealed: Set[Coord] = field(default_factory=set)
    flagged: Set[Coord] = field(default_factory=set)
    exploded: bool = False

    @staticmethod
    def from_mines(
        rows: int, cols: int, mine_positions: Iterable[Coord]
    ) -> "MineSweeper":
        mines = set(mine_positions)
        assert all(0 <= r < rows and 0 <= c < cols for r, c in mines), (
            "Mine out of bounds"
        )
        return MineSweeper(rows, cols, mines)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int) -> Iterable[Coord]:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield (nr, nc)

    def adj_count(self, r: int, c: int) -> int:
        return sum((nr, nc) in self.mines for nr, nc in self.neighbors(r, c))

    def step(self, r: int, c: int) -> None:
        """
        Reveal a cell. If it's a mine, game over.
        If it's a zero-adjacent-mine cell, flood-fill reveal neighbors.
        """
        if self.exploded or (r, c) in self.revealed or not self.in_bounds(r, c):
            return

        if (r, c) in self.mines:
            self.exploded = True
            self.revealed.add((r, c))
            return

        # BFS flood-fill on zeros; otherwise reveal just the cell.
        q: deque[Coord] = deque()
        q.append((r, c))
        while q:
            cr, cc = q.popleft()
            if (cr, cc) in self.revealed:
                continue
            self.revealed.add((cr, cc))
            if self.adj_count(cr, cc) == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if (nr, nc) not in self.revealed and (nr, nc) not in self.mines:
                        q.append((nr, nc))

    def is_won(self) -> bool:
        # Win if all non-mine cells are revealed and you haven't exploded
        return not self.exploded and len(self.revealed) == self.rows * self.cols - len(
            self.mines
        )

    def toggle_flag(self, r: int, c: int) -> None:
        if not self.in_bounds(r, c) or (r, c) in self.revealed:
            return
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
        else:
            self.flagged.add((r, c))

    def display(self, reveal_mines: bool = False) -> str:
        """
        Returns a string board view.
        - Hidden: '■'
        - Flagged: 'F'
        - Mine (if revealed or reveal_mines=True): '*'
        - Empty: '.' for zero-adjacent cells, or '1'..'8' for counts
        """
        lines: List[str] = []
        for r in range(self.rows):
            row_chars: List[str] = []
            for c in range(self.cols):
                pos = (r, c)
                if pos in self.revealed:
                    if pos in self.mines:
                        row_chars.append("*")
                    else:
                        cnt = self.adj_count(r, c)
                        row_chars.append("." if cnt == 0 else str(cnt))
                else:
                    if reveal_mines and pos in self.mines:
                        row_chars.append("*")
                    elif pos in self.flagged:
                        row_chars.append("F")
                    else:
                        row_chars.append("■")
            lines.append(" ".join(row_chars))
        return "\n".join(lines)


# --- Quick tests / sanity checks ---
if __name__ == "__main__":
    # 1) Zero flood-fill on a 3x3 with a single mine in a corner (2,2)
    g = MineSweeper.from_mines(3, 3, {(2, 2)})
    g.step(0, 0)  # (0,0) has adj_count 0 -> flood-fills
    assert not g.exploded
    assert (2, 2) not in g.revealed  # mine stays hidden
    # Flood-fill should reveal all non-mine cells (8 of them) in this simple layout
    assert len(g.revealed) == 8
    assert g.is_won()  # all safe cells revealed

    # 2) Stepping on a mine explodes
    g2 = MineSweeper.from_mines(2, 2, {(0, 1)})
    g2.step(0, 1)  # boom
    assert g2.exploded
    assert (0, 1) in g2.revealed
    _ = g2.display(reveal_mines=True)  # ensure no exceptions

    # 3) Win condition: 2x2 with one mine, reveal all safe cells
    g3 = MineSweeper.from_mines(2, 2, {(0, 0)})
    g3.step(0, 1)
    g3.step(1, 0)
    g3.step(1, 1)
    assert g3.is_won()
    assert not g3.exploded

    # 4) Flagging toggles and doesn't affect revealed
    g4 = MineSweeper.from_mines(2, 3, {(0, 2)})
    g4.toggle_flag(0, 2)
    assert (0, 2) in g4.flagged and (0, 2) not in g4.revealed
    g4.toggle_flag(0, 2)
    assert (0, 2) not in g4.flagged

    # 5) Clicking a non-zero should only reveal that cell
    g5 = MineSweeper.from_mines(3, 3, {(0, 0)})  # (1,1) has adj=1 here
    g5.step(1, 1)
    assert (1, 1) in g5.revealed
    assert len(g5.revealed) == 1  # no flood-fill expands

    print("All Minesweeper tests passed ✅")
