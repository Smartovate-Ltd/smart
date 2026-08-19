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

    if not verify_signature(
        payload_body,
        signature_header,
        GITHUB_WEBHOOK_SECRET,
    ):
        logger.warning("Webhook reçu avec une signature invalide — requête rejetée.")
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(payload_body)
    event_type = request.headers.get("X-GitHub-Event", "unknown")

    logger.info("Événement GitHub reçu : type='%s'", event_type)

    delivery_id = request.headers.get("X-GitHub-Delivery")

    if delivery_id and delivery_id in DELIVERIES_TRAITEES:
        logger.info(
            "Livraison %s déjà traitée précédemment — événement ignoré (idempotence).",
            delivery_id,
        )
        return {"status": "already_processed", "event": event_type}

    if delivery_id:
        DELIVERIES_TRAITEES.add(delivery_id)

    if (
        event_type == "pull_request"
        and payload.get("action") in ("opened", "synchronize")
    ):
        try:
            installation_id = payload["installation"]["id"]
            full_name = payload["repository"]["full_name"]
            owner, repo = full_name.split("/", 1)
            pr_number = payload["pull_request"]["number"]

            logger.info(
                "PR #%d détectée sur %s (action: %s) — démarrage de l'extraction du diff.",
                pr_number,
                full_name,
                payload.get("action"),
            )

            installation_token = get_installation_token(installation_id)

            logger.info("Token d'installation obtenu avec succès.")

            diff_text = get_pr_diff(
                owner,
                repo,
                pr_number,
                installation_token,
            )

            logger.info(
                "Diff de la PR #%d récupéré (%d octets).",
                pr_number,
                len(diff_text),
            )

            fichiers = parser_diff(diff_text)
            chemins = [f["chemin"] for f in fichiers]

            logger.info(
                "Diff parsé : %d fichier(s) pertinent(s) trouvé(s) : %s",
                len(fichiers),
                chemins,
            )

            commentaires = analyser_code(fichiers)

            logger.info(
                "Analyse LLM terminée : %d commentaire(s) généré(s).",
                len(commentaires),
            )

            commentaires = valider_commentaires(commentaires, fichiers)

            nb_valides = sum(
                1 for c in commentaires if c["ligne_valide"]
            )

            nb_invalides = len(commentaires) - nb_valides

            logger.info(
                "Validation terminée : %d commentaire(s) sur ligne valide, "
                "%d à reclasser en commentaire global.",
                nb_valides,
                nb_invalides,
            )

            for c in commentaires:
                marqueur = (
                    "OK"
                    if c["ligne_valide"]
                    else "!! ligne invalide"
                )

                logger.info(
                    "  [%s] %s ligne %s : %s",
                    marqueur,
                    c.get("fichier", "?"),
                    c.get("ligne", "?"),
                    c.get("contenu", ""),
                )

        except Exception as exc:
            logger.error(
                "Erreur lors du traitement de la PR (event=%s) : %s",
                event_type,
                exc,
            )

    return {"status": "received", "event": event_type}
