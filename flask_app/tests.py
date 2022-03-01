import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/index")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>Use this site to maintain and organize your notes.</h2>' in response.text, True)

    def test_notes(self):
        response = requests.get("http://127.0.0.1:5000/notes")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Title' and 'Date' in response.text, True)

    def test_note(self):
        response = requests.get("http://127.0.0.1:5000/note/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Second db note' in response.text, True)

    def test_new(self):
        response = requests.get("http://127.0.0.1:5000/notes/new")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form action="new" method="post">' in response.text, True)

    def test_delete(self):
        response = requests.get('http://127.0.0.1:5000/notes/delete')
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

if __name__ == " __main__":
    unittest.main()
