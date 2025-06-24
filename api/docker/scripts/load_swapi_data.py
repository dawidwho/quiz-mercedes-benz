#!/usr/bin/env python3
"""
Standalone script to load people and planets data from Star Wars API (SWAPI) into the database.
This version doesn't rely on the app module structure.
"""

import requests
import time
import sys
import os
from typing import Dict, List, Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# Database configuration - will be read from environment variables
import os

# Get database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://quiz_user:quiz_password@postgres:5432/quiz_db"
)

# Create database engine and session
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Define models directly in this script
class People(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    height = Column(String, nullable=True)
    mass = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    skin_color = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    birth_year = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Planets(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    diameter = Column(String, nullable=True)
    rotation_period = Column(String, nullable=True)
    orbital_period = Column(String, nullable=True)
    gravity = Column(String, nullable=True)
    population = Column(String, nullable=True)
    climate = Column(String, nullable=True)
    terrain = Column(String, nullable=True)
    surface_water = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


def init_database():
    """Initialize database tables."""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise


class SWAPIDataLoader:
    """Class to handle loading data from SWAPI into the database."""

    def __init__(self):
        self.base_url = "https://swapi.py4e.com/api"
        self.session = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def fetch_all_pages(self, endpoint: str) -> List[Dict[str, Any]]:
        """Fetch all pages from a SWAPI endpoint."""
        all_data = []
        url = f"{self.base_url}/{endpoint}/"

        print(f"Fetching data from {endpoint}...")

        while url:
            try:
                print(f"  Fetching: {url}")
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                data = response.json()
                all_data.extend(data.get("results", []))

                # Get next page URL
                url = data.get("next")

                # Add a small delay to be respectful to the API
                time.sleep(0.1)

            except requests.RequestException as e:
                print(f"Error fetching data from {url}: {e}")
                break

        print(f"  Total {endpoint} records fetched: {len(all_data)}")
        return all_data

    def create_people(self, people_data: Dict[str, Any]) -> People:
        """Create a People object from SWAPI data."""
        return People(
            name=people_data.get("name", ""),
            height=people_data.get("height", ""),
            mass=people_data.get("mass", ""),
            hair_color=people_data.get("hair_color", ""),
            skin_color=people_data.get("skin_color", ""),
            eye_color=people_data.get("eye_color", ""),
            birth_year=people_data.get("birth_year", ""),
            gender=people_data.get("gender", ""),
        )

    def create_planet(self, planet_data: Dict[str, Any]) -> Planets:
        """Create a Planets object from SWAPI data."""
        return Planets(
            name=planet_data.get("name", ""),
            diameter=planet_data.get("diameter", ""),
            rotation_period=planet_data.get("rotation_period", ""),
            orbital_period=planet_data.get("orbital_period", ""),
            gravity=planet_data.get("gravity", ""),
            population=planet_data.get("population", ""),
            climate=planet_data.get("climate", ""),
            terrain=planet_data.get("terrain", ""),
            surface_water=planet_data.get("surface_water", ""),
        )

    def load_people(self):
        """Load people data from SWAPI."""
        print("\n=== Loading People Data ===")

        # Fetch people data from SWAPI
        swapi_people = self.fetch_all_pages("people")

        if not swapi_people:
            print("No people data found!")
            return

        # Insert into database
        inserted_count = 0
        for person_data in swapi_people:
            try:
                person = self.create_people(person_data)
                self.session.add(person)
                self.session.commit()
                inserted_count += 1
                print(f"  Inserted: {person.name}")
            except Exception as e:
                print(f"  Error inserting {person_data.get('name', 'Unknown')}: {e}")
                self.session.rollback()

        print(f"Successfully inserted {inserted_count} people records")

    def load_planets(self):
        """Load planets data from SWAPI."""
        print("\n=== Loading Planets Data ===")

        # Fetch planets data from SWAPI
        swapi_planets = self.fetch_all_pages("planets")

        if not swapi_planets:
            print("No planets data found!")
            return

        # Insert into database
        inserted_count = 0
        for planet_data in swapi_planets:
            try:
                planet = self.create_planet(planet_data)
                self.session.add(planet)
                self.session.commit()
                inserted_count += 1
                print(f"  Inserted: {planet.name}")
            except Exception as e:
                print(f"  Error inserting {planet_data.get('name', 'Unknown')}: {e}")
                self.session.rollback()

        print(f"Successfully inserted {inserted_count} planets records")

    def load_all_data(self):
        """Load both people and planets data."""
        print("Starting SWAPI data loading process...")

        try:
            self.load_people()
            self.load_planets()
            print("\n=== Data Loading Complete ===")
        except Exception as e:
            print(f"Error during data loading: {e}")
            raise


def main():
    """Main function to run the data loader."""
    print("SWAPI Data Loader (Standalone)")
    print("==============================")

    try:
        # Initialize database tables first
        init_database()

        # Load data
        with SWAPIDataLoader() as loader:
            loader.load_all_data()
        print("Data loading completed successfully!")
    except Exception as e:
        print(f"Failed to load data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
