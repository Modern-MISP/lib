from mmisp.workflows.input import Filter, Operator, WorkflowInput


def test_match_attribute_tag_names_with_equals():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "NCT tag")

    input.add_filter(fil)
    input.filter()

    attribute_1 = input.data[0][0]
    attribute_2 = input.data[0][1]

    attribute_1_tags = attribute_1["Tag"]
    attribute_2_tags = attribute_2["Tag"]

    assert isinstance(input.data, list)
    assert len(input.data) == 1

    assert isinstance(attribute_1_tags, dict)
    assert len(attribute_1_tags) == 1

    assert isinstance(attribute_2_tags, list)
    assert len(attribute_2_tags) == 0

    assert attribute_1_tags["2"] == {"id": 4, "name": "NCT tag", "exportable": True}


def test_match_attribute_type_not_equals():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "type", Operator.NOT_EQUALS, "wow")

    input.add_filter(fil)
    input.filter()

    assert isinstance(input.data, list)
    assert len(input.data) == 1

    assert isinstance(input.data[0], list)
    assert len(input.data[0]) == 1

    assert input.data[0] == [
        {
            "id": 33,
            "type": "ip-src",
            "Tag": {
                "1": {"id": 127, "name": "gr tag", "exportable": True},
                "2": {"id": 4, "name": "NCT tag", "exportable": True},
            },
        }
    ]


def test_empty_selection():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("", "type", Operator.NOT_EQUALS, "wow")

    input.add_filter(fil)
    input.filter()

    assert len(input.data) == 1
    assert len(input.data[0]) == 0

    assert input.data[0] == []


def test_check_attribute_ids_with_in_operator():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.id", Operator.IN, ["127", "5"])

    input.add_filter(fil)
    input.filter()

    assert len(input.data) == 1
    assert isinstance(input.data[0], list)
    assert len(input.data[0]) == 2

    attribute_1 = input.data[0][0]
    attribute_2 = input.data[0][1]

    assert len(attribute_1["Tag"]) == 1
    assert len(attribute_2["Tag"]) == 1

    assert attribute_1["Tag"]["1"] == {"id": 127, "name": "gr tag", "exportable": True}
    assert attribute_2["Tag"][0] == {"id": 5, "name": "BTS tag", "exportable": False}


def load_data() -> dict:
    data = {
        "Event": {
            "id": 1,
            "info": "blabal",
            "Tag": [
                {"id": 0, "name": "cool_tag", "exportable": True},
                {"id": 1, "name": "other_tag", "exportable": False},
            ],
            "_AttributeFlattened": [
                {
                    "id": 33,
                    "type": "ip-src",
                    "Tag": {
                        "1": {"id": 127, "name": "gr tag", "exportable": True},
                        "2": {"id": 4, "name": "NCT tag", "exportable": True},
                    },
                },
                {
                    "id": 35,
                    "type": "wow",
                    "Tag": [
                        {"id": 333, "name": "IVE tag", "exportable": True},
                        {"id": 5, "name": "BTS tag", "exportable": False},
                    ],
                },
            ],
        }
    }
    return data
