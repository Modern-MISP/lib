
This is the library package. In this repository are modules that are required by both the API and the worker repository.

## Components

![workflow-component-diagram](diagrams/firstTryComponentProperLightTheme.svg)

This diagram shows the components that workflows use.

## Workflows
The concept of workflows arises from the simple necessity for users to manipulate the default behavior of MISP. 
Therefore, the MISP Platform must provide the following abilities to users:

* Ability to prevent the execution of default MISP behavior in certain scenarios.
* Ability to hook specific actions to trigger user-defined behavior.

The worker needs access to the workflow classes because non-blocking workflows can be executed asynchronously. 
This approach speeds up execution and enhances responsiveness. 
The API also depends on the library because synchronous triggers are executed directly within the API, potentially blocking subsequent actions.

## Execution of blocking and non-blocking workflows

![activity-diagram-for-non-blocking-workflows](diagrams/activityNonBlockingV1.svg)

This diagram describes the execution of non blocking workflows.

![activity-diagram-for-blocking-workflows](diagrams/activityBlocking.svg)

This diagram describes the execution of blocking workflows.

## Class diagram for the workflow core structure

![class-diagram-for-workflow-structure](diagrams/classes.svg)
