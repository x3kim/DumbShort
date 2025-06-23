# 🔩 DumbShort

A dumb simple URL shortener app that does exactly one thing: Take long URLs and make them shorter and dumber. Built with Python (Flask) and Vanilla JavaScript.

_(Tip: Take a cool screenshot of your running app and upload it to Imgur or similar, then link it here)_

No accounts, no cookies (except for dark mode), no bullshit. Just paste a URL, get a short link.

## Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🐳 Deployment with Docker](#-deployment-with-docker)
- [👨‍💻 Local Development](LOCAL_DEVELOPMENT.md) _(I'll provide this later)_
- [✨ Features](#-features)
- [⚙️ Configuration](#️-configuration)
- [🛡️ Security](#️-security)
- [🛠️ Technical Details](#️-technical-details)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## 🚀 Quick Start

### Option 1: Docker (For Dummies)

```bash
# Pull and start with one command
docker run -d -p 5000:5000 -v ./data/dumbshort.db:/app/dumbshort.db --name dumbshort x3kim/dumbshort:latest
```

_(Note: Replace `x3kim/dumbshort` with your Docker Hub name, e.g. `x3kim/dumbshort`)_

1.  Go to `http://localhost:5000`
2.  Paste a long URL and press Enter/Space.
3.  Enjoy how dumb simple that was.

### Option 2: Docker Compose (For Dummies Who Like to Customize)

Create a `docker-compose.yml` file:

```yaml
services:
  dumbshort:
    image: x3kim/dumbshort:latest # Replace this with your image name
    ports:
      - "5000:5000"
    volumes:
      # This is where your database will be stored persistently
      - ./data:/app/data
    environment:
      # Change the port the app runs on inside the container
      - PORT=5000
      # Set the number of Gunicorn workers
      - WORKERS=3
      # Change the log level for more or less verbose output
      - LOG_LEVEL=info
    # Always restarts the container unless it is explicitly stopped
    restart: unless-stopped
```

_(Note: For environment variables to work, we would need to adjust the `CMD` line in the Dockerfile. This is an optional, advanced step.)_

Then run:

```bash
docker compose up -d
```

1.  Go to `http://localhost:5000`
2.  Shorten a URL. The data will be stored in `./data/dumbshort.db`.
3.  Enjoy the glory of your dumb, short links.

> **Note:** The `./data` folder on your computer is mounted into the container. We store the `dumbshort.db` there so your links persist after a restart. Create the `./data` folder before starting.

### Option 3: Local Run (For Developers)

For local development, debugging, and advanced usage, see the dedicated guide:

👉 [Local Development Guide](LOCAL_DEVELOPMENT.md) _(We can create this file if needed)_

## ✨ Features

- 🚀 **Blazing Fast Shortening:** Paste a URL, press Space/Enter, done.
- 📋 **Auto-Copy:** The shortened link is immediately copied to your clipboard.
- 🎨 **Clean, Responsive UI:** With dark mode to save your eyes.
- 📊 **Dumb Stats:** See how many links you've created and how often they've (accidentally) been clicked.
- 🔍 **Searchable Overview:** Find all your links in a simple table.
- ✏️ **Editable Names:** Give your links names to identify them more easily.
- 🗑️ **Delete Function:** Remove links that were dumber than allowed.
- 📦 **Docker Support:** Easy configuration and deployment.
- 📱 **PWA-ready:** "Install" the website as an app on your desktop or phone.
- 🛡️ **No Tracking, No Bullshit:** What happens in DumbShort stays in DumbShort.

## ⚙️ Configuration

### Environment Variables (for Docker)

| Variable    | Description                                          | Default | Required |
| ----------- | ---------------------------------------------------- | ------- | -------- |
| `PORT`      | The port the app listens on in the container.        | 5000    | No       |
| `WORKERS`   | Number of Gunicorn worker processes.                 | 3       | No       |
| `LOG_LEVEL` | Log level for Gunicorn (`debug`, `info`, `warning`). | info    | No       |

## 🛡️ Security

Security by stupidity.

- **No User Data:** We don't store any personal data, so we can't lose any.
- **No External Scripts:** Everything that runs is part of this project. No tracking by third parties.
- **Simple Database:** SQLite is a file. No open database port to be attacked.

## 🛠️ Technical Details

### Stack

- **Backend**: Python 3.11 with Flask
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Database**: SQLite
- **Container**: Docker with Multi-Stage-Builds
- **WSGI Server**: Gunicorn

### Dependencies

- **Python**: Flask, Gunicorn
- **Node.js (only for the build)**: tailwindcss

## 🤝 Contributing

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'feat: Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## Support the Project

If you like this dumb app, give the repo a star or buy me a coffee... oh wait, i don't have a buymeacoffee account yet.. damn.

---

Made with ❤️ by [x3kim](https://github.com/x3kim) - inspired by [DumbWare.io](https://dumbware.io)

## 📜 License

This project is licensed under the [MIT License](LICENSE). Dumb, simple, and free.
