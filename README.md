# Public API Access — AI Compatible

[![APIs](https://img.shields.io/badge/APIs-1%2C850-blue?style=flat-square&logo=json)](https://github.com/shivtcdfinance/public-api-access-ai-compatible)
[![Trusted](https://img.shields.io/badge/trusted-252-green?style=flat-square&logo=shield)](https://github.com/shivtcdfinance/public-api-access-ai-compatible#trust-rating-system)
[![Size](https://img.shields.io/badge/size-470KB-orange?style=flat-square)](https://github.com/shivtcdfinance/public-api-access-ai-compatible)
[![License](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](LICENSE)
[![Pages](https://img.shields.io/badge/demo-live-ff69b4?style=flat-square)](https://shivtcdfinance.github.io/public-api-access-ai-compatible/)

> **1,850 curated public APIs — trust-rated, AI-ready, and 470 KB small.**
> The first API directory built for both humans AND AI agents.

---

## 🚀 Quick Start

### For AI Agents (primary use case)

```bash
# Load directly into any LLM context
curl -s https://raw.githubusercontent.com/shivtcdfinance/public-api-access-ai-compatible/main/api_access.min.json
```

**Claude / Cursor / Copilot:**
```
Load this file: https://raw.githubusercontent.com/shivtcdfinance/public-api-access-ai-compatible/main/ai_prompt.txt
Then ask: "Find me a free HTTPS API for currency exchange rates"
```

**Python:**
```python
import json, urllib.request

url = "https://raw.githubusercontent.com/shivtcdfinance/public-api-access-ai-compatible/main/api_access.min.json"
apis = json.loads(urllib.request.urlopen(url).read())

# Safe APIs: trusted + no auth + HTTPS
safe = [a for a in apis if a['trust'] == 'trusted' and a['auth'] == 'no' and a['https']]
weather = [a for a in safe if 'weather' in a['name'].lower()]
print(weather[0]['url'])  # Ready to call
```

### For Humans — [Live Demo](https://shivtcdfinance.github.io/public-api-access-ai-compatible/)

---

## ✨ Why This Exists

Every other API directory (public-apis, RapidAPI, APIList) is built for human browsing — long markdown tables, vague descriptions, no filtering. **AI agents can't use those.**

API Canon is different:

| Feature | Other directories | API Canon |
|---|---|---|
| **Format** | Markdown tables | Structured JSON |
| **Trust signal** | None | Domain-level rating (trusted/likely/unknown/suspicious) |
| **Fits in LLM context** | 5+ MB (too big) | 472 KB (fits everywhere) |
| **Live demo** | None | Searchable web UI |
| **AI agent ready** | No | Prompt templates included |
| **Health-checked** | Dead links rot silently | CI pings 100 random APIs weekly |

---

## 🚀 Quick Start

### Web Browser — [Live Demo](https://shivtcdfinance.github.io/api-canon/)

Open the demo, type "weather" or "crypto", filter by trust rating. Instant.

### For Humans

```bash
# Search for APIs by keyword
curl -s https://raw.githubusercontent.com/shivtcdfinance/public-api-access-ai-compatible/main/api_access.min.json \
  | jq '.[] | select(.name | test("weather"; "i")) | {name, trust, auth}'
```

### For AI Agents

**Claude / Cursor / Copilot:**
```
Load this file into your context: https://raw.githubusercontent.com/shivtcdfinance/api-canon/main/ai_prompt.txt
Then ask: "Find me a free HTTPS API for currency exchange rates"
```

**ChatGPT Custom GPT:**
```
Upload api_canon.min.json to your Knowledge.
Then prompt: "Using the API Canon, find the best API for [task]"
```

**Python:**
```python
import json, urllib.request

url = "https://raw.githubusercontent.com/shivtcdfinance/api-canon/main/api_canon.min.json"
apis = json.loads(urllib.request.urlopen(url).read())

# Safe APIs: trusted + no auth + HTTPS
safe = [a for a in apis if a['trust'] == 'trusted' and a['auth'] == 'no' and a['https']]
weather = [a for a in safe if 'weather' in a['name'].lower()]
print(weather[0]['url'])  # Ready to call
```

---

## 📊 Data Structure

Every API entry:

```json
{
  "name": "OpenWeatherMap",
  "desc": "Current weather forecasts, and historical data",
  "cat": "weather",
  "domain": "openweathermap.org",
  "url": "https://openweathermap.org/api",
  "auth": "apikey",
  "https": true,
  "cors": "unknown",
  "trust": "trusted",
  "source": "marcelscruz"
}
```

| Field | Values | Description |
|---|---|---|
| `name` | string | API name |
| `desc` | string | Short description |
| `cat` | string | Category (finance, weather, geocoding, etc.) |
| `domain` | string | Provider domain |
| `url` | string | API documentation URL |
| `auth` | `no` / `apikey` / `oauth` | Authentication required |
| `https` | `true` / `false` | HTTPS support |
| `cors` | `yes` / `no` / `unknown` | Cross-origin support |
| `trust` | `trusted` / `likely_safe` / `marketplace` / `unknown` / `suspicious` | Trust rating |
| `source` | `marcelscruz` / `public-api-lists` | Data provenance |

---

## 🔒 Trust Rating System

Every API domain is classified automatically:

| Rating | Count | Criteria |
|---|---|---|
| **trusted** | 252 | Google, Microsoft, Stripe, .gov/.edu, known providers |
| **likely_safe** | 61 | Hosted on Vercel/Render/GitHub Pages — reputable platforms |
| **marketplace** | 75 | RapidAPI, APYHub — vet individual APIs |
| **unknown** | 1,453 | Valid SSL, active DNS — probably fine, check before uploading data |
| **suspicious** | 10 | .xyz, .cf, .gq TLDs — excluded from trust tiers |

### Methodology

1. **Domain whitelist** — ~200 known trusted organizations (Google, Microsoft, Stripe, GitHub, etc.)
2. **TLD blocklist** — Free/cheap TLDs commonly used for disposable services
3. **Gov/edu detection** — `.gov`, `.edu`, `.mil` domains auto-trusted
4. **Platform detection** — `vercel.app`, `netlify.app`, `github.io` = likely_safe
5. **SSL validation** — Spot-checked: 98% of unknown domains have valid SSL
6. **Health check** — Weekly CI pings 100 random APIs, flags dead domains

---

## 📂 Files

| File | Size | Use |
|---|---|---|
| `api_access.min.json` | 470 KB | **Primary** — load this into your app/AI agent |
| `api_access.full.json` | 770 KB | Full version with category/auth indexes |
| `docs/index.html` | — | GitHub Pages searchable demo |
| `examples/` | — | Python, curl, Node.js, AI prompt examples |
| `scripts/` | — | Rebuild from upstream sources |
| `tests/` | — | Schema + trust + health validation |

## 🔄 Auto-Sync Pipeline

This repo is kept in sync from a central curated database:

```
Central DB (local, private)
  └─ health_check.py   → Weekly: pings APIs, prunes dead ones
  └─ sync_to_github.py → Sanitizes & pushes clean data here
      ✓ Strips personal API keys / private entries
      ✓ Only marcelscruz + public-api-lists sources
      ✓ Zero personal data ever touches this repo
```

---

## ⚡ Integration

### Data Sources

Built from two community-maintained API directories:
- **[marcelscruz/public-apis](https://github.com/marcelscruz/public-apis)** — 1,605 APIs in structured JSON
- **[public-api-lists/public-api-lists](https://github.com/public-api-lists/public-api-lists)** — 730+ community-vetted APIs

Both MIT-licensed. Clean, no malware, no telemetry. [Full audit →](AUDIT.md)

### Rebuilding

```bash
cd scripts
python3 build_db.py  # Pulls latest from upstream, rebuilds api_canon.json
```

---

## 📋 Contributing

Found a dead API? Wrong trust rating? Missing category?

1. Open an issue with the API name and what's wrong
2. Or: edit `api_canon.min.json` directly and open a PR
3. PRs are auto-validated by CI for JSON schema + trust consistency

---

## ⭐ Credits

- **Shivansh Rao** ([@shivtcdfinance](https://github.com/shivtcdfinance)) — curation, trust system, build pipeline
- **[marcelscruz/public-apis](https://github.com/marcelscruz/public-apis)** — upstream data source
- **[public-api-lists/public-api-lists](https://github.com/public-api-lists/public-api-lists)** — upstream data source
- **Jarvis** (Hermes Agent) — built, audited, and deployed end-to-end

---

**License:** MIT — use freely in any project, commercial or personal.
