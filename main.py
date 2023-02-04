from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def todic(self):
        # Method 1.
        # dictionary={}
        #
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name]=getattr(self,column.name)
        #     print(dictionary)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/random",methods=["GET"])
# def get_random_cafe():
#     all_cafes_list=db.session.query()

# @app.route("/random")
# def get_random_cafe():
#     all_cafes_list = db.session.query(Cafe).all()
#     random_cafe = random.choice(all_cafes_list)
#     return jsonify( cafe={
#
#         # Omit the id from the response
#             # "id": random_cafe.id,
#             "name": random_cafe.name,
#             "map_url": random_cafe.map_url,
#             "img_url": random_cafe.img_url,
#             "location": random_cafe.location,
#             "seats": random_cafe.seats,
#             "coffee_price": random_cafe.coffee_price,
#         # Put some properties in a sub-category
#         "amenities": {
#             "can_take_calls": random_cafe.can_take_calls,
#             "has_toilet": random_cafe.has_toilet,
#             "has_wifi": random_cafe.has_wifi,
#             "has_sockets": random_cafe.has_sockets
#           }
#
#         })


@app.route("/random")
def get_random_cafe():
    all_cafes_list = db.session.query(Cafe).all()
    random_cafe=random.choice(all_cafes_list)
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=random_cafe.todic())

@app.route("/all")
def allcafes():
    allcafeslist=db.session.query(Cafe).all()
    return jsonify(cafes=[eachcafe.todic() for eachcafe in allcafeslist])

@app.route("/search",methods=["GET"])
def search():
    locationtobegiven= request.args.get("loc")                                                       #    explain:  req.args.get
    cafe_find=db.session.query(Cafe).filter_by(location=locationtobegiven).first()                    #  page = request.args.get('page', default = 1, type = int)
    if cafe_find:                                 #if first() is not given then it gets all matches of querys like with the same name                                                   # /my-route?page=34               -> page: 34
        return jsonify(cafe=cafe_find.todic())
    else:
        return jsonify(error={"Not Found":"Sorry, we couldn't find any cafe at that Location."})

@app.route("/add",methods=["POST"])
def add_cafe():
    new_cafe=Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<int:cafeid>",methods=["PATCH"])
def patch_newprice(cafeid):
    new_price=request.args.get("newwprice")        #here new_price is what we naming the action to use in code
    cafe=db.session.query(Cafe).get(cafeid)         # but newwprice is what we are going to give in postman url like localhost:5000/update-price/22?newwprice=33$
    if cafe:
        cafe.coffee_price=new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == '__main__':
    app.run(debug=True)
















# https://documenter.getpostman.com/view/19786007/2s935oKipY