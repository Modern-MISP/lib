from typing import List, Dict

class IsAcyclicInfo():
    nodeId1: int
    nodeID2: int
    cycle: str = "Cycle"
    
class IsAcyclic():
    """
    It should look like this:
    "is_acyclic": {
        "is_acyclic": false,
        "cycles": [
            [
                4,
                3,
                "Cycle"
            ],
            [
                3,
                4,
                "Cycle"
            ]
        ]
    }
    """
    is_acyclic: bool
    cycles: List[IsAcyclicInfo]
        

class MultibleOutputConnection():
    """
    It should look like this:
    "multiple_output_connection": {
        "has_multiple_output_connection": true,
        "edges": {
            "1": [
                5,
                3
            ]
        }
    }
    """
    has_multiple_output_connection: bool
    edges: Dict[int, List[int]]
    
class PathWarningsInfo():
    source_id: str
    next_node_id: str
    warning: str
    blocking: bool
    module_name: str
    module_id: int
    

class PathWarnings():
    """
    It should look like this:
    "path_warnings": {
        "has_path_warnings": true,
        "edges": [
            [
                "5",
                "2",
                "This path leads to a blocking node from a non-blocking context",
                true,
                "stop-execution",
                2
            ]
        ]
    }
    """
    has_path_warnings: bool
    edges: List[PathWarningsInfo]

class CheckGraphResponse():
    """
    Response schema from the API for checking a graph.
    
    - **is_acyclic** Indicates whether the graph is acyclig and gives information for the first cycle.
    - **multiple_output_connection** Indicates whether the graph has multiple output connections. 
    States what modules have multiple output connections
    - **path_warnings** If a path leads to a blocking node from a 'Concurrent Task' node, a warning is recorded. 
    """
    is_acyclic: IsAcyclic
    multiple_output_connection: MultibleOutputConnection
    path_warnings: PathWarnings
    
