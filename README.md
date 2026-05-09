<div align="center">

<img src="frontend/public/raven.svg" width="67" alt="Lodestone Logo" />

<h1>Lodestone</h1>

![Version](https://img.shields.io/badge/version-0.15.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![GitHub stars](https://img.shields.io/github/stars/bremsstrahlung-57/lodestone)
![Last commit](https://img.shields.io/github/last-commit/bremsstrahlung-57/lodestone)

<p>Lodestone is a local-first document retrieval system. Drop in files, query with natural language, get answers grounded in your documents. Everything runs on your machine.</p>

> ⚠️ **Note**: Lodestone is under active development, so breaking changes and rough edges are still possible.

<img src="demos/lodestone_demo.gif" width="600" alt="Lodestone Demo GIF" />

</div>

---

## Quickstart

The easiest way to run Lodestone is with the Docker-based setup and the Lodestone CLI.

**Prerequisites**: Docker

**Install the CLI globally**:

```bash
npm install -g lodestone-r
```
**Start Lodestone**:
```bash
lodestone start
```
**Open**:
```bash
http://localhost:8090
```
Then add your API key in Settings, drop in a file, and search.

> 💡 Note: On Linux, you may need `sudo npm install -g lodestone-r` if your npm global directory is system-managed. Using nvm avoids that nonsense.

**Other ways**:
**macOS/Linux (Bash)**:
```bash
curl -sSL https://raw.githubusercontent.com/bremsstrahlung-57/lodestone/master/install.sh | bash
```

**Windows (PowerShell)**:
```powershell
iwr "https://raw.githubusercontent.com/bremsstrahlung-57/lodestone/master/install.ps1" -OutFile "$env:TEMP\install.ps1"; powershell -ExecutionPolicy Bypass -File "$env:TEMP\install.ps1"
```

> 💡 **Note**: Some antivirus software may flag or block the automated install script. If this happens, you can safely allow it.



Open `http://localhost:8090`. Add your API key in Settings, drop in a file, and search.

---

## CLI Commands

Lodestone provides a CLI wrapper for managing your local instance:

- `lodestone start` — Download the latest compose config and start the containers
- `lodestone stop` — Stop the containers
- `lodestone update` — Fetch the latest configuration, pull new Docker images, and restart
- `lodestone logs` — Tail the container logs
- `lodestone delete` — Stop containers and remove local images, while keeping data and volumes
- `lodestone prune` — Completely remove containers, images, volumes, and installation data, while keeping config

---

## Features

- Semantic search over your own documents using sentence embeddings
- AI-answered queries with retrieved context as grounding
- Drag-and-drop file ingestion from the browser
- Full document viewer with expandable neighboring chunks
- Switchable LLM providers: Anthropic, OpenAI, Gemini, Groq
- Content-addressed deduplication via SHA3-256

---

## How It Works

Ingested documents are chunked, embedded with MiniLM-L6-v2, and stored in a local Qdrant instance. Queries go through optional AI rewriting, dense vector search, cross-encoder reranking, and score-based filtering before results are returned. Full document content is cached in SQLite. Everything is async end-to-end.

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | FastAPI |
| Vector store | Qdrant (local via Docker) |
| Metadata store | SQLite via aiosqlite |
| Embeddings | MiniLM-L6-v2 |
| Reranking | Cross-encoder |
| LLM providers | Anthropic, OpenAI, Gemini, Groq |

---

## Local Development

If you want to run Lodestone from source for development:

**Prerequisites**: Python 3.12+, Node.js 18+, Docker

```bash
# Start Qdrant
docker run -p 8092:6333 qdrant/qdrant

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8091

# Frontend
cd frontend
npm install
npm run dev
```

---

## Configuration

Lodestone follows the XDG base directory spec. On first run, config files are created at:

- `~/.config/lodestone/config.toml` — general settings and defaults
- `~/.config/lodestone/keys.toml` — API keys, gitignored by default

---

## Credits

- Logo: [Raven icon](https://www.svgrepo.com/svg/156257/raven) from SVG Repo

---
