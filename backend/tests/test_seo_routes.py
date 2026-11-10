from datetime import datetime, timedelta

from app import db


def test_sitemap_lists_static_pages_and_problems(client, problem):
    res = client.get("/sitemap.xml")
    assert res.status_code == 200
    assert res.mimetype == "application/xml"
    body = res.get_data(as_text=True)
    assert "<loc>https://pypycode.com/pricing</loc>" in body
    assert f"<loc>https://pypycode.com/problems/{problem.slug}</loc>" in body


def test_sitemap_problem_lastmod_prefers_updated_at(client, problem):
    problem.created_at = datetime(2024, 1, 1)
    problem.updated_at = datetime(2025, 6, 15, 12, 30)
    db.session.commit()

    body = client.get("/sitemap-problems.xml").get_data(as_text=True)
    assert "<lastmod>2025-06-15</lastmod>" in body
    assert "<lastmod>2024-01-01</lastmod>" not in body


def test_sitemap_problem_lastmod_falls_back_to_created_at(client, problem):
    problem.created_at = datetime(2024, 3, 9)
    problem.updated_at = None
    db.session.commit()

    body = client.get("/sitemap-problems.xml").get_data(as_text=True)
    assert "<lastmod>2024-03-09</lastmod>" in body
