# backend/token_verifier.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth, credentials, initialize_app

app = FastAPI()

# Initialize Firebase Admin SDK once
cred = credentials.Certificate("firebase_credentials.json")  # Place your service account key here
initialize_app(cred)

# Allow Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Be strict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify-token")
async def verify_token(request: Request):
    data = await request.json()
    id_token = data.get("idToken")

    try:
        decoded_token = auth.verify_id_token(id_token)
        return {"uid": decoded_token["uid"], "email": decoded_token.get("email", ""), "phone_number": decoded_token.get("phone_number", "")}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

