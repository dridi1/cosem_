import os
import tempfile
import unittest
from pathlib import Path


TEST_DB_PATH = Path(tempfile.gettempdir()) / "cosem_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["SECRET_KEY"] = "test-secret-key"

from api import index as app_module


app = app_module.app
db = app_module.db
User = app_module.User
Polygon = app_module.Polygon
bcrypt = app_module.bcrypt


class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        password_hash = bcrypt.generate_password_hash("password123").decode("utf-8")
        user = User(username="tester", email="tester@example.com", password=password_hash)
        db.session.add(user)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.engine.dispose()

        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()

    def login(self, route="/login"):
        return self.client.post(
            route,
            data={"username": "tester", "password": "password123", "remember-me": "on"},
            follow_redirects=False,
        )

    def test_private_dashboard_requires_login(self):
        response = self.client.get("/private_dashboard")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_save_polygon_requires_login(self):
        response = self.client.post("/save_polygon", json={"coordinates": [[1, 1], [2, 2], [3, 3]]})

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_logged_in_user_can_save_polygon(self):
        self.login()

        response = self.client.post("/save_polygon", json={"coordinates": [[35.1, 9.8], [35.2, 9.9], [35.3, 9.7]]})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")
        self.assertEqual(Polygon.query.count(), 1)

    def test_invalid_polygon_payload_is_rejected(self):
        self.login()

        response = self.client.post("/save_polygon", json={"coordinates": "not-a-polygon"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["status"], "error")
        self.assertEqual(Polygon.query.count(), 0)

    def test_contact_fr_redirects_to_french_thank_you_page(self):
        response = self.client.post(
            "/contact_fr",
            data={
                "name": "Test User",
                "email": "contact@example.com",
                "subject": "Question",
                "message": "Hello from the test suite.",
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/merci", response.headers["Location"])

    def test_home_pages_render_localized_navigation(self):
        home_response = self.client.get("/en")
        home_fr_response = self.client.get("/")

        self.assertEqual(home_response.status_code, 200)
        home_html = home_response.get_data(as_text=True)
        self.assertIn("About", home_html)
        self.assertIn("Public Dashboard", home_html)
        self.assertIn("French", home_html)

        self.assertEqual(home_fr_response.status_code, 200)
        home_fr_html = home_fr_response.get_data(as_text=True)
        self.assertIn("À propos", home_fr_html)
        self.assertIn("Tableau de bord public", home_fr_html)
        self.assertIn("Français", home_fr_html)

    def test_analyze_templates_use_correct_routes(self):
        self.login()

        analyze_response = self.client.get("/analyze")
        analyze_fr_response = self.client.get("/analyse_fr")

        self.assertEqual(analyze_response.status_code, 200)
        self.assertIn(b'data-results-url="/yourdash"', analyze_response.data)
        self.assertIn(b'href="/logout"', analyze_response.data)

        self.assertEqual(analyze_fr_response.status_code, 200)
        self.assertIn(b'data-results-url="/yourdash_fr"', analyze_fr_response.data)
        self.assertIn(b'href="/logout_fr"', analyze_fr_response.data)
        self.assertIn("Analyse".encode("utf-8"), analyze_fr_response.data)
        self.assertIn("Déconnexion".encode("utf-8"), analyze_fr_response.data)

    def test_private_dashboard_templates_use_localized_navigation(self):
        self.login()

        dashboard_response = self.client.get("/private_dashboard")
        dashboard_fr_response = self.client.get("/private_dashboard_fr")

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertIn(b"Dashboard", dashboard_response.data)
        self.assertIn(b"Analyze", dashboard_response.data)
        self.assertIn(b"Sign out", dashboard_response.data)

        self.assertEqual(dashboard_fr_response.status_code, 200)
        self.assertIn("Tableau de bord".encode("utf-8"), dashboard_fr_response.data)
        self.assertIn("Analyse".encode("utf-8"), dashboard_fr_response.data)
        self.assertIn("Déconnexion".encode("utf-8"), dashboard_fr_response.data)


if __name__ == "__main__":
    unittest.main()
