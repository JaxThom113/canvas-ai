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

### 2. Run the backend

```bash
# from canvas-ai/backend, with venv activated
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`. Leave this running in its own terminal.

### 3. Frontend / extension setup

```bash
cd canvas-ai/frontend

npm install
npm run build       # builds the extension into frontend/dist
```

### 4. Load the extension in Chrome

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked**
4. Select the `canvas-ai/frontend/dist` folder

### 5. Using the extension

- Make sure the backend (step 2) is running.
- Log into Canvas (any `*.instructure.com` site) in Chrome.
- Click the CanvasAI extension icon to open the popup.

### Notes

- Whenever frontend source (`src/`) changes, re-run `npm run build` and click the reload icon for the extension on `chrome://extensions` to pick up changes.
- `.env` and `venv/` are gitignored — each clone must recreate them.
