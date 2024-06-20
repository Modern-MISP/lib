from typing import List, Dict

class IsAcyclicInfo():
    nodeId1: int
    nodeID2: int
    cycle: str = "Cycle"
    
class IsAcyclic():
    """
    - **is_acyclic** False if the graph contains at least one cycle.
    - **cycles** A list with entries containing 2 node id's and a "Cycle" string.
     
    It should look like this:
    '''
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
    '''
    """
    is_acyclic: bool
    cycles: List[IsAcyclicInfo]
        

class MultibleOutputConnection():
    """
    Represents the acyclic status of a graph and details of detected cycles.

    Attributes:
    - **is_acyclic (bool)**: False if the graph contains at least one cycle.
    - **cycles (List[IsAcyclicInfo])**: A list of entries, each containing two node IDs and a "Cycle" string.

    Example:
    ```json
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
    ```
    """
    has_multiple_output_connection: bool
    edges: Dict[int, List[int]]
    
class PathWarningsInfo():
    
    source_id: int # is a string in legacy misp
    next_node_id: int # is a string in legacy misp
    warning: str
    blocking: bool
    module_name: str
    module_id: int
    

class PathWarnings():
    """
    Represents warnings for paths in a graph.

    Attributes:
    - **has_path_warnings**: True if the graph contains at least one warning.
    - **edges**: A list containing all connections which are flagged as warnings.

    Example:
    ```json
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
    ```
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
    
