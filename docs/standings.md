# Standings Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Standings

**VERIFIED** — Returns division standings for the American and National Leagues.

**Endpoint:** `GET /standings`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `leagueId` | ✅ | League IDs (`103` = AL, `104` = NL) | `103,104` |
| `season` | ✅ | Season year | `2025` |
| `standingsTypes` | ❌ | Standing type (see below) | `regularSeason` |
| `date` | ❌ | Standings as of a specific date | `2025-07-04` |
| `hydrate` | ❌ | Sub-resources to embed | `team,league,division` |
| `fields` | ❌ | Fields to return | `records,teamRecords,wins,losses` |

```bash
# AL and NL regular season standings
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason"

# AL standings with team and division hydrated
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103&season=2025&standingsTypes=regularSeason&hydrate=team,division"

# Mid-season standings (July 4)
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason&date=2025-07-04"
```

**Response top-level keys:** `copyright`, `records`

### Standings Types

| Value | Description |
|-------|-------------|
| `regularSeason` | Standard regular season standings |
| `wildCard` | Wild card standings |
| `divisionLeaders` | Division leader standings |
| `firstHalf` | First half standings (split-season leagues) |
| `secondHalf` | Second half standings |
| `springTraining` | Spring training standings |
| `firstHalfOnly` | First half only |
| `postseason` | Postseason standings |
| `byLeague` | League-level standings |
| `byDivision` | Division-level standings |

---

### Records Object

The `records` array contains one entry per division.

```json
{
  "records": [
    {
      "standingsType": "regularSeason",
      "league": { "id": 103, "name": "American League", "link": "/api/v1/league/103" },
      "division": { "id": 200, "name": "AL West", "link": "/api/v1/divisions/200" },
      "lastUpdated": "2025-04-15T12:00:00Z",
      "teamRecords": [ ... ]
    }
  ]
}
```

---

### Team Record Object Key Fields

| Field | Description |
|-------|-------------|
| `team` | Team name and ID |
| `wins` | Wins |
| `losses` | Losses |
| `ties` | Ties |
| `winningPercentage` | Win % as string (e.g., `".603"`) |
| `gamesBack` | Games behind first place |
| `wildCardGamesBack` | Wild card games behind |
| `leagueRecord` | `{ wins, losses, ties, pct }` |
| `divisionRecord` | `{ wins, losses, ties, pct }` |
| `records.splitRecords` | Home, away, last 10, road, etc. |
| `streak` | Current streak (e.g., `W3`) |
| `divisionRank` | Position in division |
| `leagueRank` | Overall league rank |
| `wildCardRank` | Wild card rank |
| `sportRank` | Overall MLB rank |
| `clinched` | Boolean — clinched division |
| `eliminationNumber` | Games until eliminated |
| `magicNumber` | Games until clinching |
| `runsScored` | Total runs scored |
| `runsAllowed` | Total runs allowed |
| `runDifferential` | Runs scored − runs allowed |

**Sample team record (abridged):**
```json
{
  "team": { "id": 119, "name": "Los Angeles Dodgers" },
  "wins": 98,
  "losses": 64,
  "winningPercentage": ".605",
  "gamesBack": "-",
  "wildCardGamesBack": "-",
  "divisionRank": "1",
  "leagueRank": "1",
  "streak": { "streakType": "wins", "streakNumber": 4, "streakCode": "W4" }
}
```

### Split Records

Each `teamRecord.records.splitRecords[]` entry has a `type` and `wins`/`losses`/`pct`:

| `type` | Description |
|--------|-------------|
| `home` | Home games |
| `away` | Away games |
| `lastTen` | Last 10 games |
| `extraInning` | Extra-inning games |
| `oneRun` | One-run games |
| `winners` | vs. winning teams |
| `day` | Day games |
| `night` | Night games |
| `grassSurface` | Grass surface games |
| `artificialTurf` | Turf surface games |
