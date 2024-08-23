import json
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


current_dir = dirname(abspath(__file__))
wellknown_path = join(current_dir, ".well-known")
historical_data = join(current_dir, "weather.json")

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory=wellknown_path), name="static")


# load historical json data and serialize it:
with open(historical_data, "r") as f:
    data = json.load(f)

@app.get('/')
def root():
    """
    Allows to open the API documentation in the browser directly instead of
    requiring to open the /docs path.
    """
    return RedirectResponse(url='/docs', status_code=301)


@app.get('/countries')
def countries():
    return list(data.keys())


@app.get('/countries/{country}/{city}/{month}')
def monthly_average(country: str, city: str, month: str):
    return data[country][city][month]

#return cities
@app.get('/countries/{country}')
def cities(country: str):
    return list(data[country].keys())

#return cities for all countries
@app.get('/cities')
def cities():
    cities = []
    for country in data:
        for city in data[country]:
            cities.append(city)
    return



# Generate the OpenAPI schema:
openapi_schema = app.openapi()
with open(join(wellknown_path, "openapi.json"), "w") as f:
    json.dump(openapi_schema, f)