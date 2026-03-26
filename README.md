# MLB Stats API Documentation

**Disclaimer:** This is documentation for MLB's undocumented public API. I am not affiliated with MLB. Use responsibly and follow MLB's terms of service.

---

## ☕ Support This Project

If this documentation has saved you time, consider supporting ongoing development and maintenance:

| Platform | Link |
|----------|------|
| ☕ Buy Me a Coffee | [buymeacoffee.com/pseudo_r](https://buymeacoffee.com/pseudo_r) |
| 💖 GitHub Sponsors | [github.com/sponsors/Kloverdevs](https://github.com/sponsors/Kloverdevs) |

---

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [API Versioning](#api-versioning)
- [API Endpoint Patterns](#api-endpoint-patterns)
  - [Sports & Leagues](#sports--leagues)
  - [Teams](#teams)
  - [Schedule](#schedule)
  - [Standings](#standings)
  - [People (Players)](#people-players)
  - [Game Data](#game-data)
  - [Venues](#venues)
  - [Draft](#draft)
  - [Transactions](#transactions)
  - [Stats](#stats)
  - [Reference](#reference)
- [Parameters Reference](#parameters-reference)
- [Docs](docs/)
- [CHANGELOG](CHANGELOG.md)

---

## Overview

MLB provides undocumented public APIs that power MLB.com, the MLB app, and Statcast. These endpoints return JSON data for scores, teams, players, statistics, standings, and more.

**Additional domains documented:** `statsapi.mlb.com` · `bdfed.stitch.mlbinfra.com` (Statcast)

### Important Notes

- **Unofficial:** These APIs are not officially supported and may change without notice
- **No Authentication Required:** All documented endpoints are publicly accessible
- **Rate Limiting:** No official limits published — implement caching and backoff in your applications
- **CORS:** The API does not enforce CORS, so browser requests work without a proxy

---

## Base URL

```
https://statsapi.mlb.com/api/v1/
```

All endpoints in this documentation use this base unless otherwise noted.

---

## Quick Start

```bash
# Get all MLB teams
curl "https://statsapi.mlb.com/api/v1/teams?sportId=1"

# Today's MLB schedule
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-04-15"

# AL/NL standings (current season)
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason"

# Shohei Ohtani's player profile
curl "https://statsapi.mlb.com/api/v1/people/660271"
```

---

## Authentication

No authentication is required. No API key, token, or header is needed for any of the documented endpoints.

---

## API Versioning

> **v1 is the only active version.** All documented endpoints use `/api/v1/`.

Live tests confirmed:

| Version path | Status |
|-------------|--------|
| `/api/v1/` | ✅ Active — all endpoints work here |
| `/api/v2/` | ❌ Dead — all routes return 404 |
| `/api/v3/` | ❌ Dead — all routes return 404 |

MLB's Stats API does not have a versioning scheme with separate v2/v3 branches the way ESPN's Core API does. All current and future endpoints live under `/api/v1/`.

---

### Sports & Leagues

> See [docs/sports_leagues.md](docs/sports_leagues.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /sports` | All sports tracked by the Statsapi |
| `GET /sports/{sportId}` | A single sport |
| `GET /leagues` | All leagues |
| `GET /leagues/{leagueId}` | A single league |

```bash
# All sports
curl "https://statsapi.mlb.com/api/v1/sports"

# MLB leagues (American League = 103, National League = 104)
curl "https://statsapi.mlb.com/api/v1/leagues"
```

**Response top-level keys:** `copyright`, `sports` / `leagues`

---

### Teams

> See [docs/teams.md](docs/teams.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /teams` | All teams (filter by `sportId`) |
| `GET /teams/{teamId}` | A single team |
| `GET /teams/{teamId}/roster` | Active roster for a team |
| `GET /teams/{teamId}/stats` | Team stats |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Sport filter (`1` = MLB) | `1` |
| `season` | ❌ | Season year | `2025` |
| `leagueIds` | ❌ | Filter by league IDs | `103,104` |
| `fields` | ❌ | Comma-separated field list to return | `teams,id,name` |

```bash
# All active MLB teams
curl "https://statsapi.mlb.com/api/v1/teams?sportId=1"

# LA Dodgers (teamId = 119)
curl "https://statsapi.mlb.com/api/v1/teams/119"

# LA Dodgers active roster
curl "https://statsapi.mlb.com/api/v1/teams/119/roster?rosterType=active"
```

**Response top-level keys:** `copyright`, `teams`

**Key team fields:** `id`, `name`, `teamName`, `abbreviation`, `teamCode`, `fileCode`, `venue`, `league`, `division`, `sport`, `locationName`, `firstYearOfPlay`, `active`

---

### Schedule

> See [docs/schedule.md](docs/schedule.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /schedule` | Games for a date or date range |
| `GET /schedule/games` | Same as `/schedule` |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Sport (`1` = MLB) | `1` |
| `date` | ❌ | Single date `YYYY-MM-DD` | `2025-04-15` |
| `startDate` | ❌ | Range start | `2025-04-01` |
| `endDate` | ❌ | Range end | `2025-04-07` |
| `teamId` | ❌ | Filter to one team | `119` |
| `leagueId` | ❌ | Filter to one league | `103` |
| `season` | ❌ | Season year | `2025` |
| `gamePk` | ❌ | Filter to one game | `745444` |
| `hydrate` | ❌ | Embed sub-resources | `team,linescore,probablePitcher` |

```bash
# All MLB games on April 1, 2025
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-04-01"

# Dodgers games in April 2025
curl "https://statsapi.mlb.com/api/v1/schedule?teamId=119&startDate=2025-04-01&endDate=2025-04-30"

# With linescore and probable pitchers
curl "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-04-01&hydrate=team,linescore,probablePitcher"
```

**Response top-level keys:** `copyright`, `totalItems`, `totalEvents`, `totalGames`, `totalGamesInProgress`, `dates`

**`dates[].games[]` key fields:** `gamePk`, `gameDate`, `status`, `teams`, `venue`, `linescore`, `seriesDescription`, `gameType`

---

### Standings

> See [docs/standings.md](docs/standings.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /standings` | Division standings |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `leagueId` | ✅ | AL = `103`, NL = `104` | `103,104` |
| `season` | ✅ | Season year | `2025` |
| `standingsTypes` | ❌ | `regularSeason`, `springTraining`, `firstHalf`, `secondHalf`, `playoffs` | `regularSeason` |
| `date` | ❌ | Standings as of date | `2025-07-04` |
| `hydrate` | ❌ | Embed sub-resources | `team,league,division` |

```bash
# AL and NL standings, 2025 regular season
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason"

# Standings as of a specific date
curl "https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=2025&standingsTypes=regularSeason&date=2025-07-04"
```

**Response top-level keys:** `copyright`, `records`

**`records[].teamRecords[]` key fields:** `team`, `wins`, `losses`, `winningPercentage`, `gamesBack`, `magicNumber`, `wildCardGamesBack`, `leagueRecord`, `divisionRecord`, `lastTen`, `streak`, `clinched`, `divisionRank`, `leagueRank`, `wildCardRank`, `sportRank`

---

### People (Players)

> See [docs/people.md](docs/people.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /people/{personId}` | Player profile |
| `GET /people/{personId}/stats` | Player stats |
| `GET /people/{personId}/currentGameStats` | Live game stats |
| `GET /people/{personId}/gameLog` | Game log |
| `GET /people/search` | Search players by name |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `personId` | ✅ (path) | MLB player ID | `660271` |
| `stats` | ❌ | Stats type: `season`, `career`, `yearByYear`, `gameLog` | `season` |
| `group` | ❌ | Stat group: `hitting`, `pitching`, `fielding` | `hitting` |
| `season` | ❌ | Season year | `2025` |
| `hydrate` | ❌ | Embed sub-resources | `stats(group=[hitting],type=[season])` |

```bash
# Shohei Ohtani profile
curl "https://statsapi.mlb.com/api/v1/people/660271"

# Ohtani 2024 hitting stats
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&group=hitting&season=2024"

# Ohtani 2024 pitching stats
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=season&group=pitching&season=2024"

# Ohtani career stats year-by-year
curl "https://statsapi.mlb.com/api/v1/people/660271/stats?stats=yearByYear&group=hitting"

# Search by name
curl "https://statsapi.mlb.com/api/v1/people/search?names=Ohtani"
```

**Response top-level keys:** `copyright`, `people`

**Key player fields:** `id`, `fullName`, `firstName`, `lastName`, `primaryNumber`, `currentTeam`, `primaryPosition`, `batSide`, `pitchHand`, `birthDate`, `birthCity`, `birthCountry`, `height`, `weight`, `active`, `mlbDebutDate`

---

### Game Data

> See [docs/game.md](docs/game.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /game/{gamePk}/feed/live` | Full live game feed (play-by-play, boxscore, linescore) |
| `GET /game/{gamePk}/boxscore` | Boxscore only |
| `GET /game/{gamePk}/linescore` | Linescore only |
| `GET /game/{gamePk}/playByPlay` | Play-by-play events |
| `GET /game/{gamePk}/winProbability` | Win probability by play |
| `GET /game/{gamePk}/decisions` | W/L/S pitcher decisions |
| `GET /game/{gamePk}/content` | Game media content (highlights, editorial) |

```bash
# Full live feed for game 745444
curl "https://statsapi.mlb.com/api/v1/game/745444/feed/live"

# Boxscore only
curl "https://statsapi.mlb.com/api/v1/game/745444/boxscore"

# Linescore only
curl "https://statsapi.mlb.com/api/v1/game/745444/linescore"

# Play-by-play
curl "https://statsapi.mlb.com/api/v1/game/745444/playByPlay"

# Pitcher decisions
curl "https://statsapi.mlb.com/api/v1/game/745444/decisions"

# Highlights and editorial
curl "https://statsapi.mlb.com/api/v1/game/745444/content"
```

**`/boxscore` top-level keys:** `copyright`, `teams`, `officials`, `info`, `pitchingNotes`

**`/linescore` top-level keys:** `copyright`, `currentInning`, `currentInningOrdinal`, `inningState`, `innings`, `teams`, `balls`, `strikes`, `outs`, `offense`, `defense`

> **Note:** `feed/live` may return 404 for completed historical games depending on the game PK. Use `/boxscore` and `/linescore` for historical data.

---

### Venues

> See [docs/venues.md](docs/venues.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /venues` | All venues |
| `GET /venues/{venueId}` | A single venue |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Filter by sport | `1` |
| `season` | ❌ | Season year | `2025` |
| `hydrate` | ❌ | Embed sub-resources | `location,fieldInfo` |

```bash
# All MLB venues
curl "https://statsapi.mlb.com/api/v1/venues?sportId=1"

# Dodger Stadium (venueId = 22) with field info
curl "https://statsapi.mlb.com/api/v1/venues/22?hydrate=location,fieldInfo"
```

**Response top-level keys:** `copyright`, `venues`

**Key venue fields:** `id`, `name`, `link`, `active`, `season`, `location` (city, state, country, latitude, longitude), `fieldInfo` (capacity, turfType, roofType, leftLine, leftCenter, center, rightCenter, rightLine)

---

### Draft

> See [docs/draft.md](docs/draft.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /draft/{year}` | Full draft results for a year |
| `GET /draft/{year}/latest` | Latest round/pick in an active draft |

```bash
# 2024 MLB Draft
curl "https://statsapi.mlb.com/api/v1/draft/2024"

# Live draft updates during draft week
curl "https://statsapi.mlb.com/api/v1/draft/2025/latest"
```

**Response top-level keys:** `copyright`, `drafts`

**`drafts.rounds[].picks[]` key fields:** `pickRound`, `pickNumber`, `roundPickNumber`, `rank`, `pickType`, `team`, `person` (name, id), `school`, `position`, `signingBonus`, `headshotLink`

---

### Transactions

> See [docs/transactions.md](docs/transactions.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /transactions` | Player transactions in a date range |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `startDate` | ✅ | Start date `YYYY-MM-DD` | `2025-03-01` |
| `endDate` | ✅ | End date `YYYY-MM-DD` | `2025-03-10` |
| `teamId` | ❌ | Filter to one team | `119` |
| `playerId` | ❌ | Filter to one player | `660271` |
| `sportId` | ❌ | Sport filter | `1` |
| `limit` | ❌ | Max records | `100` |

```bash
# All MLB transactions, March 1–10 2025
curl "https://statsapi.mlb.com/api/v1/transactions?startDate=2025-03-01&endDate=2025-03-10"

# Dodgers transactions only
curl "https://statsapi.mlb.com/api/v1/transactions?startDate=2025-03-01&endDate=2025-03-31&teamId=119"
```

**Response top-level keys:** `copyright`, `transactions`

**Key transaction fields:** `id`, `person`, `toTeam`, `fromTeam`, `date`, `effectiveDate`, `resolutionDate`, `typeCode`, `typeDesc`, `description`

---

### Stats

> See [docs/stats.md](docs/stats.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /stats` | Aggregated stats (cross-team, cross-player) |
| `GET /stats/leaders` | Statistical leaders (leaderboard) |
| `GET /stats/streaks` | Active streaks |

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `stats` | ✅ | `season`, `career`, `gameLog`, `yearByYear` | `season` |
| `group` | ✅ | `hitting`, `pitching`, `fielding` | `hitting` |
| `season` | ✅ | Season year | `2025` |
| `sportId` | ❌ | Sport filter | `1` |
| `leaderCategories` | ✅ (leaders) | Stat category to rank | `homeRuns` |
| `limit` | ❌ | Max leaders to return | `10` |

```bash
# Home run leaders, 2025
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=homeRuns&season=2025&sportId=1"

# ERA leaders, 2025
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=era&season=2025&sportId=1"

# Batting average leaders (top 10)
curl "https://statsapi.mlb.com/api/v1/stats/leaders?leaderCategories=battingAverage&season=2025&sportId=1&limit=10"
```

**`/stats/leaders` top-level keys:** `copyright`, `leagueLeaders`

**`leagueLeaders[].leaders[]` key fields:** `rank`, `value`, `team`, `league`, `person`

---

### Reference

> See [docs/reference.md](docs/reference.md) for full details.

| Endpoint | Description |
|----------|-------------|
| `GET /positions` | All position codes and types |
| `GET /gameTypes` | All game type codes |
| `GET /awards` | Awards list (MVP, Cy Young, etc.) |
| `GET /awards/{awardId}/recipients` | Award winners |
| `GET /attendance` | Team/league attendance records |
| `GET /jobs` | Umpire crew assignments |
| `GET /schedule/postseason` | Postseason bracket |
| `GET /schedule/postseason/series` | Postseason series breakdown |

```bash
# All positions
curl "https://statsapi.mlb.com/api/v1/positions"

# All game type codes
curl "https://statsapi.mlb.com/api/v1/gameTypes"

# All MLB awards
curl "https://statsapi.mlb.com/api/v1/awards?sportId=1"

# 2024 Cy Young recipients
curl "https://statsapi.mlb.com/api/v1/awards/MLBCY/recipients?season=2024"

# Dodgers 2024 attendance
curl "https://statsapi.mlb.com/api/v1/attendance?teamId=119&season=2024&gameType=R"

# Umpire assignments
curl "https://statsapi.mlb.com/api/v1/jobs?jobType=UMP&sportId=1&date=2025-04-15"
```

---


| Parameter | Type | Description |
|-----------|------|-------------|
| `sportId` | integer | `1` = MLB, `11` = AAA, `12` = AA, `13` = A+, `14` = A, `16` = ROK |
| `leagueId` | integer | `103` = American League, `104` = National League |
| `season` | integer | Season year (e.g., `2025`) |
| `teamId` | integer | MLB team ID (e.g., `119` = Dodgers, `147` = Yankees) |
| `gamePk` | integer | Unique game primary key |
| `personId` | integer | MLB player ID |
| `venueId` | integer | MLB venue ID |
| `date` | string | `YYYY-MM-DD` format |
| `startDate` | string | `YYYY-MM-DD` format |
| `endDate` | string | `YYYY-MM-DD` format |
| `hydrate` | string | Comma-separated list of sub-resources to embed in the response |
| `fields` | string | Comma-separated list of fields to include (response trimming) |
| `limit` | integer | Maximum records to return |
| `offset` | integer | Pagination offset |

### Common `hydrate` values

| Value | Description |
|-------|-------------|
| `team` | Embed full team object |
| `person` | Embed full person object |
| `venue` | Embed full venue object |
| `league` | Embed full league object |
| `division` | Embed full division object |
| `linescore` | Embed linescore in schedule response |
| `probablePitcher` | Embed probable pitcher in schedule |
| `stats(group=[hitting],type=[season])` | Embed stats inline |
| `currentTeam` | Embed current team in people response |
| `location,fieldInfo` | Embed venue location and field dimensions |

### Known Team IDs

| ID | Team | Abbreviation |
|----|------|-------------|
| `108` | Los Angeles Angels | LAA |
| `109` | Arizona Diamondbacks | ARI |
| `110` | Baltimore Orioles | BAL |
| `111` | Boston Red Sox | BOS |
| `112` | Chicago Cubs | CHC |
| `113` | Cincinnati Reds | CIN |
| `114` | Cleveland Guardians | CLE |
| `115` | Colorado Rockies | COL |
| `116` | Detroit Tigers | DET |
| `117` | Houston Astros | HOU |
| `118` | Kansas City Royals | KC |
| `119` | Los Angeles Dodgers | LAD |
| `120` | Washington Nationals | WSH |
| `121` | New York Mets | NYM |
| `133` | Oakland Athletics | ATH |
| `134` | Pittsburgh Pirates | PIT |
| `135` | San Diego Padres | SD |
| `136` | Seattle Mariners | SEA |
| `137` | San Francisco Giants | SF |
| `138` | St. Louis Cardinals | STL |
| `139` | Tampa Bay Rays | TB |
| `140` | Texas Rangers | TEX |
| `141` | Toronto Blue Jays | TOR |
| `142` | Minnesota Twins | MIN |
| `143` | Philadelphia Phillies | PHI |
| `144` | Atlanta Braves | ATL |
| `145` | Chicago White Sox | CWS |
| `146` | Miami Marlins | MIA |
| `147` | New York Yankees | NYY |
| `158` | Milwaukee Brewers | MIL |

---

## Response Structure

All MLB Stats API responses follow a consistent shape:

```json
{
  "copyright": "Copyright 2025 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt",
  "<data_key>": [ ... ]
}
```

The `<data_key>` matches the resource name (e.g., `teams`, `people`, `schedules`, `records`).

---

## Docs

| File | Description |
|------|-------------|
| [docs/sports_leagues.md](docs/sports_leagues.md) | Sports, leagues, and divisions |
| [docs/teams.md](docs/teams.md) | Teams, rosters, team stats |
| [docs/schedule.md](docs/schedule.md) | Schedule and game discovery |
| [docs/standings.md](docs/standings.md) | Division standings |
| [docs/people.md](docs/people.md) | Player profiles, stats, search |
| [docs/game.md](docs/game.md) | Live feed, boxscore, linescore, play-by-play |
| [docs/venues.md](docs/venues.md) | Stadiums and field dimensions |
| [docs/draft.md](docs/draft.md) | MLB Draft results |
| [docs/transactions.md](docs/transactions.md) | Trades, signings, IL moves |
| [docs/stats.md](docs/stats.md) | Statistical leaders and aggregates |
| [docs/reference.md](docs/reference.md) | Positions, game types, awards, attendance, umpires |

---

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute endpoint discoveries, corrections, and improvements.
