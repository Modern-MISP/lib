from mmisp.workflows.input import (
    Filter,
    FilterError,
    InvalidOperationError,
    InvalidPathError,
    InvalidSelectionError,
    InvalidValueError,
    Operator,
    WorkflowInput,
)


def test_match_attribute_tag_names_with_equals():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "NCT tag")

    response = input.add_filter(fil)

    assert response == None
    input.filter()

    attribute_1 = input.data[0][0]
    attribute_2 = input.data[0][1]

    attribute_1_tags = attribute_1["Tag"]
    attribute_2_tags = attribute_2["Tag"]

    assert isinstance(input.data, list)
    assert len(input.data) == 1

    assert isinstance(attribute_1_tags, list)
    assert len(attribute_1_tags) == 1

    assert isinstance(attribute_2_tags, list)
    assert len(attribute_2_tags) == 0

    assert attribute_1_tags[0] == {"id": 4, "name": "NCT tag", "exportable": True}


def test_match_attribute_type_not_equals():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "type", Operator.NOT_EQUALS, "wow")

    response = input.add_filter(fil)

    assert response == None
    input.filter()

    assert isinstance(input.data, list)
    assert len(input.data) == 1

    assert isinstance(input.data[0], list)
    assert len(input.data[0]) == 1

    assert input.data[0] == [
        {
            "id": 33,
            "type": "ip-src",
            "Tag": [
                {"id": 127, "name": "gr tag", "exportable": True},
                {"id": 4, "name": "NCT tag", "exportable": True},
            ],
        }
    ]


def test_check_attribute_ids_with_in_operator():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened", "Tag.{n}.id", Operator.IN, ["127", "5"])

    response = input.add_filter(fil)

    assert response == None
    input.filter()

    assert len(input.data) == 1
    assert isinstance(input.data[0], list)
    assert len(input.data[0]) == 2

    attribute_1 = input.data[0][0]
    attribute_2 = input.data[0][1]

    assert len(attribute_1["Tag"]) == 1
    assert len(attribute_2["Tag"]) == 1

    assert attribute_1["Tag"][0] == {"id": 127, "name": "gr tag", "exportable": True}
    assert attribute_2["Tag"][0] == {"id": 5, "name": "BTS tag", "exportable": False}


def test_empty_path():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened", "", Operator.EQUALS, "test")

    response = input.add_filter(fil)

    assert isinstance(response, InvalidPathError)


def test_invalid_value():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened", "Tag.{n}.name", Operator.IN, "test")

    response = input.add_filter(fil)

    assert isinstance(response, InvalidValueError)


def test_any_value():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event.Tag", "exportable", Operator.ANY_VALUE, "")

    response = input.add_filter(fil)

    assert response == None
    input.filter()

    what = input.data

    assert len(input.data) == 1
    assert len(input.data[0]) == 1
    assert input.data[0][0] == {"id": 1, "name": "other_tag", "exportable": False}


def test_any_value2():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event.Attribute.{n}", "object_relation", Operator.ANY_VALUE, "")

    response = input.add_filter(fil)

    assert response == None

    input.filter()

    wow = input.data

    assert len(input.data) == 1
    assert isinstance(input.data[0], list)
    assert len(input.data[0]) == 0


def test_not_in():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened", "id", Operator.NOT_IN, ["35"])

    response = input.add_filter(fil)

    assert response == None

    input.filter()

    assert len(input.data) == 1
    assert len(input.data[0]) == 1
    assert input.data[0][0] == {
        "id": 33,
        "type": "ip-src",
        "Tag": [
            {"id": 127, "name": "gr tag", "exportable": True},
            {"id": 4, "name": "NCT tag", "exportable": True},
        ],
    }


def test_empty_selection():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("", "id", Operator.NOT_IN, ["35"])

    response = input.add_filter(fil)

    assert isinstance(response, InvalidSelectionError)


def test_delete_all_tags():
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "test")

    response = input.add_filter(fil)

    assert response == None
    input.filter()

    attribute_1 = input.data[0][0]
    attribute_2 = input.data[0][1]

    attribute_1_tags = attribute_1["Tag"]
    attribute_2_tags = attribute_2["Tag"]

    assert isinstance(input.data, list)
    assert len(input.data) == 1

    assert attribute_1_tags == []
    assert attribute_2_tags == []


def test_multiple_filters():
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter1 = Filter("Event._AttributeFlattened", "type", Operator.NOT_EQUALS, "ip-src")

    response = input.add_filter(filter1)

    assert response == None

    filter2 = Filter("{n}.Tag", "id", Operator.EQUALS, "3")

    response = input.add_filter(filter2)

    assert response == None

    input.filter()

    assert len(input.data) == 2
    assert input.data[0] == [
        {
            "id": 35,
            "type": "wow",
            "Tag": [
                {"id": 333, "name": "IVE tag", "exportable": True},
                {"id": 5, "name": "BTS tag", "exportable": False},
            ],
        },
    ]

    assert input.data[1] == []


def load_data() -> dict:
    data = {
        "Event": {
            "id": 1,
            "info": "blabal",
            "Tag": [
                {"id": 0, "name": "cool_tag"},
                {"id": 1, "name": "other_tag", "exportable": False},
            ],
            "Org": {"id": 1, "name": "ORGNAME", "uuid": "5de83b4-36ba-49d6-9530-2a315caeece"},
            "Attribute": [{"id": 4444, "type": "network activity", "object_relation": None}],
            "_AttributeFlattened": [
                {
                    "id": 33,
                    "type": "ip-src",
                    "Tag": [
                        {"id": 127, "name": "gr tag", "exportable": True},
                        {"id": 4, "name": "NCT tag", "exportable": True},
                    ],
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
