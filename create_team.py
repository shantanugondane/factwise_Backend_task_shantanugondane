import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


def create_team():
    # First, let's create a user who will be the team admin
    user_response = requests.post(
        f"{BASE_URL}/users/", json={"name": "team_admin", "display_name": "Team Admin"}
    )
    user_id = user_response.json()["id"]
    print(f"Created admin user with ID: {user_id}")

    # Now create the team
    team_response = requests.post(
        f"{BASE_URL}/teams/",
        json={
            "name": "new_team",
            "description": "A new team for project development",
            "admin": user_id,
        },
    )

    if team_response.status_code == 201:
        team_id = team_response.json()["id"]
        print(f"\nSuccessfully created team!")
        print(f"Team ID: {team_id}")
        print("\nYou can now:")
        print(f"1. View team details: {BASE_URL}/teams/{team_id}/")
        print(f"2. Add members: {BASE_URL}/teams/{team_id}/add_users/")
        print(f"3. Create a board: {BASE_URL}/boards/boards/")
    else:
        print("Error creating team:", team_response.json())


if __name__ == "__main__":
    create_team()
