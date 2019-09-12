from sevilla.services import NotesService
from tests import BaseTest, utils
from tests.test_notes_service import VALID_ID


class TestFrontend(BaseTest):
    def setUp(self):
        super().setUp()
        self.client.post(
            "/login", data={"password": self.app.config["SEVILLA_PASSWORD"]}
        )

    def test_create_note(self):
        rv = self.client.post(
            "/notes/" + VALID_ID + "?timestamp=1",
            data="Hello, world!",
            headers={"Content-type": "text/plain"},
        )
        self.assertEqual(rv.status_code, 200)

        note = NotesService.get_note(VALID_ID)
        self.assertEqual(note.contents, "Hello, world!")

    def test_update_note(self):
        rv = self.client.post(
            "/notes/" + VALID_ID + "?timestamp=1000",
            data="foo",
            headers={"Content-type": "text/plain"},
        )
        self.assertEqual(rv.status_code, 200)

        rv = self.client.post(
            "/notes/" + VALID_ID + "?timestamp=2000",
            data="bar",
            headers={"Content-type": "text/plain"},
        )
        self.assertEqual(rv.status_code, 200)

        note = NotesService.get_note(VALID_ID)
        self.assertEqual(note.contents, "bar")
        self.assertEqual(utils.timestamp_seconds(note.modified), 2)

    def test_try_update_note(self):
        rv = self.client.post(
            "/notes/" + VALID_ID + "?timestamp=2000",
            data="foo",
            headers={"Content-type": "text/plain"},
        )
        self.assertEqual(rv.status_code, 200)

        rv = self.client.post(
            "/notes/" + VALID_ID + "?timestamp=1000",
            data="bar",
            headers={"Content-type": "text/plain"},
        )
        self.assertEqual(rv.status_code, 200)

        note = NotesService.get_note(VALID_ID)
        self.assertEqual(note.contents, "foo")
        self.assertEqual(utils.timestamp_seconds(note.modified), 2)

    def test_hide_note(self):
        NotesService.upsert_note(VALID_ID, "hello", utils.now())
        rv = self.client.post(
            "/notes/" + VALID_ID + "/hide", data={"page": 1, "pageSize": 10}
        )

        self.assertEqual(rv.status_code, 302)
        self.assertTrue(NotesService.get_note(VALID_ID).hidden)

    def test_view_index(self):
        with self.client.get("/") as rv:
            self.assertEqual(rv.status_code, 200)

    def test_view_notes(self):
        with self.client.get("/notes") as rv:
            self.assertEqual(rv.status_code, 200)

    def test_view_note(self):
        NotesService.upsert_note(VALID_ID, "hello", utils.now())
        with self.client.get("/notes/" + VALID_ID) as rv:
            self.assertEqual(rv.status_code, 200)


class TestFrontendNoLogin(BaseTest):
    def test_view_login(self):
        with self.client.get("/login") as rv:
            self.assertEqual(rv.status_code, 200)

    def test_login_fail(self):
        rv = self.client.post("/login")
        self.assertEqual(rv.status_code, 401)

        rv = self.client.post("/login", data={"password": "foobar"})
        self.assertEqual(rv.status_code, 401)

    def test_upsert_note_unauthorized(self):
        rv = self.client.post("/notes/" + VALID_ID)
        self.assertEqual(rv.status_code, 401)

    def test_hide_note_unauthorized(self):
        rv = self.client.post("/notes/" + VALID_ID + "/hide")
        self.assertEqual(rv.status_code, 401)

    def test_view_index_redirect(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 302)

    def test_view_notes_redirect(self):
        rv = self.client.get("/notes")
        self.assertEqual(rv.status_code, 302)

    def test_view_note_redirect(self):
        rv = self.client.get("/notes/" + VALID_ID)
        self.assertEqual(rv.status_code, 302)