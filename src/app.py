"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer team practicing skills and preparing for inter-school matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, skill drills, and team scrimmages",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 15,
        "participants": ["ryan@mergington.edu", "kate@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, rehearsals, and seasonal productions",
        "schedule": "Wednesdays and Saturdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["linda@mergington.edu", "marco@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Drawing, painting, and mixed-media projects for all skill levels",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["nora@mergington.edu", "leo@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design and build robots, compete in challenges, and learn electronics",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["omar@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking, argumentation, and competitive debate formats",
        "schedule": "Mondays and Thursdays, 6:00 PM - 7:30 PM",
        "max_participants": 16,
        "participants": ["chris@mergington.edu", "bella@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
