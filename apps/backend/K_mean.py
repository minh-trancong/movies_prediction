import matplotlib
from flask import Flask, render_template, request
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from apps import db
from apps.authentication.models import Movies
from sqlalchemy import func
import io
import base64

def euclid(x1, x2):
    # Calculate the Euclidean distance between two points
    distance = 0.0
    for i in range(len(x1)): # both x1, x2: budget, rating, runtime
        distance += (x1[i] - x2[i]) ** 2 # i dont' use sqrt here because there is no need to check for the distance, we only need to compare distance
    return distance

def predict_gross(genre, budget, rating, runtime):
    # Get movies data filtered by genre
    movies = Movies.query.filter_by(genre=genre).all()

    # Load the data read from the database to the data array
    data = [(movie.budget, movie.rating, movie.runtime, movie.gross) for movie in movies]

    # Calculate the Euclidean distance between the input features and each data point
    distances = []
    for val in data:
        x = val[:-1]  # Features (budget, rating, runtime) || ": -1" all columns except the last one (gross)
        y = val[-1]   # Target variable (gross) || last column
        distance = euclid([budget, rating, runtime], x) # first is the data from the movie need to compare, x is data from database
        distances.append((x, y, distance))

    # sort the [2] element (distance) in ascending order
    distances.sort(key=lambda z: z[2])

    k = 5 # set k for the below calculation

    # Select the k nearest neighbors
    neighbors = distances[:k] # take the first 5 shortest distance

    # Calculate the average gross of the k nearest neighbors
    total_gross = sum(neighbor[1] for neighbor in neighbors)
    predicted_gross = total_gross / k   # we set the predict one to be the average of the 5 closest
    return predicted_gross

def calculate_average_values(genre):
    average_gross = db.session.query(func.avg(Movies.gross)).filter_by(genre=genre).scalar()
    average_budget = db.session.query(func.avg(Movies.budget)).filter_by(genre=genre).scalar()
    return average_gross, average_budget

def list_genres():
    # Get unique genres from the database
    genres = db.session.query(Movies.genre.distinct()).all()
    genre_data = []
    for genre in genres:
        genre_name = genre[0]
        average_gross, average_budget = calculate_average_values(genre_name)
        average_ratio = average_gross / average_budget
        genre_data.append({"genre": genre_name, "average_ratio": average_ratio})

    # Sort genre_data by average_ratio in descending order
    genre_data.sort(key=lambda x: x["average_ratio"], reverse=True)
    return genre_data


def statistic():
    # Get movies data filtered by genre
    list_genres()
    genre = input("Enter genre: ")

    # Get budget and gross data for the selected genre
    data = db.session.query(Movies.budget, Movies.gross).filter_by(genre=genre).all()

    # Separate budget and gross into separate lists
    budget = [val[0] for val in data]
    gross = [val[1] for val in data]

    # Convert budget and gross lists to numpy arrays
    budget = np.array(budget).reshape(-1, 1)
    gross = np.array(gross)

    # Fit a linear regression model, aka: redline
    regression_model = LinearRegression()
    regression_model.fit(budget, gross)

    # Generate predicted values for the regression line
    predicted_gross = regression_model.predict(budget)

    # Plot budget vs gross
    plt.scatter(budget, gross)
    plt.xlabel("Budget")
    plt.ylabel("Gross")
    plt.title(f"Budget vs Gross for Genre: {genre}")

    # label axis
    budget_ticks = [tick / 10000000 for tick in plt.xticks()[0]]
    gross_ticks = [tick / 10000000 for tick in plt.yticks()[0]]
    plt.xticks(plt.xticks()[0], ['${:.1f}M'.format(tick) for tick in budget_ticks])
    plt.yticks(plt.yticks()[0], ['${:.2f}M'.format(tick) for tick in gross_ticks])

    # Plot the regression line
    plt.plot(budget, predicted_gross, 'r-', label='Regression Line')
    plt.show()

def menu():
    while True:
        print("Menu:")
        print("1. Statistical Analysis")
        print("2. Gross Prediction")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            statistic()
            break
        elif choice == "2":
            list_genres()
            genre = input("Enter genre: ")
            budget = int(input("Enter budget: "))
            rating = float(input("Enter rating: "))
            if (rating > 10 or rating < 0):
                print("Rating is between 0.0 and 10.0, please try again")
                exit()
            runtime = int(input("Enter runtime: "))
            predicted_gross = predict_gross(genre, budget, rating, runtime)
            print(f"The predicted gross for a movie with genre={genre}, budget={budget}, rating={rating}, and runtime={runtime} days, is around ${predicted_gross:.2f}")
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
def generate_statistic_data(genre):
    # Get budget and gross data for the selected genre
    data = db.session.query(Movies.budget, Movies.gross).filter_by(genre=genre).all()

    # Separate budget and gross into separate lists
    budget = [val[0] for val in data]
    gross = [val[1] for val in data]

    # Convert budget and gross lists to numpy arrays
    budget = np.array(budget).reshape(-1, 1)
    gross = np.array(gross)

    # Fit a linear regression model
    regression_model = LinearRegression()
    regression_model.fit(budget, gross)

    # Generate predicted values for the regression line
    predicted_gross = regression_model.predict(budget)

    return budget, gross, predicted_gross


def generate_plot_url(genre):
    budget, gross, predicted_gross = generate_statistic_data(genre)

    # Create a figure and axis with higher resolution
    fig, ax = plt.subplots(dpi=300)

    # Plot budget vs gross
    ax.scatter(budget, gross)
    ax.set_xlabel("Budget")
    ax.set_ylabel("Gross")
    ax.set_title(f"Budget vs Gross for Genre: {genre}")

    # Label axis
    budget_ticks = [tick / 10000000 for tick in ax.get_xticks()]
    gross_ticks = [tick / 10000000 for tick in ax.get_yticks()]
    ax.set_xticklabels(['${:.1f}M'.format(tick) for tick in budget_ticks])
    ax.set_yticklabels(['${:.2f}M'.format(tick) for tick in gross_ticks])

    # Plot the regression line
    ax.plot(budget, predicted_gross, 'r-', label='Regression Line')

    # Adjust the layout to prevent labels from overflowing
    plt.tight_layout()

    # Save the plot to a BytesIO object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # Encode the image as base64 string
    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Create the URL for the base64 image
    plot_url = f"data:image/png;base64,{encoded_image}"

    return plot_url