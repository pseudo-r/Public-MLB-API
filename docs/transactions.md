# Transactions Endpoints

> All endpoints use base URL `https://statsapi.mlb.com/api/v1/`.

---

## Transactions

**VERIFIED** — Returns player transactions (trades, signings, DFA, IL placements, call-ups, optionals) in a date range.

**Endpoint:** `GET /transactions`

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `startDate` | ✅ | Start date `YYYY-MM-DD` | `2025-03-01` |
| `endDate` | ✅ | End date `YYYY-MM-DD` | `2025-03-10` |
| `teamId` | ❌ | Filter to one team | `119` |
| `playerId` | ❌ | Filter to one player | `660271` |
| `sportId` | ❌ | Sport filter (`1` = MLB) | `1` |
| `limit` | ❌ | Max records | `100` |
| `offset` | ❌ | Pagination offset | `0` |
| `fields` | ❌ | Fields to return | `transactions,id,person,typeDesc,date` |

```bash
# All MLB transactions, March 1–10 2025
curl "https://statsapi.mlb.com/api/v1/transactions?startDate=2025-03-01&endDate=2025-03-10"

# Dodgers transactions, full spring training
curl "https://statsapi.mlb.com/api/v1/transactions?startDate=2025-02-15&endDate=2025-03-31&teamId=119"

# Transactions for a specific player
curl "https://statsapi.mlb.com/api/v1/transactions?startDate=2024-01-01&endDate=2024-12-31&playerId=660271"
```

**Response top-level keys:** `copyright`, `transactions`

---

### Transaction Object Key Fields

| Field | Description |
|-------|-------------|
| `id` | Transaction ID |
| `person` | `{ id, fullName, link }` — the player |
| `toTeam` | `{ id, name, link }` — destination team |
| `fromTeam` | `{ id, name, link }` — origin team |
| `date` | Transaction date `YYYY-MM-DD` |
| `effectiveDate` | Date the transaction takes effect |
| `resolutionDate` | Date resolved (e.g., IL return) |
| `typeCode` | Short code (see Transaction Types) |
| `typeDesc` | Human-readable description |
| `description` | Full transaction description |

**Sample transaction:**
```json
{
  "id": 1001234,
  "person": { "id": 660271, "fullName": "Shohei Ohtani" },
  "toTeam": { "id": 119, "name": "Los Angeles Dodgers" },
  "fromTeam": null,
  "date": "2023-12-09",
  "effectiveDate": "2024-03-29",
  "typeCode": "SC",
  "typeDesc": "Signed as a Free Agent",
  "description": "Signed by the Los Angeles Dodgers as a Free Agent"
}
```

---

### Transaction Type Codes

| Code | Description |
|------|-------------|
| `SC` | Signed as a Free Agent |
| `TE` | Traded |
| `DES` | Designated for Assignment |
| `RE` | Released |
| `PUR` | Purchased from Minors |
| `WV` | Placed on Waivers |
| `RET` | Retired |
| `TR` | Transferred |
| `SU` | Called Up from minors |
| `OA` | Optioned to minors |
| `OUT` | Outrighted |
| `IL` | Placed on Injured List |
| `ACT` | Activated from Injured List |
| `NRI` | Non-Roster Invitee |
| `PCT` | Placed on Paternity List |
| `RPC` | Reinstated from Paternity |
| `BRV` | Placed on Bereavement List |
| `RBL` | Reinstated from Bereavement |
| `EXC` | Exhibition Contract |
| `MIN` | Signed Minor League Contract |
