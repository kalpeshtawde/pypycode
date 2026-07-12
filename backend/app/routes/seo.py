from flask import Blueprint, Response
from datetime import datetime
from ..models import Problem

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/sitemap.xml", methods=["GET"])
def sitemap():
    """Generate main sitemap with static pages and problems."""
    base_url = "https://pypycode.com"
    
    urls = []
    
    # Static pages
    static_pages = [
        ("/", "daily", 1.0),
        ("/problems", "daily", 0.9),
        ("/leaderboard", "hourly", 0.8),
        ("/pricing", "weekly", 0.7),
        ("/about", "monthly", 0.6),
        ("/contact", "monthly", 0.5),
    ]
    
    for path, changefreq, priority in static_pages:
        urls.append({
            "loc": f"{base_url}{path}",
            "changefreq": changefreq,
            "priority": priority,
        })
    
    # Problems (all problems are included)
    problems = Problem.query.all()
    for problem in problems:
        urls.append({
            "loc": f"{base_url}/problems/{problem.slug}",
            "lastmod": problem.created_at.isoformat() if problem.created_at else None,
            "changefreq": "weekly",
            "priority": 0.8,
        })
    
    xml = _generate_sitemap_xml(urls)
    return Response(xml, mimetype="application/xml")


@seo_bp.route("/sitemap-problems.xml", methods=["GET"])
def sitemap_problems():
    """Generate problems-only sitemap for large problem sets."""
    base_url = "https://pypycode.com"
    
    urls = []
    problems = Problem.query.all()
    
    for problem in problems:
        urls.append({
            "loc": f"{base_url}/problems/{problem.slug}",
            "lastmod": problem.created_at.isoformat() if problem.created_at else None,
            "changefreq": "weekly",
            "priority": 0.8,
        })
    
    xml = _generate_sitemap_xml(urls)
    return Response(xml, mimetype="application/xml")


def _generate_sitemap_xml(urls):
    """Generate XML sitemap from URL list."""
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    
    for url in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{_escape_xml(url['loc'])}</loc>")
        
        if url.get("lastmod"):
            xml_lines.append(f"    <lastmod>{url['lastmod']}</lastmod>")
        
        if url.get("changefreq"):
            xml_lines.append(f"    <changefreq>{url['changefreq']}</changefreq>")
        
        if url.get("priority") is not None:
            xml_lines.append(f"    <priority>{url['priority']}</priority>")
        
        xml_lines.append("  </url>")
    
    xml_lines.append("</urlset>")
    return "\n".join(xml_lines)


def _escape_xml(text):
    """Escape XML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
