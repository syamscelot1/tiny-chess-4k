[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/syamscelot1/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/syamscelot1/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01 entry

A 3,649-byte chess engine in a single `main.py` (Python 3.13, standard
library only). Original code, MIT licensed. The packed `main.py` is built
from the readable `src.py` with `makefun compress` (the source is sent
beside the sessions when bundling; it is not committed).

## How it plays

- 0x88 board, negamax with alpha-beta pruning.
- Iterative deepening to a 100,000-node budget per move (deterministic:
  node count only, never the clock), keeping the last fully searched
  iteration's move.
- Quiescence search over captures and promotions at the horizon, with
  full check evasions (no stand-pat while in check).
- Transposition table storing score, bound flag (exact/lower/upper) and
  best move, keyed by Zobrist hash of pieces + side + en-passant file.
- Null-move pruning (R=2, only with non-pawn material and never in
  check, never twice in a row) and check extension (+1 ply).
- Killer moves (2 per ply) and MVV-LVA move ordering, TT best move first.
- Evaluation: material + piece-square tables (pawn, knight, bishop,
  rook, queen, king middlegame/endgame tapered by game phase) and a
  +30 bishop-pair bonus. En passant is generated and replayed
  correctly (including the captured pawn and the Zobrist hash).
- Legal moves are checked lazily inside the search (a move that leaves
  the king in check is skipped), so cutoffs never pay for moves that are
  never tried. Castling is supported.

## Protocol

Runs as `python3 -P -s /bot/main.py` and talks to the trial env at
`MAKEFUN_ENV_URL` (`POST /game`, `/move`). It assumes every game starts
from the standard position (the env's `START_FEN`) and replays the
game's move list to reach the current position.

## Size

`main.py` is 3,649 bytes (limit 4,096). Whole repo snapshot is under
the 8,192-byte cap, no file over 4,096.

## Local practice results (kit trials, this engine)

| trial | Elo | W/D/L |
|-------|-----|-------|
| trial-0 | 1364 | 3/1/2 |
| trial-1 | 1654 | 5/0/1 |
| trial-2 | 1545 | 4/1/1 |

Mean ≈ 1425, practice floor is 1,154. The first submission of the
previous engine scored 876 officially; this is a rewrite (the old
engine crashed on en-passant replays and had no null-move pruning,
no killer moves, no tapered king tables and no bishop-pair bonus).

## Grade it locally

With the competition dev kit and the `makefun` CLI (Docker driver):

    makefun grade-local --kit . --bot <your repository> --driver docker

Or drive the env yourself; see `RULES.txt` in the kit.
