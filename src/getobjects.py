from rdflib import Graph, Namespace, URIRef, Literal, Dataset, XSD
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
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
PM = Namespace("https://pressingmatter.nl/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
DCT = Namespace("http://purl.org/dc/terms/")

# Fetch SPARQL query results from the endpoint with pagination.
def get_target_instance(offset):
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX skos: <{SKOS}>
    PREFIX rdfs: <{RDFS}>
    PREFIX aat: <{AAT}>
    PREFIX dct: <{DCT}>
    
    SELECT ?object {{
        # temporary constraints
        # ?object crm:P141i_was_assigned_by/crm:P141_assigned <https://hdl.handle.net/20.500.11840/event423> .
        {{
            GRAPH <{OLD_GRAPH_URI}> {{
                ?object a crm:E22_Human-Made_Object .
            }}
        }}
    }} LIMIT {BATCH_SIZE} OFFSET {offset}
    """
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        return [str(row["object"]["value"]) for row in results["results"]["bindings"]]
    except Exception as e:
        print(f"Error querying SPARQL endpoint: {e}")
        return []
    
# Executes a given SPARQL query and returns the results.
def execute_sparql_query(query):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"Error querying SPARQL endpoint: {e}")
        return []

# Fetch object image from the SPARQL endpoint.
def query_images(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?image WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P65_shows_visual_item ?i_BNODE .
        ?i_BNODE a crm:E36_Visual_Item .
        ?i_BNODE <https://linked.art/ns/terms/digitally_shown_by> ?image__id.
        ?image__id <https://linked.art/ns/terms/access_point> ?image .
    }}
    """
    return execute_sparql_query(query)

# Fetch the title of the object.
def query_title(instance):
    query = f"""
    PREFIX dct: <{DCT}>
    SELECT ?object ?title WHERE {{
        BIND(<{instance}> AS ?object)
        ?object dct:title ?title .
    }}
    """
    return execute_sparql_query(query)

# Fetch the identifier of the object.
def query_identifier(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?identifier WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P1_is_identified_by ?identifier__id .
        ?identifier__id crm:P2_has_type <http://vocab.getty.edu/aat/300445023> .
        ?identifier__id crm:P190_has_symbolic_content ?identifier .
    }}
    """
    return execute_sparql_query(query)

# Fetch the inventory number of the object.
def query_inventory_number(instance_uri):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?inventoryNumber WHERE {{
        BIND(<{instance_uri}> AS ?object)
        ?object crm:P1_is_identified_by ?inventoryNumber__id .
        ?inventoryNumber__id crm:P2_has_type <http://vocab.getty.edu/aat/300404626> .
        ?inventoryNumber__id crm:P190_has_symbolic_content ?inventoryNumber .
    }}
    """
    return execute_sparql_query(query)

# Fetch the type of the object.
def query_type(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?type WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P2_has_type ?type .
        
    }}
    """
    return execute_sparql_query(query)

# Fetch the material of the object.
def query_material(instance):

    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?material WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P45_consists_of ?material .
    }}
    """
    return execute_sparql_query(query)

# Fetch the intended use of the object.
def query_intended_use(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?intendedUse__id ?intendedUse__label WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P103_was_intended_for ?intendedUse__id . 
        ?intendedUse__id crm:P190_has_symbolic_content ?intendedUse__label . 
    }}
    """
    return execute_sparql_query(query)

# Fetch the object's production (maker, place, timespan) of the object.
def query_production_details(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?maker ?productionPlace ?productionTimeSpan ?startDate ?endDate WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P108i_was_produced_by ?production__id .
        OPTIONAL{{
            ?production__id crm:P108i_was_produced_by/crm:P14_carried_out_by ?maker .
        }}
        OPTIONAL{{
            ?production__id crm:P108i_was_produced_by/crm:P7_took_place_at ?productionPlace .
        }}
        OPTIONAL {{
            ?production__id crm:P108i_was_produced_by/crm:P4_has_time-span ?productionTimeSpan . 
            OPTIONAL {{?productionTimeSpan crm:P82a_begin_of_the_begin ?startDate . }}
            OPTIONAL {{?productionTimeSpan crm:P82b_end_of_the_end ?endDate . }}
        }}
    }}
    """
    return execute_sparql_query(query)

