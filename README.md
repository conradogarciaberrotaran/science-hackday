# Conrado Garcia - Science hack-day project

## Rationale
_The user in this use-case is a health provider supply administrator._

After analysing the data provided in the dataset, I had the idea to present the data in a way that may provide some insight hard to see otherwise. 
Each "record" of the dataset contains some geographical information, such as state, city and R.U.C.A (Rural-Urban Commuting Area codes).
With this parameters, the idea of finding the most common procedures performed in a given state, aggregated by cities which fall inside a R.U.C.A range.
This could give the "user" the lead on which procedures should be prioritized on certain zones and distribute supplies accordingly.
For example: most common procedures in Rural Texas or the Metropolitan cities of New York.

## Pre-requisites
1. Have docker-compose installed
3. Have the public dataset from Centers for Medicare and Medicaid Services (CSV file, must be named _MUP_PHY_R21_P04_V10_D19_Prov_Svc.csv_)

## How to run for development
1. Git clone the repo
3. Make sure you're in a new virtualenv
3. Run `pip install -r requirements-dev.txt` 
4. Run `pytest` at the root of the project, all tests should pass
5. You're ready for development!

## How to run for production
1. Git clone the repo
2. Move the CSV to `app/data/MUP_PHY_R21_P04_V10_D19_Prov_Svc.csv`
3. At the root of the repo, run `docker-compose up --build -d`
4. To load data, run `docker-compose run api /code/load_data.sh`
5. Wait for the data to load, 1 million records should be added to the database
6. In your browser, go to http://localhost:8000/docs
7. In the OpenAPI interface, select the /procedure/ endpoint and click "Try it out"
8. Try different values for `state_abbreviation`, `min_ruca` and `max_ruca`
