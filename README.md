Planetarium API Service 🌌

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
pip install -r requirements.xtx

3. Configure Environment
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
docker should be installed
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
![image](https://github.com/user-attachments/assets/b07db50a-bfb1-4de4-bc1a-0bad722631b2)


🐳 Docker Commands Cheat Sheet
Command	Description
docker-compose up -d	Start containers
docker-compose down	Stop containers
docker-compose logs -f web	View Django logs
docker-compose exec web bash	Enter container shell
docker-compose restart db	Restart PostgreSQL
