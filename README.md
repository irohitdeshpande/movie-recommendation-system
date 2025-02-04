# Movie Recommendation System

This project is a Movie Recommendation System using content-based filtering. The system recommends movies to users based on the similarity of movie content such as genres, actors, directors, etc.

## Features

- Recommend movies based on content similarity
- User-friendly interface
- Easy to run locally and on Streamlit

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Movie_Recommendation.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Movie_Recommendation
    ```
3. Create a virtual environment using Anaconda:
    ```bash
    conda create --name venv python=3.12
    conda activate venv
    ```

## Running the App Locally

1. Ensure you have all dependencies installed.
2. Run the application:
    ```bash
    python app.py
    ```
3. Open your web browser and go to `http://localhost:8501` to access the app.

## Running the App on Streamlit

1. Ensure you have Streamlit installed:
    ```bash
    pip install streamlit
    ```
2. Run the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```
3. Streamlit will automatically open a new tab in your web browser with the app running.

## Deployment

This app is also deployed on Streamlit. You can access it [here](https://movie-recommendation-system-5q9abndpc2xx7tparpucu5.streamlit.app/).