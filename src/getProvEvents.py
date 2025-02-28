from rdflib import Graph, Namespace, URIRef, Literal, Dataset, XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import time

# SPARQL Endpoint
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
NEW_GRAPH_URI = "https://pressimngmatter.nl/nmvw/graph/provenance"
OUTPUT_FILE = "data/provEvents.trig"
BATCH_SIZE = 1000  # Number of results per query

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
DCT = Namespace("http://purl.org/dc/terms/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
PM = Namespace("https://pressingmatter.nl/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")


def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX dct: <{DCT}>
    PREFIX rdfs: <{RDFS}>
    PREFIX rdf: <{RDF}>
    
    SELECT ?event ?object ?eventLabel ?provType ?eventType ?timeSpan ?startDate ?endDate ?fromActor ?toActor {{
        # temporary constraints
        ?object crm:P141i_was_assigned_by/crm:P141_assigned <https://hdl.handle.net/20.500.11840/event423> .
        ?object crm:P24i_changed_ownership_through | crm:P30i_custody_transferred_through ?event .
        ?event rdf:type ?provType .
        {{?event rdfs:label ?eventLabel .}}
        UNION{{?event crm:P2_has_type ?eventType .}}
        UNION{{
            ?event crm:P4_has_time-span ?timeSpan .
            OPTIONAL {{?timeSpan crm:P82a_begin_of_the_begin ?startDate .}}
            OPTIONAL {{?timeSpan crm:P82b_end_of_the_end ?endDate .}}
        }}
        UNION{{?event crm:P23_transferred_title_from | crm:P28_Custody_Surrendered_by ?fromActor .}}
        UNION{{?event crm:P22_transferred_title_to | crm:P29_Custody_Recieved_By  ?toActor .}}
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
        event = URIRef(row["event"]["value"])
        prov_type = URIRef(row["provType"]["value"])
        graph.add((event, RDF["type"], prov_type))
        if "object" in row:
            obj = URIRef(row["object"]["value"])
            if prov_type == CRM["E10_Transfer_of_Custody"]:
                graph.add((obj, CRM["P30i_custody_transferred_through"], event))
            if prov_type == CRM["E8_Acquisition"]:   
                graph.add((obj, CRM["P24i_changed_ownership_through"], event))
        if "fromActor" in row:
            if prov_type == CRM["E10_Transfer_of_Custody"]:
                graph.add((event, CRM["crm:P28_Custody_Surrendered_by"], URIRef(row["fromActor"]["value"])))
            if prov_type == CRM["E8_Acquisition"]:
                graph.add((event, CRM["P23_transferred_title_from"], URIRef(row["fromActor"]["value"])))
        if "toActor" in row:
            if prov_type == CRM["E10_Transfer_of_Custody"]:
                graph.add((event, CRM["crm:P29_Custody_Recieved_By"], URIRef(row["toActor"]["value"])))
            if prov_type == CRM["E8_Acquisition"]:
                graph.add((event, CRM["P22_transferred_title_to"], URIRef(row["toActor"]["value"])))
        if "eventLabel" in row:
            graph.add((event, RDFS["label"], Literal(row["eventLabel"]["value"])))
        if "eventType" in row:
            graph.add((event, CRM["P2_has_type"], URIRef(row["eventType"]["value"])))
        if "timeSpan" in row:
            timeSpan_URI = URIRef(row["timeSpan"]["value"])
            graph.add((event, CRM["P4_has_time-span"], timeSpan_URI))
            graph.add((timeSpan_URI, RDF["type"], CRM["Time-Span"]))
            if "startDate" in row:
                graph.add((timeSpan_URI, CRM["P82a_begin_of_the_begin"], Literal(row["startDate"]["value"], datatype=XSD.date)))
            if "endDate" in row:
                graph.add((timeSpan_URI, CRM["P82b_end_of_the_end"], Literal(row["endDate"]["value"], datatype=XSD.date)))
        


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