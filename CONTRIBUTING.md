# Contributing to Public-MLB-API

Thank you for your interest in contributing! This project documents the unofficial MLB Stats API.

## Ways to Contribute

### 📖 Documentation
- Add or correct endpoint URLs
- Add missing query parameters or fields
- Improve or add curl examples
- Fix errors, typos, or outdated information
- Add response schema examples

### 🐛 Report a Bug
Open an issue. Please include:
- The endpoint URL you used
- What you expected
- What you actually received (status code, response snippet)

### 🔍 Report a Missing Endpoint
Open an issue if you've found an MLB Stats API endpoint not documented here.

---

## Verification Levels

All endpoints should be labeled with one of the following:

| Label | Meaning |
|-------|---------|
| **VERIFIED** | Tested live against `statsapi.mlb.com` and confirmed working |
| **PARTIALLY VERIFIED** | Response structure confirmed but some parameters untested |
| **UNVERIFIED** | Discovered via docs/source review but not yet live-tested |

---

## Pull Request Guidelines

1. **Branch off `main`**
2. **One concern per PR** — keep changes focused
3. **Write clear commit messages** — reference the endpoint or file you changed
4. **Update docs** if you add or change endpoints

### Commit message format

```
type: short description

- Bullet detail if needed
```

Types: `docs`, `fix`, `chore`

---

## Documentation Style Guide

### Endpoint tables

```markdown
| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/teams` | All teams |
```

### Parameter tables

```markdown
| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `sportId` | ❌ | Sport filter | `1` |
| `season` | ✅ | Season year | `2025` |
```

### Curl examples

- Use `https://` always
- Add a `# comment` above each example describing what it does
- Use real, working IDs in examples (e.g., `teamId=119`, not `{teamId}`)

### File locations

| What | Where |
|------|-------|
| Core endpoint docs | `docs/{resource}.md` |
| Site-wide docs | `README.md` |
| Change history | `CHANGELOG.md` |

---

## Code of Conduct

Be kind and respectful. This is a community resource — everyone is welcome.

---

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) as this project.
