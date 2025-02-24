# Provenance Events Schema

## Overview
This schema defines the structure of **Provenance Events** data based on the collection provenance events query. It aligns with Linked Data standards to support interoperability and semantic clarity.

## Namespace Prefixes
```turtle
prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>
prefix dct: <http://purl.org/dc/terms/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix pm: <https://pressingmatter.nl/>
```

## Class: `crm:E8_Acquisition`

### Properties

### Connection with Object
- **Predicate:** `^crm:P24i_changed_ownership_through`
- **Description:** Links the provenance events to an object involved in the Events.

### Events Label
- **Predicate:** `rdfs:label`
- **Description:** A human-readable label for the provenance Events.

### Event Type
- **Predicate:** `crm:P2_has_type`
- **Label Property:** `rdfs:label`
- **Description:** Specifies the type of acquisition (e.g., purchase, donation, confiscation).

### Event Time Span
- **Predicate:** `crm:P4_has_time-span`
- **Start Date:** `crm:P82a_begin_of_the_begin`
- **End Date:** `crm:P82b_end_of_the_end`
- **Description:** The time period when the provenance events occurred.

### From Actor
- **Predicate:** `crm:P23_transferred_title_from`
- **Label Property:** `rdfs:label`
- **Description:** Identifies the entity that transferred ownership or custody of the object.

### To Actor
- **Predicate:** `crm:P22_transferred_title_to`
- **Label Property:** `rdfs:label`
- **Description:** Identifies the entity that received ownership or custody of the object.


## Example Data
```trig
@prefix ns1: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://pressimngmatter.nl/nmvw/graph/provenance> {
    <https://hdl.handle.net/20.500.11840/602272> ns1:P24i_changed_ownership_through <https://data.colonialcollections.nl/.well-known/genid/d1a257d700bb4bb9b3b810753edb6959>,
            <https://data.colonialcollections.nl/nmvw/provenance/activity/1696546/event/602272> .

    <https://data.colonialcollections.nl/.well-known/genid/bf81767e2c4f4be9b0daf86cf00b435c> a ns1:Time-Span ;
        ns1:P82a_begin_of_the_begin "1883-02-01" ;
        ns1:P82b_end_of_the_end "1883-02-01" .

    <https://data.colonialcollections.nl/.well-known/genid/d1a257d700bb4bb9b3b810753edb6959> a ns1:E8_Acquisition ;
        rdfs:label "Aankoop" ;
        ns1:P2_has_type <http://vocab.getty.edu/aat/300417642> ;
        ns1:P4_has_time-span <https://data.colonialcollections.nl/.well-known/genid/bf81767e2c4f4be9b0daf86cf00b435c> .

    <https://data.colonialcollections.nl/nmvw/provenance/activity/1696546/event/602272> a ns1:E8_Acquisition ;
        rdfs:label "Verwerving: aankoop" ;
        ns1:P22_transferred_title_to <https://data.colonialcollections.nl/nmvw/id/constituent/69799> ;
        ns1:P23_transferred_title_from <https://hdl.handle.net/20.500.11840/pi78246> ;
        ns1:P2_has_type <http://vocab.getty.edu/aat/300417642> .
}
```

## Class: `crm:E10_Transfer_of_Custody`

### Properties

### Connection with Object
- **Predicate:** `^crm:P30i_custody_transferred_through`
- **Description:** Links the provenance events to an object involved in the Events.

### Events Label
- **Predicate:** `rdfs:label`
- **Description:** A human-readable label for the provenance Events.

### Event Type
- **Predicate:** `crm:P2_has_type`
- **Label Property:** `rdfs:label`
- **Description:** Specifies the type of acquisition (e.g., purchase, donation, confiscation).

### Event Time Span
- **Predicate:** `crm:P4_has_time-span`
- **Start Date:** `crm:P82a_begin_of_the_begin`
- **End Date:** `crm:P82b_end_of_the_end`
- **Description:** The time period when the provenance events occurred.

### From Actor
- **Predicate:** `crm:P28_custody_surrendered_by`
- **Label Property:** `rdfs:label`
- **Description:** Identifies the entity that transferred ownership or custody of the object.

### To Actor
- **Predicate:** `crm:P29_custody_received_by`
- **Label Property:** `rdfs:label`
- **Description:** Identifies the entity that received ownership or custody of the object.



## Example Data
```trig
@prefix ns1: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://pressimngmatter.nl/nmvw/graph/provenance> {
    <https://hdl.handle.net/20.500.11840/56844> ns1:P24i_changed_ownership_through <https://data.colonialcollections.nl/.well-known/genid/fa4691000cf946e68e888f576a268293> ;
        ns1:P30i_custody_transferred_through <https://data.colonialcollections.nl/nmvw/provenance/activity/10245/event/56844> .

    <https://data.colonialcollections.nl/.well-known/genid/cb38e7b81233456cbd489e2f4007b6b0> a ns1:Time-Span ;
        ns1:P82a_begin_of_the_begin "1941-01-01" ;
        ns1:P82b_end_of_the_end "1941-01-01" .

    <https://data.colonialcollections.nl/.well-known/genid/fa4691000cf946e68e888f576a268293> a ns1:E8_Acquisition ;
        rdfs:label "Bruikleen" ;
        ns1:P2_has_type <http://vocab.getty.edu/aat/300417645> ;
        ns1:P4_has_time-span <https://data.colonialcollections.nl/.well-known/genid/cb38e7b81233456cbd489e2f4007b6b0> .

    <https://data.colonialcollections.nl/nmvw/provenance/activity/10245/event/56844> a ns1:E10_Transfer_of_Custody ;
        rdfs:label "Verwerving: bruikleen" ;
        ns1:P2_has_type <http://vocab.getty.edu/aat/300417645> .
}

```


## License
This schema is open for use and adaptation under an open data license.

## Contact
For inquiries, please contact: **Sarah Shoilee** at [s.b.a.shoilee@vu.nl](mailto:s.b.a.shoilee@vu.nl).

