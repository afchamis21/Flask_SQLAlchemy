from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

from models import People, Activities, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


# USERS = {
#     'andre': '321',
#     'chamis': '456'
# }
#
#
# @auth.verify_password
# def verification(login, password):
#     if not (login, password):
#         return False
#
#     return USERS.get(login) == password

@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False

    return Users.query.filter_by(login=login, password=password).first()


class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                'nome': person.name,
                'age': person.age,
                'id': person.id
            }

        except AttributeError:
            response = {
                'status': 'error',
                'message': 'person not registered'
            }

        return response

    @auth.login_required
    def put(self, name):
        person = People.query.filter_by(name=name).first()

        try:
            data = request.json
            if data['name']:
                person.name = data['name']

            if data['age']:
                person.age = data['age']

            person.save()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'person not registered'
            }
        return response

    @auth.login_required
    def delete(self, name):
        person = People.query.filter_by(name=name).first()
        person.delete()
        return {'status': 'success', 'message': 'person deleted successfully'}


class ListPeople(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [{
            'name': person.name,
            'age': person.age,
            'id': person.id
        } for person in people]

        return response

    @auth.login_required
    def post(self):
        data = request.json
        person = People(name=data['name'], age=data['age'])
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response


class ListActivities(Resource):
    @auth.login_required
    def get(self):
        activities = Activities.query.all()
        response = [
            {
                'person': activity.person.name,
                'name': activity.name,
                'id': activity.id
            } for activity in activities
        ]
        return response

    @auth.login_required
    def post(self):
        data = request.json
        person = People.query.filter_by(name=data['person']).first()
        activity = Activities(name=data['name'], person=person)
        activity.save()
        response = {
            'person': activity.person.name,
            'name': activity.name,
            'id': activity.id
        }
        return response


api.add_resource(ListPeople, '/person')
api.add_resource(Person, '/person/<string:name>')
api.add_resource(ListActivities, '/activities')


if __name__ == '__main__':
    app.run(debug=True)
