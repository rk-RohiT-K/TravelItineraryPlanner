from neo4j import GraphDatabase
from fastapi import FastAPI
from pydantic import BaseModel

class TourGraph:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def create_or_update_user_preferences(self, user_id, preferences):
        # Create user if not exists and update preferences
        with self.driver.session() as session:
            session.run("""
            MERGE (u:User {user_id: $user_id})
            FOREACH (pref IN $preferences | 
                MERGE (p:Preference {type: pref})
                MERGE (u)-[:PREFERS]->(p)
            )
            """, user_id=user_id, preferences=preferences)

    def update_preferences(self, user_id, new_preferences):
        # Add new preferences
        with self.driver.session() as session:
            for preference in new_preferences:
                session.run("""
                MATCH (u:User {user_id: $user_id})
                MERGE (p:Preference {type: $preference})
                MERGE (u)-[:PREFERS]->(p)
                """, user_id=user_id, preference=preference)

    def retrieve_preferences(self, user_id):
        # Retrieve user preferences
        with self.driver.session() as session:
            result = session.run("""
            MATCH (u:User {user_id: $user_id})-[:PREFERS]->(p:Preference)
            RETURN p.type AS preference
            """, user_id=user_id)
            preferences = [record["preference"] for record in result]
            return preferences

app = FastAPI()
tour_graph = TourGraph("bolt://localhost:8001", "user", "pass")

class UserPreferences(BaseModel):
    user_id: str
    preferences: list

@app.post("/add_user_preferences/")
async def add_user_preferences(user: UserPreferences):
    tour_graph.create_or_update_user_preferences(user.user_id, user.preferences)
    return {"message": "User preferences added successfully."}

@app.post("/update_user_preferences/")
async def update_user_preferences(user: UserPreferences):
    tour_graph.update_preferences(user.user_id, user.preferences)
    return {"message": "User preferences updated successfully."}

@app.get("/get_user_preferences/{user_id}")
async def get_user_preferences(user_id: str):
    preferences = tour_graph.retrieve_preferences(user_id)
    return {"preferences": preferences}
