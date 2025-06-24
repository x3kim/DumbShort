# Local Development Guide for DumbShort

This guide is for developers who want to run the application on their local machine without Docker. This is useful for debugging, testing, and contributing new (and dumber) features.

## Prerequisites

- **Python 3.11+**: Make sure it's installed and available in your PATH.
- **Node.js and npm**: Required to build the frontend assets (Tailwind CSS). You can download it from nodejs.org.
- **A Python virtual environment tool**: We recommend using the built-in venv.

## ⚙️ Setup and Installation

Follow these steps to get your local development environment up and running.

### 1. Clone the Repository

First, get the code onto your machine.

```bash
git clone https://github.com/x3kim/DumbShort.git
cd DumbShort
```

### 2. Set Up the Python Virtual Environment

It's a best practice to keep your project's Python dependencies isolated.

```bash
# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

Your terminal prompt should now be prefixed with (venv), indicating that the virtual environment is active.

### 3. Install Dependencies

Now, install all the required Python and Node.js packages.

```bash
# Install Python packages
pip install -r requirements.txt

# Install Node.js packages (for Tailwind CSS)
npm install
```

## 🚀 Running the Application

To run the application, you'll need **two terminals** running simultaneously: one for the Python backend and one for the CSS build process.

### Terminal 1: Run the CSS Watcher

This command will watch your `.html` and `input.css` files for changes and automatically rebuild the `output.css` file. Leave this terminal running in the background while you work.

```bash
./node_modules/.bin/tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

### Terminal 2: Run the Flask Backend Server

This command starts the Python web server. It will automatically reload if you make changes to the `app.py` file.

```bash
python app.py
```

### Accessing the App

Once both processes are running, you can access your local instance of DumbShort in your web browser at:

👉 **[http://localhost:5000](http://localhost:5000)**

### How it Works Locally

- The Python server (`app.py`) handles all API requests and serves the main `index.html` file.
- When you make changes to `app.py`, the Flask development server will restart automatically.
- When you make changes to `templates/index.html` or `static/css/input.css`, the `npm run css:watch` command will rebuild `static/css/output.css`. You may need to refresh your browser to see the style changes.
- The SQLite database file (`dumbshort.db`) will be created in the `data` directory, which will be created in the root of the project when you first run the app.

## 🛑 Stopping the Application

To stop the local servers, simply press `Ctrl+C` in each of the two terminals.

To deactivate the Python virtual environment when you're done, just type:

```bash
deactivate
```
