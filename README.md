[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/syamscelot1/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/syamscelot1/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01 entry

A 4,091-byte chess engine in a single `main.py` (Python 3.13, standard
library only). Original code, MIT licensed.

## How it plays

- 0x88 board, negamax with alpha-beta pruning.
- Iterative deepening to a 50,000-node budget per move (deterministic:
  node count only, never the clock), keeping the last fully searched
  iteration's move.
- Quiescence search over captures and promotions at the horizon.
- Transposition table (score, keyed by Zobrist hash of pieces + side).
- Piece-square tables (pawn, knight, bishop, king) plus material values;
  MVV-LVA move ordering.
- Legal moves are checked lazily inside the search (a move that leaves
  the king in check is skipped), so cutoffs never pay for moves that are
  never tried. Castling is supported; en passant captures are not
  generated (a deliberate size trade-off — they are rare, and the engine
  never plays an illegal move because of it).

## Protocol

Runs as `python3 -P -s /bot/main.py` and talks to the trial env at
`MAKEFUN_ENV_URL` (`POST /game`, `/move`). It assumes every game starts
from the standard position (the env's `START_FEN`) and replays the
game's move list to reach the current position.

## Size

`main.py` is 4,091 bytes (limit 4,096). Whole repo snapshot is under
the 8,192-byte cap, no file over 4,096.

## Grade it locally

With the competition dev kit and the `makefun` CLI (Docker driver):

    makefun grade-local --kit . --bot <your repository> --driver docker

Or drive the env yourself; see `RULES.txt` in the kit.
