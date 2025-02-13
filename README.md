This repository provides source code for converting colonial collections data for use in the PM-SAMPO application. It includes codes for processing existing Linked Data and deploying a Fuseki triplestore for querying through endpoint.

Live Data Portal: [Colonial Collections](https://data.colonialcollections.nl/)
Existing Endpoint: https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql

# colonial-collections-data

https://data.colonialcollections.nl/

## Build Fuseki container for publishing the data

`docker build -t colonial-collections-fuseki .`

## Run

`docker run -d -p 3048:3030 --name colonial-collections colonial-collections-fuseki`

Get the Fuseki control panel password with `docker logs colonial-collections`

## Upgrade

```
docker build -t colonial-collections-fuseki .
docker stop colonial-collections
docker rm colonial-collections
docker run -d -p 3048:3030 --restart unless-stopped --name colonial-collections colonial-collections-fuseki
```