# Fetch the provenance details (type, time span, actors involved) of the object.
def query_provenance_details(instance):
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?provenanceType ?provenanceTimeSpan ?provenanceStart ?provenanceEnd ?provenanceFrom ?provenanceTo WHERE {{
        BIND(<{instance}> AS ?object)
        ?object (crm:P24i_changed_ownership_through | crm:P30i_custody_transferred_through) ?provenance__id .
        OPTIONAL{{
            ?provenance__id crm:P2_has_type ?provenanceType .
        }}
        OPTIONAL {{
            ?provenance__id crm:P4_has_time-span ?provenanceTimeSpan .
            OPTIONAL{{?provenanceTimeSpan crm:P82a_begin_of_the_begin ?provenanceStart .}}
            OPTIONAL{{?provenanceTimeSpan crm:P82b_end_of_the_end ?provenanceEnd .}}
        }}
        OPTIONAL {{
            ?provenance__id crm:P23_transferred_title_from | crm:P28_custody_surrendered_by ?provenanceFrom .
        }}
        OPTIONAL {{
            ?provenance__id crm:P22_transferred_title_to | crm:P29_custody_received_by ?provenanceTo .
        }}
    }}
    """
    return execute_sparql_query(query)

# Fetch historical events related to the object.
def query_historical_events(instance):
    """Fetch historical events related to the object."""
    query = f"""
    PREFIX crm: <{CRM}>
    SELECT ?object ?historicalEvent WHERE {{
        BIND(<{instance}> AS ?object)
        ?object crm:P141i_was_assigned_by/crm:P141_assigned ?historicalEvent .
    }}
    """
    return execute_sparql_query(query)


def store_triples_in_graph(results, ds):
    graph = ds.graph(URIRef(f"{NEW_GRAPH_URI}"))

    for row in results:
        obj = URIRef(row["object"]["value"])
        graph.add((obj, RDF["type"], CRM["E22_Human-Made_Object"])) 
        graph.add((obj, PM["source"], URIRef("https://wereldmuseum.nl/")))
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
                graph.add((productionTimeSpan_URI, CRM["P82a_begin_of_the_begin"], Literal(row["startDate"]["value"], datatype=XSD.date)))
            if "endDate" in row:
                graph.add((productionTimeSpan_URI, CRM["P82b_end_of_the_end"], Literal(row["endDate"]["value"], datatype=XSD.date)))
        if "provenanceType" in row:
            graph.add((obj, PM["provenance_type"], URIRef(row["provenanceType"]["value"])))
        if "provenanceTimeSpan" in row:
            provenanceTimeSpan_URI = URIRef(row["provenanceTimeSpan"]["value"])
            graph.add((obj, PM["provenance_time_span"], provenanceTimeSpan_URI))
            graph.add((provenanceTimeSpan_URI, RDF["type"], CRM["Time-Span"]))
            if "provenanceStart" in row:
                graph.add((provenanceTimeSpan_URI, CRM["P82a_begin_of_the_begin"], Literal(row["provenanceStart"]["value"], datatype=XSD.date)))
            if "provenanceEnd" in row:
                graph.add((provenanceTimeSpan_URI, CRM["P82b_end_of_the_end"], Literal(row["provenanceEnd"]["value"], datatype=XSD.date)))
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
            # results = fetch_sparql_results(offset)
            uri_list = get_target_instance(offset)

            if len(uri_list) == 0:
                print("No more instance found. Stopping query.")
                break
            
            for uri in tqdm(uri_list):
                results = query_images(uri)
                store_triples_in_graph(results, ds)

                results = query_title(uri)
                store_triples_in_graph(results, ds)

                results = query_identifier(uri)
                store_triples_in_graph(results, ds)

                results = query_inventory_number(uri)
                store_triples_in_graph(results, ds)

                results = query_type(uri)
                store_triples_in_graph(results, ds)

                results = query_material(uri)
                store_triples_in_graph(results, ds)

                results = query_intended_use(uri)
                store_triples_in_graph(results, ds)

                results = query_production_details(uri)
                store_triples_in_graph(results, ds)

                results = query_provenance_details(uri)
                store_triples_in_graph(results, ds)

                results = query_historical_events(uri)
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