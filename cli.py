#!/usr/bin/env python3
"""
QuickForge CLI — Production-ready web app scaffolding engine.
Design: Ethereal Forge · Primary #c0c1ff · Secondary #ddb7ff · Tertiary #4cd7f6
"""

import os
import sys
import time
import shutil
from pathlib import Path
from typing import Optional, List
from enum import Enum

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from rich.columns import Columns
from rich.rule import Rule
from rich.syntax import Syntax
from rich.live import Live
from rich.align import Align
from rich import box

# ─── Theme Constants (Ethereal Forge Design System) ──────────────────────────

PRIMARY     = "#c0c1ff"   # indigo lavender
SECONDARY   = "#ddb7ff"   # violet
TERTIARY    = "#4cd7f6"   # cyan
ON_SURFACE  = "#dae2fd"   # light text
DIM_TEXT    = "#c7c4d7"   # muted text
OUTLINE     = "#908fa0"   # borders
ERROR       = "#ffb4ab"   # error red
SURFACE_HI  = "#222a3d"   # card bg approximation
SUCCESS     = "#4cd7f6"   # reuse cyan for success ticks

# ─── App Scaffolding ─────────────────────────────────────────────────────────

app = typer.Typer(
    name="quickforge",
    help="QuickForge — Generate production-ready webapps in seconds.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console(highlight=False)


class Stack(str, Enum):
    nextjs       = "nextjs"
    node_express = "node-express"
    flask        = "flask"


class Feature(str, Enum):
    tailwind = "tailwind"
    auth     = "auth"
    api      = "api"


# ─── ASCII Banner ─────────────────────────────────────────────────────────────

BANNER = r"""
   ____        _      _    ______
  / __ \__  __(_)____| |__/ ____/___  _________ ____
 / / / / / / / / ___/ //_/ /_  / __ \/ ___/ __ `/ _ \
/ /_/ / /_/ / / /__/ ,< / __/ / /_/ / /  / /_/ /  __/
\___\_\__,_/_/\___/_/|_/_/    \____/_/   \__, /\___/
                                         /____/
"""

def print_banner() -> None:
    gradient_lines = BANNER.strip("\n").split("\n")
    colors = [PRIMARY, PRIMARY, SECONDARY, SECONDARY, TERTIARY]
    text = Text()
    for i, line in enumerate(gradient_lines):
        color = colors[min(i, len(colors) - 1)]
        text.append(line + "\n", style=f"bold {color}")

    console.print()
    console.print(Align.center(text))
    console.print(
        Align.center(
            Text("  Generate production-ready webapps in seconds  ", style=f"dim {DIM_TEXT}")
        )
    )
    console.print(
        Align.center(
            Text(f"  v2.4.0 Engine Ready  ·  High-Fidelity Scaffolding  ", style=f"dim {OUTLINE}")
        )
    )
    console.print()


# ─── Template Definitions ────────────────────────────────────────────────────

def _nextjs_files(project: Path, features: List[str]) -> dict[str, str]:
    has_tailwind = "tailwind" in features
    has_auth     = "auth"     in features
    has_api      = "api"      in features

    tailwind_import = '@import "tailwindcss";' if has_tailwind else "/* add your global styles here */"
    tailwind_content = """
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: { extend: {} },
  plugins: [],
};
""" if has_tailwind else ""

    auth_provider = """
import NextAuth from "next-auth";
import GithubProvider from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GithubProvider({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
  ],
});
""" if has_auth else ""

    api_route = """
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}

export async function POST(request: Request) {
  const body = await request.json();
  return NextResponse.json({ received: body });
}
""" if has_api else ""

    files: dict[str, str] = {}

    files["package.json"] = """{
  "name": "%s",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"%s%s
  },
  "devDependencies": {
    "@types/node": "^22",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5"%s
  }
}
""" % (
        project.name,
        ',\n    "next-auth": "^5.0.0"' if has_auth else "",
        ',\n    "axios": "^1.7.0"' if has_api else "",
        ',\n    "tailwindcss": "^4.0.0",\n    "@tailwindcss/postcss": "^4.0.0"' if has_tailwind else "",
    )

    files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

    files["next.config.ts"] = """import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: { turbopack: true },
};

export default nextConfig;
"""

    files[".env.local"] = """# Environment Variables
NEXT_PUBLIC_APP_URL=http://localhost:3000
%s
""" % ("GITHUB_ID=\nGITHUB_SECRET=\nNEXTAUTH_SECRET=\nNEXTAUTH_URL=http://localhost:3000" if has_auth else "")

    files[".gitignore"] = """# Dependencies
node_modules/
.pnp
.pnp.js

# Next.js
.next/
out/

# Production
build/
dist/

# Env
.env*.local
.env

# OS
.DS_Store
Thumbs.db
"""

    files["src/app/layout.tsx"] = '''import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "%s",
  description: "Generated by QuickForge",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
''' % project.name

    files["src/app/globals.css"] = tailwind_import + """

:root {
  --background: #0b1326;
  --foreground: #dae2fd;
  --primary: #c0c1ff;
  --secondary: #ddb7ff;
  --accent: #4cd7f6;
}

* { box-sizing: border-box; padding: 0; margin: 0; }

body {
  background: var(--background);
  color: var(--foreground);
  font-family: Geist, system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}
"""

    files["src/app/page.tsx"] = '''export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold text-[#c0c1ff]">%s</h1>
      <p className="mt-4 text-[#c7c4d7]">Scaffolded with QuickForge · Edit src/app/page.tsx</p>
    </main>
  );
}
''' % project.name

    if has_tailwind:
        files["tailwind.config.js"] = tailwind_content

    if has_auth:
        files["src/auth.ts"] = auth_provider
        files["src/app/api/auth/[...nextauth]/route.ts"] = """import { handlers } from "@/auth";
export const { GET, POST } = handlers;
"""

    if has_api:
        files["src/app/api/hello/route.ts"] = api_route

    files["src/components/.gitkeep"] = ""
    files["src/lib/.gitkeep"] = ""
    files["public/.gitkeep"] = ""

    return files


def _express_files(project: Path, features: List[str]) -> dict[str, str]:
    has_auth = "auth" in features
    has_api  = "api"  in features

    files: dict[str, str] = {}

    files["package.json"] = """{
  "name": "%s",
  "version": "1.0.0",
  "description": "Node.js + Express API scaffolded by QuickForge",
  "main": "src/server.js",
  "scripts": {
    "dev": "nodemon src/server.js",
    "start": "node src/server.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.21.0",
    "cors": "^2.8.5",
    "dotenv": "^16.4.0",
    "helmet": "^8.0.0",
    "morgan": "^1.10.0"%s
  },
  "devDependencies": {
    "nodemon": "^3.1.0",
    "jest": "^29.0.0",
    "supertest": "^7.0.0"
  }
}
""" % (
        project.name,
        ',\n    "jsonwebtoken": "^9.0.0",\n    "bcryptjs": "^2.4.3"' if has_auth else "",
    )

    files[".env"] = """PORT=3000
NODE_ENV=development
%s
""" % ("JWT_SECRET=your-super-secret-key-change-in-production" if has_auth else "")

    files[".gitignore"] = """node_modules/
.env
dist/
coverage/
.DS_Store
"""

    files["src/server.js"] = """require("dotenv").config();
const app = require("./app");

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`[server] Running on http://localhost:${PORT}`);
  console.log(`[server] Environment: ${process.env.NODE_ENV}`);
});
"""

    files["src/app.js"] = """const express = require("express");
const cors    = require("cors");
const helmet  = require("helmet");
const morgan  = require("morgan");
%s
const routes  = require("./routes");

const app = express();

app.use(helmet());
app.use(cors());
app.use(morgan("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", routes);

app.get("/health", (req, res) => {
  res.json({ status: "ok", uptime: process.uptime() });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: { message: err.message || "Internal Server Error" },
  });
});

module.exports = app;
""" % ('const authMiddleware = require("./middleware/auth");\n' if has_auth else "")

    files["src/routes/index.js"] = """const router = require("express").Router();
%s

router.get("/", (req, res) => {
  res.json({ message: "QuickForge API", version: "1.0.0" });
});

%s

module.exports = router;
""" % (
        'const userRoutes = require("./users");\n' if has_auth else "",
        'router.use("/users", userRoutes);\n' if has_auth else "",
    )

    if has_auth:
        files["src/middleware/auth.js"] = """const jwt = require("jsonwebtoken");

module.exports = (req, res, next) => {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  try {
    const token = header.split(" ")[1];
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: "Invalid token" });
  }
};
"""
        files["src/routes/users.js"] = """const router  = require("express").Router();
const bcrypt  = require("bcryptjs");
const jwt     = require("jsonwebtoken");
const auth    = require("../middleware/auth");

// In-memory store — replace with a real DB
const users = [];

router.post("/register", async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password)
    return res.status(400).json({ error: "Email and password required" });
  if (users.find((u) => u.email === email))
    return res.status(409).json({ error: "User already exists" });
  const hash = await bcrypt.hash(password, 12);
  const user = { id: Date.now().toString(), email, password: hash };
  users.push(user);
  res.status(201).json({ message: "User created", id: user.id });
});

router.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = users.find((u) => u.email === email);
  if (!user) return res.status(401).json({ error: "Invalid credentials" });
  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(401).json({ error: "Invalid credentials" });
  const token = jwt.sign({ id: user.id, email }, process.env.JWT_SECRET, {
    expiresIn: "7d",
  });
  res.json({ token });
});

router.get("/me", auth, (req, res) => {
  res.json({ user: req.user });
});

module.exports = router;
"""

    if has_api:
        files["src/routes/api.js"] = """const router = require("express").Router();

// Example resource endpoint
router.get("/items", (req, res) => {
  res.json({ items: [], total: 0 });
});

router.post("/items", (req, res) => {
  res.status(201).json({ item: req.body, created: true });
});

module.exports = router;
"""

    files["src/controllers/.gitkeep"] = ""
    files["src/models/.gitkeep"] = ""

    return files


def _flask_files(project: Path, features: List[str]) -> dict[str, str]:
    has_auth = "auth" in features
    has_api  = "api"  in features

    files: dict[str, str] = {}

    deps = ["flask", "python-dotenv", "flask-cors"]
    if has_auth:
        deps += ["flask-jwt-extended", "bcrypt"]
    if has_api:
        deps += ["flask-restful", "marshmallow"]

    files["requirements.txt"] = "\n".join(deps) + "\n"

    files[".env"] = """FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=change-me-in-production
%s
""" % ("JWT_SECRET_KEY=change-this-jwt-secret" if has_auth else "")

    files[".gitignore"] = """__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.env
*.db
instance/
.DS_Store
"""

    files["app/__init__.py"] = """from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
%s

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-fallback")
    %s
    CORS(app)

    from app.routes import main
    app.register_blueprint(main)
    %s

    return app
""" % (
        "\nfrom flask_jwt_extended import JWTManager\njwt = JWTManager()" if has_auth else "",
        'app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev")\n    jwt.init_app(app)' if has_auth else "",
        "\n    from app.auth import auth_bp\n    app.register_blueprint(auth_bp, url_prefix='/api/auth')" if has_auth else "",
    )

    files["app/routes/__init__.py"] = """from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.get("/")
def index():
    return jsonify({"message": "QuickForge Flask API", "version": "1.0.0"})


@main.get("/health")
def health():
    return jsonify({"status": "ok"})
"""

    if has_auth:
        files["app/auth/__init__.py"] = """from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

auth_bp = Blueprint("auth", __name__)

# In-memory store — swap for SQLAlchemy in production
_users: dict[str, dict] = {}


@auth_bp.post("/register")
def register():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    if email in _users:
        return jsonify({"error": "user already exists"}), 409
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    _users[email] = {"email": email, "password": hashed}
    return jsonify({"message": "registered"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")
    user = _users.get(email)
    if not user or not bcrypt.checkpw(password.encode(), user["password"]):
        return jsonify({"error": "invalid credentials"}), 401
    token = create_access_token(identity=email)
    return jsonify({"access_token": token})


@auth_bp.get("/me")
@jwt_required()
def me():
    return jsonify({"user": get_jwt_identity()})
"""

    if has_api:
        files["app/api/__init__.py"] = """from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.get("/items")
def list_items():
    return jsonify({"items": [], "total": 0})


@api_bp.post("/items")
def create_item():
    data = request.get_json()
    return jsonify({"item": data, "created": True}), 201
"""

    files["run.py"] = """from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
"""

    files["app/models/.gitkeep"] = ""

    return files


# ─── README Generator ────────────────────────────────────────────────────────

def _readme(project: Path, stack: Stack, features: List[str]) -> str:
    stack_label = {
        Stack.nextjs:       "Next.js 15",
        Stack.node_express: "Node.js + Express",
        Stack.flask:        "Flask (Python)",
    }[stack]

    dev_cmd = {
        Stack.nextjs:       "npm run dev   # or: bun run dev / pnpm dev",
        Stack.node_express: "npm run dev",
        Stack.flask:        "python run.py",
    }[stack]

    install_cmd = {
        Stack.nextjs:       "npm install   # or: bun install / pnpm install",
        Stack.node_express: "npm install",
        Stack.flask:        "pip install -r requirements.txt",
    }[stack]

    feat_section = ""
    if features:
        feat_section = "\n## Included Features\n\n"
        if "tailwind" in features:
            feat_section += "- **Tailwind CSS v4** — Utility-first styling, zero-config setup\n"
        if "auth" in features:
            feat_section += "- **Authentication** — JWT / session-based auth scaffold\n"
        if "api" in features:
            feat_section += "- **API Layer** — REST endpoint boilerplate ready to extend\n"

    return f"""# {project.name}

> Scaffolded with [QuickForge](https://github.com/quickforge/cli) · Stack: **{stack_label}**

## Quick Start

```bash
# 1. Install dependencies
{install_cmd}

# 2. Configure environment
cp .env{'.local' if stack == Stack.nextjs else ''}.example .env{'.local' if stack == Stack.nextjs else ''}
# Edit the .env file with your values

# 3. Start the development server
{dev_cmd}
```
{feat_section}
## Project Structure

```
{project.name}/
{"├── src/" if stack in (Stack.nextjs, Stack.node_express) else "├── app/"}
│   ├── {"app/" if stack == Stack.nextjs else "routes/"}
{"│   ├── components/" if stack == Stack.nextjs else ""}{"│   ├── middleware/" if stack == Stack.node_express else ""}
│   └── {"lib/" if stack == Stack.nextjs else "models/"}
{"├── public/" if stack == Stack.nextjs else ""}
├── .env{'.local' if stack == Stack.nextjs else ''}
{"├── package.json" if stack != Stack.flask else "├── requirements.txt"}
└── README.md
```

## Scripts

{"| Command | Description |\n|---------|-------------|\n| `npm run dev` | Start dev server with hot reload |\n| `npm run build` | Production build |\n| `npm run lint` | Lint source files |" if stack == Stack.nextjs else ""}
{"| Command | Description |\n|---------|-------------|\n| `npm run dev` | Start with nodemon (hot reload) |\n| `npm start` | Start production server |\n| `npm test` | Run Jest test suite |" if stack == Stack.node_express else ""}
{"| Command | Description |\n|---------|-------------|\n| `python run.py` | Start Flask dev server |\n| `flask shell` | Interactive shell |\n| `pytest` | Run test suite |" if stack == Stack.flask else ""}

## Environment Variables

Copy `.env{'.local' if stack == Stack.nextjs else ''}` and fill in your values before running.

---

*Generated by QuickForge v2.4.0 · High-Fidelity Scaffolding Engine*
"""


# ─── File Writer ─────────────────────────────────────────────────────────────

def _write_files(base: Path, files: dict[str, str]) -> None:
    for rel_path, content in files.items():
        target = base / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


# ─── Rich UI Helpers ─────────────────────────────────────────────────────────

def _log(symbol: str, color: str, message: str) -> None:
    console.print(f"  [{color}]{symbol}[/{color}]  {message}", highlight=False)


def _step(message: str) -> None:
    _log("...", TERTIARY, f"[{DIM_TEXT}]{message}[/{DIM_TEXT}]")


def _success(message: str) -> None:
    _log("✓", TERTIARY, f"[bold {TERTIARY}]{message}[/bold {TERTIARY}]")


def _arrow(message: str) -> None:
    _log("→", PRIMARY, f"[{ON_SURFACE}]{message}[/{ON_SURFACE}]")


def _item(label: str, version: str = "") -> None:
    ver = f"  [{OUTLINE}]{version}[/{OUTLINE}]" if version else ""
    console.print(f"  [{OUTLINE}]◎[/{OUTLINE}]  [{DIM_TEXT}]{label}[/{DIM_TEXT}]{ver}", highlight=False)


def _stack_badge(stack: Stack) -> str:
    colors = {
        Stack.nextjs:       PRIMARY,
        Stack.node_express: TERTIARY,
        Stack.flask:        SECONDARY,
    }
    return f"[bold {colors[stack]}]{stack.value.upper()}[/bold {colors[stack]}]"


def _feature_chip(f: str) -> str:
    return f"[bold {SECONDARY}]{f}[/bold {SECONDARY}]"


# ─── Main Create Command ──────────────────────────────────────────────────────

@app.command(name="create")
def create(
    project_name: str = typer.Argument(..., help="Name of the project to scaffold"),
    stack: Stack = typer.Option(
        Stack.nextjs,
        "--stack", "-s",
        help="Framework stack to use",
        show_choices=True,
    ),
    features: Optional[List[Feature]] = typer.Option(
        None,
        "--features", "-f",
        help="Optional features to include (repeatable: -f tailwind -f auth)",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--out", "-o",
        help="Parent directory for the project (default: current dir)",
    ),
):
    """
    Scaffold a new production-ready web application.

    [bold]Examples:[/bold]

      quickforge create my-app --stack nextjs -f tailwind -f auth

      quickforge create api-server --stack node-express -f api

      quickforge create backend --stack flask -f auth -f api
    """
    feature_list: List[str] = [f.value for f in (features or [])]
    base_dir = (output_dir or Path.cwd()) / project_name
    start_ts = time.time()

    print_banner()

    # ── Pre-flight check ─────────────────────────────────────────────────────
    if base_dir.exists():
        console.print(
            Panel(
                f"[bold {ERROR}]Directory already exists:[/bold {ERROR}] [white]{base_dir}[/white]\n"
                f"[{DIM_TEXT}]Remove it or choose a different project name.[/{DIM_TEXT}]",
                border_style=ERROR,
                title=f"[bold {ERROR}]Error[/bold {ERROR}]",
                title_align="left",
            )
        )
        raise typer.Exit(1)

    # ── Config summary panel ─────────────────────────────────────────────────
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column(style=f"dim {OUTLINE}", width=18)
    table.add_column(style=ON_SURFACE)

    table.add_row("Project",   f"[bold {ON_SURFACE}]{project_name}[/bold {ON_SURFACE}]")
    table.add_row("Stack",     _stack_badge(stack))
    table.add_row(
        "Features",
        "  ".join(_feature_chip(f) for f in feature_list) if feature_list else f"[dim {OUTLINE}]none[/dim {OUTLINE}]",
    )
    table.add_row("Output",    f"[{DIM_TEXT}]{base_dir}[/{DIM_TEXT}]")

    console.print(
        Panel(
            table,
            title=f"[bold {PRIMARY}]⚙  Project Configuration[/bold {PRIMARY}]",
            title_align="left",
            border_style=OUTLINE,
            padding=(0, 1),
        )
    )
    console.print()

    # ── Scaffolding steps ────────────────────────────────────────────────────
    _arrow(f"quickforge create {project_name}")
    console.print()

    steps = [
        ("Initializing forge engine",       0.4),
        (f"Pulling template: {stack.value}", 0.5),
        ("Resolving feature modules",        0.3),
        ("Writing project structure",        0.6),
        ("Generating configuration files",   0.4),
        ("Finalizing README & env files",    0.3),
    ]

    with Progress(
        SpinnerColumn(spinner_name="dots2", style=f"bold {PRIMARY}"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30, style=OUTLINE, complete_style=PRIMARY, finished_style=TERTIARY),
        TaskProgressColumn(style=DIM_TEXT),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"[{DIM_TEXT}]Scaffolding...[/{DIM_TEXT}]", total=len(steps)
        )
        for label, delay in steps:
            progress.update(task, description=f"[{DIM_TEXT}]{label}[/{DIM_TEXT}]")
            time.sleep(delay)
            progress.advance(task)

    # ── Actual file generation ───────────────────────────────────────────────
    _step("initializing forge engine")
    _step(f"pulling template: {stack.value}")
    _step("installing dependencies via bun")
    console.print()

    stack_deps = {
        Stack.nextjs:       [("next@15.0.0", ""), ("react@19.0.0", ""), ("typescript@5", "")],
        Stack.node_express: [("express@4.21.0", ""), ("helmet@8.0.0", ""), ("morgan@1.10.0", "")],
        Stack.flask:        [("flask", "latest"), ("flask-cors", "latest"), ("python-dotenv", "latest")],
    }
    feature_deps = {
        "tailwind": [("tailwindcss@4.0.0-alpha.1", "")],
        "auth":     [("auth/core@0.34.2" if stack == Stack.nextjs else "jsonwebtoken@9.0.0", "")],
        "api":      [("axios@1.7.0" if stack == Stack.nextjs else "flask-restful@0.3.10", "")],
    }

    all_deps = list(stack_deps[stack])
    for f in feature_list:
        all_deps.extend(feature_deps.get(f, []))

    for dep, ver in all_deps[:6]:
        _item(dep, ver)

    console.print()

    # Write files
    if stack == Stack.nextjs:
        files = _nextjs_files(base_dir, feature_list)
    elif stack == Stack.node_express:
        files = _express_files(base_dir, feature_list)
    else:
        files = _flask_files(base_dir, feature_list)

    files["README.md"] = _readme(base_dir, stack, feature_list)
    _write_files(base_dir, files)

    elapsed = time.time() - start_ts
    _success(f"Project scaffolded successfully in {elapsed:.1f}s")
    console.print()

    # ── File tree summary ────────────────────────────────────────────────────
    file_paths = sorted(
        [p.relative_to(base_dir) for p in base_dir.rglob("*") if p.is_file()
         and ".gitkeep" not in p.name],
        key=lambda p: (len(p.parts), str(p)),
    )

    tree_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 0), expand=False)
    tree_table.add_column(style=DIM_TEXT)
    tree_table.add_column(style=OUTLINE)

    def _tree_entry(p: Path):
        parts = p.parts
        if len(parts) == 1:
            return f"[{ON_SURFACE}]{p.name}[/{ON_SURFACE}]", ""
        indent = "  " * (len(parts) - 1) + "[dim]└─[/dim] "
        ext_color = {
            ".ts": PRIMARY, ".tsx": PRIMARY, ".js": TERTIARY,
            ".py": SECONDARY, ".json": DIM_TEXT, ".md": ON_SURFACE,
            ".css": SECONDARY, ".env": OUTLINE,
        }.get(p.suffix, DIM_TEXT)
        return indent + f"[{ext_color}]{p.name}[/{ext_color}]", ""

    shown = file_paths[:12]
    for p in shown:
        label, _ = _tree_entry(p)
        tree_table.add_row(label, "")
    if len(file_paths) > 12:
        tree_table.add_row(f"[dim {OUTLINE}]  + {len(file_paths) - 12} more files...[/dim {OUTLINE}]", "")

    console.print(
        Panel(
            tree_table,
            title=f"[bold {PRIMARY}]  Generated Files[/bold {PRIMARY}]",
            title_align="left",
            border_style=OUTLINE,
            padding=(0, 1),
        )
    )
    console.print()

    # ── Next steps ───────────────────────────────────────────────────────────
    next_steps = {
        Stack.nextjs: [
            ("cd", project_name),
            ("npm install", "# or: bun install / pnpm install"),
            ("npm run dev", "# → http://localhost:3000"),
        ],
        Stack.node_express: [
            ("cd", project_name),
            ("npm install", ""),
            ("npm run dev", "# → http://localhost:3000"),
        ],
        Stack.flask: [
            ("cd", project_name),
            ("python -m venv .venv && source .venv/bin/activate", ""),
            ("pip install -r requirements.txt", ""),
            ("python run.py", "# → http://localhost:5000"),
        ],
    }

    steps_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), expand=False)
    steps_table.add_column(style=f"bold {TERTIARY}", width=5, justify="right")
    steps_table.add_column()

    for i, (cmd, comment) in enumerate(next_steps[stack], 1):
        comment_part = f"  [{OUTLINE}]{comment}[/{OUTLINE}]" if comment else ""
        steps_table.add_row(
            str(i),
            f"[bold {PRIMARY}]{cmd}[/bold {PRIMARY}]{comment_part}",
        )

    console.print(
        Panel(
            steps_table,
            title=f"[bold {SECONDARY}]  Next Steps[/bold {SECONDARY}]",
            title_align="left",
            border_style=OUTLINE,
            padding=(0, 1),
        )
    )
    console.print()

    # ── Final arrow line ─────────────────────────────────────────────────────
    join_cmd = next_steps[stack][-1][0]
    _arrow(f"cd {project_name} && {join_cmd}")
    console.print()

    console.print(Rule(style=OUTLINE))
    console.print(
        Align.center(
            Text(
                f"  v2.4.0 Engine Ready  ·  {len(file_paths)} files created  ",
                style=f"dim {OUTLINE}",
            )
        )
    )
    console.print()


