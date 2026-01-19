"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import select
from models import db, User, Characters, Planets, Films, Vehicles, Species, Favorites_characters, Favorites_planets, Favorites_films, Favorites_vehicles, Favorites_species
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/<case>', methods=['GET', 'POST'])
def handle_cases(case):
    response_body = ""
    if request.method == "GET":
        match case:
            case "planets":
                planets = db.session.execute(select(Planets)).scalars().all()
                response_body = {
                    "planets": list(map(lambda planets: planets.serialize(), planets))
                }, 200
            case "characters":
                characters = db.session.execute(
                    select(Characters)).scalars().all()
                response_body = {
                    "characters": list(map(lambda characters: characters.serialize(), characters))
                }, 200
            case "films":
                films = db.session.execute(select(Films)).scalars().all()
                response_body = {
                    "films": list(map(lambda films: films.serialize(), films))
                }, 200
            case "vehicles":
                vehicles = db.session.execute(select(Vehicles)).scalars().all()
                response_body = {
                    "vehicles": list(map(lambda vehicles: vehicles.serialize(), vehicles))
                }, 200
            case "species":
                species = db.session.execute(select(Species)).scalars().all()
                response_body = {
                    "species": list(map(lambda species: species.serialize(), species))
                }, 200
            case "users":
                users = db.session.execute(select(User)).scalars().all()
                response_body = {
                    "users": list(map(lambda users: users.serialize(), users))
                }, 200
            case _:
                response_body = {
                    "Operation not found"
                }, 400
    else:
        request_body = request.json
        match case:
            case "planets":
                planet = Planets(**request_body)
                db.session.add(planet)
                db.session.commit()
                response_body = {
                    "planet": planet.name + "Has been added"
                }, 200
            case "characters":
                character = Characters(**request_body)
                db.session.add(character)
                db.session.commit()
                response_body = {
                    "character": character.name + "Has been added"
                }, 200
            case "films":
                film = Films(**request_body)
                db.session.add(film)
                db.session.commit()
                response_body = {
                    "film": film.title + "Has been added"
                }, 200
            case "vehicles":
                vehicle = Vehicles(**request_body)
                db.session.add(vehicle)
                db.session.commit()
                response_body = {
                    "vehicle": vehicle.name + "Has been added"
                }, 200
            case "species":
                species = Species(**request_body)
                db.session.add(species)
                db.session.commit()
                response_body = {
                    "species": species.name + "Has been added"
                }, 200
            case _:
                response_body = {
                    "Operation not found"
                }, 200

    return jsonify(response_body)


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def user_favorites(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"msg": "Womp womp, no user found"}), 404

    favorite_planets = db.session.execute(
        select(Favorites_planets).where(Favorites_planets.user_id == user_id)
    ).scalars().all()

    favorite_characters = db.session.execute(
        select(Favorites_characters).where(
            Favorites_characters.user_id == user_id)
    ).scalars().all()

    favorite_films = db.session.execute(
        select(Favorites_films).where(Favorites_films.user_id == user_id)
    ).scalars().all()

    favorite_vehicles = db.session.execute(
        select(Favorites_vehicles).where(Favorites_vehicles.user_id == user_id)
    ).scalars().all()

    favorite_species = db.session.execute(
        select(Favorites_species).where(Favorites_species.user_id == user_id)
    ).scalars().all()
    

    return jsonify({
        "username": user.username,
        "favorite planets": list(map(lambda favorite_planets: favorite_planets.serialize(), favorite_planets)),
        "favorite characters": list(map(lambda favorite_characters: favorite_characters.serialize(), favorite_characters)),
        "favorite films": list(map(lambda favorite_films: favorite_films.serialize(), favorite_films)),
        "favorite vehicles": list(map(lambda favorite_vehicles: favorite_vehicles.serialize(), favorite_vehicles)),
        "favorite species": list(map(lambda favorite_species: favorite_species.serialize(), favorite_species))
    }), 200

