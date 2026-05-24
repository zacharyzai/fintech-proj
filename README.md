# fintech-proj
summer project


# FinFlow 💸
> AI-Powered Personal Finance Platform · Singapore Fintech

Upload your bank statement → Claude AI parses every transaction → Get a personalised daily budget and financial health score.

---

## What It Does

FinFlow eliminates the biggest reason people abandon budgeting apps — manual expense entry. Upload your DBS, OCBC, or UOB bank statement and Claude AI automatically reads and categorises every transaction. The app analyses spending patterns, flags unusual transactions, and tracks month-over-month trends on an interactive dashboard.

**Daily Budget Formula:**
```
Income − Bills − Planned Expenses − Savings Goal ÷ Days Remaining = Daily Budget
```

Under the hood, every transaction is recorded using a **double-entry ledger** and moves through a payment state machine (`PENDING → CLEARED → FAILED`) — the same primitives used by Stripe and PayPal — with a nightly reconciliation job keeping the books balanced.

---

## Features

### 📄 Smart PDF / CSV Parsing
- Upload DBS, OCBC, and UOB statements
- Claude AI reads and categorises every transaction row
- Pandas cleans and normalises CSV exports
- Raw file deleted immediately after parsing

### 📊 Spending Dashboard
- Category breakdown (Food, Transport, Entertainment, etc.)
- Month-over-month trend charts
- Unusual transaction detection via 2σ rule
- Interactive Vue-ChartJS visualisations

### 🗓️ Prescriptive Budget Planner
- Calendar view for upcoming planned expenses
- Daily budget with green / yellow / red day indicators
- Google Calendar sync for planned costs

### 🏆 Financial Health Score
- Composite score (0–100), updated monthly
- Dimensions: savings rate, expense volatility, bill regularity, budget adherence
- AI-generated tips targeting your weakest dimension

### 🎯 Savings Goal Tracker
- Set goal name, target amount, and deadline
- Reverse-engineers required monthly saving amount
- Visual progress bar per goal

### 🏦 Fintech-Grade Backend
- Double-entry ledger for every transaction
- Payment state machine (`PENDING → CLEARED → FAILED`)
- Nightly reconciliation job at 2AM SGT
- Same accounting model used by Stripe and PayPal

---

## Tech Stack

### Frontend
| Technology | Version | Role |
|---|---|---|
| Vue.js 3 | `^3.4` | UI framework — reactive components and routing |
| Tailwind CSS | `^3.4` | Utility-first styling |
| Vue-ChartJS | `^5.3` | Spending charts and trend visualisations |
| Pinia | `^2.1` | Lightweight client state management |
| Supabase JS | `^2.x` | Auth session and direct DB queries from client |
| Axios | `^1.7` | HTTP client for FastAPI REST calls |
| VueUse | `^10` | Composables — scroll, storage, media queries |

### Backend
| Technology | Version | Role |
|---|---|---|
| FastAPI | `0.111` | REST API framework |
| Uvicorn | `standard` | ASGI server for FastAPI |
| Pandas | `2.2` | CSV parsing, categorisation, analytics |
| pdfplumber | `0.11` | PDF table extraction before Claude parsing |
| Anthropic SDK | `0.28` | Claude API client for AI parsing |
| Supabase Python | `2.4` | Server-side DB reads and writes |
| APScheduler | `3.10` | Nightly 2AM reconciliation cron job |
| slowapi | `0.1` | Rate limiting on upload endpoint |

### Database & Auth
| Component | Technology | Role |
|---|---|---|
| Primary DB | Supabase PostgreSQL | All app data — transactions, goals, scores |
| Row Level Security | Supabase RLS | Users can only query their own rows |
| Authentication | Supabase Auth | JWT sessions, Google OAuth, optional MFA |
| File Storage | Supabase Storage | Temporary statement uploads (private bucket) |
| Ledger | PostgreSQL | Double-entry ledger entries per transaction |
| Cron Log | PostgreSQL | Nightly reconciliation run history |

### AI & Integrations
| Service | Provider | Role |
|---|---|---|
| AI Parsing | Claude API (Anthropic) | PDF statement reading and categorisation |
| SGD FX Rates | MAS API | Official Monetary Authority of Singapore rates |
| Multi-currency | Exchange Rates API | Live forex conversion |
| Calendar Sync | Google Calendar API | Push planned expenses to user's calendar |
| Daily Alerts | Telegram Bot API | Daily budget reminder notifications |
| Monthly Report | Resend | Monthly email summary and health score |

