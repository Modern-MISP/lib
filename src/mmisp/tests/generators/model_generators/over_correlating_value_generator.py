from mmisp.db.models.correlation import OverCorrelatingValue


def generate_over_correlating_value_value_turla():
    return OverCorrelatingValue(
        id=1,
        value="Turla",
        occurrence=1,
    )
