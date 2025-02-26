from rdflib import Graph, Namespace, URIRef, Literal, Dataset
from SPARQLWrapper import SPARQLWrapper, JSON
import time

# SPARQL Endpoint
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
OLD_GRAPH_URI = "https://data.colonialcollections.nl/nmvw/graph/objects"
NEW_GRAPH_URI = "https://data.colonialcollections.nl/nmvw/graph/objects"
OUTPUT_FILE = "data/objects.trig"
BATCH_SIZE = 1000  # Number of results per query

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
AAT = Namespace("http://vocab.getty.edu/aat/")
PM = Namespace("http:/pressingmatter.nl/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
DCT = Namespace("http://purl.org/dc/terms/")

def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX skos: <{SKOS}>
    PREFIX rdfs: <{RDFS}>
    PREFIX aat: <{AAT}>
    PREFIX dct: <{DCT}>
    
    SELECT ?object ?image ?title ?identifier ?inventoryNumber ?type ?material ?intendedUse__id ?intendedUse__label  ?maker ?productionPlace ?productionTimeSpan ?startDate ?endDate
           ?provenanceType ?provenanceTimeSpan ?provenanceStart ?provenanceEnd ?provenanceFrom ?provenanceTo ?historicalEvent {{
        # temporary constraints
        ?object crm:P141i_was_assigned_by/crm:P141_assigned <https://hdl.handle.net/20.500.11840/event423> .
        {{
            GRAPH <{OLD_GRAPH_URI}> {{
                ?object a crm:E22_Human-Made_Object .
            }}
        }}
        UNION {{ 
            ?object crm:P65_shows_visual_item ?i_BNODE .
            ?i_BNODE a crm:E36_Visual_Item .
            ?i_BNODE <https://linked.art/ns/terms/digitally_shown_by> ?image__id.
            ?image__id <https://linked.art/ns/terms/access_point> ?image .
        }}
        UNION {{ ?object dct:title ?title . }}
        UNION {{ 
            ?object crm:P1_is_identified_by ?identifier__id .
            ?identifier__id crm:P2_has_type <http://vocab.getty.edu/aat/300445023> .
            ?identifier__id crm:P190_has_symbolic_content ?identifier . 
        }}
        UNION {{ 
            ?object crm:P1_is_identified_by ?inventoryNumber__id .
            ?inventoryNumber__id crm:P2_has_type <http://vocab.getty.edu/aat/300404626> .
            ?inventoryNumber__id crm:P190_has_symbolic_content ?inventoryNumber . 
        }}
        UNION {{ ?object crm:P2_has_type ?type . }}
        UNION {{ ?object crm:P45_consists_of ?material . }}
        UNION {{ 
            ?object crm:P103_was_intended_for ?intendedUse__id . 
            ?intendedUse__id crm:P190_has_symbolic_content ?intendedUse__label . }}
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
        UNION {{ ?object crm:P141i_was_assigned_by/crm:P141_assigned ?historicalEvent . }}
    }} LIMIT {BATCH_SIZE} OFFSET {offset}
    """
    
    # print(query)

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
    graph = ds.graph(URIRef(f"{NEW_GRAPH_URI}"))
    
    for row in results:
        obj = URIRef(row["object"]["value"])
        graph.add((obj, RDF["type"], CRM["E22_Human-Made_Object"])) 
        if "image" in row:
            graph.add((obj, PM["shown_by"], Literal(row["image"]["value"])))
        if "title" in row:
            graph.add((obj, DCT["title"], Literal(row["title"]["value"])))
        if "identifier" in row:
            graph.add((obj, PM["identified_by"], Literal(row["identifier"]["value"])))
        if "inventoryNumber" in row:
            graph.add((obj, PM["inventory_number"], Literal(row["inventoryNumber"]["value"])))
        if "type" in row:
            graph.add((obj, CRM["P2_has_type"], URIRef(row["type"]["value"])))
        if "material" in row:
            graph.add((obj, PM["materials_used"], URIRef(row["material"]["value"])))
        if "intendedUse__id" in row:
            intendedUse = URIRef(row["intendedUse__id"]["value"])
            graph.add((obj, PM["intended_use"], intendedUse))
            graph.add((intendedUse, RDFS["label"], Literal(row["intendedUse__label"]["value"])))
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
            graph.add((obj, PM["provenance_time_span"], provenanceTimeSpan_URI))
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
            graph.add((obj, PM["related_to"], URIRef(row["historicalEvent"]["value"])))


def main():
    """Main function to execute paginated SPARQL queries and store the data."""
    start_time = time.time()
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

        print("\n")
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
        print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
        print(f"Total Triples Added: {len(ds)}")
        hours, rem = divmod(execution_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Execution Time: {int(hours)}h {int(minutes)}m {seconds:.4f}s")


if __name__ == "__main__":
    main()