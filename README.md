This repository provides source code for converting colonial collections data for use in the PM-SAMPO application. It includes codes for processing existing Linked Data and deploying a Fuseki triplestore for querying through endpoint.

- Colonial Collection Endpoint: https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql


# Conversion Documentation

|Graph | Description |Source| Properties
|----- | --- |----| ---|
|collections| objects information |----| [schema](schema/collections.md)|
|provEvents| events, i.e., Acqusition and Transfer of Custody related to object provenance| ----| [schema](schema/provEvents.md) |
|actors| makers and provenance constituents |----| [schema](schema/actors.md)|
|histEvents| historical events recorderd by wereldmuseum |Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|thesaurus| Wereldmuseum thesauri |Download from [colonial collection datahub](https://data.colonialcollections.nl/nmvw/collection-archives)| |
|geonames| longitute and latitue of the place |Extracted from [geonames API](http://secure.geonames.org)| |

Note: [site](https://data.colonialcollections.nl/nmvw/graph/sites) graph is not covered in PM-SAMPO.


# Current Data Schema

```SPARQL
PREFIX pm: <https://pressingmatter.nl>  
PREFIX la: <https://linked.art/ns/terms/>  
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>  
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
PREFIX dct: <http://purl.org/dc/terms/>  
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>  
```

### **Objects (Class: crm:E22_Human-Made_Object)**
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Title              | `dct:title`   | same as before                    |
| Image              | `pm:shown_by` | `crm:P65_shows_visual_item/la:digitally_shown_by/la:access_point` |
| Identifier         | `pm:identified_by` | `crm:P1_is_identified_by/crm:P190_has_symbolic_content` (filtered by `aat:300445023`) |
| Inventory Number   | `pm:inventory_number` | `crm:P1_is_identified_by/crm:P190_has_symbolic_content` (filtered by `aat:300404626`) |
| Type              | `crm:P2_has_type` | `skos:prefLabel` (filtered by `thesuari term conceptscheme2`) |
| Materials         | `pm:materials_used` | `crm:P45_consists_of/skos:altLabel` |
| Intended Use      | `pm:intended_use` | `crm:P103_was_intended_for/crm:P190_has_symbolic_content` |
| Maker            | `pm:maker` | `crm:P108i_was_produced_by/crm:P14_carried_out_by` |
| Production Place | `pm:production_place` | `crm:P108i_was_produced_by/crm:P7_took_place_at` |
| Production Time  | `pm:production_time_span` | `crm:P108i_was_produced_by/crm:P4_has_time-span` |
| Historical Event | `pm:related_to` | `crm:P141i_was_assigned_by/crm:P141_assigned` |
### **Provenance Events (Class: crm:E8_Acquisition or crm:E10_Transfer_of_Custody)**
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Connection Object | `^crm:P24i_changed_ownership_through` | same as before |
| Events Label     | `rdfs:label` | same as before |
| Event Type      | `crm:P2_has_type` | same as before |
| From Actor     | `crm:P23_transferred_title_from` | same as before |
| To Actor       | `crm:P22_transferred_title_to` | same as before |
### **Actors (Class: crm:E21_Person or crm:E39_Actor or crm:E74_Group)**
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Label          | `rdfs:label` | same as before |
| Names         | `pm:identified_by` | `crm:P1_is_identified_by/crm:P190_has_symbolic_content` (filtered by `aat:300404650`) |
| Role          | `pm:roles` | `P2_has_type / (skos:prefLabel | rdfs:label)` (filtered by `aat:300404650`) |
| Gender       | `pm:gender` | `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` (filtered by `aat:300055147`) |
| Nationality  | `pm:nationality` | `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` (filtered by `aat:300379842`) |
| Biography    | `pm:biography` | `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` (filtered by `aat:300435422`) |
| Remarks      | `pm:remarks` | `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` (filtered by `aat:300435415`) |
| Profession   | `pm:profession` | `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` (filtered by `aat:300393201`) |
### **Historical Event (Class: crm:E5_Event)**
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Label        | `crm:P1_is_identified_by` | same as before |
| Time Span    | `crm:P4_has_time-span` | same as before |
| Description  | `crm:P67i_is_referred_to_by` | same as before |
### **Place (Class: crm:E53_Place)**
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Longitude    | `wgs84:long` | new addition |
| Latitude     | `wgs84:lat` | new addition |
### **Time-span (Class: crm:E52_Time-Span)** 
| **Property**        | **Predicate** | **Previous Predicate** |
|---------------------|--------------|------------------------|
| Start Date   | `crm:P82a_begin_of_the_begin` | same as before |
| End Date     | `crm:P82b_end_of_the_end` | same as before |



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

# TODO:
- add data source
