from application import create_app
from application.models import db
import unittest

class TestCostumers(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_costumer(self):
        costumer_payload = {
            "name": "John Doe",
           	"phone": "3125550305",
            "email": "jd@email.com",
            "password": "123"
        }

        response = self.app.post('/costumers/', json=costumer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")