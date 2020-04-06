from flask import jsonify, Blueprint, request, Response
from rest.models.person import Person

people = Blueprint('person', __name__)


@people.route('/people', methods=['GET'])
def list_people():
    people = Person.list_people()
    serialized_people = []
    if people:
        for person in people:
            serialized_people.append(person.serialized_person())
        return jsonify(serialized_people), 200
    else:
        return Response(status=204)


@people.route('/people', methods=['POST'])
def add_person():
    name, last_name = request.json.get('name'), request.json.get('last_name')
    if name and last_name:
        person = Person(name, last_name)
        person.add_person()
        return jsonify(person.serialized_person()), 201
    else:
        return jsonify({"message": "Bad request"}), 400


@people.route('/people/<int:id>', methods=['PUT'])
def fully_update_person(id):
    person = Person.query.get_or_404(id)
    name, last_name = request.json.get('name'), request.json.get('last_name')
    if name and last_name:
        person.update_person(name, last_name)
        return jsonify(person.serialized_person()), 200
    else:
        return jsonify({"message": "Bad request"}), 400


@people.route('/people/<int:id>', methods=['PATCH'])
def partially_update_person(id):
    updated = False
    person = Person.query.get_or_404(id)
    name, last_name = request.json.get('name'), request.json.get('last_name')
    if name:
        person.update_name(name)
        updated = True
    if last_name:
        person.update_last_name(last_name)
        updated = True
    if updated:
        return jsonify(person.serialized_person()), 200
    else:
        return jsonify({"message": "Bad request"}), 400
