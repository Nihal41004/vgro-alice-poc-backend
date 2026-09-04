import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="VGRO Alice Blue POC",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vgro-alice-test.vercel.app",
        "http://localhost",
        "http://127.0.0.1"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthCallbackRequest(BaseModel):
    authCode: str
    userId: str
    appCode: str


@app.get("/api")
def root():
    return {
        "message": "VGRO Alice Blue POC Backend Running"
    }


@app.get("/api/health")
def health():

    app_code = os.getenv("ALICE_APP_CODE")
    api_secret = os.getenv("ALICE_API_SECRET")

    return {
        "status": "healthy",
        "app_code_configured": bool(app_code),
        "api_secret_configured": bool(api_secret)
    }


@app.post("/auth/callback")
def auth_callback(data: AuthCallbackRequest):

    configured_app_code = os.getenv("ALICE_APP_CODE")

    if not configured_app_code:
        raise HTTPException(
            status_code=500,
            detail="Alice Blue App Code is not configured"
        )

    if data.appCode != configured_app_code:
        raise HTTPException(
            status_code=400,
            detail="Invalid App Code"
        )

    return {
        "success": True,
        "message": "Authentication response received successfully",
        "userId": data.userId
    }