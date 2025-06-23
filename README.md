# DumbShort 🔩

Eine dumm einfache URL-Kürzungs-App, die genau eine Sache macht: Lange URLs nehmen und sie kürzer und dümmer machen. Gebaut mit Python (Flask) und Vanilla JavaScript.

_(Tipp: Mache einen coolen Screenshot von deiner laufenden App und lade ihn z.B. bei Imgur hoch, um den Link hier einzufügen)_

Keine Accounts, keine Cookies (außer für den Dark Mode), kein Bullshit. Nur eine URL einfügen, einen Kurzlink bekommen.

## Inhaltsverzeichnis

- [🚀 Quick Start](#-quick-start)
- [🐳 Bereitstellung mit Docker](#-bereitstellung-mit-docker)
- [👨‍💻 Lokale Entwicklung](LOCAL_DEVELOPMENT.md) _(können wir später erstellen)_
- [✨ Features](#-features)
- [⚙️ Konfiguration](#️-konfiguration)
- [🛡️ Sicherheit](#️-sicherheit)
- [🛠️ Technische Details](#️-technische-details)
- [🤝 Mitwirken](#-mitwirken)
- [📜 Lizenz](#-lizenz)

## 🚀 Quick Start

### Option 1: Docker (Für Dummies)

```bash
# Ziehen und starten mit einem Befehl
docker run -d -p 5000:5000 -v ./data/dumbshort.db:/app/dumbshort.db --name dumbshort dumbwareio/dumbshort:latest
```

_(Hinweis: Ersetze `dumbwareio/dumbshort` durch deinen Docker-Hub-Namen, z.B. `x3kim/dumbshort`)_

1.  Gehe zu `http://localhost:5000`
2.  Füge eine lange URL ein und drücke Enter/Leerzeichen.
3.  Freu dich, wie dumm einfach das war.

### Option 2: Docker Compose (Für Dummies, die gerne anpassen)

Erstelle eine `docker-compose.yml` Datei:

```yaml
services:
  dumbshort:
    image: dumbwareio/dumbshort:latest # Ersetze dies mit deinem Image-Namen
    ports:
      - "5000:5000"
    volumes:
      # Hier wird deine Datenbank persistent gespeichert
      - ./data:/app/data
    environment:
      # Ändere den Port, auf dem die App im Container läuft
      - PORT=5000
      # Setze die Anzahl der Gunicorn-Worker
      - WORKERS=3
      # Ändere den Loglevel für mehr oder weniger dumme Ausgaben
      - LOG_LEVEL=info
    # Startet den Container immer neu, es sei denn, er wird explizit gestoppt
    restart: unless-stopped
```

_(Hinweis: Damit die Environment-Variablen funktionieren, müssten wir die `CMD`-Zeile im Dockerfile anpassen. Das ist ein optionaler, fortgeschrittener Schritt.)_

Dann führe aus:

```bash
docker compose up -d
```

1.  Gehe zu `http://localhost:5000`
2.  Kürze eine URL. Die Daten landen in `./data/dumbshort.db`.
3.  Genieße den Ruhm deiner dummen, kurzen Links.

> **Hinweis:** Der Ordner `./data` auf deinem Computer wird in den Container gemountet. Wir speichern die `dumbshort.db` dort, damit deine Links auch nach einem Neustart noch da sind. Erstelle den Ordner `./data` vor dem Start.

### Option 3: Lokale Ausführung (Für Entwickler)

Für die lokale Entwicklung, Fehlersuche und fortgeschrittene Nutzung, siehe die dedizierte Anleitung:

👉 [Anleitung zur lokalen Entwicklung](LOCAL_DEVELOPMENT.md) _(Diese Datei können wir bei Bedarf noch erstellen)_

## ✨ Features

- 🚀 **Blitzschnelles Kürzen:** URL einfügen, Leerzeichen/Enter drücken, fertig.
- 📋 **Auto-Kopieren:** Der gekürzte Link landet sofort in deiner Zwischenablage.
- 🎨 **Saubere, responsive UI:** Mit Dark Mode, der deine Augen schont.
- 📊 **Dumme Statistiken:** Sieh, wie viele Links du erstellt hast und wie oft sie (aus Versehen) geklickt wurden.
- 🔍 **Durchsuchbare Übersicht:** Finde jeden deiner Links in einer einfachen Tabelle wieder.
- ✏️ **Bearbeitbare Namen:** Gib deinen Links Namen, um sie leichter zu identifizieren.
- 🗑️ **Löschen-Funktion:** Entferne Links, die dümmer waren als erlaubt.
- 📦 **Docker-Unterstützung:** Einfache Konfiguration und Bereitstellung.
- 📱 **PWA-fähig:** "Installiere" die Webseite als App auf deinem Desktop oder Handy.
- 🛡️ **Kein Tracking, kein Bullshit:** Was in DumbShort passiert, bleibt in DumbShort.

## ⚙️ Konfiguration

### Umgebungsvariablen (für Docker)

| Variable    | Beschreibung                                        | Standard | Erforderlich |
| ----------- | --------------------------------------------------- | -------- | ------------ |
| `PORT`      | Der Port, auf dem die App im Container lauscht.     | 5000     | Nein         |
| `WORKERS`   | Anzahl der Gunicorn-Worker-Prozesse.                | 3        | Nein         |
| `LOG_LEVEL` | Loglevel für Gunicorn (`debug`, `info`, `warning`). | info     | Nein         |

## 🛡️ Sicherheit

Sicherheit durch Dummheit.

- **Keine Benutzerdaten:** Wir speichern keine persönlichen Daten, also können wir auch keine verlieren.
- **Keine externen Skripte:** Alles, was läuft, ist Teil dieses Projekts. Kein Tracking durch Dritte.
- **Simple Datenbank:** SQLite ist eine Datei. Kein offener Datenbank-Port, der angegriffen werden kann.

## 🛠️ Technische Details

### Stack

- **Backend**: Python 3.11 mit Flask
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Datenbank**: SQLite
- **Container**: Docker mit Multi-Stage-Builds
- **WSGI Server**: Gunicorn

### Abhängigkeiten

- **Python**: Flask, Gunicorn
- **Node.js (nur für den Build)**: tailwindcss

## 🤝 Mitwirken

1.  Forke das Repository.
2.  Erstelle deinen Feature-Branch (`git checkout -b feature/amazing-feature`).
3.  Committe deine Änderungen (`git commit -m 'feat: Add some amazing feature'`).
4.  Pushe zum Branch (`git push origin feature/amazing-feature`).
5.  Öffne einen Pull Request.

## Support the Project

Wenn dir diese dumme App gefällt, gib dem Repo einen Stern oder...

<a href="https://www.buymeacoffee.com/dumbware" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="60">
</a>

_(Link kann natürlich angepasst werden)_

---

Mit ❤️ gebaut von [x3kim](https://github.com/x3kim) - inspiriert von [DumbWare.io](https://dumbware.io)

## 📜 Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert. Dumm, einfach und frei.
