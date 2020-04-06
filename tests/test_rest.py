import unittest
from rest import create_app, db
from rest.config import Config
from rest.models.person import Person
import json


class TestRest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        self.app.app_context().push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_list_people(self):
        person = Person('Miguel', 'Ramos')
        db.session.add(person)
        db.session.commit()
        response = self.app.test_client().get('/people')
        self.assertEqual(response.json, [{'id': '1', 'last_name': 'Ramos', 'name': 'Miguel'}])
        self.assertEqual(response.status_code, 200)

    def test_list_people_exception(self):
        response = self.app.test_client().get('/people')
        self.assertEqual(response.status_code, 204)

    def test_add_person(self):
        response = self.app.test_client().post('/people', headers={"Content-Type": "application/json"},
                                               data=json.dumps({"name": "Foo", "last_name": "Bar"}))
        self.assertEqual(response.json, {'id': '1', 'last_name': 'Bar', 'name': 'Foo'})
        self.assertEqual(response.status_code, 201)

    def test_add_person_exception(self):
        response = self.app.test_client().post('/people', headers={"Content-Type": "application/json"},
                                               data=json.dumps({"name": "Foo"}))
        self.assertEqual(response.json, {"message": "Bad request"})
        self.assertEqual(response.status_code, 400)

    def test_fully_update_person(self):
        person = Person('Miguel', 'Ramos')
        db.session.add(person)
        db.session.commit()
        response = self.app.test_client().put('/people/1', headers={"Content-Type": "application/json"},
                                              data=json.dumps({"name": "Rodrigo", "last_name": "Amarente"}))
        self.assertEqual(response.json, {'id': '1', 'last_name': 'Amarente', 'name': 'Rodrigo'})
        self.assertEqual(response.status_code, 200)

    def test_fully_update_person_exception(self):
        person = Person('Miguel', 'Ramos')
        db.session.add(person)
        db.session.commit()
        response = self.app.test_client().put('/people/1', headers={"Content-Type": "application/json"},
                                              data=json.dumps({"name": "Rodrigo"}))
        self.assertEqual(response.json, {"message": "Bad request"})
        self.assertEqual(response.status_code, 400)

    def test_partially_update_person(self):
        person = Person('Rodrigo', 'Amarante')
        db.session.add(person)
        db.session.commit()
        response = self.app.test_client().patch('/people/1', headers={"Content-Type": "application/json"},
                                                data=json.dumps({"name": "Marcelo", "last_name": "Camelo"}))
        self.assertEqual(response.json, {'id': '1', 'last_name': 'Camelo', 'name': 'Marcelo'})
        self.assertEqual(response.status_code, 200)

    def test_partially_update_person_exception(self):
        person = Person('Rodrigo', 'Amarante')
        db.session.add(person)
        db.session.commit()
        response = self.app.test_client().patch('/people/1', headers={"Content-Type": "application/json"},
                                                data=json.dumps({"data": "dummy"}))
        self.assertEqual(response.json, {"message": "Bad request"})
        self.assertEqual(response.status_code, 400)
