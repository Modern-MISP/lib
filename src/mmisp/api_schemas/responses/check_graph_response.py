from typing import List

class CycleGraphConnection():
    nodeId1: int
    nodeID2: int
    cycle: str = "Cycle"
    
class Edge():
    output_node_id: int
    input_node_ids: List[int]
    
    
class IsAcyclic():
    is_asyclic: bool
    cycles: List[CycleGraphConnection]
    """
    It should look like this:
    "cycles": [
            [
                5,
                2,
                "Cycle"
            ],
            [
                6,
                5,
                "Cycle"
            ],
            [
                2,
                6,
                "Cycle"
            ]
        ]
    """

class MultibleOutputConnection():
    has_multiple_output_connection: bool
    edges: List[Edge]
    """
    It should look like this:
    "edges": {
            "7": [
                8,
                9
            ],
            "9": [
                7,
                8
            ]
        }
    """
      
class PathWarnings():
    has_path_warnings: bool
    edges: List[Edge]

class CheckGraphResponse():
    is_acyclic: IsAcyclic
    multiple_output_connection: MultibleOutputConnection
    path_warnings: PathWarnings
    
