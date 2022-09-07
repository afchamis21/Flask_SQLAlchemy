from flask import Flask, request
from flask_restful import Resource, Api

from models import People, Activities

app = Flask(__name__)
api = Api(app)


class Person(Resource):
    @staticmethod
    def get(name):
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

    @staticmethod
    def put(name):
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

    @staticmethod
    def delete(name):
        person = People.query.filter_by(name=name).first()
        person.delete()
        return {'status': 'success', 'message': 'person deleted successfully'}


class ListPeople(Resource):
    @staticmethod
    def get():
        people = People.query.all()
        response = [{
            'name': person.name,
            'age': person.age,
            'id': person.id
        } for person in people]

        return response

    @staticmethod
    def post():
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
    @staticmethod
    def get():
        activities = Activities.query.all()
        response = [
            {
                'person': activity.person.name,
                'name': activity.name,
                'id': activity.id
            } for activity in activities
        ]
        return response

    @staticmethod
    def post():
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