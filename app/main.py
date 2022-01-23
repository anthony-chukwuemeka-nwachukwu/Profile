from flask import Flask, render_template
from app.utils import *
import app.utils_portfolio as ut_port

app = Flask(__name__)

@app.route('/')
def index():
    title, link, desc, author, date, img = ut_port.call()
    title, link, desc, author, date, img = title[:3], link[:3], desc[:3], author[:3], date[:3], img[:3]
    return render_template("home.html", interests=zip(clas, tit, par), interes=zip(clas, tit, par), skillgroups=zip(group, skillrates),
                           latestprojects=zip(link, img, date, title, desc),
                           platforms=zip(platforms_name, platforms_link, platforms_img, platforms_desc))
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/send_email')
def email():
    return render_template("send_email.php")

@app.route('/portfolio')
def portfolio():
    title, link, desc, author, date, img = ut_port.call()
    return render_template("portfolio.html", github_portfolio=zip(title, link, img, desc, author, date))


if __name__ == '__main__':
    app.run(debug=True)