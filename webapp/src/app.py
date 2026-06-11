import os
import requests
from fastapi import FastAPI, HTTPException, Query
from typing import List
from pydantic import BaseModel

app = FastAPI(title="Star Wars API")

SWAPI_BASE_URL = "https://swapi.info/api"

HELLO_WORLD_MESSAGE = os.getenv("HELLO_WORLD_MESSAGE", "Hello, World!")


class Person(BaseModel):
    name: str
    height: str
    mass: str
    bmi: float


@app.get("/")
def hello():
    return {"message": HELLO_WORLD_MESSAGE}


@app.get("/data")
def get_star_wars_data(id: int = Query(default=1, description="ID del personaje")):
    try:
        response = requests.get(f"{SWAPI_BASE_URL}/people/{id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


@app.get("/top-people-by-bmi", response_model=List[Person])
def top_people_by_bmi():
    try:
        response = requests.get(f"{SWAPI_BASE_URL}/people", timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")

    people_list = data if isinstance(data, list) else data.get("results", [])

    people_with_bmi = []
    for person in people_list:
        try:
            height_cm = float(person["height"])
            mass_kg = float(person["mass"].replace(",", ""))
            if height_cm <= 0:
                continue
            height_m = height_cm / 100.0
            bmi = round(mass_kg / (height_m ** 2), 2)
            people_with_bmi.append(Person(
                name=person["name"],
                height=person["height"],
                mass=person["mass"],
                bmi=bmi,
            ))
        except (ValueError, KeyError, ZeroDivisionError):
            continue

    people_with_bmi.sort(key=lambda p: p.bmi, reverse=True)
    return people_with_bmi[:20]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
