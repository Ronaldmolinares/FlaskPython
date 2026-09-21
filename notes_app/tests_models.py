import unittest

from app import create_app
from models import Note, db


class NotesTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def test_create_note(self):
        with self.app.app_context():
            note_db = Note(title="Test Note", content="This is a test note.", user_id=1)
            db.session.add(note_db)
            db.session.commit()

            note = Note.query.first()

            self.assertEqual(note.title, "Test Note")
            self.assertEqual(note.content, "This is a test note.")
            self.assertEqual(note.user_id, 1)
