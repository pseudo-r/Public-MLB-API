# Stats Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Statistical Leaders

**VERIFIED** — Returns a leaderboard for a given statistical category.

**Endpoint:** `GET /stats/leaders`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `leaderCategories` | ✅ | Stat category to rank (see below) | `homeRuns` |
| `season` | ✅ | Season year | `2025` |
| `sportId` | ❌ | Sport filter (`1` = MLB) | `1` |
| `leagueId` | ❌ | Limit to one league | `103` |
| `teamId` | ❌ | Limit to one team | `119` |
| `statGroup` | ❌ | `hitting`, `pitching`, `fielding`, `running` | `hitting` |
| `gameType` | ❌ | `R` (regular), `P` (postseason) | `R` |
| `limit` | ❌ | Max leaders | `10` |
| `offset` | ❌ | Pagination offset | `0` |
| `position` | ❌ | Filter by position code (e.g., `P`, `C`, `1B`) | `SS` |

```bash
# Home run leaders, 2025
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=homeRuns&season=2025&sportId=1"

# ERA leaders, top 10
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=era&season=2025&sportId=1&limit=10"

# Batting average leaders, AL only
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=battingAverage&season=2025&leagueId=103&limit=10"

# Stolen base leaders
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=stolenBases&season=2025&sportId=1"

# Saves leaders
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=saves&season=2025&sportId=1"
```

**Response top-level keys:** `copyright`, `leagueLeaders`

### Response Structure

```json
{
  "leagueLeaders": [
    {
      "leaderCategory": "homeRuns",
      "season": "2025",
      "gameType": { "id": "R", "description": "Regular Season" },
      "leaders": [
        {
          "rank": 1,
          "value": "42",
          "team": { "id": 119, "name": "Los Angeles Dodgers" },
          "league": { "id": 104, "name": "National League" },
          "person": { "id": 660271, "fullName": "Shohei Ohtani", "link": "/api/v1/people/660271" }
        }
      ]
    }
  ]
}
```

---

### Hitting Leader Categories

| Category | Description |
|----------|-------------|
| `battingAverage` | Batting average |
| `onBasePercentage` | On-base percentage |
| `slugging` | Slugging percentage |
| `onBasePlusSlugging` | OPS |
| `hits` | Hits |
| `homeRuns` | Home runs |
| `doubles` | Doubles |
| `triples` | Triples |
| `totalBases` | Total bases |
| `rbi` | Runs batted in |
| `runs` | Runs scored |
| `stolenBases` | Stolen bases |
| `walks` | Walks (BB) |
| `strikeouts` | Strikeouts |
| `groundIntoDoublePlay` | GIDP |
| `atBats` | At-bats |
| `plateAppearances` | Plate appearances |
| `sacBunts` | Sacrifice bunts |
| `sacFlies` | Sacrifice flies |
| `hitByPitch` | Hit by pitch |
| `intentionalWalks` | Intentional walks |

---

### Pitching Leader Categories

| Category | Description |
|----------|-------------|
| `era` | Earned run average |
| `wins` | Wins |
| `losses` | Losses |
| `saves` | Saves |
| `holds` | Holds |
| `blownSaves` | Blown saves |
| `strikeouts` | Strikeouts |
| `walks` | Walks (BB) |
| `whip` | WHIP |
| `inningsPitched` | Innings pitched |
| `earnedRuns` | Earned runs |
| `homeRuns` | Home runs allowed |
| `shutouts` | Shutouts |
| `completeGames` | Complete games |
| `strikeoutsPer9Inn` | K/9 |
| `walksPer9Inn` | BB/9 |
| `strikeoutWalkRatio` | K/BB |
| `hitsPer9Inn` | H/9 |
| `saveOpportunities` | Save opportunities |

---

## Stats Aggregates

**PARTIALLY VERIFIED** — Returns aggregate stats across players or teams.

**Endpoint:** `GET /stats`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `stats` | ✅ | `season`, `career`, `yearByYear` | `season` |
| `group` | ✅ | `hitting`, `pitching`, `fielding` | `hitting` |
| `season` | ❌ | Season year | `2025` |
| `teamId` | ❌ | Filter to team | `119` |
| `playerPool` | ❌ | `All`, `Qualified`, `Rookies` | `Qualified` |
| `position` | ❌ | Position filter | `OF` |
| `limit` | ❌ | Results limit | `50` |
| `offset` | ❌ | Pagination offset | `0` |
| `sortStat` | ❌ | Sort by stat | `homeRuns` |
| `order` | ❌ | `asc` or `desc` | `desc` |

```bash
# Qualified hitters, 2025, sorted by OPS
curl "https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&season=2025&playerPool=Qualified&sortStat=onBasePlusSlugging&order=desc"

# All pitchers, 2025 ERA
curl "https://statsapi.mlb.com/api/v1/stats?stats=season&group=pitching&season=2025&playerPool=Qualified&sortStat=era&order=asc"
```

---

## Active Streaks

**PARTIALLY VERIFIED** — Returns players with active hitting, on-base, or win streaks.

**Endpoint:** `GET /stats/streaks`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `streakType` | ✅ | `hitting`, `onBase`, `wins`, `saves` | `hitting` |
| `streakSpan` | ❌ | `career`, `season` | `season` |
| `season` | ❌ | Season year | `2025` |
| `sportId` | ❌ | Sport filter | `1` |
| `limit` | ❌ | Max results | `10` |

```bash
# Active hitting streaks
curl "https://statsapi.mlb.com/api/v1/stats/streaks?streakType=hitting&streakSpan=season&season=2025&sportId=1"
```
