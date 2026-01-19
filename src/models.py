from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)

    favorites_characters_user: Mapped[List["Favorites_characters"]] = relationship(
        back_populates="user")
    favorites_planets_user: Mapped[List["Favorites_planets"]] = relationship(
        back_populates="user")
    favorites_films_user: Mapped[List["Favorites_films"]] = relationship(
        back_populates="user")
    favorites_vehicles_user: Mapped[List["Favorites_vehicles"]] = relationship(
        back_populates="user")
    favorites_species_user: Mapped[List["Favorites_species"]] = relationship(
        back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    imageLink: Mapped[str] = mapped_column(nullable=False)

    favorites_characters: Mapped[List["Favorites_characters"]] = relationship(
        back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "imageLink": self.imageLink
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    imageLink: Mapped[str] = mapped_column(nullable=False)

    favorites_planets: Mapped[List["Favorites_planets"]
                              ] = relationship(back_populates="planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "imageLink": self.imageLink
            # do not serialize the password, its a security breach
        }


class Films(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    imageLink: Mapped[str] = mapped_column(nullable=False)

    favorites_films: Mapped[List["Favorites_films"]
                            ] = relationship(back_populates="films")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "imageLink": self.imageLink
            # do not serialize the password, its a security breach
        }


class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    imageLink: Mapped[str] = mapped_column(nullable=False)

    favorites_vehicles: Mapped[List["Favorites_vehicles"]] = relationship(
        back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "imageLink": self.imageLink
            # do not serialize the password, its a security breach
        }


class Species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    imageLink: Mapped[str] = mapped_column(nullable=False)

    favorites_species: Mapped[List["Favorites_species"]
                              ] = relationship(back_populates="species")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "imageLink": self.imageLink
            # do not serialize the password, its a security breach
        }


class Favorites_characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    user: Mapped["User"] = relationship(
        back_populates="favorites_characters_user")
    characters: Mapped["Characters"] = relationship(
        back_populates="favorites_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }


class Favorites_planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    user: Mapped["User"] = relationship(
        back_populates="favorites_planets_user")
    planets: Mapped["Planets"] = relationship(
        back_populates="favorites_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
            # do not serialize the password, its a security breach
        }


class Favorites_films(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    # Emparentar a User.
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    films_id: Mapped[int] = mapped_column(ForeignKey("films.id"))

    user: Mapped["User"] = relationship(back_populates="favorites_films_user")
    films: Mapped["Films"] = relationship(back_populates="favorites_films")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }


class Favorites_vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    vehicles_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    user: Mapped["User"] = relationship(
        back_populates="favorites_vehicles_user")
    vehicles: Mapped["Vehicles"] = relationship(
        back_populates="favorites_vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicles_id": self.vehicles_id,
            # do not serialize the password, its a security breach
        }


class Favorites_species(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))

    user: Mapped["User"] = relationship(
        back_populates="favorites_species_user")
    species: Mapped["Species"] = relationship(
        back_populates="favorites_species")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "species_id": self.species_id,
            # do not serialize the password, its a security breach
        }
