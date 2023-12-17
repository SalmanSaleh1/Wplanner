

WPlanner is a weather planning application that allows users to schedule events based on weather conditions. This project is the final IT492 project, showcasing practical application of concepts learned in class.

## Technologies Used
- Flask
- AJAX
- MongoDB
- Open-Meteo API

## Bug Description: Date Input Issue

Users inputting a date along with a place experience a bug where the Open-Meteo API fetches weather data only for the current day at the specified place, ignoring the provided date. This leads to inaccurate weather information for planned events.

## Getting Started

Follow these steps to set up and run the project:

1. Ensure you have Docker installed on your machine.

2. Ensure you start Docker.

3. Open a terminal and navigate to the project directory.

4. Run the following commands(or run start.sh file):

   ```bash
   docker-compose down
   docker-compose up --build
   
This will start the application.

Open your web browser and go to http://localhost:5000 to access WPlanner.

## Author
Salman Saleh Alkhalifah