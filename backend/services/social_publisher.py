"""
Social Publisher — Facebook + Instagram Graph API + Email
═══════════════════════════════════════════════════════════
Meta App: Softwa Desig (ID 122100895335285764)

Handles:
  • Facebook OAuth code → long-lived page token
  • Instagram Business account discovery
  • Publish to Facebook Pages (text + image)
  • Publish to Instagram Business (image required)
  • Email sharing via SMTP (or fallback mailto link)
  • Token storage & refresh
"""

import os
import re
import json
import logging
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# ── Meta / Facebook Graph API Config ────────────────────────────────────
META_APP_ID = "122100895335285764"
META_APP_SECRET = os.getenv("META_APP_SECRET", "")  # Set in .env for production
GRAPH_API_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# Permissions needed for FB Pages + IG Business
META_SCOPES = [
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_posts",
    "instagram_basic",
    "instagram_content_publish",
    "email",
]

# In-memory token store (use DB in production)
_token_store: Dict[str, Any] = {}

# We use aiohttp for async HTTP calls
try:
    import aiohttp
    _HAS_AIOHTTP = True
except ImportError:
    _HAS_AIOHTTP = False
    aiohttp = None


# ═══════════════════════════════════════════════════════════════════════
# OAUTH  –  Code Exchange + Long-Lived Tokens
# ═══════════════════════════════════════════════════════════════════════

def get_oauth_url(redirect_uri: str, state: str = "meta_connect") -> str:
    """Build the Facebook OAuth dialog URL."""
    scopes = ",".join(META_SCOPES)
    return (
        f"https://www.facebook.com/{GRAPH_API_VERSION}/dialog/oauth?"
        f"client_id={META_APP_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
        f"&state={state}"
        f"&response_type=code"
    )


