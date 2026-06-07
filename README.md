# Repository Name
cars-dealership

# Project Name
Cars Dealership

Cars Dealership is a full-stack web application for a national car retailer in the United States.

The application allows users to:
- View all dealerships
- Filter dealerships by state
- Register and log in
- View dealer details
- Read customer reviews
- Submit new reviews
- Analyze review sentiment

## Technologies
- Django
- React
- Flask
- Node.js
- SQLite
- GitHub Actions
- Docker
- Kubernetes
- IBM Cloud Code Engine

## Run locally
```bash
cd server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Optional microservices:
```bash
cd nodeapp && npm install && npm start
cd flaskapp && pip install -r requirements.txt && python app.py
```
