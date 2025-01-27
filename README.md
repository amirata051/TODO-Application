# TODO Application

## Overview

TODO Application is a Django-based project designed to manage tasks efficiently. The application includes features such as task creation, updating, deletion, filtering, searching, and ordering. It also provides a fully documented API using Swagger and ReDoc for seamless integration with other systems.

---

## Features

- Create, update, delete, and retrieve tasks.
- Filter tasks by completion status, due date, or creation date.
- Search tasks by title or description.
- Order tasks by due date or creation date.
- API documentation with Swagger and ReDoc.
- Dockerized for easy deployment.
- Continuous Integration (CI) setup using GitHub Actions.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.12+
- Docker (optional, for containerized deployment)
- Git

---

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/amirata051/TODO-Application.git
   cd TODO-Application
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000`.

---

## Using Docker

1. Build the Docker image:
   ```bash
   docker build -t todo-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 todo-app
   ```

3. Access the application at `http://localhost:8000`.

---

## Running Tests

The project includes automated tests to ensure functionality.

1. Run tests:
   ```bash
   python manage.py test
   ```

2. Check test coverage (optional):
   ```bash
   coverage run manage.py test
   coverage report
   ```

---

## CI/CD

The project uses GitHub Actions for Continuous Integration:

- Automated testing on each commit.
- Code linting with `flake8`.

No Continuous Deployment (CD) has been configured at this stage.

---

## API Documentation

The project includes a fully documented API available at the following endpoints:

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

---

## Technologies Used

- **Django**: Web framework for the backend.
- **Django REST Framework**: API development.
- **drf-yasg**: API documentation.
- **Docker**: Containerization.
- **GitHub Actions**: Continuous Integration.

---

## Future Improvements

- Adding user authentication (e.g., JWT-based).
- Implementing Continuous Deployment (CD).
- Enhancing API security and rate-limiting.

---

## Contribution

Contributions are welcome! Please fork the repository and create a pull request for any feature or bug fix.

---

## License

This project is licensed under the BSD License. See the LICENSE file for more details.

