# Diamond Club Dashboard

Welcome to the Diamond Club Dashboard repository! This project is a comprehensive dashboard developed for a client in Greece, tailored to provide a robust interface for managing customer interactions and insights effectively.

## Project Overview

The Diamond Club Dashboard is designed to streamline the operations of the Diamond Club by customizing the Django admin interface and providing REST APIs for app development teams. It features real-time data presentation and is hosted on PythonAnywhere, ensuring reliable access and performance.

## Features

- **Custom Django Admin Panel**: Enhanced Django admin interface for better management of the club's operations.
- **REST API Integration**: APIs developed to support external application interactions.
- **Real-Time Data Updates**: Ensure that all displayed data is current and accurately reflects the club's operations.

## Technologies Used

- **Django**: For the backend and customization of the admin panel.
- **Django REST Framework**: For creating RESTful APIs.
- **Bootstrap**: For styling and responsive design.
- **MySQL**: Used as the database for storing all application data.
- **PythonAnywhere**: Hosting platform to deploy the Django application.

## Local Setup

To get this project up and running locally on your machine, follow the steps below:

```bash
# Clone the repository
git clone https://github.com/anirudh1117/Diamond-club.git

# Navigate to the project directory
cd Diamond-club

# Install the required dependencies
pip install -r requirements.txt

# Apply the migrations
python manage.py migrate

# Run the server
python manage.py runserver