### Hosting & DevOps
| Layer | Technology | Role |
|---|---|---|
| Frontend | Vercel | Auto-deploy from GitHub, CDN, HTTPS |
| Backend | Railway | FastAPI container, auto-deploy, env vars |
| CI/CD | GitHub Actions | Run tests and build checks on every push |
| Error Tracking | Sentry | Runtime error monitoring in production |
| Dev Proxy | Vite dev server | Proxies `/api` to FastAPI locally |

---

## Architecture Flow

```
Upload     →  User uploads PDF or CSV via Vue.js frontend (Vercel)
Parse      →  FastAPI validates file → Pandas cleans CSV or Claude API reads PDF → raw file deleted
Ledger     →  Each transaction creates two ledger entries (double-entry debit + credit) in Supabase
State      →  Transactions enter PENDING; 2AM cron job moves balanced ones to CLEARED
Analytics  →  Pandas computes monthly trends, anomaly flags, and health score dimensions
Dashboard  →  Vue.js fetches JSON from FastAPI and renders charts via Vue-ChartJS
Notify     →  Telegram Bot sends daily budget reminder; Resend delivers monthly email report
```

---

## Database Schema

| Table | Key Columns | Notes |
|---|---|---|
| `users` | id, email, created_at | Managed by Supabase Auth |
| `accounts` | id, user_id, name, currency | One user → many accounts |
| `transactions` | id, account_id, date, description, withdrawal, credit, category, state | Parsed from statements |
| `ledger_entries` | id, transaction_id, account, entry_type (DR/CR), amount | Double-entry rows |
| `planned_expenses` | id, user_id, name, amount, due_date, category | User-added future costs |
| `savings_goals` | id, user_id, name, target, saved, deadline | Goal tracking |
| `health_scores` | id, user_id, month, score, dimensions (JSONB) | Monthly computed score |
| `reconciliation_log` | id, run_date, total_processed, discrepancies | Nightly job output |

---

## Security Model

| Layer | Implementation |
|---|---|
| Authentication | Supabase Auth with JWT sessions. Google OAuth supported. MFA available. |
| Row Level Security | RLS enforced on every table — users can only query their own rows, enforced at DB level. |
| File Handling | Statements stored in private Supabase buckets. Deleted immediately post-parse. Signed URLs with short expiry. |
| API Keys | All keys (Claude, Supabase service role, Telegram) stored server-side in `.env` only. Never sent to client. |
| Logging Policy | No financial data (amounts, merchant names) in server logs. Only event types and user IDs. |
| Rate Limiting | Upload and parse endpoints rate-limited via slowapi to prevent abuse and control AI costs. |
| PDPA Compliance | Data minimisation applied — only store what the app needs. User can delete all data on request. |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- A [Supabase](https://supabase.com) project
- An [Anthropic API key](https://console.anthropic.com)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/your-username/finflow.git
cd finflow/backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Fill in your keys in .env

# Run the development server
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd finflow/frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Fill in your Supabase URL and anon key

# Run the development server
npm run dev
```

### Environment Variables

```env
# Backend (.env)
ANTHROPIC_API_KEY=your_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
TELEGRAM_BOT_TOKEN=your_bot_token
RESEND_API_KEY=your_resend_key
GOOGLE_CALENDAR_CLIENT_ID=your_client_id
GOOGLE_CALENDAR_CLIENT_SECRET=your_client_secret
```

---

## Roadmap

### Phase 1 — MVP ✅
- [x] Statement upload (PDF + CSV) + Claude AI parsing
- [x] Spending dashboard with Vue-ChartJS
- [x] Double-entry ledger + payment state machine
- [x] Daily budget calculator
- [x] Savings goal tracker
- [x] Supabase Auth + RLS security

### Phase 2 — Enrich ✅
- [x] Financial Health Score (0–100)
- [x] MAS API for live SGD FX rates
- [x] Google Calendar sync
- [x] Telegram daily budget alerts
- [x] Monthly email report via Resend

### Phase 3 — Impress ✅
- [x] Receipt photo scanning (Veryfi)
- [x] MyInfo / Singpass integration
- [x] Multi-account aggregation
- [x] PDF export of monthly report
- [x] AI personalised saving tips

---

## Disclaimer

Raw bank statements are never stored — they are deleted immediately after parsing. This is a portfolio project and is not affiliated with DBS, OCBC, UOB, or the Monetary Authority of Singapore.