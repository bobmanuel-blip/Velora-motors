# Velora Motors — "Drive Your Dream. Anywhere."

This is **Milestone 1** of the Velora Motors platform: a real, runnable Django
project with the marketplace foundation in place. It is not the entire
enterprise spec (that would take a funded team 12+ months) — it's the solid
base to build every other feature on top of, one working piece at a time.

## What's included right now

- Custom user model with roles: **Buyer**, **Dealer**, **Admin**
- Dealer profiles with a "Verified Dealer" badge
- Vehicle marketplace: create/edit/delete listings, image galleries, rich
  specs (engine, horsepower, torque, features, VIN, etc.)
- Search & filter (make, model, year, price, country, mileage, fuel type,
  transmission, drivetrain, body style, condition)
- A rule-based **AI natural-language search** ("black Mercedes G63 under
  $170,000") — see `vehicles/ai_search.py`. This is written so you can swap
  in a real LLM call later without touching any views or templates.
- Wishlist, recently viewed, similar vehicles, side-by-side compare
- Buyer ↔ Dealer **chat** (polling-based real-time updates every 3s), with
  a rule-based AI FAQ auto-responder (`chatapp/ai_assistant.py`) — same
  swap-in-a-real-LLM design as search
- Dealer dashboard (inventory, stats, profile)
- Buyer dashboard (wishlist)
- Django's built-in Admin, rebranded, as the seed of the Enterprise Admin
  Dashboard
- Contact page, FAQ, trust badges, floating support buttons, 24/7 support
  number displayed throughout
- Premium dark-mode glassmorphism UI (Tailwind CDN) matching the brand brief

## What's intentionally NOT built yet (next milestones)

Auctions, auto parts marketplace, payments/Stripe/PayPal, real-time
WebSocket chat (Channels), VIN decoding against a real database, fraud
detection, GraphQL API, Elasticsearch, mobile apps, Kubernetes/CI-CD,
multi-language i18n, and the full LLM-powered AI assistant. The codebase is
structured so each of these slots in cleanly — ask for any of them next and
we'll build it the same way: real, working code, one piece at a time.

## Running this in PyCharm

1. **Open the project**: File → Open → select the `velora_motors` folder.
2. **Create a virtual environment** (PyCharm will usually prompt you, or do
   it manually):
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
6. **Create an admin superuser** (for the Admin Dashboard at `/admin/`):
   ```bash
   python manage.py createsuperuser
   ```
7. **(Optional but recommended) Seed demo data** so the marketplace isn't
   empty on first run:
   ```bash
   python manage.py seed_demo
   ```
   This creates a demo dealer (`demo_dealer` / `VeloraDemo123!`) with 8
   sample luxury/EV/SUV listings.
8. **Run the server**:
   ```bash
   python manage.py runserver
   ```
9. Visit **http://127.0.0.1:8000/** for the site, and
   **http://127.0.0.1:8000/admin/** for the admin dashboard.

### In PyCharm specifically
- Set the Python interpreter to your `.venv` (PyCharm Settings → Project →
  Python Interpreter).
- Right-click `manage.py` → "Modify Run Configuration" and set it up as a
  Django server run config, or just use the terminal commands above — both
  work identically.
- If PyCharm shows import errors for `django` before you've installed
  requirements, that's expected — they resolve once the interpreter points
  at an environment with `requirements.txt` installed.

## Moving from SQLite to Postgres later

`velora_motors/settings.py` has a commented-out Postgres `DATABASES` block
ready to uncomment — just install `psycopg2-binary` (already listed,
commented, in `requirements.txt`), set your DB env vars, and run
`migrate` again.

## Suggested build order for the next milestones

1. Auto parts marketplace (mirrors the `vehicles` app structure)
2. Stripe/PayPal payments + order model
3. Real-time chat via Django Channels + WebSockets
4. Live auctions (bidding, countdown, reserve price)
5. Real AI integration (swap `ai_search.py` / `ai_assistant.py` internals
   for Anthropic API calls)
6. REST/GraphQL API layer for a future mobile app
7. Deployment: Docker, CI/CD, Postgres, Cloudflare/CDN

Tell me which of these to build next and I'll do it the same way this was
built — real, working code you can run immediately.
