from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)
@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep  # Return the newly added sheep data

@app.delete("/sheep/{sheep_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(sheep_id: int):
    try:
        db.delete_sheep(sheep_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return None
@app.put("/sheep/{sheep_id}", response_model=Sheep)
def update_sheep(sheep_id: int, sheep: Sheep):
    sheep.id = sheep_id
    try:
        return db.update_sheep(sheep)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sheep not found")

@app.get("/sheep/", response_model=List[Sheep])
def read_all_sheep():
    return db.list_sheep()
