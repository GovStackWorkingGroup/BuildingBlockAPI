# Test Plan for the Digital Registries BB

Non-functional tests: 

1. All `examples` must be runnable via `docker compose up`.

2. Tests in `/test` will include the expected HTTP status codes for the current endpoints.

3. Via a basic SSH script we will recurse through the `examples` directory, run `docker compose up` for
   each example, wait until we get a running set of containers, and then execute
   the api endpoint tests for _that_ example.

Functional tests: 

1. ensure that application can be launched via docker with a adaptor and a security server (Information Mediator integration).
2. check that all defined API endpoints in the openAPI-spec.json return proper response codes.
3. test API endpoints for DB schema and data.
4. test UI functionality, CRUD a registry database schema and updates to the registry DB. 
5. test UI functionality, CRUD data of the registry DB. 
6. test multiple registries in one instance (multi-tenant).
7. test user rights management.   
8. test log system.  