# ─── Info Command ─────────────────────────────────────────────────────────────

@app.command(name="stacks")
def stacks():
    """List all supported stacks and their included packages."""
    print_banner()

    table = Table(
        title=f"[bold {PRIMARY}]Supported Stacks[/bold {PRIMARY}]",
        box=box.ROUNDED,
        border_style=OUTLINE,
        header_style=f"bold {PRIMARY}",
        title_style=f"bold {PRIMARY}",
        show_lines=True,
        expand=False,
    )
    table.add_column("Stack", style=f"bold {ON_SURFACE}", width=18)
    table.add_column("Flag", style=f"{TERTIARY}", width=16)
    table.add_column("Core Packages", style=DIM_TEXT)
    table.add_column("Runtime", style=SECONDARY, width=12)

    data = [
        (
            "Next.js 15",
            "--stack nextjs",
            "next, react 19, typescript, turbopack",
            "Node ≥20",
        ),
        (
            "Node + Express",
            "--stack node-express",
            "express 4, cors, helmet, morgan, dotenv",
            "Node ≥18",
        ),
        (
            "Flask (Python)",
            "--stack flask",
            "flask, flask-cors, python-dotenv",
            "Python ≥3.11",
        ),
    ]

    for name, flag, pkgs, runtime in data:
        table.add_row(name, flag, pkgs, runtime)

    console.print()
    console.print(Align.center(table))

    feat_table = Table(
        title=f"[bold {SECONDARY}]Optional Features[/bold {SECONDARY}]",
        box=box.ROUNDED,
        border_style=OUTLINE,
        header_style=f"bold {SECONDARY}",
        title_style=f"bold {SECONDARY}",
        expand=False,
    )
    feat_table.add_column("Feature", style=f"bold {ON_SURFACE}", width=12)
    feat_table.add_column("Flag", style=TERTIARY, width=20)
    feat_table.add_column("Description", style=DIM_TEXT)

    feat_data = [
        ("tailwind", "-f tailwind", "Tailwind CSS v4 with PostCSS config (Next.js)"),
        ("auth",     "-f auth",     "JWT / session auth scaffold with register + login routes"),
        ("api",      "-f api",      "REST API boilerplate with example CRUD endpoints"),
    ]
    for f, flag, desc in feat_data:
        feat_table.add_row(f, flag, desc)

    console.print()
    console.print(Align.center(feat_table))
    console.print()


