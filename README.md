import json

from fastapi import FastAPI, HTTPException, Request

from config import GITHUB_WEBHOOK_SECRET, get_logger
from diff_parser import parser_diff
from github_client import get_installation_token, get_pr_diff
from llm_client import analyser_code
from review_validator import valider_commentaires
from security import verify_signature

logger = get_logger(__name__)

app = FastAPI(
    title="smartovate-ai-reviewer",
    description="Agent IA automatisé de revue de code pour Pull Requests — Smartovate Ltd",
    version="0.2.0",
)

DELIVERIES_TRAITEES: set[str] = set()


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.post("/webhook")
async def github_webhook(request: Request):
    payload_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256", "")

    if not GITHUB_WEBHOOK_SECRET:
        logger.error("GITHUB_WEBHOOK_SECRET n'est pas configuré dans .env")
        raise HTTPException(status_code=500, detail="Server misconfiguration")

    if no verify_signature(
        payload_body,
        signature_header,
        GITHUB_WEBHOOK_SECRET,
    ):
       
