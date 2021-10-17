# Replicated_Log

This is a repo for Replicated Log task from Distributed Systems course at UCU.
It contains the following files:

1. Primary folder with primary.py. It uses Flask and request modules to create routing for GET and POST for primary node. 
2. secondary_frst folder with secondary.py to receive POST from primary and store the message.
3. Docker-compose that spins up containers for Dockers images for 3 nodes (primary and 2 secondaries) on different ports. 

Ports:
1. primary: "5000:5000"
2. secondary_frst: "5001:5001"
3. secondary_scnd: "5002:5001"
****

Use the following steps to start Docker:
1. `docker-compose build` 
2. `docker-compose up`

For testing purposes, you can use Postman Import for **Replicated Log UCU.postman_collection.json**. It stores a collection of POST and GET requests to test primary and secondary message replication.

**Testing:**

1. Run POST to Primary (port = 5000)
2. Run GET from Secondary 1 (port = 5001)
3. Run GET from Secondary 2 (port = 5002)