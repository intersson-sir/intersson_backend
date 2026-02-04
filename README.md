# Intersson Backend

Backend for the Intersson website built with Django and Django REST Framework.

## Setup

1.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Populate Industries**
    Initialize the 10 required industries:
    ```bash
    python manage.py populate_industries
    ```

5.  **Create Superuser (for Admin)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run Server**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

*   **Contact Form:** `POST /api/contact/discuss-project/`
*   **Industries:** `GET /api/subscriptions/industries/`
*   **Templates:** `GET /api/subscriptions/templates/?industry_id=X`
*   **Reviews (Submit):** `POST /api/reviews/reviews/`
*   **Reviews (List):** `GET /api/reviews/reviews/` (Only returns approved reviews)

## Admin

Access the admin panel at `/admin/` to manage submissions, templates, and reviews.
