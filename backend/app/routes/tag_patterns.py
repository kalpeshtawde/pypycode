from flask import Blueprint, jsonify
from app.models import TagPattern

tag_patterns_bp = Blueprint("tag_patterns", __name__)


@tag_patterns_bp.get("/")
def list_tag_patterns():
    """Return a map of tag -> pattern for all tags that have a saved pattern.

    Public, read-only endpoint. Patterns are maintained directly in the
    database (no admin UI yet), so this just exposes whatever is stored.
    """
    rows = TagPattern.query.all()
    return jsonify({row.tag: row.pattern for row in rows})
