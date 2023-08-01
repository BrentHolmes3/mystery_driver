import pandas as pd
import random
from fuzzywuzzy import process

df = pd.read_excel('./driver_data_base.xlsx')

def find_closest_matches(drivers_list, user_input, n=3):
    if user_input is None or not isinstance(user_input, str):
        return []

    drivers_column = [driver for driver in drivers_list if driver is not None]
    closest_matches = process.extract(user_input, drivers_column, limit=n)
    return [match[0] for match in closest_matches]

def main():
    # Randomly pick the mystery driver
    mystery_driver = random.choice(df['driver'])
    i = 0
    while(i < 6): 
        print("Enter a driver's name:")
        entered_driver = input()
    
        if entered_driver in df['driver'].values:
            if entered_driver == mystery_driver:
                print("You win!")
                i = 100
            else:
                i += 1
                # Look up the row for the entered driver
                entered_driver_row = df[df['driver'] == entered_driver].iloc[0]
        
                # Check if flag is the same
                if entered_driver_row['flag'] == df[df['driver'] == mystery_driver]['flag'].iloc[0]:
                    print(f"Flag is {entered_driver_row['flag']}.")
                else:
                    print(f"Flag is not {entered_driver_row['flag']}.")
                
                # Check if team is the same
                if entered_driver_row['team'] == df[df['driver'] == mystery_driver]['team'].iloc[0]:
                    print(f"Team is {entered_driver_row['team']}.")
                else:
                    print(f"Team is not {entered_driver_row['team']}.")
        
                # Compare Car number
                if entered_driver_row['car_number'] < df[df['driver'] == mystery_driver]['car_number'].iloc[0]:
                    print(f"Car number greater than {entered_driver_row['car_number']}.")
                elif entered_driver_row['car_number'] > df[df['driver'] == mystery_driver]['car_number'].iloc[0]:
                    print(f"Car number less than {entered_driver_row['car_number']}.")
                else:
                    print(f"Car number {entered_driver_row['car_number']}.")
        
                # Compare wins
                if entered_driver_row['wins'] < df[df['driver'] == mystery_driver]['wins'].iloc[0]:
                    print(f"Wins is greater than {entered_driver_row['wins']}.")
                elif entered_driver_row['wins'] > df[df['driver'] == mystery_driver]['wins'].iloc[0]:
                    print(f"Wins is fewer than {entered_driver_row['wins']}.")
                else:
                    print(f"Wins is {entered_driver_row['wins']}.")
        
        
                # Compare birth year
                if entered_driver_row['birth year'] < df[df['driver'] == mystery_driver]['birth year'].iloc[0]:
                    print(f"Birth year is later than {entered_driver_row['birth year']}.")
                elif entered_driver_row['birth year'] > df[df['driver'] == mystery_driver]['birth year'].iloc[0]:
                    print(f"Birth year is earlier than {entered_driver_row['birth year']}.")
                else:
                    print(f"Birth year is {entered_driver_row['birth year']}.")
            
                # Compare start year
                if entered_driver_row['start year'] < df[df['driver'] == mystery_driver]['start year'].iloc[0]:
                    print(f"Start year is later than {entered_driver_row['start year']}.")
                elif entered_driver_row['start year'] > df[df['driver'] == mystery_driver]['start year'].iloc[0]:
                    print(f"Start year is earlier than {entered_driver_row['start year']}.")
                else:
                    print(f"Start year is {entered_driver_row['start year']}.")
        else:
            print("The entered driver is not in the data frame.")
            # Assuming 'drivers' is the column name in the CSV file
            drivers_column = df['driver'].tolist()
            # Find the closest matching entries
            closest_matches = find_closest_matches(drivers_column, entered_driver)
            print("Did you mean?")
            for match in closest_matches:
                print(match)
    if i == 6:
        print(f"You have lost. The answer was {mystery_driver}")


if __name__ == "__main__":
    main()
