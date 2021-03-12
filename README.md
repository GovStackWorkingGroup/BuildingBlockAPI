# Building Block API Definitions

This repository will hold OpenAPI (Swagger) definitions for building blocks that have been developed by the GovStack expert working groups. 

Each building block API definition should be stored in a YAML file that is compatible with the OpenAPI 3.1 standard


# How will groups work with the architecture group?

Each working group is responsible for defining and documenting the functional requirements for their block. A building block definition template will be provided to assist with this process: https://docs.google.com/document/d/1l-AFTtwBY3RpnlcCiUi3ifBVUNMI1AiM/edit?rtpof=true 

Diagrams and charts MUST be created and stored on the working group’s Github repository in a text-based format.

After functional requirements are gathered, data models and service APIs are documented. Then, each data model MUST be converted to a JSON schema and each service API MUST be written into OpenAPI 3.1 specification with appropriate documentation. Example JSON schema and OpenAPI templates will be provided for each group in a Github repository. JSON schemas and OpenAPI templates MUST be committed to Github. 

Finally, a compliance test kit (CTK) MUST be created to help future implementations comply with the block’s expectations.

This approach is designed to be as lightweight as possible, while supporting bottom-up collaboration with the architecture group and other stakeholders. Each block’s diagrams, models and APIs are versioned and reviewed via pull requests. Also, each working group’s repository is forked from a base repository. 


See https://github.com/GovStackWorkingGroup/BuildingBlockAPI for the base repository with diagrams, JSON schema and OpenAPI examples.

As best practices and patterns are identified, they can be merged back to the base repository, allowing them to be shared across working groups.

A version of the building block definition template SHOULD be uploaded to Teams for commenting and feedback once a week. It must be marked as read only, and team leaders are responsible for gathering feedback and applying it back to the source document.



# Tooling suggestions
Except where identified in the Architecture Blueprint, working groups should feel free to use the tools they feel are most productive for the group. Here are some tools we’ve found helpful:

## Video Conferencing
https://meet.jit.si/

## Chat

https://ict-building-blocks.cloud.mattermost.com/signup_user_complete/?id=4mebo8ipz3baidf4iabbctcyhe 

## Documents
https://docs.google.com/ for collaborative document editing and for gathering feedback.
https://asciidoctor.org/ for document generation. The https://asciidoc.org/  standard is already used on GitHub for Gists, Wikis and the like.

## Diagrams
https://app.diagrams.net/ and https://www.websequencediagrams.com/ for diagrams.

## OpenAPI
https://github.com/swagger-api/swagger-editor and https://swagger.io/tools/swaggerhub/ for editing OpenAPI specifications.
https://bootprint.knappi.org/ for generating OpenAPI documentation.

## JSON Schema
https://jsonschema.net/ for creating JSON Schemas.
https://json-editor.github.io/json-editor/ For editing and viewing JSON schemas as a working UI
https://github.com/cloudflare/json-schema-tools/tree/master/workspaces/doca for generating documentation from JSON Schemas.
