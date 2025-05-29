import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


def create_user():
    response = requests.post(
        f"{BASE_URL}/users/", json={"name": "john_doe", "display_name": "John Doe"}
    )
    print("Created user:", response.json())
    return response.json()["id"]


def create_team(user_id):
    response = requests.post(
        f"{BASE_URL}/teams/",
        json={
            "name": "development_team",
            "description": "Main development team",
            "admin": user_id,
        },
    )
    print("Created team:", response.json())
    return response.json()["id"]


def create_board(team_id):
    response = requests.post(
        f"{BASE_URL}/boards/boards/",
        json={"name": "sprint_1", "description": "Sprint 1 tasks", "team": team_id},
    )
    print("Created board:", response.json())
    return response.json()["id"]


def create_task(board_id, user_id):
    response = requests.post(
        f"{BASE_URL}/boards/tasks/",
        json={
            "title": "Implement login feature",
            "description": "Create user authentication system",
            "board": board_id,
            "assigned_to": user_id,
        },
    )
    print("Created task:", response.json())
    return response.json()["id"]


def main():
    # Create a user
    user_id = create_user()

    # Create a team with the user as admin
    team_id = create_team(user_id)

    # Create a board for the team
    board_id = create_board(team_id)

    # Create a task on the board
    task_id = create_task(board_id, user_id)

    print("\nCreated resources:")
    print(f"User ID: {user_id}")
    print(f"Team ID: {team_id}")
    print(f"Board ID: {board_id}")
    print(f"Task ID: {task_id}")


if __name__ == "__main__":
    main()
