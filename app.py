import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
    items = Item.query.all()
    return render_template("items.html", items=items)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        item = Item(
            name=request.form["name"],
            category=request.form["category"],
            quantity=int(request.form["quantity"]),
            unit=request.form["unit"],
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("form.html", item=None)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.category = request.form["category"]
        item.quantity = int(request.form["quantity"])
        item.unit = request.form["unit"]
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("form.html", item=item)


@app.route("/delete/<int:id>")
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("home"))


with app.app_context():
    try:
        db.create_all()
    except Exception:
        pass

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
