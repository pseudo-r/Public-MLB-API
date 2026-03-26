# Teams Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Teams List

**VERIFIED** — Returns all teams, optionally filtered by sport, league, or season.

**Endpoint:** `GET /teams`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter by sport (`1` = MLB) | `1` |
| `leagueIds` | ❌ | Filter by league IDs | `103,104` |
| `season` | ❌ | Season year | `2025` |
| `activeStatus` | ❌ | `Y`, `N`, or `B` (both) | `Y` |
| `hydrate` | ❌ | Sub-resources to embed | `league,division,venue` |
| `fields` | ❌ | Comma-separated fields | `teams,id,name,abbreviation` |

```bash
# All active MLB teams
curl "https://statsapi.mlb.com/api/v1/teams?sportId=1"

# All teams with venue info
curl "https://statsapi.mlb.com/api/v1/teams?sportId=1&hydrate=venue"

# AL teams only
curl "https://statsapi.mlb.com/api/v1/teams?leagueIds=103"
```

**Response top-level keys:** `copyright`, `teams`

**Key `teams[]` fields:** `id`, `name`, `teamName`, `locationName`, `shortName`, `abbreviation`, `teamCode`, `fileCode`, `firstYearOfPlay`, `active`, `venue`, `league`, `division`, `sport`, `record` (when hydrated)

**Sample response (abridged):**
```json
{
  "teams": [
    {
      "id": 119,
      "name": "Los Angeles Dodgers",
      "teamName": "Dodgers",
      "locationName": "Los Angeles",
      "abbreviation": "LAD",
      "teamCode": "lan",
      "firstYearOfPlay": "1884",
      "active": true,
      "venue": { "id": 22, "name": "Dodger Stadium", "link": "/api/v1/venues/22" },
      "league": { "id": 104, "name": "National League", "link": "/api/v1/league/104" },
      "division": { "id": 203, "name": "NL West", "link": "/api/v1/divisions/203" }
    }
  ]
}
```

---

## Single Team

**VERIFIED** — Returns details for a specific team.

**Endpoint:** `GET /teams/{teamId}`

```bash
# LA Dodgers
curl "https://statsapi.mlb.com/api/v1/teams/119"

# New York Yankees
curl "https://statsapi.mlb.com/api/v1/teams/147"
```

---

## Team Roster

**VERIFIED** — Returns the current roster for a team.

**Endpoint:** `GET /teams/{teamId}/roster`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `rosterType` | ❌ | `active`, `40Man`, `fullRoster`, `depthChart`, `gameday` | `active` |
| `season` | ❌ | Season year | `2025` |
| `date` | ❌ | Roster as of date | `2025-04-01` |
| `hydrate` | ❌ | Sub-resources to embed | `person` |

```bash
# LA Dodgers active roster
curl "https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=active"

# 40-man roster
curl "https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=40Man"

# Roster with full player info
curl "https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=active&hydrate=person"
```

**Response top-level keys:** `copyright`, `roster`, `teamId`, `rosterType`

**`roster[]` key fields:** `person` (id, fullName, link), `jerseyNumber`, `position` (code, name, type, abbreviation), `status` (code, description), `parentTeamId`

---

## Team Stats

**PARTIALLY VERIFIED** — Returns aggregated stats for a team.

**Endpoint:** `GET /teams/{teamId}/stats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `stats` | ✅ | `season`, `career`, `yearByYear` | `season` |
| `group` | ✅ | `hitting`, `pitching`, `fielding` | `hitting` |
| `season` | ❌ | Season year | `2025` |

```bash
# Dodgers 2025 team hitting stats
curl "https://statsapi.mlb.com/api/v1/teams/119/stats?stats=season&group=hitting&season=2025"

# Dodgers 2025 pitching stats
curl "https://statsapi.mlb.com/api/v1/teams/119/stats?stats=season&group=pitching&season=2025"
```

---

## Team Leaders

**PARTIALLY VERIFIED** — Returns statistical leaders within a team.

**Endpoint:** `GET /teams/{teamId}/leaders`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `leaderCategories` | ✅ | Stat category | `homeRuns` |
| `season` | ✅ | Season year | `2025` |
| `limit` | ❌ | Max results | `5` |

```bash
# Dodgers home run leaders 2025
curl "https://statsapi.mlb.com/api/v1/teams/119/leaders?leaderCategories=homeRuns&season=2025"
```

---

## Teams History

**UNVERIFIED** — Returns historical team information (name changes, relocations).

**Endpoint:** `GET /teams/history`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamIds` | ✅ | Team ID(s) | `119` |
| `startSeason` | ❌ | Start season | `1900` |
| `endSeason` | ❌ | End season | `2025` |
| `fields` | ❌ | Fields to return | — |

```bash
curl "https://statsapi.mlb.com/api/v1/teams/history?teamIds=119"
```

---

## Teams Affiliates

**UNVERIFIED** — Returns team affiliations (MLB team → MiLB affiliates).

**Endpoint:** `GET /teams/affiliates`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamIds` | ✅ | MLB team ID | `119` |
| `sportId` | ❌ | Sport filter | `1` |
| `season` | ❌ | Season year | `2025` |
| `fields` | ❌ | Fields to return | — |

```bash
# Dodgers minor league affiliates
curl "https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=119&season=2025"
```

---

## Team Alumni

**UNVERIFIED** — Returns alumni (former players) for a team.

**Endpoint:** `GET /teams/{teamId}/alumni`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamId` | ✅ (path) | Team ID | `119` |
| `season` | ✅ | Season year | `2024` |
| `group` | ❌ | `hitting`, `pitching`, `fielding` | `hitting` |
| `hydrate` | ❌ | Sub-resources | `person` |
| `fields` | ❌ | Fields to return | — |

```bash
# Dodgers 2024 alumni
curl "https://statsapi.mlb.com/api/v1/teams/119/alumni?season=2024"
```

---

## Team Coaches

**UNVERIFIED** — Returns coaching staff for a team.

**Endpoint:** `GET /teams/{teamId}/coaches`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamId` | ✅ (path) | Team ID | `119` |
| `season` | ❌ | Season year | `2025` |
| `date` | ❌ | Coaches as of date | `2025-04-01` |
| `fields` | ❌ | Fields to return | — |

```bash
# Dodgers 2025 coaching staff
curl "https://statsapi.mlb.com/api/v1/teams/119/coaches?season=2025"
```

---

## Team Personnel

**UNVERIFIED** — Returns front office and personnel for a team.

**Endpoint:** `GET /teams/{teamId}/personnel`

```bash
curl "https://statsapi.mlb.com/api/v1/teams/119/personnel"
```

---

## Team Uniforms

**UNVERIFIED** — Returns uniform information for a team's season.

**Endpoint:** `GET /uniforms/team`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `teamIds` | ✅ | Comma-separated team IDs | `119` |
| `season` | ❌ | Season year | `2025` |
| `fields` | ❌ | Fields to return | — |

```bash
curl "https://statsapi.mlb.com/api/v1/uniforms/team?teamIds=119&season=2025"
```
