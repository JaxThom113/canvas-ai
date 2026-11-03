# Canvy

<img alt="Canvy Logo Full" width="400" src="./frontend/src/assets/canvy_logo_full.png">

AI search assist tool for Canvas

## Run with Docker

Creating the build folder
1. Fill in environment variables in the `backend/.env` file (`DB_SSL_CA` can be left blank)
2. Navigate to root project directory
3. Create the build folder and start backend with `docker compose up --build`
4. Open web browser and go to **chrome://extensions** and load `build/canvy` as an unpacked extension

Make sure to use `docker compose down` to stop the backend, and rerun `docker compose up --build` if making any changes to either frontend or backend.

## Run with Basic Commands

Frontend: 
1. Navigate to frontend with `cd frontend`
2. Download dependencies with `npm install`
3. Build with `npm run build`
4. Open web browser and go to **chrome://extensions** and load `frontend/dist` as an unpacked extension

Backend: 
1. Navigate to backend with `cd backend`
2. Activate the Python virtual environment with `venv/Scripts/activate`
3. Download dependencies with `pip install -r requirements.txt`
4. Start backend with `uvicorn main:app --reload`

Make sure to use `npm run build` on the frontend and `uvicorn main:app --reload` on the backend if making any changes.
