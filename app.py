from flask import Flask ,jsonify, abort, request
import json
from flask_sqlalchemy import SQLAlchemy

appli = Flask(__name__)
appli.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:babythiat11@localhost/dbase'
db = SQLAlchemy(appli)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    adress = db.Column(db.String(50))
    hobbies = db.Column(db.String(20))
    numberPhone = db.Column(db.String(20))

    def __init__(self, name, surname, adress,hobbies,numberPhone):
        self.name = name
        self.surname = surname
        self.adress = adress
        self.hobbies = hobbies
        self.numberPhone = numberPhone

@appli.route('/std/', methods = ['GET'])
def index():
    data = json.load(open("dbase.json"))
    print(data['tables']['Student'])
    student = json.dumps(data['tables']['Student'])
    print(student)
    # return 'test'
    # request.get_json()
    return jsonify({'student': student})

@appli.route('/stdi/<string:column>/')
def get_std(column):
    chaine = column[1:-1]
    colu = str(chaine).split('=')
    data = json.load(open("dbase.json"))
    students = data['tables']['Student']
    print(colu)
    for student in students:
        if(student[colu[0]] == colu[1]):
            return jsonify({'student': student})
    return 'student not found'


@appli.route('/std/<string:column>')
def get_stdBycol(column):
    print(column)
    chaine = column[1:-1]
    column = chaine.split(',')
    
    print(column)
    students = []
    st = {}
    data = json.load(open("dbase.json"))
    allStudents = data['tables']['Student']
    for student in allStudents:
        for col in column:
            print('ccc ', col)
            if col in student:
                st[col] = student[col]
        students.append(st)
    return jsonify({'student': students})


@appli.route('/std/', methods = ['POST'])
def create_std():
	if not request.json or not 'name' in request.json:
 		abort(400) 
	Student = Student(request.json.name, request.json.get('surname', ''), request.json.get('adress',''), request.json.get('hobbies',''), request.json.get('numberPhone',''))
	db.session.add(Student)
	db.session.commit()
	return jsonify( { 'Student': Student } ), 201

@appli.route('/std/<int:id>', methods = ['DELETE'])
def delete_std(id):
    db.session.delete(Users.query.get(id))
    db.session.commit()
    return jsonify( { 'result': True } )

@appli.route('/std/<int:id>', methods = ['PUT'])
def update_std(id):
    std = std.query.get(id)
    std.name = request.json.get('name', std.name)
    std.surname = request.json.get('surname',std.name)
    std.adress = request.json.get('adress', std.adress)
    std.hobbies = request.json.get('hobbies', std.hobbies)
    std.numberPhone = request.json.get('adress', std.numberPhone)
    db.session.commit()
    return jsonify( { 'std': std } )

if __name__ == '__main__':
    appli.run(debug = True, host = 'localhost', port = 8889)
