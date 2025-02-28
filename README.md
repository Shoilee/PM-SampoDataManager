This repository provides source code for converting colonial collections data for use in the PM-SAMPO application. It includes codes for processing existing Linked Data and deploying a Fuseki triplestore for querying through endpoint.

- Live Data Portal: [Colonial Collections](https://data.colonialcollections.nl/)
- Existing Endpoint: https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql


# Conversion Documentation

|Graph | Description |Source| Properties
|----- | --- |----| ---|
|collections| objects information |----| [schema](schema/collections.md)|
|provEvents| events, i.e., Acqusition and Transfer of Custody related to object provenance| ----| [schema](schema/provEvents.md) |
|actors| makers and provenance constituents |----| [schema](schema/actors.md)|
|histEvents| historical events recorderd by wereldmuseum |Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|thesaurus| Wereldmuseum thesauri |Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|geonames| longitute and latitue of the place |Extracted from [geonames API](http://secure.geonames.org)| |

Note: [site](https://data.colonialcollections.nl/nmvw/graph/sites) graph is something that PM-SAMPO didn't cover


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

