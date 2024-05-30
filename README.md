# Movie Recommendation System

This project is a movie recommendation system designed to help users discover new movies based on their preferences. It is developed as an assignment for the Programming for Data Science course.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Description

The Movie Recommendation System allows users to input movies they have watched along with their ratings and preferences such as favorite genres, actors, or directors. Based on this input, the system recommends new movies that align with the user's tastes.

## Features

- **Movie Input and Preferences**: Users can input movies they have watched along with ratings, and specify their favorite genres, actors, or directors.
- **Recommendation Algorithm**: The system employs a basic recommendation algorithm to suggest new movies based on user preferences and ratings.
- **Data Visualization**: Users can visualize their movie data with breakdowns by genre, actor, or director, enabling them to analyze trends in their preferences.

## Installation

To run the Movie Recommendation System locally, follow these steps:

1. Ensure Python and pip are installed:
   * Download and install Python from the official website: Python.org
   * Ensure pip (Python package installer) is installed. It usually comes with Python. You can verify the installation by running python --version and pip --version in your terminal.
2. Ensure Git is installed:
   * Download and install Git from the official website: Git-scm.com
   * Verify the installation by running git --version in your terminal.
3. Clone the repository: `git clone https://github.com/PythonDataScience24/group_27_movie_recom.git`
4. Navigate to the project directory: `cd group_27_movie_recom`
5. Install dependencies: `pip install -r requirements.txt`
6. Remove lines 294-297 in `MovieRecom\env\Lib\site-packages\kivy_garden\matplotlib\backend_kivy.py`

## Usage

1. Input movies you have watched along with ratings using the provided interface.
2. Optionally specify your favorite genres, actors, or directors.
3. Receive personalized movie recommendations based on your input.
4. Explore visualizations to analyze trends in your movie preferences.