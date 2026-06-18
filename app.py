from flask import Flask, render_template
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

class Base(DeclarativeBase):
    ...

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URL"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/home")
@app.route("/")
def hello():
    return render_template("home.html", name="Moein")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)