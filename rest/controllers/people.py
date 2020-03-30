from flask import jsonify, Blueprint, request, abort
from rest.models.person import Person

people = Blueprint('person', __name__)


@people.route('/people', methods=['GET'])
def list_people():
    people = Person.list_people()
    serialized_people = []
    if people:
        for person in people:
            serialized_people.append(person.serialized_person())
        return jsonify(serialized_people)


@people.route('/people', methods=['POST'])
def add_person():
    name, last_name = request.json.get('name'), request.json.get('last_name')
    if name and last_name:
        person = Person(name, last_name)
        person.add_person()
        return jsonify(person.serialized_person())
    else:
        return abort(400)
