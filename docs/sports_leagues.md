# Sports & Leagues Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Sports

**VERIFIED** — Returns all sports tracked by the MLB Stats API, including MLB, MiLB levels, and international leagues.

**Endpoint:** `GET /sports`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter to a single sport | `1` |
| `fields` | ❌ | Comma-separated fields to return | `sports,id,name` |

```bash
# All sports
curl "https://statsapi.mlb.com/api/v1/sports"

# MLB only
curl "https://statsapi.mlb.com/api/v1/sports/1"
```

**Response top-level keys:** `copyright`, `sports`

**Key `sports[]` fields:** `id`, `name`, `link`, `abbreviation`, `sortOrder`, `activeStatus`

**Known `sportId` values:**

| ID | Name |
|----|------|
| `1` | Major League Baseball |
| `11` | Triple-A |
| `12` | Double-A |
| `13` | High-A |
| `14` | Single-A |
| `16` | Rookie |
| `17` | Winter Leagues |
| `51` | International Baseball |
| `508` | College Baseball |
| `586` | Amateur / Independent |

---

## Leagues

**VERIFIED** — Returns all leagues, optionally filtered by sport.

**Endpoint:** `GET /leagues`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter leagues by sport | `1` |
| `leagueId` | ❌ | Single league | `103` |
| `season` | ❌ | Season year | `2025` |
| `fields` | ❌ | Comma-separated fields | `leagues,id,name` |

```bash
# All leagues
curl "https://statsapi.mlb.com/api/v1/leagues"

# MLB leagues only (AL + NL)
curl "https://statsapi.mlb.com/api/v1/leagues?sportId=1"

# American League only
curl "https://statsapi.mlb.com/api/v1/leagues/103"
```

**Response top-level keys:** `copyright`, `leagues`

**Key `leagues[]` fields:** `id`, `name`, `link`, `abbreviation`, `nameShort`, `seasonState`, `hasWildCard`, `hasSplitSeason`, `numGames`, `hasPlayoffPoints`, `numTeams`, `numWildcardTeams`, `seasonDateInfo`, `season`, `orgCode`, `conferencesInUse`, `divisionsInUse`, `sport`, `sortOrder`, `active`

**Known MLB league IDs:**

| ID | Name |
|----|------|
| `103` | American League |
| `104` | National League |

**Sample response (abridged):**
```json
{
  "copyright": "Copyright 2025 MLB Advanced Media...",
  "leagues": [
    {
      "id": 103,
      "name": "American League",
      "link": "/api/v1/league/103",
      "abbreviation": "AL",
      "nameShort": "American",
      "seasonState": "inseason",
      "hasWildCard": true,
      "numGames": 162,
      "numTeams": 15,
      "sport": { "id": 1, "link": "/api/v1/sports/1", "name": "Major League Baseball" }
    }
  ]
}
```

---

## Divisions

**PARTIALLY VERIFIED** — Returns division information.

**Endpoint:** `GET /divisions`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `leagueId` | ❌ | Filter by league | `103` |
| `sportId` | ❌ | Filter by sport | `1` |
| `divisionId` | ❌ | Single division | `200` |

```bash
# All MLB divisions
curl "https://statsapi.mlb.com/api/v1/divisions?sportId=1"

# AL divisions only
curl "https://statsapi.mlb.com/api/v1/divisions?leagueId=103"
```

**Known division IDs:**

| ID | Name |
|----|------|
| `200` | AL West |
| `201` | AL East |
| `202` | AL Central |
| `203` | NL West |
| `204` | NL East |
| `205` | NL Central |
