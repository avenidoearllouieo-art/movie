# Movie Collection REST API

This Django project implements a versioned REST API for managing a movie collection. It was created as part of a laboratory exercise on *Design and Implement a Versioned REST API*, where the chosen domain was movies.

## 📌 Project Overview

- **Concept**: A movie database allowing clients to perform CRUD operations on movies, reviews, user ratings and comments.
- **Versioning**: API versioning is handled via the URL path (`/api/v1/...`).
- **Technology stack**: Django 6.0, Django REST Framework, drf-spectacular for schema generation.
- **Database**: SQLite (used for development).

## 🔗 Endpoints (v1)

- `/api/v1/movies/` – list, create, retrieve, update, delete movies
- `/api/v1/reviews/` – list and manage reviews; `?movie_id=` filter available
- `/api/v1/ratings/` – list and manage user ratings; `?movie_id=` filter available
- `/api/v1/comments/` – list and manage comments; can filter by `movie_id` or `review_id`

Each viewset exposes additional actions:

- `movies/{id}/average_rating/` – GET average user rating for a movie
- `reviews/{id}/mark_helpful/` – POST to increment helpful count

The DRF router handles registration of these endpoints automatically (`movies/urls.py`).

## 🧠 Design Notes

- **Models** include `Movie`, `Review`, `Rating`, and `Comment`. Relationships use `ForeignKey` with `related_name` for easy reverse access.
- **Serializers** implement field validation (e.g. rating bounds, release year not in future) and nested serializers for reviews/comments/ratings.
- **Versioning** uses `URLPathVersioning` configured in `settings.py`. The tests and router configuration reflect this.
- **Administration**: admin classes are defined in `movies/admin.py` with helpful search fields and display options.
- **Homepage**: basic template at `movies/templates/movies/homepage.html` showing movie stats.

## 🛠️ Extending the Lab

Additional non‑disruptive enhancements you could commit:

1. **Expand automated tests** (`movies/tests.py`) to cover all endpoints, validations and custom actions.
2. **Add documentation** or comments explaining the versioning strategy and lab goal.
3. **Provide fixtures or sample data** for quick setup in development.
4. **Enhance the homepage template** with styling or more details about the API.
5. **Add a `README`** (this file) summarizing the project and linking back to the lab instructions.

## 🚀 Running the Project

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```
4. Access the API at `http://localhost:8000/api/v1/` or visit the Django admin at `/admin/`.

## 📚 References

- Laboratory description: `Laboratory 4: Design and Implement a Versioned REST API` (PDF)
- DRF documentation: https://www.django-rest-framework.org/
- drf-spectacular: https://drf-spectacular.readthedocs.io/

---

> This project structure and API design were generated and extended during the course of the lab activity.