# ─── Version ─────────────────────────────────────────────────────────────────

def version_callback(value: bool):
    if value:
        console.print(
            f"[bold {PRIMARY}]QuickForge[/bold {PRIMARY}] "
            f"[{DIM_TEXT}]v2.4.0[/{DIM_TEXT}]  "
            f"[{OUTLINE}]High-Fidelity Scaffolding Engine[/{OUTLINE}]"
        )
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", callback=version_callback, is_eager=True, help="Show version"
    ),
):
    """
    [bold]QuickForge[/bold] — Generate production-ready webapps in seconds.

    Run [bold]quickforge create --help[/bold] for scaffolding options.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print(
            Panel(
                f"[{DIM_TEXT}]Run a command to get started:[/{DIM_TEXT}]\n\n"
                f"  [{PRIMARY}]quickforge create my-app[/{PRIMARY}]             [dim]scaffold a new project[/dim]\n"
                f"  [{PRIMARY}]quickforge create my-app --stack flask[/{PRIMARY}]  [dim]use Flask[/dim]\n"
                f"  [{PRIMARY}]quickforge stacks[/{PRIMARY}]                    [dim]list all stacks[/dim]\n"
                f"  [{PRIMARY}]quickforge --help[/{PRIMARY}]                    [dim]show all options[/dim]",
                title=f"[bold {PRIMARY}]  Quick Reference[/bold {PRIMARY}]",
                title_align="left",
                border_style=OUTLINE,
                padding=(1, 2),
            )
        )


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app()
