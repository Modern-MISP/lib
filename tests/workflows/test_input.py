import pytest

from mmisp.workflows.input import (
    Filter,
    InvalidOperationError,
    InvalidPathError,
    InvalidSelectionError,
    InvalidValueError,
    Operator,
    WorkflowInput,
    evaluate_condition,
    extract_path,
    get_path,
)


def test_match_attribute_tag_names_with_equals() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "NCT tag")

    input.add_filter("A", fil)

    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 1

    assert len(result[0]["Tag"]) == 2
    assert result[0]["Tag"] == [
        {"id": 127, "name": "gr tag", "exportable": True},
        {"id": 4, "name": "NCT tag", "exportable": True},
    ]


def test_match_attribute_type_not_equals() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "type", Operator.NOT_EQUALS, "wow")

    input.add_filter("A", fil)

    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 1
    assert result[0]["id"] == 33


def test_match_all_retained() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "type", Operator.NOT_EQUALS, "lalala")

    input.add_filter("A", fil)

    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 2
    assert [x["id"] for x in result] == [33, 35]


def test_check_attribute_ids_with_any_value_from_operator() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "list", Operator.IN_OR, [1, 7])

    input.add_filter("A", fil)
    result = input.data["Event"]["_AttributeFlattened"]
    assert result == [
        {
            "id": 33,
            "type": "ip-src",
            "deeper": {
                "foo": "bar",
            },
            "list": [1, 2, 3],
            "Tag": [
                {"id": 127, "name": "gr tag", "exportable": True},
                {"id": 4, "name": "NCT tag", "exportable": True},
            ],
        }
    ]


def test_empty_path() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened", "", Operator.EQUALS, "test")

    try:
        input.add_filter("A", fil)
        pytest.fail()
    except InvalidPathError:
        pass


def test_invalid_value() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.IN_OR, "test")

    try:
        input.add_filter("A", fil)
        pytest.fail()
    except InvalidValueError:
        pass


def test_any_value() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event.Tag.{n}", "exportable", Operator.ANY_VALUE, "")

    input.add_filter("A", fil)
    result = input.data["Event"]["Tag"]
    assert len(result) == 1
    assert result[0] == {"id": 1, "name": "other_tag", "exportable": False}


def test_any_value2() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event.Attribute.{n}", "object_relation", Operator.ANY_VALUE, "")

    input.add_filter("A", fil)

    result = input.data["Event"]["Attribute"]

    assert len(result) == 0


def test_not_in() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "list", Operator.NOT_IN, 5)

    input.add_filter("A", fil)
    result = input.data["Event"]["_AttributeFlattened"]

    assert result == [
        {
            "id": 33,
            "type": "ip-src",
            "deeper": {
                "foo": "bar",
            },
            "list": [1, 2, 3],
            "Tag": [
                {"id": 127, "name": "gr tag", "exportable": True},
                {"id": 4, "name": "NCT tag", "exportable": True},
            ],
        }
    ]


def test_empty_selection() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("", "id", Operator.NOT_IN, ["35"])

    try:
        input.add_filter("A", fil)
        pytest.fail()
    except InvalidSelectionError:
        pass


def test_delete_all_tags() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "test")

    input.add_filter("A", fil)

    result = input.data["Event"]["_AttributeFlattened"]
    assert result == []


def test_multiple_filters() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter1 = Filter("Event._AttributeFlattened.{n}", "type", Operator.NOT_EQUALS, "ip-src")

    input.add_filter("A", filter1)

    filter2 = Filter("Event.Tag.{n}", "id", Operator.EQUALS, "1")

    input.add_filter("B", filter2)

    result = input.data
    flattened = result["Event"]["_AttributeFlattened"]

    assert len(flattened) == 1
    assert flattened[0]["id"] == 35

    tag = result["Event"]["Tag"]
    assert len(tag) == 1
    assert tag[0]["id"] == 1


