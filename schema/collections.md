# Colonial Collections Data Schema

## Overview
This document describes the schema used in the **PMSAMPOs** demonstrator. The schema is based on existing Linked Data available through colonial Collection endpoint. Tjis new  knowledge discovery.

## Namespace Prefixes
```
prefix crm: <http://www.cidoc-crm.org/cidoc-crm/>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix pm: <https://pressingmatter.nl/>
```

## CLASS: crm:E22_Human-Made_Object

### Prperties
### Image
- **Predicate:** `pm:shown_by`
- **Previous Predicate:** `crm:P65_shows_visual_item/<https://linked.art/ns/terms/digitally_shown_by>/<https://linked.art/ns/terms/access_point>`
- **Description:** Categorizes the object based on object type; connects to thesuari term that is explained by concept scheme <https://hdl.handle.net/20.500.11840/conceptscheme2>.

### Object Type
- **Predicate:** `crm:P2_has_type`
- **Label Property:** `skos:prefLabel`
- **Description:** Categorizes the object based on object type; connects to thesuari term that is explained by concept scheme <https://hdl.handle.net/20.500.11840/conceptscheme2>.

### Materials
- **Predicate:** `pm:materials_used`
- **Prevous Predicate:** `crm:P45_consists_of/skos:altLabel`
- **Description:** The materials the object is made of.
- **Note:** lost thesuari links.

### Intended Use
- **Predicate:** `pm:intended_use`
- **Predicate:** `crm:P103_was_intended_for/crm:P190_has_symbolic_content`
- **Description:** The intended function or meaning of the object.
- **Note:** lost thesuari links.

### Produced 
- **Predicate:** `pm:intended_use`
- **Predicate:** `crm:P103_was_intended_for/crm:P190_has_symbolic_content`
- **Description:** The intended function or meaning of the object.
- **Note:** lost thesuari links.

### Maker
- **Predicate:** `pm:maker:`
- **Previous Predicate:** `crm:P108i_was_produced_by/crm:P14_carried_out_by`
- **Label Property:** `rdfs:label`
- **Description:** Identifies the person or entity responsible for producing the object.
- **Note:** Duplication to benefit facet.

### Production Place
- **Predicate:** `pm:production_place`
- **Previous Predicate:** `crm:P108i_was_produced_by/crm:P7_took_place_at`
- **Label Property:** `skos:prefLabel`
- **Description:** The geographic location where the object was produced.
- - **Note:** Duplication to benefit facet.

### Production Time Span
- **Predicate**: `pm:production_time_span`
- **Predicate:** `crm:P108i_was_produced_by/crm:P4_has_time-span`
- **Start Date:** `crm:P82a_begin_of_the_begin`
- **End Date:** `crm:P82b_end_of_the_end`
- **Description:** The time period during which the object was created.

### Provenance Type
- **Previous Predicate:** `(crm:P24i_changed_ownership_through | crm:P30i_custody_transferred_through) / crm:P2_has_type`
- ***
- **Label Property:** federated query over <https://data.getty.edu/vocab/sparql> `rdfs:label`
- **Description:** Describes how the object was acquired (e.g., purchase, donation, looting).

### Provanence Time Span
- **Predicate:** `(crm:P24i_changed_ownership_through|crm:P30i_custody_transferred_through) / crm:P4_has_time-span`
- **Start Date:** `crm:P82a_begin_of_the_begin`
- **End Date:** `crm:P82b_end_of_the_end`
- **Description:** The time period when the acquisition took place.

### Provenance (from) Actor
- **Predicate:** `pm:provenance_from_actor`
- **Previous Predicate:**`(crm:P24i_changed_ownership_through/crm:P23_transferred_title_from) | (crm:P30i_custody_transferred_through/crm:P28_custody_surrendered_by)`
- **Label Property:** `rdfs:label`
- **Description:** Describes the connected person or entity involved in objects acquisition or transfer of custody.

### Provenance (to) Actor
- **Predicate:** `pm:provenance_from_actor`
- **Previous Predicate:**`crm:P24i_changed_ownership_through/crm:P22_transferred_title_to) | (crm:P30i_custody_transferred_through/crm:P29_custody_received_by)`
- **Label Property:** `rdfs:label`
- **Description:** Describes the connected person or entity involved in objects acquisition or transfer of custody.

### Historical Event
- **Predicate:** `pm:related_to`
- **Previous Predicate:**`crm:P141i_was_assigned_by/crm:P141_assigned`
- **Label Property:** `crm:P1_is_identified_by / crm:P190_has_symbolic_content`
- **Description:** Describes the connected person or entity involved in objects acusition or transfer of custody.


## Example Data
```turtle

```

## License


## Contact
For inquiries, please contact: Sarah Shoilee at s.b.a.shoilee@vu.nl.