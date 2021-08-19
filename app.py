from flask import Flask, render_template, request, redirect, url_for #looking for template directory
from flask_sqlalchemy import SQLAlchemy #saves todo items to library for handling database
#SQLAlchemy is a library that facilitates the communication between Python programs and databases.

app = Flask(__name__) #setting up db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #Name of path to DB, relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True) #structuring DB, creating a unique value for each todo item 
    title = db.Column(db.String(100)) #string must not exceed 100 char
    complete = db.Column(db.Boolean)

@app.route('/') #request on line 1 allows us to go to route
def index(): #prints todo list
    contact_list = Contact.query.all()
    print(contact_list)
    return render_template('base.html', contact_list=contact_list) #renders html page 


@app.route("/add", methods=["POST"]) #Queries db to get this item
def add():
    #adds new item
    title = request.form.get("title")
    new_contact = Contact(title=title, complete=False) #creates object to a class
    db.session.add(new_contact) #add list item to DB
    db.session.commit() #sends query to db
    return redirect(url_for("index")) # redirects user to index/homepage

@app.route("/update/<int:contact_id>", methods=["POST","GET"])
def update(contact_id): #todo variable added in html
#     #updates new item
    contact = Contact.query.filter_by(id=contact_id).first()
    #todo_update = Todo.query.get_OR_404(todo_id)

    if request.method == "POST":
        #todo_update.title = request.form['title']
        contact.title = request.form['title']
        try:
            db.session.commit()
            return redirect(url_for("index"))
        except:
            return 'There was an issue while updating that task'
    else:
        #return render_template('update.html', todo_update=todo_update)
        return render_template('update.html', contact=contact)

@app.route("/delete/<int:contact_id>")
def delete(contact_id):
    contact = Contact.query.filter_by(id=contact_id).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all() #creates database file
    # app.run(debug=True)

    app.run(host ='0.0.0.0', port = 5000, debug = True)

# app2.run(host='0.0.0.0',port=5000)