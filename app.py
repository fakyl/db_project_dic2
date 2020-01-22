from flask import Flask ,jsonify, abort, request
import json
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db


appli = Flask(__name__)
# appli.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:geekenthusiast@localhost/dbase'
# db = SQLAlchemy(appli)



# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     surname = db.Column(db.String(20))
#     adress = db.Column(db.String(50))
#     hobbies = db.Column(db.String(20))
#     numberPhone = db.Column(db.String(20))

#     def __init__(self, name, surname, adress,hobbies,numberPhone):
#         self.name = name
#         self.surname = surname
#         self.adress = adress
#         self.hobbies = hobbies
#         self.numberPhone = numberPhone

#     def saveData(self, Student):
#         self.connection.execute("""INSERT INTO Student(name, surname, address, numberPhone) VALUES('{Student.name}', '{Student.surname}', '{Student.address}', '{Student.hobbies}', '{Student.numberPhone}')""")



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
    data = json.load(open("db.json"))
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
    db.session.delete(Student.query.get(id))
    db.session.commit()
    return jsonify( { 'result': True } )

@appli.route('/std/<int:id>', methods = ['PUT'])
def update_std(id):
    std = std.query.get(id)
    std.name = request.json.get('name', std.name)
    std.surname = request.json.get('surname',std.surname)
    std.adress = request.json.get('adress', std.adress)
    std.hobbies = request.json.get('hobbies', std.hobbies)
    std.numberPhone = request.json.get('adress', std.numberPhone)
    db.session.commit()
    return jsonify( { 'std': std } )

@appli.route('/insert/<table>/<string:valeurs>')
def insert(table,valeurs):
    newstudent = {}
    values = valeurs.split(',')
    print(values)
    data = json.load(open('db.json'))
    for val in values:
        v = val.split('=')
        newstudent.update({v[0]:v[1]})
    with open('db.json','w') as database:
        data['tables'][table].append(newstudent)
        json.dump(data, database, indent=4)
    return "Insertion dans : "+table+" les valeurs "+ valeurs

@appli.route('/create/<table>/')
def create(table):
    f= open('db.json','r')
    data = json.load(f)
    tables = data['tables']
    tables[table] = []
    f.close()

    f= open('db.json','w')
    json.dump(data,f)
    return "Table cree : "+table

if __name__ == '__main__':
    appli.run(debug = True, host = 'localhost', port = 8889)