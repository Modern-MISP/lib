from mmisp.db.models.correlation import CorrelationValue


def correlation_value_a_generator() -> CorrelationValue:
    return CorrelationValue(
        value="a",
    )


def correlation_value_b_generator() -> CorrelationValue:
    return CorrelationValue(
        value="b",
    )


def correlation_value_c_generator() -> CorrelationValue:
    return CorrelationValue(
        value="c",
    )


def correlation_value_a_to_c_generator() -> list[CorrelationValue]:
    return [correlation_value_a_generator(), correlation_value_b_generator(), correlation_value_c_generator()]
