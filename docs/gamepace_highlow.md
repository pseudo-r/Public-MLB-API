# Game Pace & High-Low Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Game Pace

**UNVERIFIED** — Returns pace-of-game metrics (average game time, time between pitches, etc.) for a season.

**Endpoint:** `GET /gamePace`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `season` | ✅ | Season year | `2025` |
| `teamIds` | ❌ | Comma-separated team IDs | `119,147` |
| `leagueIds` | ❌ | Filter by league | `103,104` |
| `leagueListId` | ❌ | Predefined league list | `mlb` |
| `sportId` | ❌ | Sport filter | `1` |
| `gameType` | ❌ | Game type filter | `R` |
| `startDate` | ❌ | `YYYY-MM-DD` | `2025-04-01` |
| `endDate` | ❌ | `YYYY-MM-DD` | `2025-04-30` |
| `venueIds` | ❌ | Venue filter | `22` |
| `orgType` | ❌ | Organization type | `team` |
| `includeChildren` | ❌ | Include minor leagues | `false` |
| `fields` | ❌ | Fields to return | — |

```bash
# 2025 MLB game pace (all teams)
curl "https://statsapi.mlb.com/api/v1/gamePace?season=2025&sportId=1"

# Dodgers 2025 game pace
curl "https://statsapi.mlb.com/api/v1/gamePace?season=2025&teamIds=119"
```

**Response top-level keys:** `copyright`, `sports` (or `teams` depending on `orgType`)

---

## High-Low Records

**UNVERIFIED** — Returns single-game or single-season high/low statistical records.

**Endpoint:** `GET /highLow/{orgType}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `orgType` | ✅ (path) | Org type — `player`, `team`, `division`, `league`, `sport` | `player` |
| `sortStat` | ✅ | Stat to rank by | `homeRuns` |
| `season` | ✅ | Season year | `2025` |
| `statGroup` | ❌ | `hitting`, `pitching`, `fielding` | `hitting` |
| `gameType` | ❌ | Game type | `R` |
| `teamId` | ❌ | Filter to team | `119` |
| `leagueId` | ❌ | Filter to league | `104` |
| `sportIds` | ❌ | Sport filter | `1` |
| `limit` | ❌ | Max results | `10` |
| `fields` | ❌ | Fields to return | — |

```bash
# Player single-game home run highs, 2025
curl "https://statsapi.mlb.com/api/v1/highLow/player?sortStat=homeRuns&season=2025&statGroup=hitting&sportIds=1"

# Team single-game run highs
curl "https://statsapi.mlb.com/api/v1/highLow/team?sortStat=runs&season=2025&statGroup=hitting&sportIds=1"

# Pitching strikeout highs
curl "https://statsapi.mlb.com/api/v1/highLow/player?sortStat=strikeOuts&season=2025&statGroup=pitching&sportIds=1"
```

**Valid `orgType` values:** `player`, `team`, `division`, `league`, `sport`, `types`

---

## Home Run Derby

**UNVERIFIED** — Returns Home Run Derby bracket and pool data for the All-Star Game weekend.

**Endpoint:** `GET /homeRunDerby/{gamePk}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `gamePk` | ✅ (path) | HRD game PK | `745444` |
| `bracket` | ❌ | Append `/bracket` to URL | — |
| `pool` | ❌ | Append `/pool` to URL | — |
| `fields` | ❌ | Fields to return | — |

```bash
# Home Run Derby bracket
curl "https://statsapi.mlb.com/api/v1/homeRunDerby/{gamePk}/bracket"

# Pool data
curl "https://statsapi.mlb.com/api/v1/homeRunDerby/{gamePk}/pool"
```

> Use the Schedule endpoint with `gameType=A` (All-Star) to find the correct gamePk for the Home Run Derby.
