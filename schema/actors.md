# Actors Schema

## Overview
This schema defines the structure of **Actors** data based on the collection provenance events query. By actors this schema covers both makers and provenance constituensts

### **Label**
- **Predicate:** `rdfs:label`
- **Description:** Actors label

### **Names**
- **Predicate:** `pm:identified_by`
- **Previous Predicate:** `crm:P1_is_identified_by/crm:P190_has_symbolic_content` filtered by aat:300404650
- **Description:** Actors Names

### **Type**
- **Predicate:** `rdf:type`
- **Description:** Typ of actors (e.g., Person, Group, Actor)

### **Role**
- **Predicate:** `pm:roles`
- **Previous Predicate:** `P2_has_type / (kos:prefLabel | rdfs:label)` filtered by aat:300404650
- **Description:** Rlle of the actor is available

### **Gender**
- **Predicate:** `pm:gender`
- **Previous Predicate:** `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` filtered by aat:300055147
- **Description:** Gender if available

### **Nationality**
- **Predicate:** `pm:nationality`
- **Previous Predicate:** `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` filtered by aat:300379842
- **Description:** Nationality reference if available

### **Biography**
- **Predicate:** `pm:biography`
- **Previous Predicate:** `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` filtered by aat:300435422
- **Description:** Biography reference if available

### **Remarks**
- **Predicate:** `pm:remarks`
- **Previous Predicate:** `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` filtered by aat:300435415
- **Description:** Extra remarks

### **Profession**
- **Predicate:** `pm:profession`
- **Previous Predicate:** `crm:P67i_is_referred_to_by/crm:P190_has_symbolic_content` filtered by aat:300393201
- **Description:** Profession reference if available