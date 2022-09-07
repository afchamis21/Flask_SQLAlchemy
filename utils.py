from models import People


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


if __name__ == '__main__':
    insert_person()
