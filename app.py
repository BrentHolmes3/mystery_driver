import pandas as pd
import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

df = pd.read_excel('./driver_data_base.xlsx')

import difflib

def find_closest_matches(drivers_list, user_input, n=3):
    if user_input is None or not isinstance(user_input, str):
        return []

    drivers_column = [driver for driver in drivers_list if driver is not None]
    closest_matches = difflib.get_close_matches(user_input, drivers_column, n=n, cutoff=0.6)
    return closest_matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mystery_driver', methods=['POST'])
def check_mystery_driver():
    # Get the JSON data from the POST request
    data = request.json

    # Randomly pick the mystery driver
    mystery_driver = random.choice(df['driver'])
    i = 0
    response = {}

    while i < 6:
        entered_driver = data.get('entered_driver')

        if entered_driver in df['driver'].values:
            if entered_driver == mystery_driver:
                response['result'] = "You win!"
                break
            else:
                i += 1
                # Look up the row for the entered driver
                entered_driver_row = df[df['driver'] == entered_driver].iloc[0]

                # Compare the attributes
                response['Flag'] = f"{'not ' if entered_driver_row['flag'] != df[df['driver'] == mystery_driver]['flag'].iloc[0] else ''}{entered_driver_row['flag']}"
                response['Team'] = f"{'not ' if entered_driver_row['team'] != df[df['driver'] == mystery_driver]['team'].iloc[0] else ''}{entered_driver_row['team']}"
                response['Car number'] = f"{'greater than' if entered_driver_row['car_number'] < df[df['driver'] == mystery_driver]['car_number'].iloc[0] else 'less than' if entered_driver_row['car_number'] > df[df['driver'] == mystery_driver]['car_number'].iloc[0] else ''} {entered_driver_row['car_number']}"
                response['Wins'] = f"{'greater than' if entered_driver_row['wins'] < df[df['driver'] == mystery_driver]['wins'].iloc[0] else 'fewer than' if entered_driver_row['wins'] > df[df['driver'] == mystery_driver]['wins'].iloc[0] else ''} {entered_driver_row['wins']}"
                response['Birth year'] = f"{'later than' if entered_driver_row['birth year'] < df[df['driver'] == mystery_driver]['birth year'].iloc[0] else 'earlier than' if entered_driver_row['birth year'] > df[df['driver'] == mystery_driver]['birth year'].iloc[0] else ''} {entered_driver_row['birth year']}"
                response['Start year'] = f"{'later than' if entered_driver_row['start year'] < df[df['driver'] == mystery_driver]['start year'].iloc[0] else 'earlier than' if entered_driver_row['start year'] > df[df['driver'] == mystery_driver]['start year'].iloc[0] else ''} {entered_driver_row['start year']}"
        else:
            response['result'] = "The entered driver is not in the data frame."
            # Assuming 'drivers' is the column name in the CSV file
            drivers_column = df['driver'].tolist()
            # Find the closest matching entries
            closest_matches = find_closest_matches(drivers_column, entered_driver)
            response['closest_matches'] = closest_matches

    if i == 6:
        response['result'] = f"You have lost. The answer was {mystery_driver}"

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
