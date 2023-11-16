# Calculator Project

A web-based application comprising a Django backend and React frontend, designed to perform basic calculations and maintain a history of user calculations.

Getting Started

## Installing and Running the Project

### Step 1: Clone the Repository

Clone the repository to your local machine:

    https://github.com/dtarg16/Calculator.git

    cd calculator-project

### Step 2: Docker Setup

Ensure Docker and Docker Compose are installed on your system. You can download them from the official Docker website.

### Step 3: Build and Run with Docker

In the root directory of the project, where the docker-compose.yml file is located, execute the following command:

    docker-compose up --build

This command will build the Docker images for both the Django backend and React frontend and start the containers.

### Step 4: Accessing the Application

The Django backend will be accessible at http://localhost:8000.

The React frontend will be accessible at http://localhost:3000.

Using the Application

Navigate to http://localhost:3000 in your browser to use the Calculator. You can perform calculations and, if logged in, view the history of your calculations.
