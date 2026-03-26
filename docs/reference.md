# Reference Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

These are lightweight reference/lookup endpoints that return static or semi-static configuration data.

---

## Positions

**VERIFIED** — Returns all position definitions used across MLB and MiLB.

**Endpoint:** `GET /positions`

```bash
curl "https://statsapi.mlb.com/api/v1/positions"
```

**Response:** Raw JSON array (no `copyright` wrapper).

**Sample response:**
```json
[
  { "code": "1", "shortName": "Pitcher", "fullName": "Pitcher", "abbrev": "P", "formalName": "Pitcher", "gamePosition": false, "pitcher": true, "type": "Pitcher" },
  { "code": "2", "shortName": "Catcher", "fullName": "Catcher", "abbrev": "C", "formalName": "Catcher", "gamePosition": true, "pitcher": false, "type": "Catcher" },
  { "code": "SS", "shortName": "Shortstop", "fullName": "Shortstop", "abbrev": "SS", "gamePosition": true, "pitcher": false, "type": "Infielder" }
]
```

**Key position codes:**

| Code | Position |
|------|----------|
| `1` | Pitcher |
| `2` | Catcher |
| `3` | First Base |
| `4` | Second Base |
| `5` | Third Base |
| `6` | Shortstop |
| `7` | Left Field |
| `8` | Center Field |
| `9` | Right Field |
| `10` | Designated Hitter |
| `11` | Pinch Hitter |
| `12` | Pinch Runner |
| `SS` | Shortstop (alt) |
| `OF` | Outfield (generic) |
| `IF` | Infield (generic) |
| `P` | Pitcher (alt) |
| `C` | Catcher (alt) |
| `DH` | Designated Hitter (alt) |

---

## Game Types

**VERIFIED** — Returns all valid game type codes and their descriptions.

**Endpoint:** `GET /gameTypes`

```bash
curl "https://statsapi.mlb.com/api/v1/gameTypes"
```

**Response:** Raw JSON array (no `copyright` wrapper).

```json
[
  { "id": "S", "description": "Spring Training" },
  { "id": "R", "description": "Regular Season" },
  { "id": "F", "description": "Wild Card Game" },
  { "id": "D", "description": "Division Series" },
  { "id": "L", "description": "League Championship Series" },
  { "id": "W", "description": "World Series" }
]
```

**Full game type reference:**

| Code | Description |
|------|-------------|
| `S` | Spring Training |
| `E` | Exhibition |
| `R` | Regular Season |
| `F` | Wild Card Game |
| `D` | Division Series (ALDS/NLDS) |
| `L` | League Championship Series (ALCS/NLCS) |
| `W` | World Series |
| `C` | Championship |
| `N` | Nineteenth Century Series |
| `P` | Playoffs (all postseason) |
| `A` | All-Star Game |
| `I` | Intraleague |
| `B` | Preseason |

---

## Awards

**VERIFIED** — Returns all awards tracked by MLB (MVP, Cy Young, Rookie, etc.).

**Endpoint:** `GET /awards`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter by sport | `1` |
| `leagueId` | ❌ | Filter by league | `103` |

```bash
# All MLB awards
curl "https://statsapi.mlb.com/api/v1/awards"

# With sport filter
curl "https://statsapi.mlb.com/api/v1/awards?sportId=1"
```

**Response top-level keys:** `copyright`, `awards`

**Key award fields:** `awardId`, `name`, `description`, `sport`, `league`, `notes`

**Notable award IDs:**

| ID | Award |
|----|-------|
| `MLBMVP` | MLB Most Valuable Player |
| `MLBCY` | Cy Young Award |
| `MLBROY` | Rookie of the Year |
| `MLBGOLD` | Gold Glove Award |
| `MLBSILVER` | Silver Slugger Award |
| `MLBHANK` | Hank Aaron Award |
| `MLBALL` | MLB All-Star selection |

### Award Recipients

**PARTIALLY VERIFIED** — Returns winners of a specific award.

**Endpoint:** `GET /awards/{awardId}/recipients`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `awardId` | ✅ (path) | Award ID string | `MLBMVP` |
| `season` | ❌ | Filter by season | `2024` |

```bash
# All MVP winners
curl "https://statsapi.mlb.com/api/v1/awards/MLBMVP/recipients"

# 2024 Cy Young winners
curl "https://statsapi.mlb.com/api/v1/awards/MLBCY/recipients?season=2024"
```

---

## Attendance

**VERIFIED** — Returns attendance records for a team or league.

**Endpoint:** `GET /attendance`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamId` | ❌ | Filter to team | `119` |
| `leagueId` | ❌ | Filter to league | `104` |
| `season` | ❌ | Season year | `2024` |
| `date` | ❌ | Specific date | `2024-07-04` |
| `leagueListId` | ❌ | League list | `mlb` |
| `gameType` | ❌ | Game type filter | `R` |
| `fields` | ❌ | Fields to return | `records,openingDay,attendance` |

```bash
# Dodgers 2024 attendance
curl "https://statsapi.mlb.com/api/v1/attendance?teamId=119&season=2024&gameType=R"

# NL 2024 attendance
curl "https://statsapi.mlb.com/api/v1/attendance?leagueId=104&season=2024"
```

**Response top-level key:** `records`

---

## Jobs (Umpires)

**VERIFIED** — Returns job/assignment information. Useful for umpire crew assignments.

**Endpoint:** `GET /jobs`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `jobType` | ❌ | `UMP` for umpires | `UMP` |
| `sportId` | ❌ | Sport filter | `1` |
| `date` | ❌ | Date for assignments | `2025-04-01` |

```bash
# Umpire assignments for April 1, 2025
curl "https://statsapi.mlb.com/api/v1/jobs?jobType=UMP&sportId=1&date=2025-04-01"
```

**Response top-level keys:** `copyright`, (minimal data — use `jobType=UMP` with a specific date)

---

## Schedule Post-Season

**PARTIALLY VERIFIED** — Returns the postseason bracket structure.

**Endpoint:** `GET /schedule/postseason`

```bash
# 2024 postseason bracket
curl "https://statsapi.mlb.com/api/v1/schedule/postseason?season=2024&sportId=1"

# 2024 postseason series
curl "https://statsapi.mlb.com/api/v1/schedule/postseason/series?season=2024&sportId=1"
```
