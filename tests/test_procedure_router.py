import pytest
from fastapi import status

from tests.factories import RecordFactory


@pytest.mark.parametrize("min_ruca, max_ruca", [(5, 3), (10, 2), (9, 1), (6.01, 6)])
def test_invalid_parameters(session, client, min_ruca, max_ruca):
    assert (
        min_ruca > max_ruca
    ), "pre-condition failed, min_ruca must be larger than max_ruca"

    response = client.get(
        f"/procedure?min_ruca={min_ruca}&max_ruca={max_ruca}&state_abbreviation=CA"
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "min_ruca must be less or equal than max_ruca"}


def test_get_procedure_one_record_per_state(session, client):
    states = ["CA", "PA", "OH", "WI"]
    for state in states:
        session.add(
            RecordFactory(
                ruca=2.0, state_abbreviation=state, city="city1", procedure_code="A"
            )
        )
    session.commit()

    response = client.get("/procedure?min_ruca=1.0&max_ruca=3.0&state_abbreviation=PA")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {"city": "city1", "ruca": "2.0", "procedure_code": "A", "quantity": 1}
    ]


def test_get_multiple_procedure_in_one_city(session, client):
    session.add(
        RecordFactory(
            ruca=2.0, state_abbreviation="CA", city="city1", procedure_code="A"
        )
    )
    session.add(
        RecordFactory(
            ruca=2.0, state_abbreviation="CA", city="city1", procedure_code="A"
        )
    )
    session.add(
        RecordFactory(
            ruca=3.0, state_abbreviation="CA", city="city1", procedure_code="B"
        )
    )
    session.add(
        RecordFactory(
            ruca=1.0, state_abbreviation="CA", city="city1", procedure_code="C"
        )
    )
    session.commit()

    response = client.get("/procedure?min_ruca=1.0&max_ruca=3.0&state_abbreviation=CA")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"city": "city1", "ruca": "2.0", "procedure_code": "A", "quantity": 2},
        {"city": "city1", "ruca": "3.0", "procedure_code": "B", "quantity": 1},
        {"city": "city1", "ruca": "1.0", "procedure_code": "C", "quantity": 1},
    ]


def test_multiple_records_with_ruca_out_of_bounds(session, client):
    session.add(
        RecordFactory(
            ruca=1.0, state_abbreviation="CA", city="city1", procedure_code="A"
        )
    )
    session.add(
        RecordFactory(
            ruca=1.0, state_abbreviation="CA", city="city1", procedure_code="A"
        )
    )
    session.add(
        RecordFactory(
            ruca=4.0, state_abbreviation="CA", city="city2", procedure_code="C"
        )
    )
    session.add(
        RecordFactory(
            ruca=1.0, state_abbreviation="CA", city="city1", procedure_code="B"
        )
    )
    session.commit()

    response = client.get("/procedure?min_ruca=1.0&max_ruca=3.0&state_abbreviation=CA")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"city": "city1", "ruca": "1.0", "procedure_code": "A", "quantity": 2},
        {"city": "city1", "ruca": "1.0", "procedure_code": "B", "quantity": 1},
    ]


def test_limits_response_to_10(session, client):
    records = RecordFactory.build_batch(20, ruca=1.0, state_abbreviation="CA")
    [session.add(record) for record in records]
    session.commit()
    response = client.get("/procedure?min_ruca=1.0&max_ruca=3.0&state_abbreviation=CA")

    assert len(response.json()) == 10
