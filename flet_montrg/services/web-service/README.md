# 🌐 Web Service (APIs Web Service)

Unified Swagger UI web client for API documentation. Built with Svelte 4, Vite 5, and Tailwind CSS. Backend: `integrated-swagger-service` (proxy/API).

## ✨ Stack

- **Svelte 4** — UI framework
- **Vite 5** — build tool
- **Tailwind CSS (CDN)** — styling
- **Swagger UI** — API docs

## 📜 npm scripts

```bash
# Install dependencies (first time)
npm install

# Dev server (hot reload)
npm run dev

# Production build
npm run build

# Preview build
npm run preview
```

## ⚙️ Config

- **API base**: Set via `?apiBase=URL`. If omitted, `window.location.origin` is used.
- **Theme**: localStorage key `felt-montrg-theme` (`light` | `dark`)

## 🚀 Run

### Local

```bash
# If using nvm and npm not found in shell
source ~/.zshrc
# or
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

npm run dev
```

- App: <http://localhost:5173>
- With custom API host: <http://localhost:5173?apiBase=http://localhost:30001>

### K8s (Kind)

- **NodePort**: `30000` (see project [README](../../README.md) for port layout)
- Deploy: `Dockerfile` and `k8s/web-service/` manifests.

## 📦 Deploy

```bash
npm run build
```

Serve the `dist/` folder with nginx, Apache, S3+CloudFront, or any static host. For Docker/K8s, use the repo `Dockerfile` and `k8s/web-service/` manifests.

## 🐛 Troubleshooting

- Build fails: Run `npm install` and use a matching Node version (e.g. 18+). Check dependency errors.
- API not loading: Set `apiBase` (e.g. `?apiBase=http://localhost:30001`) so the client can reach integrated-swagger-service.

## 📚 References

- [Svelte](https://svelte.dev/)
- [Vite](https://vitejs.dev/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

Last updated: February 2026

