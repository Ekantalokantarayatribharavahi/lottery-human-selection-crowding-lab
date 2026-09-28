# Lottery Human Selection Crowding Lab

Deterministic feature and scoring engine for estimating how human-looking a valid lottery combination is.

> Crowding score estimates expected player-selection concentration; it does not alter the lottery draw probability.

## CLI

```bash
crowding score --game lotto --combination "7,18,29,34,41,52"
crowding explain --game lotto --combination "7,18,29,34,41,52"
```

The MVP uses explicitly registered proxy features. Unverified intuition cannot silently enter production scoring.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```
