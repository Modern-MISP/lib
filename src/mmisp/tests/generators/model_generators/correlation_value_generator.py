from mmisp.db.models.correlation import CorrelationValue


def generate_correlation_value_a() -> CorrelationValue:
    return CorrelationValue(
        value="a",
    )


def generate_correlation_value_b() -> CorrelationValue:
    return CorrelationValue(
        value="b",
    )


def generate_correlation_value_c() -> CorrelationValue:
    return CorrelationValue(
        value="c",
    )


def generate_correlation_value_a_to_c() -> list[CorrelationValue]:
    return [generate_correlation_value_a(), generate_correlation_value_b(), generate_correlation_value_c()]
