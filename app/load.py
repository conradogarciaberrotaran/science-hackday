import csv
from itertools import islice

from tqdm import tqdm

from app.models import Base, Record, SessionLocal, engine

SIZE = 1_000_000


def load_data(path):
    # create table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    with open(path) as f:
        db_session = SessionLocal()
        reader = csv.DictReader(f)
        # Only loads SIZE rows in the database
        for row in tqdm(islice(reader, SIZE), total=SIZE):
            state_abbreviation = row["Rndrng_Prvdr_State_Abrvtn"]
            city = row["Rndrng_Prvdr_City"]
            country = row["Rndrng_Prvdr_Cntry"]
            ruca = row["Rndrng_Prvdr_RUCA"]
            procedure_code = row["HCPCS_Cd"]
            if all([state_abbreviation, city, country, ruca, procedure_code]):
                # doesn't add incomplete rows
                db_session.add(
                    Record(
                        state_abbreviation=state_abbreviation,
                        city=city,
                        country=country,
                        ruca=ruca,
                        procedure_code=procedure_code,
                    )
                )
        db_session.commit()


if __name__ == "__main__":
    load_data("app/data/MUP_PHY_R21_P04_V10_D19_Prov_Svc.csv")
