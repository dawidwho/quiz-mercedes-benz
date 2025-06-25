"""
AI Insights router for simulating AI-generated descriptions.
"""

import random
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps, schemas, crud
from app.db.models import People as PeopleModel, Planets as PlanetsModel

router = APIRouter(prefix="/simulate-ai-insight", tags=["ai-insights"])

# Create CRUD instances
people_crud = crud.CRUDBase(PeopleModel)
planets_crud = crud.CRUDBase(PlanetsModel)


def generate_people_insight(person_data: dict) -> str:
    """Generate a fake AI insight for a person."""
    name = person_data.get("name", "Unknown")
    height = person_data.get("height", "unknown")
    mass = person_data.get("mass", "unknown")
    hair_color = person_data.get("hair_color", "unknown")
    eye_color = person_data.get("eye_color", "unknown")
    gender = person_data.get("gender", "unknown")
    birth_year = person_data.get("birth_year", "unknown")

    insights = [
        f"Based on my analysis of {name}'s profile, this individual exhibits remarkable characteristics. "
        f"With a height of {height}cm and mass of {mass}kg, they demonstrate a unique physical constitution. "
        f"Their distinctive {hair_color} hair and {eye_color} eyes suggest a genetic heritage that's quite fascinating. "
        f"As a {gender} born in {birth_year}, they represent an interesting case study in demographic patterns.",
        f"My AI analysis reveals that {name} is an extraordinary being with intriguing attributes. "
        f"Their physical measurements ({height}cm height, {mass}kg mass) indicate a body type that's statistically significant. "
        f"The combination of {hair_color} hair and {eye_color} eyes creates a distinctive appearance profile. "
        f"Being a {gender} from {birth_year}, they embody certain cultural and temporal characteristics worth noting.",
        f"Through advanced pattern recognition, I've identified {name} as a subject of particular interest. "
        f"Their biometric data shows {height}cm height and {mass}kg mass, placing them in an interesting percentile range. "
        f"Their {hair_color} hair and {eye_color} eyes suggest genetic markers that could be significant. "
        f"As a {gender} individual from {birth_year}, they represent a valuable data point in our demographic analysis.",
        f"AI analysis indicates that {name} possesses unique characteristics that warrant deeper examination. "
        f"With dimensions of {height}cm height and {mass}kg mass, they fall into a distinctive physical category. "
        f"Their {hair_color} hair and {eye_color} eyes display phenotypic traits that are quite remarkable. "
        f"Being a {gender} born in {birth_year}, they exemplify certain temporal and cultural patterns.",
        f"Based on comprehensive data analysis, {name} emerges as a fascinating subject for study. "
        f"Their physical profile ({height}cm height, {mass}kg mass) reveals interesting biometric patterns. "
        f"Their {hair_color} hair and {eye_color} eyes suggest genetic diversity that's worth investigating. "
        f"As a {gender} from {birth_year}, they represent an important demographic sample.",
    ]

    return random.choice(insights)


def generate_planet_insight(planet_data: dict) -> str:
    """Generate a fake AI insight for a planet."""
    name = planet_data.get("name", "Unknown")
    diameter = planet_data.get("diameter", "unknown")
    population = planet_data.get("population", "unknown")
    climate = planet_data.get("climate", "unknown")
    terrain = planet_data.get("terrain", "unknown")
    gravity = planet_data.get("gravity", "unknown")
    rotation_period = planet_data.get("rotation_period", "unknown")
    orbital_period = planet_data.get("orbital_period", "unknown")

    insights = [
        f"My planetary analysis reveals that {name} is a world of remarkable complexity. "
        f"With a diameter of {diameter}km and a population of {population}, it represents a significant celestial body. "
        f"The {climate} climate combined with {terrain} terrain creates a unique environmental profile. "
        f"Gravity of {gravity} and rotation period of {rotation_period} hours suggest interesting orbital dynamics.",
        f"AI assessment of {name} indicates this is a planet with extraordinary characteristics. "
        f"Its {diameter}km diameter and {population} inhabitants place it in a notable category of celestial bodies. "
        f"The {climate} climate and {terrain} landscape suggest diverse ecological systems. "
        f"With {gravity} gravity and {rotation_period} hour days, it exhibits fascinating astronomical properties.",
        f"Through advanced planetary modeling, I've determined that {name} is a world of great interest. "
        f"Measuring {diameter}km across with {population} residents, it's a significant planetary body. "
        f"The {climate} conditions and {terrain} features indicate rich environmental diversity. "
        f"Its {gravity} gravitational field and {rotation_period} hour rotation create unique physical conditions.",
        f"Planetary analysis shows {name} to be an exceptional celestial object worth detailed study. "
        f"At {diameter}km diameter with {population} inhabitants, it represents an important planetary system. "
        f"The {climate} climate and {terrain} topography suggest complex environmental interactions. "
        f"With {gravity} gravity and {rotation_period} hour days, it demonstrates fascinating orbital mechanics.",
        f"AI evaluation of {name} reveals it to be a planet with remarkable scientific value. "
        f"Its {diameter}km size and {population} population make it a significant astronomical body. "
        f"The {climate} weather patterns and {terrain} landscape indicate diverse ecological niches. "
        f"Gravity of {gravity} and {rotation_period} hour rotation period suggest interesting physical dynamics.",
    ]

    return random.choice(insights)


