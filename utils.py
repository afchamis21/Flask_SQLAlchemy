from models import People, Users


def insert_person():
    person = People(name='Andre', age=21)
    person.save()


def select_person():
    # person = People.query.all()
    person = People.query.filter_by(name='Andre').all()
    print(person)
    for p in person:
        print(p.name, p.age)


def edit_person():
    person = People.query.filter_by(name='Andre').first()
    person.age = 25
    person.save()


def delete_person():
    person = People.query.filter_by(name='Andre').first()
    person.delete()


def insert_user(login, password):
    user = Users(login=login, password=password)
    user.save()


def lookup_users():
    users = Users.query.all()
    print(users)


if __name__ == '__main__':
    insert_user('andre', '12345')
    insert_user('chamis', '12345')
    insert_user('malu', '12345')

    lookup_users()
