# Netflix Homepage Clone (Django + React)

A Netflix-style browsing page: hero banner, scrollable category rows, hover
cards, and a detail modal. Data comes from the free **TVMaze** API, so **no API
key or signup is needed**.

- Backend: Django + Django REST Framework (SQLite)
- Frontend: React + Vite + Axios
- The React app only talks to the Django API, never to TVMaze directly.

## Setup (Windows)

### 1. Backend (Terminal 1)

```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py sync_catalog
python manage.py runserver
```

`sync_catalog` downloads shows from TVMaze into your local database. Re-run it
any time to refresh the data (it updates existing shows instead of duplicating).
Use `python manage.py sync_catalog --pages 4` to fetch more shows (250 per page).

The API runs at http://localhost:8000/api/

### 2. Frontend (Terminal 2)

```bat
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

The backend URL is set in `frontend/.env` (`VITE_API_BASE_URL`).

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/homepage/` | Hero title + all rows (one call on page load) |
| `GET /api/titles/<id>/` | Full details for the modal (404 if not found) |
| `GET /api/search/?q=text` | Search by name or genre (400 if `q` is empty) |

## Admin (optional)

```bat
python manage.py createsuperuser
```

Then visit http://localhost:8000/admin/ to view or edit titles and categories.

## Tests

```bat
cd backend
python manage.py test
```

## Project structure

```
backend/
  config/                      settings, urls
  catalog/
    models.py                  Title, Category (many-to-many)
    serializers.py, views.py, urls.py, admin.py, tests.py
    management/commands/sync_catalog.py
frontend/
  src/
    components/                Navbar, HeroBanner, Row, PosterCard,
                               TitleModal, Loading, ErrorState
    services/api.js            single Axios instance
    App.jsx, App.css
```

## Notes

- TVMaze only provides portrait posters, so the hero shows a blurred copy as the
  background with the sharp poster beside the text.
- "Play" opens the show's official website when TVMaze has one.
- Posters and summaries come from TVMaze; this project is for learning only.
