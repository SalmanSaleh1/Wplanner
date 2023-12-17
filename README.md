# ![logo (2)](https://github.com/SalmanSaleh1/Wplanner/assets/138271238/0c739b81-1d90-48d4-bcaa-aaf309006531)


WPlanner is a weather planning application that allows users to schedule events based on weather conditions. This project is the final for the university course, showcasing practical application of concepts learned in class.

## Technologies Used
- Flask
- AJAX
- MongoDB
- Open-Meteo API

## Bugs Description: 
### Date Input Issue
Users inputting a date along with a place experience a bug where the Open-Meteo API fetches weather data only for the current day at the specified place, ignoring the provided date. This leads to inaccurate weather information for planned events.

### Plan Deletion Issue
Adding weather plans to the table results in the deletion of other plans with the same date. This prevents users from adding multiple plans on the same day.

**Expected Behavior:**
Accurate weather information should be fetched for the user-specified date and place. Users should be able to add multiple plans on the same day without deletion issues.


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