def test_invalid_selection() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter = Filter("Event.wrongSelection", "id", Operator.EQUALS, "test")

    input.add_filter("A", filter)
    assert "wrongSelection" in input.data["Event"]

    # yes, this will actually be inserted:
    # https://github.com/MISP/MISP/blob/ee281d5cd1bc7f88a6236ce444cc91ee498335d6/app/Lib/Tools/WorkflowGraphTool.php#L317-L323
    assert not input.data["Event"]["wrongSelection"]


def test_multiple_selection_locations() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter = Filter("Event._AttributeFlattened.{n}.Tag.{n}", "name", Operator.NOT_EQUALS, "gr tag")
    input.add_filter("A", filter)

    result = input.data["Event"]["_AttributeFlattened"]

    assert len(result) == 2


def test_multiple_selection_locations_broken_cakephp_behavior() -> None:
    """
    Intuitively, one might expect that this gives a single attribute in
    _AttributeFlattened. However, we explicitly mimic the broken CakePHP behavior
    here (from
    https://github.com/MISP/MISP/blob/ee281d5cd1bc7f88a6236ce444cc91ee498335d6/app/Lib/Tools/WorkflowGraphTool.php#L311-L323)

    * Multiple `{n}` result in a single, flattened list:

        > Hash::extract($data, "Event._AttributeFlattened.{n}.Tag.{n}")
        = [
            [
              "id" => 127,
              "name" => "gr tag",
              "exportable" => true,
            ],
            [
              "id" => 4,
              "name" => "NCT tag",
              "exportable" => true,
            ],
            [
              "id" => 333,
              "name" => "IVE tag",
              "exportable" => true,
            ],
            [
              "id" => 5,
              "name" => "BTS tag",
              "exportable" => false,
            ],
          ]

    * All items failing the condition are filtered out. I.e.
      only the tag with ID 127 is kept in.

    * Then, the filtered data will be written into the selection path,
      `Event._AttributeFlattened.{n}.Tag.{n}` which means into both attributes:

        > Hash::insert(
            [ "Attribute" => [
              ["id" => 1, "Tag" => [ ] ],
              ["id" => 2, "Tag" => [ ] ],
            ] ],
            "Attribute.{n}.Tag", [ "id" => 127 ]
          )
        = [
            "Attribute" => [
              [
                "id" => 1,
                "Tag" => [
                  "id" => 127,
                ],
              ],
              [
                "id" => 2,
                "Tag" => [
                  "id" => 127,
                ],
              ],
            ],
          ]
    """

    data = load_data()
    input = WorkflowInput(data, None, None)
    filter = Filter("Event._AttributeFlattened.{n}.Tag.{n}", "name", Operator.EQUALS, "gr tag")
    input.add_filter("A", filter)

    result = input.data["Event"]["_AttributeFlattened"]

    assert len(result) == 2

    assert result[0]["Tag"][0]["id"] == 127
    assert len(result[0]["Tag"]) == 1
    assert result[1]["Tag"][0]["id"] == 127


def test_no_list_filter() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter = Filter("Event", "id", Operator.EQUALS, "1")

    input.add_filter("A", filter)
    assert input.data["Event"]["id"] == 1


def test_no_list_filter2() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    input.add_filter("A", Filter("Event", "id", Operator.EQUALS, "2"))
    assert input.data["Event"] == []


def test_invalid_operator() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    filter = Filter("Event._AttributeFlattened", "id", "equals", "3")

    try:
        input.add_filter("A", filter)
        pytest.fail()
    except InvalidOperationError:
        pass


def test_no_trailing_list() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    input.add_filter("A", Filter("Event._AttributeFlattened.{n}.deeper", "foo", Operator.EQUALS, "bar"))
    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 2
    assert result[0]["id"] == 33

    # Yes, this behavior is absolutely stupid. But it's how `Hash::insert` from
    # CakePHP/legacy MISP works and this testcase makes sure that compatibility
    # won't be broken by accident.
    assert result[0]["deeper"]["foo"] == "bar"
    assert result[1]["deeper"]["foo"] == "bar"


def test_list_wildcard_in_path() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    input.add_filter("A", Filter("Event._AttributeFlattened", "{n}.deeper.foo", Operator.EQUALS, "bar"))
    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 2
    assert result[0]["id"] == 33


