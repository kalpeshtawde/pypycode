import pytest
from flask_jwt_extended import create_access_token
from app import db
from app.models import Favorite, Problem, TestCase, User


@pytest.fixture
def problem2(app_ctx):
    """Create a second problem for testing"""
    problem = Problem(
        slug="valid-parentheses",
        title="Valid Parentheses",
        difficulty="medium",
        description="Check if parentheses are valid",
        starter_code="def solution(s):\n    pass",
        examples=[{"input": 's="()"', "output": "True"}],
        tags=["stack", "string"],
    )
    db.session.add(problem)
    db.session.flush()
    
    # Create test case separately
    tc = TestCase(
        problem_id=problem.id,
        serial_number=0,
        function="solution",
        input='"()"',
        expected_output="true",
    )
    db.session.add(tc)
    db.session.commit()
    return problem


class TestListFavorites:
    """Tests for GET /favorites/ endpoint"""

    def test_list_favorites_empty(self, client, user):
        """List favorites returns empty list when user has no favorites"""
        token = create_access_token(identity=user.id)
        response = client.get(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["favorites"] == []

    def test_list_favorites_with_items(self, client, user, problem, problem2):
        """List favorites returns user's favorite problems"""
        fav1 = Favorite(user_id=user.id, problem_id=problem.id)
        fav2 = Favorite(user_id=user.id, problem_id=problem2.id)
        db.session.add_all([fav1, fav2])
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.get(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["favorites"]) == 2
        problem_ids = [f["problem"]["id"] for f in data["favorites"]]
        assert problem.id in problem_ids
        assert problem2.id in problem_ids

    def test_list_favorites_only_own_favorites(self, client, user, second_user, problem):
        """List favorites only returns favorites for the authenticated user"""
        fav1 = Favorite(user_id=user.id, problem_id=problem.id)
        fav2 = Favorite(user_id=second_user.id, problem_id=problem.id)
        db.session.add_all([fav1, fav2])
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.get(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["favorites"]) == 1
        assert data["favorites"][0]["problem"]["id"] == problem.id

    def test_list_favorites_requires_auth(self, client):
        """List favorites requires authentication"""
        response = client.get("/favorites/")
        assert response.status_code == 401

    def test_list_favorites_includes_problem_details(self, client, user, problem):
        """List favorites includes relevant problem details"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.get(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        fav_data = data["favorites"][0]
        assert "id" in fav_data
        assert "createdAt" in fav_data
        prob_data = fav_data["problem"]
        assert prob_data["id"] == problem.id
        assert prob_data["slug"] == problem.slug
        assert prob_data["title"] == problem.title
        assert prob_data["difficulty"] == problem.difficulty
        assert prob_data["tags"] == problem.tags


class TestAddFavorite:
    """Tests for POST /favorites/ endpoint"""

    def test_add_favorite_success(self, client, user, problem):
        """Successfully add a problem to favorites"""
        token = create_access_token(identity=user.id)
        response = client.post(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
            json={"problemId": problem.id},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["problem"]["id"] == problem.id
        assert data["problem"]["title"] == problem.title

        # Verify in database
        fav = Favorite.query.filter_by(user_id=user.id, problem_id=problem.id).first()
        assert fav is not None

    def test_add_favorite_missing_problem_id(self, client, user):
        """Adding favorite without problemId returns error"""
        token = create_access_token(identity=user.id)
        response = client.post(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
            json={},
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "problemid" in data["error"].lower()

    def test_add_favorite_invalid_problem(self, client, user):
        """Adding favorite with non-existent problem returns 404"""
        token = create_access_token(identity=user.id)
        response = client.post(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
            json={"problemId": "non-existent-id"},
        )
        assert response.status_code == 404

    def test_add_duplicate_favorite(self, client, user, problem):
        """Adding same problem twice returns 409 conflict"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.post(
            "/favorites/",
            headers={"Authorization": f"Bearer {token}"},
            json={"problemId": problem.id},
        )
        assert response.status_code == 409
        data = response.get_json()
        assert "already" in data["error"].lower()

    def test_add_favorite_requires_auth(self, client, problem):
        """Adding favorite requires authentication"""
        response = client.post(
            "/favorites/",
            json={"problemId": problem.id},
        )
        assert response.status_code == 401


class TestRemoveFavorite:
    """Tests for DELETE /favorites/<problem_id> endpoint"""

    def test_remove_favorite_success(self, client, user, problem):
        """Successfully remove a problem from favorites"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.delete(
            f"/favorites/{problem.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "removed" in data["message"].lower()

        # Verify removed from database
        fav = Favorite.query.filter_by(user_id=user.id, problem_id=problem.id).first()
        assert fav is None

    def test_remove_nonexistent_favorite(self, client, user, problem):
        """Removing non-existent favorite returns 404"""
        token = create_access_token(identity=user.id)
        response = client.delete(
            f"/favorites/{problem.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    def test_remove_favorite_requires_auth(self, client, problem):
        """Removing favorite requires authentication"""
        response = client.delete(f"/favorites/{problem.id}")
        assert response.status_code == 401

    def test_cannot_remove_other_users_favorite(self, client, user, second_user, problem):
        """Cannot remove another user's favorite"""
        fav = Favorite(user_id=second_user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.delete(
            f"/favorites/{problem.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404  # Not found for this user

        # Verify other user's favorite still exists
        fav = Favorite.query.filter_by(user_id=second_user.id, problem_id=problem.id).first()
        assert fav is not None


class TestCheckFavorite:
    """Tests for GET /favorites/check/<problem_id> endpoint"""

    def test_check_favorite_true(self, client, user, problem):
        """Check favorite returns true when problem is favorited"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        token = create_access_token(identity=user.id)
        response = client.get(
            f"/favorites/check/{problem.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["isFavorite"] is True

    def test_check_favorite_false(self, client, user, problem):
        """Check favorite returns false when problem is not favorited"""
        token = create_access_token(identity=user.id)
        response = client.get(
            f"/favorites/check/{problem.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["isFavorite"] is False

    def test_check_favorite_requires_auth(self, client, problem):
        """Check favorite requires authentication"""
        response = client.get(f"/favorites/check/{problem.id}")
        assert response.status_code == 401


class TestFavoriteModel:
    """Tests for the Favorite model"""

    def test_favorite_model_persists(self, app_ctx, user, problem):
        """Favorite model can be persisted to database"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        saved = Favorite.query.filter_by(user_id=user.id, problem_id=problem.id).first()
        assert saved is not None
        assert saved.user_id == user.id
        assert saved.problem_id == problem.id
        assert saved.created_at is not None

    def test_favorite_unique_constraint(self, app_ctx, user, problem):
        """Cannot create duplicate favorites for same user-problem"""
        fav1 = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav1)
        db.session.commit()

        fav2 = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav2)
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()

    def test_user_cascade_delete_removes_favorites(self, app_ctx, user, problem):
        """Deleting user cascades to remove their favorites"""
        fav = Favorite(user_id=user.id, problem_id=problem.id)
        db.session.add(fav)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        fav = Favorite.query.filter_by(problem_id=problem.id).first()
        assert fav is None

    def test_different_users_can_favorite_same_problem(self, app_ctx, user, second_user, problem):
        """Different users can favorite the same problem"""
        fav1 = Favorite(user_id=user.id, problem_id=problem.id)
        fav2 = Favorite(user_id=second_user.id, problem_id=problem.id)
        db.session.add_all([fav1, fav2])
        db.session.commit()

        assert Favorite.query.filter_by(problem_id=problem.id).count() == 2
