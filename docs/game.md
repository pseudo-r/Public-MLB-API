# Game Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Live Game Feed

**PARTIALLY VERIFIED** — Returns the full game data package including boxscore, linescore, play-by-play, and metadata.

**Endpoint:** `GET /game/{gamePk}/feed/live`

```bash
# Full live feed for a game
curl "https://statsapi.mlb.com/api/v1/game/745444/feed/live"
```

**Response top-level keys:** `copyright`, `gamePk`, `metaData`, `gameData`, `liveData`

> **Note:** `feed/live` may return `404` for certain historical game PKs. Use `/boxscore` and `/linescore` as reliable alternatives for completed games.

### `gameData` key fields

| Field | Description |
|-------|-------------|
| `game` | Season, type, ID, double header flag |
| `datetime` | Game date/time |
| `status` | Game state (see coded states in schedule.md) |
| `teams` | Home and away team full objects |
| `players` | Map of player objects keyed by `ID{personId}` |
| `venue` | Full venue object |
| `weather` | `{ condition, temp, wind }` |
| `gameInfo` | Attendance, first pitch, game duration |
| `flags` | `noHitter`, `perfectGame`, `awayTeamNoHitter`, `homeTeamNoHitter` |
| `probablePitchers` | `{ home, away }` — player links |

### `liveData` key fields

| Field | Description |
|-------|-------------|
| `plays` | `currentPlay`, `allPlays[]`, `scoringPlays[]`, `playsByInning[]` |
| `linescore` | Full linescore object |
| `boxscore` | Full boxscore object |
| `decisions` | W/L/S pitcher decisions |
| `leaders` | In-game stat leaders |

---

## Boxscore

**VERIFIED** — Returns the boxscore for a completed or in-progress game.

**Endpoint:** `GET /game/{gamePk}/boxscore`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/boxscore"
```

**Response top-level keys:** `copyright`, `teams`, `officials`, `info`, `pitchingNotes`

### `teams` object structure

```json
{
  "teams": {
    "away": {
      "team": { "id": 119, "name": "Los Angeles Dodgers" },
      "teamStats": { "batting": { ... }, "pitching": { ... }, "fielding": { ... } },
      "players": { "ID660271": { ... } },
      "batters": [660271, ...],
      "pitchers": [543037, ...],
      "battingOrder": [660271, ...],
      "bench": [...],
      "bullpen": [...]
    },
    "home": { ... }
  }
}
```

### Player boxscore entry key fields

| Field | Description |
|-------|-------------|
| `person` | `{ id, fullName, link }` |
| `jerseyNumber` | Jersey number |
| `position` | `{ code, name, type, abbreviation }` |
| `status` | `{ code, description }` |
| `battingOrder` | Order string (e.g., `"100"` = leadoff) |
| `stats.batting` | Game batting line |
| `stats.pitching` | Game pitching line |
| `stats.fielding` | Fielding stats |
| `seasonStats.batting` | Season stats to date |

---

## Linescore

**VERIFIED** — Returns inning-by-inning scoring.

**Endpoint:** `GET /game/{gamePk}/linescore`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/linescore"
```

**Response top-level keys:** `copyright`, `currentInning`, `currentInningOrdinal`, `inningState`, `innings`, `teams`, `balls`, `strikes`, `outs`, `offense`, `defense`

**`innings[]` entry:**
```json
{
  "num": 1,
  "ordinalNum": "1st",
  "home": { "runs": 0, "hits": 1, "errors": 0, "leftOnBase": 1 },
  "away": { "runs": 2, "hits": 3, "errors": 0, "leftOnBase": 2 }
}
```

---

## Play-by-Play

**PARTIALLY VERIFIED** — Returns all play events for a game.

**Endpoint:** `GET /game/{gamePk}/playByPlay`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/playByPlay"
```

**Response top-level keys:** `copyright`, `allPlays`, `currentPlay`, `scoringPlays`, `playsByInning`

### Play object key fields

| Field | Description |
|-------|-------------|
| `result.type` | `atBat`, `action` |
| `result.event` | `"Single"`, `"Strikeout"`, `"Home Run"`, etc. |
| `result.description` | Full play description |
| `result.rbi` | RBI on this play |
| `result.awayScore` / `result.homeScore` | Score after play |
| `about.atBatIndex` | Sequential index |
| `about.halfInning` | `"top"` or `"bottom"` |
| `about.inning` | Inning number |
| `about.isScoringPlay` | Boolean |
| `about.isComplete` | Boolean |
| `count` | `{ balls, strikes, outs }` |
| `matchup` | `{ batter, pitcher, batSide, pitchHand }` |
| `pitchIndex` | Indices into `pitchData` |
| `actionIndex` | Indices into `actionPlayData` |
| `runners` | `[{ movement, details }]` |
| `playEvents` | Array of individual pitches/events |

---

## Win Probability

**PARTIALLY VERIFIED** — Returns win probability at each play.

**Endpoint:** `GET /game/{gamePk}/winProbability`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/winProbability"
```

Returns an array of objects, each with `atBatIndex`, `homeTeamWinProbability`, `awayTeamWinProbability`, and `homeTeamWinProbabilityAdded`.

---

## Pitcher Decisions

**PARTIALLY VERIFIED** — Returns the winning pitcher, losing pitcher, and save pitcher.

**Endpoint:** `GET /game/{gamePk}/decisions`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/decisions"
```

**Response top-level keys:** `copyright`, `winner`, `loser`, `save`

---

## Game Content

**PARTIALLY VERIFIED** — Returns editorial content, highlights, and media for a game.

**Endpoint:** `GET /game/{gamePk}/content`

```bash
curl "https://statsapi.mlb.com/api/v1/game/745444/content"
```

**Response top-level keys:** `copyright`, `link`, `editorial`, `media`, `highlights`, `summary`, `gameNotes`

`highlights.highlights.items[]` contains video highlight objects with `title`, `blurb`, `type`, `date`, `duration`, and nested `playbacks[]` (different quality streams).
