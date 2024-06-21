Workflows also use the Model-View-Controller architecture of the modern MISP project. Workflows can be viewed and edited in the frontend which represents the "view" part.
The execution of workflows happens in the "controller" part of the architecture. This means a workflow is executed primarily in the worker and API package.
This sequence is further explained and visualized in two activity diagrams further below. The base model for workflows containing the workflow graph, modules, conversion from legacy
MISP and input lies in the `src/mmisp/workflows` package. Workflows are stored in the "model" part of the modern MISP project. This means the workflows are saved in the MISP database in string representation.

## Workflows
The concept of workflows arises from the simple necessity for users to manipulate the default behavior of MISP. 
Therefore, the MISP Platform must provide the following abilities to users:

* Ability to prevent the execution of default MISP behavior in certain scenarios.
* Ability to hook specific actions to trigger user-defined behavior.

The worker needs access to the workflow classes because non-blocking workflows can be executed asynchronously. 
This approach speeds up execution and enhances responsiveness. 
The API also depends on the library because synchronous triggers are executed directly within the API, potentially blocking subsequent actions.

## Components

![workflow-component-diagram](diagrams/firstTryComponentProperLightTheme.svg)

The diagram above shows the general structure of the Modern MISP project, divided into six components, with four main code repositories: Frontend, API, Worker, and Lib. These four repositories are modified to integrate workflows into the Modern MISP Project. The core workflow structure and behavior will be implemented in the Lib repository, along with most of the workflow utilities that need to be reused by the two components that can execute workflows: API and Worker. In the API repository, endpoints that allow users to modify and review workflows will be implemented in a dedicated Workflow Python module. Additionally, all previously implemented API endpoints that can trigger workflows will be edited to enable this functionality. The Worker repository will be updated to handle jobs for executing non-blocking workflows. The Frontend will also require minor changes to handle workflows effectively.

## Execution of non-blocking and blocking workflows

![activity-diagram-for-non-blocking-workflows](diagrams/activityNonBlockingV2.svg)

This diagram describes the execution of non blocking workflows.

![activity-diagram-for-blocking-workflows](diagrams/activityBlocking.svg)

This diagram describes the execution of blocking workflows.

## Class diagram for the workflow core structure

![class-diagram-for-workflow-structure](diagrams/classDiagramV2.svg)

This class diagram shows the core structure of a workflow object which was converted from the string representation of the workflow in the MISP database. A singular trigger is linked with a number of modules in an acyclic workflow graph.
