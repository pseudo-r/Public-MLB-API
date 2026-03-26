# Venues Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Venues List

**VERIFIED** — Returns all venues tracked by the MLB Stats API.

**Endpoint:** `GET /venues`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter by sport (`1` = MLB) | `1` |
| `season` | ❌ | Season year | `2025` |
| `hydrate` | ❌ | Sub-resources to embed | `location,fieldInfo,timezone` |
| `fields` | ❌ | Fields to return | `venues,id,name` |

```bash
# All MLB venues
curl "https://statsapi.mlb.com/api/v1/venues?sportId=1"

# With location and field info hydrated
curl "https://statsapi.mlb.com/api/v1/venues?sportId=1&hydrate=location,fieldInfo"
```

**Response top-level keys:** `copyright`, `venues`

---

## Single Venue

**VERIFIED** — Returns details for a specific venue.

**Endpoint:** `GET /venues/{venueId}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `venueId` | ✅ (path) | Venue ID | `22` |
| `hydrate` | ❌ | Sub-resources | `location,fieldInfo,timezone` |
| `season` | ❌ | Season context | `2025` |

```bash
# Dodger Stadium
curl "https://statsapi.mlb.com/api/v1/venues/22"

# Dodger Stadium with full field info and location
curl "https://statsapi.mlb.com/api/v1/venues/22?hydrate=location,fieldInfo,timezone"

# Yankee Stadium
curl "https://statsapi.mlb.com/api/v1/venues/3313?hydrate=location,fieldInfo"
```

**Response top-level keys:** `copyright`, `venues`

---

### Venue Object Key Fields

| Field | Description |
|-------|-------------|
| `id` | Venue ID |
| `name` | Venue name |
| `link` | API link |
| `active` | Boolean |
| `season` | Season year |
| `location.address1` | Street address |
| `location.city` | City |
| `location.state` | State/province |
| `location.stateAbbrev` | State abbreviation |
| `location.postalCode` | Postal code |
| `location.country` | Country |
| `location.phone` | Venue phone |
| `location.latitude` | Latitude |
| `location.longitude` | Longitude |
| `timeZone.id` | IANA timezone (e.g., `America/Los_Angeles`) |
| `timeZone.offset` | UTC offset |
| `timeZone.offsetAtGameTime` | Offset during game |
| `timeZone.tz` | Abbreviation (e.g., `PDT`) |
| `fieldInfo.capacity` | Seating capacity |
| `fieldInfo.turfType` | `Grass` or `ArtificialTurf` |
| `fieldInfo.roofType` | `Open`, `Indoor`, `Retractable` |
| `fieldInfo.leftLine` | Left field line (ft) |
| `fieldInfo.left` | Left field (ft) |
| `fieldInfo.leftCenter` | Left-center field (ft) |
| `fieldInfo.center` | Center field (ft) |
| `fieldInfo.rightCenter` | Right-center field (ft) |
| `fieldInfo.right` | Right field (ft) |
| `fieldInfo.rightLine` | Right field line (ft) |

**Sample response (abridged):**
```json
{
  "venues": [
    {
      "id": 22,
      "name": "Dodger Stadium",
      "active": true,
      "location": {
        "city": "Los Angeles",
        "state": "California",
        "stateAbbrev": "CA",
        "country": "USA",
        "latitude": 34.07368,
        "longitude": -118.24015
      },
      "timeZone": { "id": "America/Los_Angeles", "tz": "PDT" },
      "fieldInfo": {
        "capacity": 56000,
        "turfType": "Grass",
        "roofType": "Open",
        "leftLine": 330,
        "leftCenter": 375,
        "center": 395,
        "rightCenter": 375,
        "rightLine": 330
      }
    }
  ]
}
```

---

### Notable Venue IDs

| ID | Venue | Team |
|----|-------|------|
| `22` | Dodger Stadium | LAD |
| `3313` | Yankee Stadium | NYY |
| `3289` | Fenway Park | BOS |
| `2395` | Oracle Park | SF |
| `4705` | Globe Life Field | TEX |
| `680` | Wrigley Field | CHC |
| `4169` | Truist Park | ATL |
| `2392` | Petco Park | SD |
| `2394` | T-Mobile Park | SEA |
| `4140` | loanDepot park | MIA |
