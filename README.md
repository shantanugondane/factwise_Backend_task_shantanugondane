# Credentials for django dashboard login

username:- shantanugondane
password:- Shantanu@1234

# Explanation Video

[Explanation Vidon Click Here](https://drive.google.com/drive/folders/1CzWZTtvbt25fnqPxW-WkTRMGySeX4lwU?usp=sharing)

# Team Project Planner

A Django-based implementation of a team project planner tool that provides APIs for managing users, teams, and project boards.

## Features

- User Management
  - Create, list, describe, and update users
  - View teams associated with a user
- Team Management
  - Create, list, describe, and update teams
  - Add/remove users from teams
  - List team members
- Project Board Management
  - Create and close boards
  - Add tasks to boards
  - Update task status
  - List boards for a team
  - Export board details

## Technical Choices

1. **Django & Django REST Framework**

   - Chosen for robust API development
   - Built-in admin interface
   - Excellent ORM for database operations
   - Strong security features

2. **JSON File Storage**

   - Using JSON files in the `db` directory for persistence
   - Simple and portable solution
   - Easy to backup and version control
   - No database setup required

3. **Project Structure**
   - Modular design with separate apps for users, teams, and boards
   - Clear separation of concerns
   - Easy to maintain and extend

## Setup Instructions

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API endpoints follow RESTful conventions and are documented in the respective view files. All requests and responses are in JSON format.

## Assumptions

1. User names and team names are case-sensitive for uniqueness
2. All timestamps are stored in UTC
3. Maximum team size is capped at 50 users
4. Board names must be unique within a team
5. Task titles must be unique within a board
6. Only team admins can modify team details and manage team members
7. Only board owners can close boards
8. Tasks can only be added to open boards