@router.post("/", response_model=schemas.AIInsightResponse)
def simulate_ai_insight(
    request: schemas.AIInsightRequest, db: Session = Depends(deps.get_db)
):
    """
    Simulate AI-generated insights for people or planets.

    This endpoint generates fake AI descriptions based on the provided name and entity type.
    It first searches for the entity in the database and then generates a contextual insight.
    """

    # Validate entity type
    if request.entity_type.lower() not in ["people", "planets"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="entity_type must be either 'people' or 'planets'",
        )

    # Search for the entity in the database
    entity_data = None

    if request.entity_type.lower() == "people":
        # Search for people by name
        people, _ = people_crud.get_multi_paginated_with_search(
            db, skip=0, limit=1, search_params={"name": request.name}
        )
        if people:
            entity_data = {
                "name": people[0].name,
                "height": people[0].height,
                "mass": people[0].mass,
                "hair_color": people[0].hair_color,
                "eye_color": people[0].eye_color,
                "gender": people[0].gender,
                "birth_year": people[0].birth_year,
            }
    else:  # planets
        # Search for planets by name
        planets, _ = planets_crud.get_multi_paginated_with_search(
            db, skip=0, limit=1, search_params={"name": request.name}
        )
        if planets:
            entity_data = {
                "name": planets[0].name,
                "diameter": planets[0].diameter,
                "population": planets[0].population,
                "climate": planets[0].climate,
                "terrain": planets[0].terrain,
                "gravity": planets[0].gravity,
                "rotation_period": planets[0].rotation_period,
                "orbital_period": planets[0].orbital_period,
            }

    # If entity not found, generate a generic insight
    if not entity_data:
        if request.entity_type.lower() == "people":
            insight = f"AI analysis indicates that {request.name} is an individual whose data is not currently available in our database. However, based on name analysis, this person likely possesses unique characteristics that would make them an interesting subject for further study."
        else:
            insight = f"Planetary analysis shows that {request.name} is a celestial body not currently catalogued in our database. The name suggests it may be a world with unique astronomical properties worth investigating further."

        return schemas.AIInsightResponse(
            name=request.name,
            entity_type=request.entity_type.lower(),
            insight=insight,
            confidence_score=0.3,
            generated_at=datetime.utcnow(),
            model_version="v1.0",
        )

    # Generate insight based on entity type
    if request.entity_type.lower() == "people":
        insight = generate_people_insight(entity_data)
    else:
        insight = generate_planet_insight(entity_data)

    # Generate a realistic confidence score
    confidence_score = round(random.uniform(0.75, 0.98), 2)

    return schemas.AIInsightResponse(
        name=entity_data["name"],
        entity_type=request.entity_type.lower(),
        insight=insight,
        confidence_score=confidence_score,
        generated_at=datetime.utcnow(),
        model_version="v1.0",
    )


@router.get("/", response_model=schemas.AIInsightResponse)
def simulate_ai_insight_get(
    name: str = Query(..., description="Name of the person or planet"),
    entity_type: str = Query(..., description="Type of entity: 'people' or 'planets'"),
    db: Session = Depends(deps.get_db),
):
    """
    Simulate AI-generated insights for people or planets (GET version).

    This endpoint generates fake AI descriptions based on the provided name and entity type.
    It first searches for the entity in the database and then generates a contextual insight.
    """

    # Create request object and reuse the POST logic
    request = schemas.AIInsightRequest(name=name, entity_type=entity_type)
    return simulate_ai_insight(request, db)
