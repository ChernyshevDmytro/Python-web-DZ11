from datetime import datetime
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect

from sqlalchemy.orm import sessionmaker

from models import Person, Phones
   
engine = create_engine('sqlite:///test_new.db', connect_args={'check_same_thread': False})  
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
app.debug = True
app.env = "development"


@app.route("/", methods=["GET"], strict_slashes=False)
@app.route("/details", methods=["POST"], strict_slashes=False)
def index():
    if request.method == "POST":
        find = request.form.get("find")
        for person in session.query(Person).all():
            if find in person.name:

                return render_template("details.html", person=person)
    else:    
        persons = session.query(Person).all()
        print(persons)
        return render_template("index.html", persons=persons)

@app.route("/details/<id>", strict_slashes=False)
def details(id):
    person = session.query(Person).filter(Person.id == id).first()
    return render_template("details.html", person=person)

@app.route("/persons/", methods=["GET", "POST"], strict_slashes=False)
def add_person():
    excist = 0
    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        phones = request.form.get("phones")
        
        for person in session.query(Person).all():
            
            
            if str(name) == str(person.name):
                excist=1
                if birthday:
                    dt_birthday = datetime(year=int(birthday[0:4]), month=int(birthday[4:6]), day=int(birthday[6:])).date()
                    person.birthday=dt_birthday.date()                      
                if phones and person.phones:
                    person.phones.append(Phones(phone=phones))
                if phones and not person.phones:
                    person.phones= [(Phones(phone=phones))]    
                session.add(person)
                session.commit()          
    
        if excist == 0:
            person = Person(name=name)        
        
            if birthday:
                dt_birthday = datetime(year=int(birthday[0:4]), month=int(birthday[4:6]), day=int(birthday[6:]))
                person.birthday=dt_birthday
                session.add(person)            
        
            if phones:
                person.phones.append(Phones(phone=phones))
                print(phones)    
                session.add(person)
            session.commit()

        return redirect("/")
    else:
        phones = session.query(Phones).all()
        birthday = session.query(Person).all()
    return render_template("persons.html", phones=phones, birthday = birthday)



@app.route("/delete/<id>", strict_slashes=False)
def delete(id):
    session.query(Person).filter(Person.id == id).delete()
    session.commit()
    return redirect("/")

@app.route("/delete_phone/<id>", strict_slashes=False)
def delete_phone(id):
    session.query(Phones).filter(Phones.id == id).delete()
    session.commit()   
    return redirect("/")

@app.route("/phones/<id>", methods=["GET", "POST"], strict_slashes=False)
def edit_phone(id):
    
    if request.method == "POST":    
        old_phone=session.query(Phones).filter(Phones.id == id).first()
        new_phone = request.form.get("new_phone")        
        old_phone.phone = int(new_phone)
        session.add(old_phone)
        session.commit()
        print(new_phone) 
        return redirect("/")

    else:
        old_phone=session.query(Phones).filter(Phones.id == id).first()
        return render_template("phones.html", phone=old_phone.phone)
         

if __name__ == "__main__":
    app.run()  