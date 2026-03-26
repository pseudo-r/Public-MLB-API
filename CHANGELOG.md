# Changelog

All notable changes to the Public MLB API documentation are listed here.

---

## [Unreleased] — April 2025

### 🆕 Added

#### Documentation
- **`README.md`** — Base URL, quick start, all core endpoint patterns, team ID reference table, `hydrate` parameter guide
- **`docs/sports_leagues.md`** — Sports and leagues endpoints with response schemas
- **`docs/teams.md`** — Teams, roster, and team stats endpoints
- **`docs/schedule.md`** — Schedule endpoints with date/range/hydrate examples
- **`docs/standings.md`** — Standings endpoints with full field reference
- **`docs/people.md`** — Player profile, stats, game log, and search endpoints
- **`docs/game.md`** — Live feed, boxscore, linescore, play-by-play, decisions, content endpoints
- **`docs/venues.md`** — Venue list and detail with fieldInfo hydration
- **`docs/draft.md`** — MLB Draft endpoints with pick-level field reference
- **`docs/transactions.md`** — Transactions endpoint with type code reference
- **`docs/stats.md`** — Statistical leaders and aggregates with category reference
- **`CONTRIBUTING.md`** — Contribution guidelines and verification level definitions
- **`CHANGELOG.md`** (this file)

#### Verified Endpoints (live-tested against `statsapi.mlb.com`)
- `GET /api/v1/sports` ✅
- `GET /api/v1/leagues` ✅
- `GET /api/v1/teams?sportId=1` ✅
- `GET /api/v1/schedule?sportId=1&date=...` ✅
- `GET /api/v1/standings?leagueId=103,104&season=...` ✅
- `GET /api/v1/people/{personId}` ✅
- `GET /api/v1/people/{personId}/stats` ✅
- `GET /api/v1/game/{gamePk}/boxscore` ✅
- `GET /api/v1/game/{gamePk}/linescore` ✅
- `GET /api/v1/venues?sportId=1` ✅
- `GET /api/v1/draft/2024` ✅
- `GET /api/v1/transactions?startDate=...&endDate=...` ✅

---

## [1.0.0] — Initial Release

### 🆕 Added
- Initial MLB Stats API documentation
- Repository structure mirroring `Public-ESPN-API` and `Public-NBA-API`
- Live endpoint discovery via `statsapi.mlb.com`
