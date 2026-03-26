# Seasons Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## All Seasons

**UNVERIFIED** — Returns a list of seasons, optionally limited to a sport.

**Endpoint:** `GET /seasons/all` or `GET /seasons`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Sport filter (`1` = MLB) | `1` |
| `divisionId` | ❌ | Filter by division | `200` |
| `withGameTypeDates` | ❌ | Include game-type date windows | `true` |
| `fields` | ❌ | Fields to return | `seasons,seasonId,seasonStartDate` |

```bash
# All MLB seasons
curl "https://statsapi.mlb.com/api/v1/seasons/all?sportId=1"

# All seasons with game type dates
curl "https://statsapi.mlb.com/api/v1/seasons/all?sportId=1&withGameTypeDates=true"
```

**Response top-level keys:** `copyright`, `seasons`

**Key `seasons[]` fields:** `seasonId`, `regularSeasonStartDate`, `regularSeasonEndDate`, `preSeasonStartDate`, `preSeasonEndDate`, `postSeasonStartDate`, `postSeasonEndDate`, `lastDate1stHalf`, `firstDate2ndHalf`, `allStarDate`, `sport`

---

## Single Season

**UNVERIFIED** — Returns details for a specific season.

**Endpoint:** `GET /seasons/{seasonId}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `seasonId` | ✅ (path) | Season year | `2025` |
| `sportId` | ❌ | Sport filter | `1` |
| `fields` | ❌ | Fields to return | `seasons,seasonId` |

```bash
# 2025 MLB season dates
curl "https://statsapi.mlb.com/api/v1/seasons/2025?sportId=1"

# 2024 season info
curl "https://statsapi.mlb.com/api/v1/seasons/2024?sportId=1"
```

**Sample response:**
```json
{
  "seasons": [
    {
      "seasonId": "2025",
      "regularSeasonStartDate": "2025-03-27",
      "regularSeasonEndDate": "2025-09-28",
      "preSeasonStartDate": "2025-02-21",
      "postSeasonStartDate": "2025-10-01",
      "allStarDate": "2025-07-15",
      "sport": { "id": 1, "link": "/api/v1/sports/1" }
    }
  ]
}
```
