from flask import Flask, jsonify, request, abort
from flask_migrate import Migrate
from src.models import db, User, Character, Planet, Favorite

def get_current_user():
    user = User.query.first()
    if not user:
        abort(404, "No hay usuarios en la base de datos")
    return user

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///starwars_blog.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    Migrate(app, db)

    @app.route('/people', methods=['GET'])
    def list_people():
        return jsonify([p.serialize() for p in Character.query.all()])

    @app.route('/people/<int:people_id>', methods=['GET'])
    def get_person(people_id):
        p = Character.query.get_or_404(people_id)
        return jsonify(p.serialize())

    @app.route('/planets', methods=['GET'])
    def list_planets():
        return jsonify([p.serialize() for p in Planet.query.all()])

    @app.route('/planets/<int:planet_id>', methods=['GET'])
    def get_planet(planet_id):
        p = Planet.query.get_or_404(planet_id)
        return jsonify(p.serialize())

    @app.route('/users', methods=['GET'])
    def list_users():
        return jsonify([u.serialize() for u in User.query.all()])

    @app.route('/users/favorites', methods=['GET'])
    def list_favorites():
        user = get_current_user()
        return jsonify([f.serialize() for f in user.favorites])

    @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
    def add_fav_planet(planet_id):
        user = get_current_user()
        planet = Planet.query.get_or_404(planet_id)
        if Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first():
            abort(400, "Planeta ya está en favoritos")
        fav = Favorite(user_id=user.id, planet_id=planet.id)
        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 201

    @app.route('/favorite/people/<int:people_id>', methods=['POST'])
    def add_fav_person(people_id):
        user = get_current_user()
        char = Character.query.get_or_404(people_id)
        if Favorite.query.filter_by(user_id=user.id, character_id=people_id).first():
            abort(400, "Personaje ya está en favoritos")
        fav = Favorite(user_id=user.id, character_id=char.id)
        db.session.add(fav)
        db.session.commit()
        return jsonify(fav.serialize()), 201

    @app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
    def remove_fav_planet(planet_id):
        user = get_current_user()
        fav = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first_or_404("No existe favorito")
        db.session.delete(fav)
        db.session.commit()
        return '', 204

    @app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
    def remove_fav_person(people_id):
        user = get_current_user()
        fav = Favorite.query.filter_by(user_id=user.id, character_id=people_id).first_or_404("No existe favorito")
        db.session.delete(fav)
        db.session.commit()
        return '', 204

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
