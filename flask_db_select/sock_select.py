""" write to a SQLite database with forms, templates
    add new record, delete a record, edit/update a record
    """

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)

# the name of the database; add path if necessary
db_name = 'postgres'    

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Periferia2020@localhost/postgres' 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# this database has only ONE table, socks
# identify all of your columns by name and data type as shown

class Sock(db.Model):
    __tablename__ = 'dbcrud'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)
    email = db.Column(db.String)

# get sock IDs and names for the select menu BELOW
socks = Sock.query.order_by(Sock.nombre).all()
# create the list of tuples needed for the choices value
pairs_list = []
for sock in socks:
    pairs_list.append( (sock.id, sock.nombre) )

# Flask-WTF form magic
# set up the quickform - select includes value, option text (value matches db)
# all that is in this form is one select menu and one submit button
class SockSelect(FlaskForm):
    select = SelectField( 'Choose a sock style:',
      choices=pairs_list
      )
    submit = SubmitField('Submit')


# routes

# starting page for app
@app.route('/')
def index():
    # make an instance of the WTF form class we created, above
    form = SockSelect()
    # pass it to the template
    return render_template('index.html', form=form)


# whichever id comes from the form, that one sock will be displayed
@app.route('/sock', methods=['POST'])
def sock_detail():
    sock_id = request.form['select']
    # get all columns for the one sock with the supplied id
    the_sock = Sock.query.filter_by(id=sock_id).first()
    # pass them to the template
    return render_template('sock.html', the_sock=the_sock)


if __name__ == '__main__':
    app.run(debug=True)