@app.route('/<case>/<int:case_id>', methods=['GET'])
def handle_cases_singular(case, case_id):
    match case:
        case "planets":
            planet = db.session.execute(select(Planets).where(Planets.id == case_id)).scalar_one_or_none()
            response_body = {
                "planet": planet.serialize()
            }, 200
        case "characters":
            character = db.session.execute(select(Characters).where(
                Characters.id == case_id)).scalar_one_or_none()
            response_body = {
                "character": character.serialize()
            }, 200
        case "films":
            film = db.session.execute(select(Films).where(
                Films.id == case_id)).scalar_one_or_none()
            response_body = {
                "film": film.serialize()
            }, 200
        case "vehicles":
            vehicle = db.session.execute(select(Vehicles).where(
                Vehicles.id == case_id)).scalar_one_or_none()
            response_body = {
                "vehicle": vehicle.serialize()
            }
        case "species":
            species = db.session.execute(select(Species).where(
                Species.id == case_id)).scalar_one_or_none()
            response_body = {
                "species": species.serialize()
            }, 200
        case _:
            response_body = {
                "Operation not found"
            }, 400

    return jsonify(response_body)

@app.route('/favorite/<case>/<int:case_id>', methods=['POST', 'DELETE'])
def handle_favorites(case, case_id):
    response_body = ""
    if request.method == "DELETE":
        match case:
            case "planets":
                planet = db.session.execute(select(Planets).where(
                    Planets.id == case_id)).scalar_one_or_none()
                db.session.delete(planet)
                db.session.commit()
                response_body = {
                    "planet": planet.name + "Has been deleted from favorites"
                }, 200
            case "characters":
                character = db.session.execute(select(Characters).where(
                    Characters.id == case_id)).scalar_one_or_none()
                db.session.delete(character)
                db.session.commit()
                response_body = {
                    "character": character.name + "Has been deleted from favorites"
                }, 200
            case "films":
                film = db.session.execute(select(Films).where(
                    Films.id == case_id)).scalar_one_or_none()
                db.session.delete(film)
                db.session.commit()
                response_body = {
                    "film": film.title + "Has been deleted from favorites"
                }, 200
            case "vehicles":
                vehicle = db.session.execute(select(Vehicles).where(
                    Vehicles.id == case_id)).scalar_one_or_none()
                db.session.delete(vehicle)
                db.session.commit()
                response_body = {
                    "vehicle": vehicle.name + "Has been deleted from favorites"
                }, 200
            case "species":
                species = db.session.execute(select(Species).where(
                    Species.id == case_id)).scalar_one_or_none()
                db.session.delete(species)
                db.session.commit()
                response_body = {
                    "species": species.name + "Has been deleted from favorites"
                }, 200
            case _:
                response_body = {
                    "Operation not found"
                }, 400
    else:
        user = db.session.execute(select(User).where(
            User.id == case_id)).scalar_one_or_none()
        match case:
            case "planets":
                planet = db.session.execute(select(Planets).where(
                    Planets.id == case_id)).scalar_one_or_none()
                favorite_planet = Favorites_planets(
                    planets_id=planet.id, user_id=user.id)
                db.session.add(favorite_planet)
                db.session.commit()
                response_body = {
                    "planet": planet.name + "Has been added to favorites"
                }, 200
            case "characters":
                character = db.session.execute(select(Characters).where(
                    Characters.id == case_id)).scalar_one_or_none()
                favorite_character = Favorites_characters(
                    character_id=character.id, user_id=user.id)
                db.session.add(favorite_character)
                db.session.commit()
                response_body = {
                    "character": character.name + "Has been added to favorites"
                }, 200
            case "films":
                film = db.session.execute(select(Films).where(
                    Films.id == case_id)).scalar_one_or_none()
                favorite_film = Favorites_films(
                    films_id=film.id, user_id=user.id)
                db.session.add(favorite_film)
                db.session.commit()
                response_body = {
                    "film": film.title + "Has been added to favorites"
                }, 200
            case "vehicles":
                vehicle = db.session.execute(select(Vehicles).where(
                    Vehicles.id == case_id)).scalar_one_or_none()
                favorite_vehicle = Favorites_vehicles(
                    vehicles_id=vehicle.id, user_id=user.id)
                db.session.add(favorite_vehicle)
                db.session.commit()
                response_body = {
                    "vehicle": vehicle.name + "Has been added to favorites"
                }, 200
            case "species":
                species = db.session.execute(select(Species).where(
                    Species.id == case_id)).scalar_one_or_none()
                favorite_species = Favorites_species(
                    species_id=species.id, user_id=user.id)
                db.session.add(favorite_species)
                db.session.commit()
                response_body = {
                    "species": species.name + "Has been added to favorites"
                }, 200
            case _:
                response_body = {
                    "Operation not found"
                }, 400
    return jsonify(response_body)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
