Planetarium API Service 🌌
https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white
https://img.shields.io/badge/django%2520rest-ff1709?style=for-the-badge&logo=django&logoColor=white

A RESTful API for managing planetarium shows, ticket bookings, and astronomical events.

🚀 Features
JWT Authentication (Access & Refresh tokens)

CRUD Operations for shows, sessions, and reservations

Automated Documentation (Swagger/OpenAPI via DRF Spectacular)

Dockerized PostgreSQL + Django development environment

Custom User Model with extended fields

Throttling for API endpoints

⚙️ System Requirements
Docker 20.10+

Docker Compose 2.5+

Python 3.11+

🛠️ Setup & Installation
1. Clone the Repository
bash
git clone https://github.com/YaroslavDidkiviskiy/planetarium-api-service.git
cd planetarium-api-service
2. Configure Environment
bash
cp .env.example .env
Edit .env with your credentials:

ini
POSTGRES_DB=planetarium
POSTGRES_USER=planetarium
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
3. Start Services
bash
docker-compose up --build -d
4. Apply Migrations
bash
docker-compose exec web python manage.py migrate
5. Create Superuser (Optional)
bash
docker-compose exec web python manage.py createsuperuser
📚 API Documentation
Access interactive docs after running the server:

Swagger UI: http://localhost:8000/api/schema/swagger-ui/

Redoc: http://localhost:8000/api/schema/redoc/

🗂 Project Structure
text
planetarium-api-service/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
├── manage.py
├── user/               # Custom user app
├── planetarium/        # Main app (shows, sessions)
└── media/              # Uploaded files
🐳 Docker Commands Cheat Sheet
Command	Description
docker-compose up -d	Start containers
docker-compose down	Stop containers
docker-compose logs -f web	View Django logs
docker-compose exec web bash	Enter container shell
docker-compose restart db	Restart PostgreSQL