async def _graph_get(url: str, params: dict = None) -> dict:
    """Async GET to Facebook Graph API."""
    if not _HAS_AIOHTTP:
        return {"error": "aiohttp not installed"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as r:
            data = await r.json()
            if r.status != 200:
                logger.warning(f"Graph GET {url} → {r.status}: {data}")
            return data


async def _graph_post(url: str, data: dict = None, json_body: dict = None) -> dict:
    """Async POST to Facebook Graph API."""
    if not _HAS_AIOHTTP:
        return {"error": "aiohttp not installed"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, json=json_body, timeout=aiohttp.ClientTimeout(total=60)) as r:
            resp = await r.json()
            if r.status != 200:
                logger.warning(f"Graph POST {url} → {r.status}: {resp}")
            return resp


async def exchange_code(code: str, redirect_uri: str) -> Dict[str, Any]:
    """
    Exchange short-lived auth code for access token,
    then upgrade to long-lived token + fetch Pages & IG accounts.
    """
    # Step 1: code → short-lived token
    token_resp = await _graph_get(f"{GRAPH_BASE}/oauth/access_token", {
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "redirect_uri": redirect_uri,
        "code": code,
    })
    short_token = token_resp.get("access_token")
    if not short_token:
        return {"success": False, "error": token_resp.get("error", {}).get("message", "Token exchange failed")}

    # Step 2: short → long-lived token
    ll_resp = await _graph_get(f"{GRAPH_BASE}/oauth/access_token", {
        "grant_type": "fb_exchange_token",
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "fb_exchange_token": short_token,
    })
    long_token = ll_resp.get("access_token", short_token)
    expires_in = ll_resp.get("expires_in", 5184000)  # default 60 days

    # Step 3: fetch user profile
    me = await _graph_get(f"{GRAPH_BASE}/me", {
        "fields": "id,name,email",
        "access_token": long_token,
    })

    # Step 4: fetch pages
    pages_resp = await _graph_get(f"{GRAPH_BASE}/me/accounts", {
        "fields": "id,name,access_token,category,picture",
        "access_token": long_token,
    })
    pages = pages_resp.get("data", [])

    # Step 5: for each page, look for connected IG Business account
    ig_accounts = []
    for page in pages:
        ig_resp = await _graph_get(f"{GRAPH_BASE}/{page['id']}", {
            "fields": "instagram_business_account{id,username,profile_picture_url,followers_count}",
            "access_token": page.get("access_token", long_token),
        })
        ig_biz = ig_resp.get("instagram_business_account")
        if ig_biz:
            ig_biz["page_id"] = page["id"]
            ig_biz["page_access_token"] = page.get("access_token", long_token)
            ig_accounts.append(ig_biz)

    # Store tokens
    user_id = me.get("id", "default")
    _token_store[user_id] = {
        "user_token": long_token,
        "user_name": me.get("name"),
        "user_email": me.get("email"),
        "expires_at": (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat(),
        "pages": pages,
        "instagram_accounts": ig_accounts,
        "connected_at": datetime.utcnow().isoformat(),
    }

    return {
        "success": True,
        "user": me,
        "pages": [{"id": p["id"], "name": p["name"], "category": p.get("category")} for p in pages],
        "instagram_accounts": ig_accounts,
        "expires_in": expires_in,
    }


def get_connected_accounts(user_id: str = "default") -> Dict[str, Any]:
    """Return cached connected pages & IG accounts."""
    stored = _token_store.get(user_id)
    if not stored:
        return {"connected": False, "pages": [], "instagram_accounts": []}
    return {
        "connected": True,
        "user_name": stored.get("user_name"),
        "pages": [{"id": p["id"], "name": p["name"], "category": p.get("category")} for p in stored.get("pages", [])],
        "instagram_accounts": stored.get("instagram_accounts", []),
        "expires_at": stored.get("expires_at"),
    }


def _get_page_token(page_id: str, user_id: str = "default") -> Optional[str]:
    """Look up the page access token."""
    stored = _token_store.get(user_id, {})
    for p in stored.get("pages", []):
        if p["id"] == page_id:
            return p.get("access_token")
    return stored.get("user_token")


# ═══════════════════════════════════════════════════════════════════════
# PUBLISH — Facebook Page Post
# ═══════════════════════════════════════════════════════════════════════

async def publish_to_facebook(
    page_id: str,
    message: str,
    image_url: Optional[str] = None,
    link: Optional[str] = None,
    user_id: str = "default",
) -> Dict[str, Any]:
    """
    Post to a Facebook Page.
    If image_url is provided, it becomes a photo post.
    """
    token = _get_page_token(page_id, user_id)
    if not token:
        return {"success": False, "error": "No page token found. Please connect your account first."}

    if image_url:
        # Photo post
        resp = await _graph_post(f"{GRAPH_BASE}/{page_id}/photos", data={
            "url": image_url,
            "message": message,
            "access_token": token,
        })
    else:
        # Text/link post
        payload = {"message": message, "access_token": token}
        if link:
            payload["link"] = link
        resp = await _graph_post(f"{GRAPH_BASE}/{page_id}/feed", data=payload)

    post_id = resp.get("id") or resp.get("post_id")
    if post_id:
        return {"success": True, "post_id": post_id, "platform": "facebook"}
    return {"success": False, "error": resp.get("error", {}).get("message", "Post failed")}


# ═══════════════════════════════════════════════════════════════════════
# PUBLISH — Instagram Business (requires image)
# ═══════════════════════════════════════════════════════════════════════

async def publish_to_instagram(
    ig_account_id: str,
    caption: str,
    image_url: str,
    user_id: str = "default",
) -> Dict[str, Any]:
    """
    Publish a photo to Instagram Business via the Content Publishing API.
    Requires a public image_url.  Two-step: create container → publish.
    """
    # Find the page token for this IG account
    stored = _token_store.get(user_id, {})
    token = None
    for ig in stored.get("instagram_accounts", []):
        if ig.get("id") == ig_account_id:
            token = ig.get("page_access_token")
            break
    if not token:
        # Try user token as fallback
        token = stored.get("user_token")
    if not token:
        return {"success": False, "error": "No token found. Please connect your Instagram account."}

    # Step 1: Create media container
    container_resp = await _graph_post(f"{GRAPH_BASE}/{ig_account_id}/media", data={
        "image_url": image_url,
        "caption": caption,
        "access_token": token,
    })
    container_id = container_resp.get("id")
    if not container_id:
        return {"success": False, "error": container_resp.get("error", {}).get("message", "Container creation failed")}

    # Step 2: Wait briefly for processing, then publish
    await asyncio.sleep(2)  # IG needs a few seconds to process
    publish_resp = await _graph_post(f"{GRAPH_BASE}/{ig_account_id}/media_publish", data={
        "creation_id": container_id,
        "access_token": token,
    })
    media_id = publish_resp.get("id")
    if media_id:
        return {"success": True, "media_id": media_id, "platform": "instagram"}
    return {"success": False, "error": publish_resp.get("error", {}).get("message", "Publish failed")}


# ═══════════════════════════════════════════════════════════════════════
# EMAIL SHARING
# ═══════════════════════════════════════════════════════════════════════

# SMTP config (set via env or config)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASSWORD", "")


async def send_email(
    to_email: str,
    subject: str,
    body_html: str,
    from_name: str = "AI Marketing Center",
    reply_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send marketing email via SMTP.
    Falls back to returning a mailto: link if SMTP is not configured.
    """
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", to_email):
        return {"success": False, "error": "Invalid email address"}

    # If SMTP is configured, send real email
    if SMTP_HOST and SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{SMTP_USER}>"
            msg["To"] = to_email
            if reply_to:
                msg["Reply-To"] = reply_to

            # Plain text fallback
            plain_text = re.sub(r"<[^>]+>", "", body_html)
            msg.attach(MIMEText(plain_text, "plain"))
            msg.attach(MIMEText(body_html, "html"))

            # Run blocking SMTP in executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, _smtp_send, msg)

            return {"success": True, "method": "smtp", "to": to_email}
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            return {"success": False, "error": str(e), "fallback": _mailto_link(to_email, subject, body_html)}
    else:
        # No SMTP configured — return mailto link
        return {
            "success": True,
            "method": "mailto",
            "mailto_link": _mailto_link(to_email, subject, body_html),
            "message": "SMTP not configured. Use the mailto link to open your email client.",
        }


def _smtp_send(msg: MIMEMultipart):
    """Blocking SMTP send (runs in executor)."""
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


def _mailto_link(to: str, subject: str, body_html: str) -> str:
    """Build a mailto: link as fallback."""
    from urllib.parse import quote
    plain_body = re.sub(r"<[^>]+>", "", body_html)[:2000]
    return f"mailto:{to}?subject={quote(subject)}&body={quote(plain_body)}"


# ═══════════════════════════════════════════════════════════════════════
# DISCONNECT
# ═══════════════════════════════════════════════════════════════════════

def disconnect_account(user_id: str = "default") -> Dict[str, Any]:
    """Remove stored tokens."""
    if user_id in _token_store:
        del _token_store[user_id]
        return {"success": True, "message": "Account disconnected"}
    return {"success": True, "message": "No account was connected"}
