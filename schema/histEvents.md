# Historical Events Schema

## Overview
This schema defines the structure of **Historical Events** data based on the collection provenance events query. It includes event identification, time span, and descriptions.

### **Label**
- **Predicate:** `crm:P1_is_identified_by`
- **Previous Predicate:** `crm:P1_is_identified_by/crm:P190_has_symbolic_content` filtered by `aat:300404650`
- **Description:** The preferred label for the historical event.

### **Time Span**
- **Predicate:** `crm:P4_has_time-span`
- **Previous Predicate:** `crm:P82a_begin_of_the_begin`, `crm:P82b_end_of_the_end`
- **Description:** The start and end date of the historical event, concatenated as a time span.

### **Description**
- **Predicate:** `crm:P67i_is_referred_to_by`
- **Previous Predicate:** `crm:P2_has_type` filtered by `aat:300435416` and `crm:P190_has_symbolic_content`
- **Description:** A textual description of the historical event.

# TODO: add P3_has_note