from datetime import datetime
import os
from src.utils.utils import *
import src.utils.utils_portfolio as ut_port
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

"""DB CONFIGURATION START"""

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# basedir = '../'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Class/Model
class Contact(db.Model):
  contact_id = db.Column(db.Integer, primary_key=True)
  sender = db.Column(db.String(250), nullable=False)
  emailAddress = db.Column(db.String(250), nullable=False)
  message = db.Column(db.String(500))
  sentAt = db.Column(db.DateTime)

  def __init__(self, sender, emailAddress, message):
    self.sender = sender
    self.emailAddress = emailAddress
    self.message = message
    self.sentAt = datetime.now()

class Newsletter(db.Model):
  email_id = db.Column(db.Integer, primary_key=True)
  emailAddress = db.Column(db.String(250), nullable=False)
  sentAt = db.Column(db.DateTime)

  def __init__(self, emailAddress):
    self.emailAddress = emailAddress
    self.sentAt = datetime.now()

# Schema
class ContactSchema(ma.Schema):
  class Meta:
    fields = ('contact_id', 'sender', 'emailAddress', 'message', 'sentAt')

class NewsletterSchema(ma.Schema):
  class Meta:
    fields = ('email_id', 'emailAddress', 'sentAt')

# Init schema
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

newsletter_schema = NewsletterSchema()
newsletters_schema = NewsletterSchema(many=True)


# Execute only once
# db.create_all()

"""DB CONFIGURATION ENDS"""

@app.route('/', methods=['GET'])
def index():
    title, link, desc, author, date, img = ut_port.call()
    title, link, desc, author, date, img = title[:3], link[:3], desc[:3], author[:3], date[:3], img[:3]
    return render_template("home.html", interests=zip(clas, tit, par), interes=zip(clas, tit, par), skillgroups=zip(group, skillrates),
                           latestprojects=zip(link, img, date, title, desc),
                           platforms=zip(platforms_name, platforms_link, platforms_img, platforms_desc))

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET'])
def contact():
    return render_template("contact.html")


@app.route('/portfolio')
def portfolio():
    title, link, desc, author, date, img = ut_port.call()
    return render_template("portfolio.html", github_portfolio=zip(title, link, img, desc, author, date))

@app.route('/contact', methods=['POST'])
def contact_form():
    sender = request.form['name']
    emailAddress = request.form['email']
    message = request.form['message']
    
    new_contact = Contact(sender, emailAddress, message)

    db.session.add(new_contact)
    db.session.commit()
    
    return render_template("contact.html")

@app.route('/', methods=['POST'])
def create_newsletter():
    emailAddress = request.form['email']
    
    new_newsletter = Newsletter(emailAddress)

    db.session.add(new_newsletter)
    db.session.commit()
    
    return render_template("newsletter.html")


# if __name__ == '__main__':
#     app.run(debug=True)