from flask import Flask, render_template, redirect, url_for
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String


app = Flask(__name__)

class Base(DeclarativeBase):
    ...

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class User(db.Model):
    # id: Mapped[int] = mapped_column(primary_key=True)
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True)
    email = mapped_column(String(80), nullable=False)

    def __repr__(self):
        return f"{self.username} - {self.email}"

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/detail/<string:username>")
def detail(username):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    return render_template("detail.html", user=user)

@app.route("/delete/<int:user_id>")
def delete(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)