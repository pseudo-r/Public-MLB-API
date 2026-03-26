# Schedule Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Schedule

**VERIFIED** — Returns games for a given date, date range, team, or sport.

**Endpoint:** `GET /schedule`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Sport filter (`1` = MLB) | `1` |
| `date` | ❌ | Single date `YYYY-MM-DD` | `2025-04-15` |
| `startDate` | ❌ | Range start `YYYY-MM-DD` | `2025-04-01` |
| `endDate` | ❌ | Range end `YYYY-MM-DD` | `2025-04-07` |
| `teamId` | ❌ | Filter to one team | `119` |
| `leagueId` | ❌ | Filter to one league | `103` |
| `season` | ❌ | Season year | `2025` |
| `gamePk` | ❌ | Single game PK | `745444` |
| `gameType` | ❌ | `R` (regular), `P` (postseason), `S` (spring training), `E` (exhibition) | `R` |
| `hydrate` | ❌ | Sub-resources to embed | `team,linescore,probablePitcher` |
| `fields` | ❌ | Fields to return | `dates,games,gamePk,gameDate` |

```bash
# All MLB games on April 15, 2025
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-04-15"

# Dodgers schedule for April 2025
curl "https://statsapi.mlb.com/api/v1/schedule?teamId=119&startDate=2025-04-01&endDate=2025-04-30"

# With linescore and probable pitchers embedded
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-04-15&hydrate=team,linescore,probablePitcher"

# Postseason schedule
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2024&gameType=P"

# Spring training schedule
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=2025&gameType=S"
```

**Response top-level keys:** `copyright`, `totalItems`, `totalEvents`, `totalGames`, `totalGamesInProgress`, `dates`

### Date object structure

```json
{
  "date": "2025-04-15",
  "totalItems": 13,
  "totalEvents": 0,
  "totalGames": 13,
  "totalGamesInProgress": 0,
  "games": [ ... ]
}
```

### Game object key fields

| Field | Description |
|-------|-------------|
| `gamePk` | Unique game primary key |
| `gameDate` | ISO 8601 datetime (UTC) |
| `officialDate` | Local date of game |
| `status.abstractGameState` | `Preview`, `Live`, `Final` |
| `status.detailedState` | `Scheduled`, `In Progress`, `Final`, `Postponed`, etc. |
| `status.codedGameState` | Single char code: `S`, `I`, `F`, `D`, `P`, `U` |
| `teams.home` / `teams.away` | Team objects with score |
| `venue` | Venue name and ID |
| `gameType` | `R`, `P`, `S`, `E` |
| `seriesDescription` | `Regular Season`, `Wild Card Series`, etc. |
| `doubleHeader` | `N`, `Y` |
| `isTie` | Boolean |

**Sample game object (abridged):**
```json
{
  "gamePk": 745444,
  "gameDate": "2024-10-05T20:08:00Z",
  "officialDate": "2024-10-05",
  "status": {
    "abstractGameState": "Final",
    "detailedState": "Final",
    "codedGameState": "F"
  },
  "teams": {
    "away": { "score": 2, "team": { "id": 119, "name": "Los Angeles Dodgers" }, "isWinner": false },
    "home": { "score": 3, "team": { "id": 137, "name": "San Francisco Giants" }, "isWinner": true }
  },
  "venue": { "id": 2395, "name": "Oracle Park" },
  "gameType": "R"
}
```

---

## Game Types

| Code | Description |
|------|-------------|
| `S` | Spring Training |
| `E` | Exhibition |
| `R` | Regular Season |
| `F` | Wild Card |
| `D` | Division Series (ALDS/NLDS) |
| `L` | League Championship Series (ALCS/NLCS) |
| `W` | World Series |
| `C` | Championship |
| `N` | Nineteenth Century |
| `P` | All Postseason |

---

## Coded Game States

| Code | State |
|------|-------|
| `S` | Scheduled |
| `P` | Pre-Game |
| `I` | In Progress |
| `F` | Final |
| `D` | Delayed |
| `U` | Suspended |
| `T` | Tied |
| `O` | Game Over |
