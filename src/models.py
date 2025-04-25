from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    favorites = relationship(
        'Favorite', back_populates='user', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }


class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20))
    gender: Mapped[str] = mapped_column(String(20))
    height: Mapped[int] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(String(20))
    skin_color: Mapped[str] = mapped_column(String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    terrain: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=True)

    user = relationship('User', back_populates='favorites')
    character = relationship('Character')
    planet = relationship('Planet')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None
        }
