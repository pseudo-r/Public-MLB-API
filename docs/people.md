# People (Player) Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Player Profile

**VERIFIED** — Returns biographical and positional information for a player.

**Endpoint:** `GET /people/{personId}`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `personId` | ✅ (path) | MLB player ID | `660271` |
| `hydrate` | ❌ | Sub-resources to embed | `currentTeam,stats(group=[hitting],type=[season])` |
| `fields` | ❌ | Fields to return | `people,id,fullName` |

```bash
# Shohei Ohtani profile
curl "https://statsapi.mlb.com/api/v1/people/660271"

# Freddie Freeman profile
curl "https://statsapi.mlb.com/api/v1/people/518692"

# With current team embedded
curl "https://statsapi.mlb.com/api/v1/people/660271?hydrate=currentTeam"
```

**Response top-level keys:** `copyright`, `people`

**Key `people[]` fields:**

| Field | Description |
|-------|-------------|
| `id` | MLB player ID |
| `fullName` | Full name |
| `firstName` | First name |
| `lastName` | Last name |
| `primaryNumber` | Jersey number |
| `birthDate` | `YYYY-MM-DD` |
| `birthCity` | Birth city |
| `birthStateProvince` | State/province |
| `birthCountry` | Country |
| `height` | Height string (e.g., `"6' 4\""`) |
| `weight` | Weight in lbs |
| `active` | Boolean |
| `currentTeam` | `{ id, name, link }` |
| `primaryPosition` | `{ code, name, type, abbreviation }` |
| `batSide` | `{ code, description }` — `R`, `L`, or `S` |
| `pitchHand` | `{ code, description }` — `R` or `L` |
| `mlbDebutDate` | `YYYY-MM-DD` |
| `isPlayer` | Boolean |
| `isPitcher` | Boolean |
| `nameSlug` | URL-safe name (e.g., `shohei-ohtani`) |

**Sample response (abridged):**
```json
{
  "people": [
    {
      "id": 660271,
      "fullName": "Shohei Ohtani",
      "firstName": "Shohei",
      "lastName": "Ohtani",
      "primaryNumber": "17",
      "birthDate": "1994-07-05",
      "birthCity": "Oshu",
      "birthCountry": "Japan",
      "height": "6' 4\"",
      "weight": 210,
      "active": true,
      "currentTeam": { "id": 119, "name": "Los Angeles Dodgers" },
      "primaryPosition": { "code": "1", "name": "Pitcher", "type": "Pitcher", "abbreviation": "P" },
      "batSide": { "code": "L", "description": "Left" },
      "pitchHand": { "code": "R", "description": "Right" },
      "mlbDebutDate": "2018-03-29"
    }
  ]
}
```

---

## Player Stats

**VERIFIED** — Returns statistical data for a player.

**Endpoint:** `GET /people/{personId}/stats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `stats` | ✅ | Stat type | `season` |
| `group` | ✅ | Stat group | `hitting` |
| `season` | ❌ | Season year (required for `season` type) | `2025` |
| `gameType` | ❌ | `R`, `P`, `S` | `R` |
| `sitCodes` | ❌ | Situational code (see below) | `h` |

```bash
# Ohtani 2024 hitting stats
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&group=hitting&season=2024"

# Ohtani 2024 pitching stats
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&group=pitching&season=2024"

# Ohtani career hitting stats year-by-year
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=yearByYear&group=hitting"

# Ohtani 2024 postseason hitting
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&group=hitting&season=2024&gameType=P"
```

**Response top-level keys:** `copyright`, `stats`

### Stat Types

| Value | Description |
|-------|-------------|
| `season` | Full season stats |
| `career` | Career totals |
| `yearByYear` | Stats split by each season |
| `yearByYearAdvanced` | Advanced metrics year-by-year |
| `gameLog` | Game-by-game log |
| `lastXGames` | Stats over last N games |
| `byDateRange` | Stats for a date range |
| `byMonth` | Stats split by month |
| `homeAndAway` | Home vs. away splits |
| `winLoss` | Win vs. loss splits |
| `vsTeam` | Stats vs. a specific team |
| `vsPitcher` | Batter vs. specific pitcher |
| `vsBatter` | Pitcher vs. specific batter |
| `sabermetrics` | Advanced/sabermetric stats |

### Stat Groups

| Value | Description |
|-------|-------------|
| `hitting` | Batting stats |
| `pitching` | Pitching stats |
| `fielding` | Fielding stats |
| `catching` | Catcher-specific stats |
| `running` | Baserunning stats |

### Key Hitting Fields

`gamesPlayed`, `atBats`, `runs`, `hits`, `doubles`, `triples`, `homeRuns`, `rbi`, `stolenBases`, `caughtStealing`, `walks`, `strikeOuts`, `avg`, `obp`, `slg`, `ops`, `leftOnBase`, `groundBalls`, `airBalls`, `groundIntoDoublePlay`

### Key Pitching Fields

`wins`, `losses`, `era`, `gamesPlayed`, `gamesStarted`, `completeGames`, `shutouts`, `saves`, `saveOpportunities`, `holds`, `blownSaves`, `inningsPitched`, `hits`, `runs`, `earnedRuns`, `homeRuns`, `strikeOuts`, `baseOnBalls`, `whip`, `strikeoutWalkRatio`, `strikeoutsPer9Inn`, `walksPer9Inn`, `hitsPer9Inn`

---

## Game Log

**PARTIALLY VERIFIED** — Returns a game-by-game log for a player.

**Endpoint:** `GET /people/{personId}/stats` with `stats=gameLog`

```bash
# Ohtani 2025 game log (hitting)
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=gameLog&group=hitting&season=2025"
```

---

## Player Search

**PARTIALLY VERIFIED** — Search for players by name.

**Endpoint:** `GET /people/search`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `names` | ✅ | Player name to search | `Ohtani` |
| `active` | ❌ | `true` / `false` | `true` |
| `sportIds` | ❌ | Filter by sport | `1` |

```bash
# Search for Ohtani
curl "https://statsapi.mlb.com/api/v1/people/search?names=Ohtani"

# Search active MLB players named "Freeman"
curl "https://statsapi.mlb.com/api/v1/people/search?names=Freeman&active=true&sportIds=1"
```

---

## Notable Player IDs

| ID | Player | Team |
|----|--------|------|
| `660271` | Shohei Ohtani | LAD |
| `518692` | Freddie Freeman | LAD |
| `660670` | Ronald Acuña Jr. | ATL |
| `592450` | Aaron Judge | NYY |
| `665742` | Juan Soto | NYM |
| `605141` | Mookie Betts | LAD |
| `514888` | Clayton Kershaw | LAD |
| `477132` | Albert Pujols | — |
| `543037` | Gerrit Cole | NYY |
| `669203` | Adley Rutschman | BAL |
