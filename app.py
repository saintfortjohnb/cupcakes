from flask import Flask, jsonify, render_template, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    connect_db(app)
    db.create_all()

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/api/cupcakes", methods=["GET"])
def get_all_cupcakes():
    all_cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET"])
def get_single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(
        flavor=request.json.get("flavor", ""),
        size=request.json.get("size", ""),
        rating=request.json.get("rating", ""),
        image=request.json.get("image", "")
    )
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
