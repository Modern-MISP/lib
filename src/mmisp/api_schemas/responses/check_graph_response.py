from typing import List, Dict

class IsAcyclicInfo():
    nodeId1: int
    nodeID2: int
    cycle: str = "Cycle"
    
class IsAcyclic():
    """
    Represents the acyclic status of a graph and details of detected cycles.

    - **is_acyclic**: False if the graph contains at least one cycle.
    - **cycles**: A list of entries, each containing two node IDs and a "Cycle" string.

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
    is_acyclic: bool
    cycles: List[IsAcyclicInfo]
        

class MultibleOutputConnection():
    """
    Represents the acyclic status of a graph and details of detected cycles.

    - **is_acyclic**: False if the graph contains at least one cycle.
    - **cycles**: A list of entries, each containing two node IDs and a "Cycle" string.

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

    - **has_path_warnings**: True if the graph contains at least one warning.
    - **edges**: A list containing all connections which are flagged as warnings.

    Example:
    ```json
    "path_warnings": {
        "has_path_warnings": true,
        "edges": [
            [
                5,
                2,
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

    Attributes:
    - **is_acyclic**: Indicates whether the graph is acyclic and provides information about the first detected cycle, if any.
    - **multiple_output_connection**: Indicates whether the graph has illegal multiple output connections, 
    detailing the nodes involved.
    - **path_warnings**: Records warnings if a path leads to a blocking node from a 'Concurrent Task' node, providing relevant details.

    Example JSON structure:
    ```json
    {
        "is_acyclic": {
            "is_acyclic": false,
            "cycles": [
                [4, 3, "Cycle"],
                [3, 4, "Cycle"]
            ]
        },
        "multiple_output_connection": {
            "has_multiple_output_connection": true,
            "edges": {
                "1": [5, 3]
            }
        },
        "path_warnings": {
            "has_path_warnings": true,
            "edges": [
                [5, 2, "This path leads to a blocking node from a non-blocking context", true, "stop-execution", 2]
            ]
        }
    }
    ```
    """
    is_acyclic: IsAcyclic
    multiple_output_connection: MultibleOutputConnection
    path_warnings: PathWarnings
    
