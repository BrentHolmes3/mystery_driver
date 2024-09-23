from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import random
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

df = pd.read_excel('./driver_data_base.xlsx')

# Store the state in a dictionary
state = {
    "mystery_driver": random.choice(df['driver']),
    "attempts": 0,
    "output": []
}

state["mystery_driver_number"] = df.loc[df['driver'] == state["mystery_driver"], 'car_number'].values[0]
state["mystery_driver_start_year"] = df.loc[df['driver'] == state["mystery_driver"], 'start year'].values[0]
state["mystery_driver_birth_year"] = df.loc[df['driver'] == state["mystery_driver"], 'birth year'].values[0]
state["mystery_driver_flag"] = df.loc[df['driver'] == state["mystery_driver"], 'flag'].values[0]
state["mystery_driver_team"] = df.loc[df['driver'] == state["mystery_driver"], 'team'].values[0]
state["mystery_driver_wins"] = df.loc[df['driver'] == state["mystery_driver"], 'wins'].values[0]

def run_mystery_driver(driver: str):
    entered_driver = driver
    response = {}

    if entered_driver == 'Random' or entered_driver == 'random':
        entered_driver = random.choice(df['driver'])
    if entered_driver in df['driver'].values:
        state["attempts"] += 1
        mystery_driver_past_teams_list = []
        # mystery_driver_past_teams_list = df.loc[df['driver'] == state["mystery_driver"], 'wins'].values[0].split(',')
        if entered_driver == state["mystery_driver"]:
            response["message"] = state["output"] + [f"It is {state["mystery_driver"]}!. {state["mystery_driver_number"]}. {state["mystery_driver_birth_year"]}. {state["mystery_driver_start_year"]}. {state["mystery_driver_wins"]}. {state["mystery_driver_flag"]}. {state["mystery_driver_team"]}."] + ["YOU WIN!"]
            state["attempts"] = 0  # Reset the attempts
            state["mystery_driver"] = random.choice(df['driver'])  # Pick a new mystery driver
            state["mystery_driver_number"] = df.loc[df['driver'] == state["mystery_driver"], 'car_number'].values[0]
            state["mystery_driver_start_year"] = df.loc[df['driver'] == state["mystery_driver"], 'start year'].values[0]
            state["mystery_driver_birth_year"] = df.loc[df['driver'] == state["mystery_driver"], 'birth year'].values[0]
            state["mystery_driver_flag"] = df.loc[df['driver'] == state["mystery_driver"], 'flag'].values[0]
            state["mystery_driver_team"] = df.loc[df['driver'] == state["mystery_driver"], 'team'].values[0]
            state["mystery_driver_wins"] = df.loc[df['driver'] == state["mystery_driver"], 'wins'].values[0]
            state["output"] = []  # Clear the output
        elif state["attempts"] < 6:
            entered_driver_number = df.loc[df['driver'] == entered_driver, 'car_number'].values[0]
            if entered_driver_number > state["mystery_driver_number"]:
                higher_equal_lower_number = "Less than"
            elif entered_driver_number < state["mystery_driver_number"]:
                higher_equal_lower_number = "Greater than"
            else:
                higher_equal_lower_number = ""
            entered_driver_birth_year = df.loc[df['driver'] == entered_driver, 'birth year'].values[0]
            if entered_driver_birth_year > state["mystery_driver_birth_year"]:
                before_after_by = "Before"
            elif entered_driver_birth_year < state["mystery_driver_birth_year"]:
                before_after_by = "After"
            else:
                before_after_by = ""
            entered_driver_start_year = df.loc[df['driver'] == entered_driver, 'start year'].values[0]
            if entered_driver_start_year > state["mystery_driver_start_year"]:
                before_after_sy = "Before"
            elif entered_driver_start_year < state["mystery_driver_start_year"]:
                before_after_sy = "After"
            else:
                before_after_sy = ""
            entered_driver_wins = df.loc[df['driver'] == entered_driver, 'wins'].values[0]
            if entered_driver_wins > state["mystery_driver_wins"]:
                higher_equal_lower_wins = "Fewer than"
            elif entered_driver_wins < state["mystery_driver_wins"]:
                higher_equal_lower_wins = "More than"
            else:
                higher_equal_lower_wins = ""
            entered_driver_flag = df.loc[df['driver'] == entered_driver, 'flag'].values[0]
            if entered_driver_flag == state["mystery_driver_flag"]:
                flag_words = ""
            else:
                flag_words = "Not"
            entered_driver_team = df.loc[df['driver'] == entered_driver, 'team'].values[0]
            if entered_driver_team == state["mystery_driver_team"]:
                team_words = ""
            elif entered_driver_team in mystery_driver_past_teams_list:
                team_words = "Previously"
            else:
                team_words = "Not"
            state["output"] = state["output"] + [f"Not {entered_driver}. {higher_equal_lower_number} {entered_driver_number}. {before_after_by} {entered_driver_birth_year}. {before_after_sy} {entered_driver_start_year}. {higher_equal_lower_wins} {entered_driver_wins}. {flag_words} {entered_driver_flag}. {team_words} {entered_driver_team}."]
            response["message"] = state["output"]
        else:
            entered_driver_number = df.loc[df['driver'] == entered_driver, 'car_number'].values[0]
            if entered_driver_number > state["mystery_driver_number"]:
                higher_equal_lower_number = "Less than"
            elif entered_driver_number < state["mystery_driver_number"]:
                higher_equal_lower_number = "Greater than"
            else:
                higher_equal_lower_number = ""
            entered_driver_birth_year = df.loc[df['driver'] == entered_driver, 'birth year'].values[0]
            if entered_driver_birth_year > state["mystery_driver_birth_year"]:
                before_after_by = "Before"
            elif entered_driver_birth_year < state["mystery_driver_birth_year"]:
                before_after_by = "After"
            else:
                before_after_by = ""
            entered_driver_start_year = df.loc[df['driver'] == entered_driver, 'start year'].values[0]
            if entered_driver_start_year > state["mystery_driver_start_year"]:
                before_after_sy = "Before"
            elif entered_driver_start_year < state["mystery_driver_start_year"]:
                before_after_sy = "After"
            else:
                before_after_sy = ""
            entered_driver_wins = df.loc[df['driver'] == entered_driver, 'wins'].values[0]
            if entered_driver_wins > state["mystery_driver_wins"]:
                higher_equal_lower_wins = "Fewer than"
            elif entered_driver_wins < state["mystery_driver_wins"]:
                higher_equal_lower_wins = "More than"
            else:
                higher_equal_lower_wins = "="
            entered_driver_flag = df.loc[df['driver'] == entered_driver, 'flag'].values[0]
            if entered_driver_flag == state["mystery_driver_flag"]:
                flag_words = ""
            else:
                flag_words = "Not"
            entered_driver_team = df.loc[df['driver'] == entered_driver, 'team'].values[0]
            if entered_driver_team == state["mystery_driver_team"]:
                team_words = ""
            elif entered_driver_team in mystery_driver_past_teams_list:
                team_words = "Previously"
            else:
                team_words = "Not"
            response["message"] = state["output"] + [f"Not {entered_driver}. {higher_equal_lower_number} {entered_driver_number}. {before_after_by} {entered_driver_birth_year}. {before_after_sy} {entered_driver_start_year}. {higher_equal_lower_wins} {entered_driver_wins}. {flag_words} {entered_driver_flag}. {team_words} {entered_driver_team}."] + [f"You have lost."] + [f"The answer was {state['mystery_driver']}. {state["mystery_driver_number"]}. {state["mystery_driver_birth_year"]}. {state["mystery_driver_start_year"]}. {state["mystery_driver_wins"]}. {state["mystery_driver_flag"]}. {state["mystery_driver_team"]}."]
            state["attempts"] = 0  # Reset the attempts
            state["mystery_driver"] = random.choice(df['driver'])  # Pick a new mystery driver
            state["mystery_driver_number"] = df.loc[df['driver'] == state["mystery_driver"], 'car_number'].values[0]
            state["mystery_driver_start_year"] = df.loc[df['driver'] == state["mystery_driver"], 'start year'].values[0]
            state["mystery_driver_birth_year"] = df.loc[df['driver'] == state["mystery_driver"], 'birth year'].values[0]
            state["mystery_driver_flag"] = df.loc[df['driver'] == state["mystery_driver"], 'flag'].values[0]
            state["mystery_driver_team"] = df.loc[df['driver'] == state["mystery_driver"], 'team'].values[0]
            state["mystery_driver_wins"] = df.loc[df['driver'] == state["mystery_driver"], 'wins'].values[0]
            state["output"] = []  # Clear the output
    else:
        response["message"] = state["output"] +["Not a driver."]
    return response

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, driver: Optional[str] = None):
    result = run_mystery_driver(driver) if driver is not None else None
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "results": state["output"]})

@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request):
    try:
        form_data = await request.form()
        driver = form_data.get("driver")
        if driver is None:
            return templates.TemplateResponse("index.html", {"request": request, "error": "Missing value for driver."})
        result = run_mystery_driver(driver)
        return templates.TemplateResponse("index.html", {"request": request, "result": result, "results": state["output"]})
    except ValueError:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid driver."})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})
