"""
AI Classifier Service — The "Automated Intelligence" (Auto-Tagging)
═══════════════════════════════════════════════════════════════════════
When you import a CSV or create content, this service:
  1. Classifies rows into categories using a Keyword Mapping Engine.
  2. Extracts entities (names, emails, amounts) using Regex Patterns.
  3. Detects sentiment polarity using a Lexicon-based scorer.

No external API calls — runs entirely offline.
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ═════════════════════════════════════════════════════════════════════════
# 1. CATEGORY CLASSIFICATION — Keyword Mapping Engine
# ═════════════════════════════════════════════════════════════════════════

# Each category maps to a list of trigger keywords (case-insensitive)
CATEGORY_MAP: Dict[str, List[str]] = {
    "Software & Cloud": [
        "aws", "gcp", "azure", "saas", "cloud", "software", "api",
        "hosting", "server", "domain", "ssl", "cdn", "heroku",
        "vercel", "netlify", "digital ocean", "firebase",
    ],
    "Advertising": [
        "google ads", "facebook ads", "instagram ads", "tiktok ads",
        "linkedin ads", "ad spend", "ppc", "cpc", "cpm", "campaign spend",
        "meta ads", "twitter ads", "promoted", "boost", "paid media",
    ],
    "Design & Creative": [
        "canva", "figma", "adobe", "photoshop", "illustrator", "design",
        "creative", "graphic", "logo", "branding", "video editing",
        "premiere", "after effects",
    ],
    "Content & SEO": [
        "seo", "blog", "content writing", "copywriting", "keyword",
        "backlink", "semrush", "ahrefs", "moz", "surfer", "article",
        "newsletter", "email marketing", "mailchimp", "sendgrid",
    ],
    "Analytics & Tools": [
        "analytics", "google analytics", "hotjar", "mixpanel", "amplitude",
        "tableau", "data studio", "looker", "tracking", "pixel",
    ],
    "Social Media": [
        "instagram", "linkedin", "twitter", "tiktok", "youtube", "facebook",
        "pinterest", "reddit", "social media", "influencer", "ugc",
        "scheduling", "buffer", "hootsuite", "sprout",
    ],
    "Salary & Freelance": [
        "salary", "payroll", "freelance", "contractor", "wages",
        "commission", "bonus", "stipend", "consultant",
    ],
    "Office & Operations": [
        "rent", "office", "utilities", "electricity", "internet",
        "phone", "supplies", "furniture", "equipment", "maintenance",
    ],
    "Subscription": [
        "subscription", "monthly plan", "annual plan", "license",
        "premium", "pro plan", "enterprise plan",
    ],
    "Revenue": [
        "payment received", "invoice paid", "revenue", "income",
        "sales", "received from", "client payment", "deposit",
    ],
}

# Pre-compile patterns for speed
_CATEGORY_PATTERNS: List[Tuple[str, re.Pattern]] = []
for category, keywords in CATEGORY_MAP.items():
    # Build a single OR pattern for the whole category
    escaped = [re.escape(kw) for kw in keywords]
    pattern = re.compile(r"\b(?:" + "|".join(escaped) + r")\b", re.IGNORECASE)
    _CATEGORY_PATTERNS.append((category, pattern))


def classify_category(text: str) -> str:
    """
    Classify a text string (transaction description, content title, etc.)
    into a marketing/business category.
    Returns the category name or 'Uncategorized'.
    """
    if not text:
        return "Uncategorized"

    # Score each category by number of keyword hits
    best_cat = "Uncategorized"
    best_score = 0

    for category, pattern in _CATEGORY_PATTERNS:
        hits = len(pattern.findall(text))
        if hits > best_score:
            best_score = hits
            best_cat = category

    return best_cat


def classify_batch(rows: List[Dict[str, Any]], text_field: str = "description") -> List[Dict[str, Any]]:
    """
    Classify a batch of rows. Adds 'ai_category' to each dict.
    """
    for row in rows:
        description = str(row.get(text_field, ""))
        row["ai_category"] = classify_category(description)
    return rows


# ═════════════════════════════════════════════════════════════════════════
# 2. ENTITY EXTRACTION — Regex Named-Entity Recognition
# ═════════════════════════════════════════════════════════════════════════

# Person name: "Payment from John Doe", "Invoice to Jane Smith-Lee"
_PERSON_RE = re.compile(
    r"(?:from|to|by|for|client|customer|vendor|paid)\s+"
    r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)*))",
)

# Email
_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Currency amounts: $1,234.56 or 1234.56 or USD 500
_AMOUNT_RE = re.compile(
    r"(?:USD?\s*|£\s*|€\s*|\$\s*)"
    r"(\d[\d,]*(?:\.\d{1,2})?)"
    r"|(\d[\d,]*(?:\.\d{1,2})?)\s*(?:USD|GBP|EUR)",
    re.IGNORECASE,
)

# Date-like: 2024-01-15, 01/15/2024, Jan 15 2024
_DATE_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}"
    r"|\d{1,2}/\d{1,2}/\d{2,4}"
    r"|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}",
    re.IGNORECASE,
)

# Invoice / reference numbers: INV-1234, REF#5678
_REF_RE = re.compile(r"(?:INV|REF|PO|SO|TXN)[#\-]?\s*\d{3,}", re.IGNORECASE)


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract structured entities from free text.
    Returns dict with: person, email, amount, date, reference
    """
    entities: Dict[str, Any] = {}

    if not text:
        return entities

    # Person
    m = _PERSON_RE.search(text)
    if m:
        entities["person"] = m.group(1).strip()

    # Email
    m = _EMAIL_RE.search(text)
    if m:
        entities["email"] = m.group(0)

    # Amount
    m = _AMOUNT_RE.search(text)
    if m:
        raw = (m.group(1) or m.group(2) or "").replace(",", "")
        try:
            entities["amount"] = float(raw)
        except ValueError:
            pass

    # Date
    m = _DATE_RE.search(text)
    if m:
        entities["date"] = m.group(0)

    # Reference
    m = _REF_RE.search(text)
    if m:
        entities["reference"] = m.group(0)

    return entities


