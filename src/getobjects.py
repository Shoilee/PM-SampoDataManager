from rdflib import Graph, Namespace, URIRef, Literal, Dataset
from SPARQLWrapper import SPARQLWrapper, JSON
import os

# SPARQL Endpoint
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
GRAPH_URI = "https://data.colonialcollections.nl/nmvw/graph/objects"
OUTPUT_FILE = "data/objects.trig"
BATCH_SIZE = 1000  # Number of results per query

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
AAT = Namespace("http://vocab.getty.edu/aat/")
PM = Namespace("http:/pressingmatter.nl/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX skos: <{SKOS}>
    PREFIX rdfs: <{RDFS}>
    PREFIX aat: <{AAT}>
    
    SELECT ?object ?image ?type ?material ?intendedUse ?maker ?productionPlace ?productionTimeSpan ?startDate ?endDate
           ?provenanceType ?provenanceTimeSpan ?provenanceTimeSpan ?provenanceStart ?provenanceEnd ?provenanceFrom ?provenanceTo ?historicalEvent {{
        # temporary constraints
        ?object crm:P141i_was_assigned_by/crm:P141_assigned <https://hdl.handle.net/20.500.11840/event11> .
        {{
            GRAPH <{GRAPH_URI}> {{
                ?object a crm:E22_Human-Made_Object .
            }}
        }}
        UNION {{ 
            ?object crm:P65_shows_visual_item ?i_BNODE .
            ?i_BNODE a crm:E36_Visual_Item .
            ?i_BNODE <https://linked.art/ns/terms/digitally_shown_by> ?image__id.
            ?image__id <https://linked.art/ns/terms/access_point> ?image .
        }}
        UNION {{ ?object crm:P2_has_type ?type . }}
        UNION {{ ?object crm:P45_consists_of/skos:altLabel ?material . }}
        UNION {{ ?object crm:P103_was_intended_for/crm:P190_has_symbolic_content ?intendedUse . }}
        UNION {{ ?object crm:P108i_was_produced_by/crm:P14_carried_out_by ?maker . }}
        UNION {{ ?object crm:P108i_was_produced_by/crm:P7_took_place_at ?productionPlace . }}
        UNION {{ 
            ?object crm:P108i_was_produced_by/crm:P4_has_time-span ?productionTimeSpan . 
            OPTIONAL {{?productionTimeSpan crm:P82a_begin_of_the_begin ?startDate . }}
            OPTIONAL {{?productionTimeSpan crm:P82b_end_of_the_end ?endDate . }}
        }}
        UNION {{ ?object (crm:P24i_changed_ownership_through | crm:P30i_custody_transferred_through) / crm:P2_has_type ?provenanceType . }}
        UNION {{ 
            ?object (crm:P24i_changed_ownership_through | crm:P30i_custody_transferred_through) / crm:P4_has_time-span ?provenanceTimeSpan . 
            OPTIONAL {{?provenanceTimeSpan crm:P82a_begin_of_the_begin ?provenanceStart . }}
            OPTIONAL {{?provenanceTimeSpan crm:P82b_end_of_the_end ?provenanceEnd .}}
        }}
        UNION {{ ?object (crm:P24i_changed_ownership_through/crm:P23_transferred_title_from | crm:P30i_custody_transferred_through/crm:P28_custody_surrendered_by) ?provenanceFrom . }}
        UNION {{ ?object (crm:P24i_changed_ownership_through/crm:P22_transferred_title_to | crm:P30i_custody_transferred_through/crm:P29_custody_received_by) ?provenanceTo . }}
        UNION {{ ?object crm:P12_occurred_in_the_presence_of ?historicalEvent . }}
    }} LIMIT {BATCH_SIZE} OFFSET {offset}
    """
    
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"Error querying SPARQL endpoint: {e}")
        return []

def store_triples_in_graph(results, ds):
    graph = ds.graph(URIRef(f"{GRAPH_URI}"))
    
    for row in results:
        obj = URIRef(row["object"]["value"])
        graph.add((obj, RDF["type"], CRM["E22_Human-Made_Object"])) 
        if "image" in row:
            graph.add((obj, PM["shown_by"], URIRef(row["image"]["value"])))
        if "type" in row:
            graph.add((obj, CRM["P2_has_type"], URIRef(row["type"]["value"])))
        if "material" in row:
            graph.add((obj, PM["materials_used"], Literal(row["material"]["value"])))
        if "intendedUse" in row:
            graph.add((obj, PM["intended_use"], Literal(row["intendedUse"]["value"])))
        if "maker" in row:
            graph.add((obj, PM["maker"], URIRef(row["maker"]["value"])))
        if "productionPlace" in row:
            graph.add((obj, PM["production_place"], URIRef(row["productionPlace"]["value"])))
        if "productionTimeSpan" in row:
            productionTimeSpan_URI = URIRef(row["productionTimeSpan"]["value"])
            graph.add((obj, PM["production_time_span"], productionTimeSpan_URI))
            graph.add((productionTimeSpan_URI, RDF["type"], CRM["Time-Span"]))
            if "startDate" in row:
                graph.add((productionTimeSpan_URI, CRM["P82a_begin_of_the_begin"], Literal(row["startDate"]["value"])))
            if "endDate" in row:
                graph.add((productionTimeSpan_URI, CRM["P82b_end_of_the_end"], Literal(row["endDate"]["value"])))
        if "provenanceType" in row:
            graph.add((obj, PM["provenance_type"], URIRef(row["provenanceType"]["value"])))
        if "provenanceTimeSpan" in row:
            provenanceTimeSpan_URI = URIRef(row["provenanceTimeSpan"]["value"])
            graph.add((obj, CRM["P4_has_time-span"], provenanceTimeSpan_URI))
            graph.add((provenanceTimeSpan_URI, RDF["type"], CRM["Time-Span"]))
            if "provenanceStart" in row:
                graph.add((provenanceTimeSpan_URI, CRM["P82a_begin_of_the_begin"], Literal(row["provenanceStart"]["value"])))
            if "provenanceEnd" in row:
                graph.add((provenanceTimeSpan_URI, CRM["P82b_end_of_the_end"], Literal(row["provenanceEnd"]["value"])))
        if "provenanceFrom" in row:
            graph.add((obj, PM["provenance_from_actor"], URIRef(row["provenanceFrom"]["value"])))
        if "provenanceTo" in row:
            graph.add((obj, PM["provenance_to_actor"], URIRef(row["provenanceTo"]["value"])))
        if "historicalEvent" in row:
            graph.add((obj, PM["historical_event"], URIRef(row["historicalEvent"]["value"])))


def main():
    """Main function to execute paginated SPARQL queries and store the data."""
    offset = 0
    ds = Dataset()
    try:
        while True:
            print(f"Fetching data with OFFSET {offset}...")
            results = fetch_sparql_results(offset)
            
            if not results:
                print("No more data found. Stopping query.")
                break
            
            store_triples_in_graph(results, ds)
            offset += BATCH_SIZE
    except KeyboardInterrupt:
        print("\nProcess interrupted. Attempting to save extracted data...")
    finally:
        print(f"Saving extracted triples to {OUTPUT_FILE}...")
        ds.serialize(destination=OUTPUT_FILE, format="trig")
        print("Data successfully saved.")


if __name__ == "__main__":
    main()