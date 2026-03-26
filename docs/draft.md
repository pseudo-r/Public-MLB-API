# Draft Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Draft Results

**VERIFIED** — Returns the full results of an MLB Draft for a given year.

**Endpoint:** `GET /draft/{year}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `year` | ✅ (path) | Draft year (4-digit) | `2024` |
| `teamId` | ❌ | Filter to one team | `119` |
| `round` | ❌ | Filter to one round | `1` |
| `limit` | ❌ | Max picks to return | `50` |
| `fields` | ❌ | Fields to return | `drafts,rounds,picks,person,team` |

```bash
# 2024 MLB Draft (all rounds)
curl "https://statsapi.mlb.com/api/v1/draft/2024"

# 2024 first round only
curl "https://statsapi.mlb.com/api/v1/draft/2024?round=1"

# 2024 Dodgers picks
curl "https://statsapi.mlb.com/api/v1/draft/2024?teamId=119"
```

**Response top-level keys:** `copyright`, `drafts`

### Drafts Object Structure

```json
{
  "drafts": {
    "draftYear": 2024,
    "rounds": [
      {
        "round": "1",
        "picks": [
          { ... }
        ]
      }
    ]
  }
}
```

### Pick Object Key Fields

| Field | Description |
|-------|-------------|
| `bisPlayerId` | Unique pick ID |
| `pickRound` | Round number string |
| `pickNumber` | Overall pick number |
| `roundPickNumber` | Pick number within round |
| `rank` | Pre-draft ranking |
| `pickType` | `"Competitive"`, `"Compensatory"`, etc. |
| `isPass` | Boolean — team passed on pick |
| `team` | `{ id, name, link }` |
| `person` | `{ id, fullName, link }` |
| `school` | `{ name, schoolType, country }` |
| `scoutingReport` | Scouting notes |
| `blurb` | Short description |
| `headshotLink` | URL to headshot image |
| `position` | `{ code, name, type, abbreviation }` |
| `signingBonus` | Signing bonus amount (USD) |
| `home` | `{ city, state, country }` |
| `year` | Draft year |
| `isDrafted` | Boolean |
| `isPass` | Boolean |

**Sample pick (abridged):**
```json
{
  "pickRound": "1",
  "pickNumber": 1,
  "roundPickNumber": 1,
  "team": { "id": 113, "name": "Cincinnati Reds" },
  "person": { "id": 695773, "fullName": "Brady House" },
  "school": { "name": "Winder-Barrow HS", "schoolType": "HighSchool" },
  "position": { "code": "6", "name": "Shortstop", "abbreviation": "SS" },
  "signingBonus": 7780000,
  "year": "2021"
}
```

---

## Latest Draft Pick (Live)

**UNVERIFIED** — Returns the most recent pick during an active draft.

**Endpoint:** `GET /draft/{year}/latest`

```bash
# Latest pick during 2025 draft
curl "https://statsapi.mlb.com/api/v1/draft/2025/latest"
```

> Use this endpoint during the MLB Draft event (typically held in July) for real-time pick data.
