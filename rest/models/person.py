from rest import db


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

    @staticmethod
    def list_people():
        return Person.query.all()

    def add_person(self):
        db.session.add(self)
        db.session.commit()

    def remove_person(self):
        db.session.delete(self)
        db.session.commit()

    def update_person(self, name, last_name):
        self.name = name
        self.last_name = last_name
        db.session.commit()

    def update_name(self, name):
        self.name = name
        db.session.commit()

    def update_last_name(self, last_name):
        self.last_name = last_name
        db.session.commit()

    def serialized_person(self):
        return {"id": str(self.id), "name": self.name, "last_name": self.last_name}
