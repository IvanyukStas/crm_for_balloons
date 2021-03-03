from datetime import datetime
import unittest
from crm import db, app
from crm.models import User, Client, ClientFamily

class UserModeCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()


    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()


    def test_password_hashing(self):
        u = User(user='Susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dfsdsf'))
        self.assertTrue(u.check_password('cat'))

if __name__ == '__main__':
    unittest.main(verbosity=2)

