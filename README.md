This repository provides source code for converting colonial collections data for use in the PM-SAMPO application. It includes codes for processing existing Linked Data and deploying a Fuseki triplestore for querying through endpoint.

- Live Data Portal: [Colonial Collections](https://data.colonialcollections.nl/)
- Existing Endpoint: https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql


# Conversion Documentation

|Graph | Source| Properties
|----- | ----| ---|
|collections| ----| [schema](schema/collections.md)|
|provEvents| ----| [schema](schema/provEvents.md) |
|actors| ----| ---|
|histEvents| Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|thesaurus| Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|geonames| Extracted from [geonames API](http://secure.geonames.org)| |


## TODO:
- `src/getPlaceCoordinate.py`: place geonames in a trig file with the Named Graph
- add data source


# Build Fuseki container for publishing the data

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

