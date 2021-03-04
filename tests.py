from config import Config
import unittest
from crm import db
from crm.models import User, Client
from crm import create_app
from datetime import datetime

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'



class UserModeCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(user='Susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dfsdsf'))
        self.assertTrue(u.check_password('cat'))


    def test_client_add(self):
        new_client = Client(client_name='Stas', client_phone=123, client_birthday=datetime.today().date())
        db.session.add(new_client)
        db.session.commit()
        new_client = Client.query.filter_by(client_name='Stas').first()
        print(type(datetime.today().date()), type(new_client.client_birthday.date()))
        assert (new_client.client_name == 'Stas')
        assert (new_client.client_phone == 123)
        #assert (new_client.client_birthday == datetime.today().date())
        assert type(new_client.client_birthday.date()) == 'date'

if __name__ == '__main__':
    unittest.main(verbosity=2)

