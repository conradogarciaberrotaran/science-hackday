from factory import Factory, LazyAttribute
from factory.fuzzy import FuzzyChoice, FuzzyFloat, FuzzyText
from us import STATES

from app.models import Record

states = [state.abbr for state in STATES]


class RecordFactory(Factory):
    class Meta:
        model = Record

    state_abbreviation = FuzzyChoice(states)
    city = LazyAttribute(lambda k: f"city-from-{k.state_abbreviation}")
    country = "US"
    ruca = FuzzyFloat(low=1.0, high=99.0)
    procedure_code = FuzzyText()