def test_list_wildcard_in_path_wrong_condition() -> None:
    data = load_data()
    input = WorkflowInput(data, None, None)
    # Same as `test_list_wildcard_in_path`, but the condition
    # is now `False`, hence `_AttributeFlattened` is now emptied.
    input.add_filter("A", Filter("Event._AttributeFlattened", "{n}.deeper.foo", Operator.NOT_EQUALS, "bar"))
    result = input.data["Event"]["_AttributeFlattened"]
    assert len(result) == 0


def test_extract_path() -> None:
    path = ["{n}", "vehicle", "car", "engine"]
    data = [
        {"vehicle": {"car": {"engine": "V12", "tires": "4"}, "motorcycle": {"engine": "V4", "tires": "3"}}},
        {"vehicle": {"yacht": {"engine": "V24", "max_speed": "80 knots"}}},
        {"vehicle": {"car": {"engine": "V8", "max_speed": "280km/h"}}},
    ]
    assert extract_path(path, data) == ["V12", "V8"]
    assert extract_path(path, data[1:2]) == []


def test_get_path() -> None:
    path = ["vehicle", "motorcycle", "tires"]
    data = {"vehicle": {"car": {"engine": "V12", "tires": "4"}, "motorcycle": {"engine": "V4", "tires": "3"}}}
    assert get_path(path, data) == "3"
    assert get_path(path[1:], data) is None


def test_evaluate_condition_in_and_not_in() -> None:
    value = "cat"
    data = ["dog", "mice", "cat"]
    assert evaluate_condition(value, Operator.IN, data)
    assert not evaluate_condition(value, Operator.NOT_IN, data)
    assert not evaluate_condition(value, Operator.IN, data[:2])
    assert evaluate_condition(value, Operator.NOT_IN, data[:2])
    assert not evaluate_condition(value, Operator.IN, {})
    assert not evaluate_condition(value, Operator.NOT_IN, {})


def test_equals_and_not_equals() -> None:
    assert not evaluate_condition("cat", Operator.EQUALS, "dog")
    assert evaluate_condition("cat", Operator.NOT_EQUALS, "dog")
    assert evaluate_condition("cat", Operator.EQUALS, "cat")
    assert not evaluate_condition("cat", Operator.NOT_EQUALS, "cat")
    assert evaluate_condition("['cat']", Operator.EQUALS, ["cat"])


def test_in_or_and_not_in_or() -> None:
    value = ["car", "motorcycle"]
    data = ["cat", "dog", "motorcycle"]
    assert evaluate_condition(value, Operator.IN_OR, data)
    assert not evaluate_condition(value, Operator.NOT_IN_OR, data)
    assert not evaluate_condition(value, Operator.IN_OR, data[:2])
    assert evaluate_condition(value, Operator.NOT_IN_OR, data[:2])
    assert not evaluate_condition("cat", Operator.IN_OR, data)
    assert not evaluate_condition("cat", Operator.NOT_IN_OR, data)


def test_in_and_and_not_in_and() -> None:
    value = ["car", "motorcycle"]
    data = ["car", "cat", "dog", "motorcycle"]
    assert evaluate_condition(value, Operator.IN_AND, data)
    assert not evaluate_condition(value, Operator.NOT_IN_AND, data)
    assert not evaluate_condition(value, Operator.IN_AND, data[:3])
    assert evaluate_condition(value, Operator.NOT_IN_AND, data[:3])


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
                    "deeper": {
                        "foo": "bar",
                    },
                    "list": [1, 2, 3],
                    "Tag": [
                        {"id": 127, "name": "gr tag", "exportable": True},
                        {"id": 4, "name": "NCT tag", "exportable": True},
                    ],
                },
                {
                    "id": 35,
                    "type": "wow",
                    "list": [4, 5, 6],
                    "Tag": [
                        {"id": 333, "name": "IVE tag", "exportable": True},
                        {"id": 5, "name": "BTS tag", "exportable": False},
                    ],
                },
            ],
        }
    }
    return data
