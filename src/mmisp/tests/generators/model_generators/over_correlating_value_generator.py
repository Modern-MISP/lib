from mmisp.db.models.correlation import OverCorrelatingValue


def generate_over_correlating_value_turla() -> OverCorrelatingValue:
    return OverCorrelatingValue(
        value="Turla",
        occurrence=1,
    )


def generate_over_correlating_value_x() -> OverCorrelatingValue:
    return OverCorrelatingValue(
        value="x",
        occurrence=1,
    )


def generate_over_correlating_value_y() -> OverCorrelatingValue:
    return OverCorrelatingValue(
        value="y",
        occurrence=1,
    )


def generate_over_correlating_value_z() -> OverCorrelatingValue:
    return OverCorrelatingValue(
        value="z",
        occurrence=1,
    )


def generate_over_correlating_value_x_to_z() -> list[OverCorrelatingValue]:
    return [generate_over_correlating_value_x(), generate_over_correlating_value_y(),
            generate_over_correlating_value_z()]
