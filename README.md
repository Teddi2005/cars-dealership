# Cars Dealership

Cars Dealership is a full-stack web application for a national car retailer in the United States.

The application allows users to view dealerships, filter dealerships by state, register, log in, read customer reviews, submit new reviews, and view sentiment analysis for reviews.

## Features

- View all dealerships
- Filter dealerships by state
- View dealer details by dealer ID
- Register and log in
- Add a customer review
- Display positive, negative, or neutral sentiment for reviews
- REST API endpoints for dealers, reviews, cars, and sentiment
- Django-only fallback endpoints so the application can run from one server on port 8000

## Technologies Used

- Django
- React
- Node.js
- Express
- Flask
- SQLite
- Bootstrap
- GitHub Actions
- Docker
- IBM Cloud / Code Engine

## Project Structure

```text
cars-dealership/
├── server/
│   ├── carsdealership/
│   ├── djangoapp/
│   └── frontend/
├── nodeapp/
├── flaskapp/
└── .github/workflows/
```

## Run Locally

```bash
cd server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Open:

```text
http://localhost:8000/djangoapp/
```

## Important Endpoints

```text
/djangoapp/
/djangoapp/login
/djangoapp/register
/djangoapp/get_dealers
/djangoapp/get_dealers/Kansas
/djangoapp/dealer/3
/djangoapp/review/3
/djangoapp/get_cars
/fetchDealers
/fetchDealers/Kansas
/fetchDealer/3
/fetchReviews
/fetchReviews/dealer/3
/analyze/Excellent service
```

## Deployment

The Django app can be deployed on Render, IBM Cloud Code Engine, or CognitiveClass Cloud IDE proxy.

Example CognitiveClass proxy format:

```text
https://xxxxx-8000.proxy.cognitiveclass.ai
```

## Author

Hòa Vũ
