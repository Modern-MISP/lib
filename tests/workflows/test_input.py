from mmisp.db.models.workflow import Workflow
from mmisp.workflows.input import Filter, Operator, WorkflowInput

def test_example():
    data = load_event()
    input = WorkflowInput(data, None, None)
    fil = Filter("Event._AttributeFlattened.{n}", "Tag.{n}.name", Operator.EQUALS, "NCT tag")

    input.add_filter(fil)
    input.filter()
    assert isinstance(input.data, list)



def load_event():
    data = {
        "Event": {
            "id": 1,
            "info": "blabal",
            "Tag": [
                {
                    "id": 0,
                    "name": "cool_tag",
                    "exportable": True
                },
                {
                    "id": 1,
                    "name": "other_tag",
                    "exportable": False
                }
            ],
            "_AttributeFlattened": [
                {
                    "id": 33,
                    "type": "ip-src",
                    "Tag": {
                        "1": {
                            "id": 127,
                            "name": "gr tag",
                            "exportable": True
                        },
                        "2": {
                            "id": 4,
                            "name": "NCT tag",
                            "exportable": True
                        }
                    }
                        
                },
                {
                    "id": 35,
                    "type": "wow",
                    "Tag": [
                        {
                            "id": 333,
                            "name": "IVE tag",
                            "exportable": True
                        },
                        {
                            "id": 5,
                            "name": "BTS tag",
                            "exportable": False
                        }
                    ]
                }
            ]
        }
    }
    return data

