# Athlete Sprint Analyzer

The **Athlete Sprint Analyzer** is a web application designed to help sprinters and coaches analyze 100m sprint performance through time-based splits. It evaluates three key physical attributes—**Explosiveness**, **Endurance**, and **Strength**—and provides tailored feedback and suggestions.

## Features

- **User Registration/Login** system
- **Run Analysis** based on:
  - Acceleration Phase (T1)
  - Max Velocity Phase (T2)
  - Sub-Max Velocity Phase (T3)
- **Automatic Calculation** of:
  - Explosiveness
  - Endurance
  - Strength
- **Category Classification**:
  - Beginner, Intermediate, Pro, Elite
- **Feedback Generation** with performance tips
- **Run History Dashboard** with charts
- **ML Application**:
  - Linear Regression model used to predict T1 and T2 from total time

## How It Works

- The user enters their sprint phase timings (or total time).
- The system calculates:
  - **Explosiveness**: based on constant acceleration in T1
  - **Endurance**: based on velocity retention in T2
  - **Strength**: based on speed decline in T3
- Based on thresholds, feedback and training suggestions are provided.

## Technologies Used

- **Frontend**: HTML, CSS, Chart.js
- **Backend**: Python (Flask)
- **Database**: SQLite
- **ML**: Scikit-learn (Linear Regression)
- **Hosting/Environment**: Local Flask server

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python backend/app.py
   ```

## Folder Structure

```
athlete_tracker_project_final/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── model_utils.py
│   ├── models/
│   │   ├── t1_model.pkl
│   │   └── t2_model.pkl
│   ├── templates/
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── result.html
│   └── static/
│       ├── style.css
│       └── chart.js
```

## License

This project is for educational use only.
