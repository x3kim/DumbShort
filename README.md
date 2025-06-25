# 🤏 DumbShort

A stupidly simple, no-bullshit URL shortener. Paste a URL. It's shortened and the result is selected. Your muscle memory for `Ctrl+C` does the rest. (localhost works with auto-copy)

Built in the spirit of [DumbWare.io](https://dumbware.io) – because sometimes the dumbest solution is the smartest choice.

> [!NOTE]  
> [DEMO PAGE](https://dumbshort-demo.x3kim.de/) <- Yup, just click it – takes you straight to the demo. Don't be shy. 🚀

https://github.com/user-attachments/assets/b043356c-77de-4005-bf21-0ebf0d909911

---

## Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [⚙️ Configuration](#️-configuration)
- [🛡️ Security & A Note on HTTPS](#️-security--a-note-on-https-and-network-access)
- [🛠️ Technical Details](#️-technical-details)
- [👨‍💻 Local Development](LOCAL_DEVELOPMENT.md)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## 🚀 Quick Start

The only sane way to run this is with Docker. Pick your level of laziness.

### Option 1: Docker Run (The "I just want it running" method)

One command to rule them all. This pulls the image from Docker Hub and starts the app on port 5001.

```bash
docker run -d --name dumbshort -p 5001:5000 -v dumbshort_data:/app/data x3kim/dumbshort:latest
```

1. Go to `http://localhost:5001` in your browser.
2. Paste a long URL and press Enter or Space.
3. Enjoy how dumb simple that was.

> **Note:** This uses a Docker-managed volume named `dumbshort_data` to store your database file, so your links persist even if you remove the container.

### Option 2: Docker Compose (Recommended for easy management)

This is the cleanest way. It uses the provided `docker-compose.yml` and is configurable.

1. Clone this repository.
2. (Optional) Create a `.env` file from `env.example` to customize the public port and other settings.
3. Run the command:

```bash
docker-compose up -d
```

4. The app will be available at `http://localhost:5001` (or your custom `APP_PORT`).

## ✨ Features

- 🚀 **Blazing Fast Workflow:** Paste a URL, press Space/Enter. The short link is created and **instantly selected** for easy copying.
- 🪄 **Magic Auto-Copy:** When accessed via `localhost`, the link is also **automatically** copied to your clipboard for maximum laziness.
- 📋 **Robust Copy Button:** A reliable manual copy button for every other situation (like accessing from another device on your network).
- 🎨 **Clean, Responsive UI:** With a dark mode to save your precious eyes from the blinding light of overly long URLs.
- 📊 **Dumb Stats:** See how many links you've launched into the void and how often they've (accidentally) been clicked.
- 🔍 **Searchable Overview:** A simple, responsive table to find all your links.
- ✏️ **Editable Names:** Give your links dumb names to identify them. Click to edit. It's that simple.
- 🗑️ **Delete Function:** Mercilessly remove links that were dumber than allowed.
- 🧠 **Smart URL Correction:** Typed `google.de`? We got you. We'll automatically fix it to `https://google.de` before saving.
- 📦 **Simple Docker Support:** Easy configuration and deployment with a single container.
- 📱 **PWA-ready:** "Install" the website as an app on your desktop or phone.

## ⚙️ Configuration

Configure the application via environment variables. Create a `.env` file from the `env.example` template for use with Docker Compose, or use `-e` flags with `docker run`.

| Variable             | Description                                          | Default |
| -------------------- | ---------------------------------------------------- | ------- |
| `APP_PORT`           | The public HTTP port the app is accessible on.       | `5001`  |
| `GUNICORN_WORKERS`   | Number of Gunicorn worker processes.                 | `4`     |
| `GUNICORN_LOG_LEVEL` | Log level for Gunicorn (`debug`, `info`, `warning`). | `info`  |

## 🛡️ Security & A Note on HTTPS and Network Access

This app runs on simple **HTTP**. This is a deliberate choice to keep the setup dumb and simple. However, modern browsers have strict security policies.

- **Why Auto-Copy & PWA Install Only Work on `localhost`:** Sensitive browser features like writing to the clipboard (`navigator.clipboard`) and the "Install App" prompt are only enabled in what browsers consider a "secure context". This is either `localhost` or any site served over `https://`.
- **Accessing from other devices:** When you access the app from another computer on your network (e.g., `http://192.168.1.50:5001`), your browser correctly identifies this as an insecure connection. The app will work perfectly, but you will need to use the manual **"Copy" button**. This is a security feature, not a bug. (sadly only works on localhost too)
- **For a full HTTPS setup:** You should run this container behind your own main reverse proxy (like Nginx Proxy Manager or Traefik), which can provide a valid SSL certificate.

## 🛠️ Technical Details

- **Backend**: Python 3.11 / Flask, Gunicorn
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **Containerization**: Docker, Docker Compose

## 👨‍💻 Local Development

For instructions on running the app locally without Docker for development purposes, see the dedicated guide:

👉 [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)

## 🤝 Contributing

This project is probably perfect as it is, but if you find a way to make it even dumber and simpler, feel free to contribute.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/EvenDumberFeature`).
3. Commit your changes (`git commit -m 'feat: Add a feature that is somehow even dumber'`).
4. Push to the branch (`git push origin feature/EvenDumberFeature`).
5. Open a Pull Request.

---

Made with ❤️ and a healthy dose of sarcasm by [x3kim](https://github.com/x3kim) - inspired by the glorious philosophy of [DumbWare.io](https://dumbware.io)

## 📜 License

This project is licensed under the [MIT License](LICENSE). Dumb, simple, and free. Do whatever you want.