def extract_entities_batch(rows: List[Dict[str, Any]], text_field: str = "description") -> List[Dict[str, Any]]:
    """
    Extract entities from a batch of rows.
    Adds 'ai_entities' dict to each row.
    """
    for row in rows:
        description = str(row.get(text_field, ""))
        row["ai_entities"] = extract_entities(description)
        # Promote person to customer field if not already set
        if "person" in row["ai_entities"] and not row.get("customer"):
            row["customer"] = row["ai_entities"]["person"]
    return rows


# ═════════════════════════════════════════════════════════════════════════
# 3. SENTIMENT ANALYSIS — Lexicon-Based Scorer
# ═════════════════════════════════════════════════════════════════════════

_POSITIVE_WORDS = {
    "great", "excellent", "amazing", "love", "good", "best", "wonderful",
    "fantastic", "awesome", "perfect", "happy", "outstanding", "brilliant",
    "impressive", "superb", "delightful", "growth", "increase", "profit",
    "success", "gain", "improve", "boost", "win", "thriving", "positive",
}

_NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "hate", "worst", "horrible", "poor",
    "disappointed", "fail", "failed", "loss", "decline", "decrease",
    "drop", "problem", "issue", "complaint", "angry", "frustrating",
    "expensive", "overpriced", "slow", "broken", "bug", "error", "negative",
}


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Simple lexicon-based sentiment analysis.
    Returns: { score: float (-1 to 1), label: str, confidence: float }
    """
    if not text:
        return {"score": 0.0, "label": "neutral", "confidence": 0.5}

    words = set(re.findall(r"\w+", text.lower()))
    pos = len(words & _POSITIVE_WORDS)
    neg = len(words & _NEGATIVE_WORDS)
    total = pos + neg

    if total == 0:
        return {"score": 0.0, "label": "neutral", "confidence": 0.5}

    score = round((pos - neg) / total, 2)
    confidence = round(min(total / 5, 1.0), 2)  # More words → higher confidence

    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {"score": score, "label": label, "confidence": confidence}


# ═════════════════════════════════════════════════════════════════════════
# 4. FULL PIPELINE — Classify + Extract + Sentiment in one call
# ═════════════════════════════════════════════════════════════════════════

def process_row(row: Dict[str, Any], text_field: str = "description") -> Dict[str, Any]:
    """
    Run the full AI classification pipeline on a single row.
    Adds: ai_category, ai_entities, ai_sentiment
    """
    text = str(row.get(text_field, ""))
    row["ai_category"] = classify_category(text)
    row["ai_entities"] = extract_entities(text)
    row["ai_sentiment"] = analyze_sentiment(text)
    if "person" in row["ai_entities"] and not row.get("customer"):
        row["customer"] = row["ai_entities"]["person"]
    return row


def process_batch(rows: List[Dict[str, Any]], text_field: str = "description") -> List[Dict[str, Any]]:
    """
    Run the full pipeline on a batch of rows.
    """
    return [process_row(row, text_field) for row in rows]


# ═════════════════════════════════════════════════════════════════════════
# 5. CONTENT CLASSIFIER — for marketing content tagging
# ═════════════════════════════════════════════════════════════════════════

CONTENT_TYPE_MAP: Dict[str, List[str]] = {
    "educational": ["how to", "tutorial", "guide", "tips", "learn", "explained", "101"],
    "promotional": ["sale", "discount", "offer", "buy now", "limited time", "deal", "promo"],
    "engagement": ["poll", "question", "what do you think", "share your", "tag a friend"],
    "inspirational": ["motivat", "inspir", "dream", "believe", "success story", "journey"],
    "behind-the-scenes": ["behind the scenes", "bts", "making of", "day in the life", "team"],
    "user-generated": ["ugc", "user generated", "customer spotlight", "testimonial", "review"],
    "announcement": ["announcing", "new launch", "coming soon", "introducing", "we're excited"],
    "seasonal": ["holiday", "christmas", "new year", "summer", "winter", "spring", "fall"],
}

_CONTENT_PATTERNS: List[Tuple[str, re.Pattern]] = []
for ctype, kws in CONTENT_TYPE_MAP.items():
    pat = re.compile(r"(?:" + "|".join(re.escape(k) for k in kws) + r")", re.IGNORECASE)
    _CONTENT_PATTERNS.append((ctype, pat))


def classify_content_type(text: str) -> str:
    """Classify marketing content into a content-type bucket."""
    best = "general"
    best_score = 0
    for ctype, pat in _CONTENT_PATTERNS:
        hits = len(pat.findall(text))
        if hits > best_score:
            best_score = hits
            best = ctype
    return best
