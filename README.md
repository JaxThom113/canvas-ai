# CanvasAI

An AI agent extension for Canvas!

## Setup Instructions

Follow these steps after cloning the repo to get the extension running locally.

**Requirements:** Python 3.13, Node.js/npm, Google Chrome.

### 1. Backend setup

```bash
cd canvas-ai/backend

# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# create a .env file in backend/ with your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 2. Database setup

The backend stores test/session/chat data in a local MariaDB database. This is entirely local per machine — nothing here is shared through git, so each teammate needs to set up their own instance.

Install and start MariaDB if you don't already have it running — skip this if you do:

```bash
# macOS (Homebrew)
brew install mariadb
brew services start mariadb

# Ubuntu/Debian
sudo apt install mariadb-server
sudo systemctl start mariadb

# Fedora/RHEL
sudo dnf install mariadb-server
sudo systemctl start mariadb
```

Create the database and its tables from the provided schema:

```bash
# from canvas-ai/
mariadb < backend/db/canvasai_DB.sql
```

Create a dedicated app user and grant it access (pick any password — it's local-only):

```bash
mariadb -e "CREATE USER 'canvas_app'@'localhost' IDENTIFIED BY 'devpassword'; GRANT ALL PRIVILEGES ON canvas_ai.* TO 'canvas_app'@'localhost'; FLUSH PRIVILEGES;"
```

Add the following lines to your `backend/.env` (alongside `GEMINI_API_KEY` — don't overwrite the file, just add these):

```
DB_HOST=localhost
DB_USER=canvas_app
DB_PASSWORD=devpassword
DB_NAME=canvas_ai
```

### 3. Run the backend

```bash
# from canvas-ai/backend, with venv activated
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`. Leave this running in its own terminal.

### 4. Frontend / extension setup

```bash
cd canvas-ai/frontend

npm install
npm run build       # builds the extension into frontend/dist
```

### 5. Load the extension in Chrome

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked**
4. Select the `canvas-ai/frontend/dist` folder

### 6. Using the extension

- Make sure the backend (step 3) is running.
- Log into Canvas (any `*.instructure.com` site) in Chrome.
- Click the CanvasAI extension icon to open the popup.
- The popup has a "Show DB Test Interface" toggle for inserting test rows directly into `login`/`session`/`chat` — useful for seeding data without writing SQL by hand.

### Notes

- Whenever frontend source (`src/`) changes, re-run `npm run build` and click the reload icon for the extension on `chrome://extensions` to pick up changes. If you're only testing the DB interface (no `chrome.*` APIs involved), `npm run dev` and a regular browser tab works too and skips the rebuild step.
- `.env` and `venv/` are gitignored — each clone must recreate them.
- The MariaDB database (step 2) is also local-only and gitignored by nature (it's not a file in the repo at all) — each person's database and data are independent of everyone else's.
