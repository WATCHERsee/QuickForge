# QuickForge

**Production-ready web app scaffolding engine.**  
Generate a fully configured, deployment-ready project in seconds — from the terminal or the browser dashboard.

**Live demo:** https://quickforge-dd2yisbs0-rajaadnanahmed1-2548s-projects.vercel.app  
**GitHub:** https://github.com/WATCHERsee/QuickForge

---

## What it does

QuickForge is a Python CLI that writes a complete, working web application to disk — not just a skeleton. Every scaffold output includes TypeScript types, a linting config, authentication wiring, database schema, CI/CD pipeline, and a Dockerfile, all pre-configured and ready to run on the first try.

The project also ships a static web dashboard (`dashboard.html`) that demonstrates the scaffold engine interactively in the browser.

---

## Supported stacks

| Stack | Flag | Includes |
|---|---|---|
| Next.js 15 | `--stack nextjs` | App Router, React 19, TypeScript, next.config.ts |
| Node.js + Express | `--stack node-express` | Express 4, typed routes, middleware chain |
| Flask | `--stack flask` | Python 3.12, Blueprints, REST API structure |

## Optional features

| Feature | Flag | What gets added |
|---|---|---|
| Tailwind CSS | `-f tailwind` | globals.css, PostCSS config, utility class setup |
| Authentication | `-f auth` | Session middleware, login/register routes, JWT |
| REST API | `-f api` | CRUD route handlers, request validation, error handling |

---

## Requirements

- Python 3.10 or higher
- pip (or the included `run.sh` which handles everything automatically)

---

## Installation

**No manual install needed.** Run the launcher script — it creates a virtual environment and installs dependencies on the first run:

```bash
git clone https://github.com/WATCHERsee/QuickForge.git
cd QuickForge
chmod +x run.sh
./run.sh --help
```

Or install dependencies manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python cli.py --help
```

---

## Usage

### Scaffold a project

```bash
# Next.js app with Tailwind and Auth
./run.sh create my-app --stack nextjs -f tailwind -f auth

# Node.js Express REST API
./run.sh create my-api --stack node-express -f api

# Flask backend with auth and API routes
./run.sh create my-backend --stack flask -f auth -f api

# Minimal — no features, just the base stack
./run.sh create my-site --stack nextjs
```

### See available stacks

```bash
./run.sh stacks
```

### Full help

```bash
./run.sh --help
./run.sh create --help
```

---

## CLI flags

| Flag | Short | Default | Description |
|---|---|---|---|
| `--stack` | `-s` | `nextjs` | Framework stack. One of `nextjs`, `node-express`, `flask`. |
| `--features` | `-f` | none | Features to include. Repeatable: `-f tailwind -f auth`. |
| `--out` | `-o` | current dir | Parent directory to write the project into. |
| `--version` | | | Print CLI version and exit. |

---

## What gets generated

Running `./run.sh create my-app --stack nextjs -f tailwind -f auth` produces:

```
my-app/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   └── dashboard/
│   │   ├── api/
│   │   │   └── auth/[...nextauth]/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/
│   │   ├── auth.ts
│   │   ├── db.ts
│   │   └── env.ts
│   └── middleware.ts
├── prisma/
│   └── schema.prisma
├── .env.example
├── Dockerfile
├── next.config.ts
├── tsconfig.json
├── .eslintrc.json
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

Every file is fully written — not a template with placeholder comments.

---

## Web dashboard

The project includes a static web dashboard (`dashboard.html`) with four additional pages:

| Page | File | Description |
|---|---|---|
| Home | `dashboard.html` | Interactive scaffold configurator |
| Features | `features.html` | Platform capabilities and benchmarks |
| Documentation | `documentation.html` | Full docs with 18 sections and SPA navigation |
| Community | `community.html` | Channels, discussions, contributors |
| Changelog | `changelog.html` | Full version history |

**Run locally:**

```bash
python3 -m http.server 7821 --directory .
# open http://localhost:7821/dashboard.html
```

---

## How it works

1. `run.sh` creates a `.venv` on first run and installs `typer` and `rich` from `requirements.txt`.
2. `cli.py` parses commands and flags using [Typer](https://typer.tiangolo.com/).
3. The `create` command builds a dictionary of file paths → file contents in memory, then writes them all to disk with a progress display.
4. The terminal output is styled with [Rich](https://rich.readthedocs.io/) using the Ethereal Forge colour palette (`#c0c1ff` primary, `#ddb7ff` secondary, `#4cd7f6` tertiary).

---

## Development

```bash
# Clone and enter
git clone https://github.com/WATCHERsee/QuickForge.git
cd QuickForge

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run CLI
python cli.py --help

# Serve dashboard locally
python3 -m http.server 7821
```

---

## Project structure

```
QuickForge/
├── cli.py              # Main CLI — all commands and file generators
├── run.sh              # Launcher — sets up venv on first run
├── requirements.txt    # Python dependencies (typer, rich)
├── dashboard.html      # Web dashboard — home page
├── features.html       # Features page
├── documentation.html  # Documentation — 18 sections, SPA navigation
├── community.html      # Community page
├── changelog.html      # Changelog page
├── vercel.json         # Vercel static deployment config
├── DESIGN.md           # Ethereal Forge design system reference
└── screen.png          # Dashboard preview screenshot
```

---

## Deployment

The dashboard is a static HTML site deployed on Vercel.

```bash
# Preview deploy
vercel

# Production deploy
vercel --prod
```

The `vercel.json` routes `/` to `dashboard.html` and sets `framework: null` for static file serving.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| [typer](https://typer.tiangolo.com/) | >=0.12.0 | CLI argument parsing and command routing |
| [rich](https://rich.readthedocs.io/) | >=13.7.0 | Terminal output — colours, tables, progress bars, panels |

---

## License

MIT
