
This is the library package. In this repository are modules that are required by both the API and the worker repository.

The Library repository is central to the workflow implementation in Modern MISP. Within these packages, the entire workflow structure and behavior will be implemented. This includes classes for storing the workflows, their component modules, the graph structure, database models, API schemas for transferring workflow data, and other utilities for workflows. These packages are reused by both the API and Worker repositories, which require the ability to execute workflows.
