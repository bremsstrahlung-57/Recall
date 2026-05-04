## **Contributing**

Contributions are welcome! Whether it's bug fixes, new features, documentation improvements, or test coverage — all help is appreciated.

### Getting Started

1. Fork the repository and clone your fork locally.
2. Make sure you have **Node.js** (for frontend), **Python 3.12+**, **Docker** (for Qdrant), and **uv** (or pip) available.
3. Install dependencies from the backend directory:
   ```
   cd backend
   uv sync
   ```
4. API keys are managed via the UI Settings panel or in `~/.config/lodestone/keys.toml`.
5. Start Qdrant locally via Docker:
   ```
   docker run -p 8092:6333 qdrant/qdrant
   ```
6. Start the frontend development server:
   ```
   cd frontend
   npm install
   npm run dev
   ```
