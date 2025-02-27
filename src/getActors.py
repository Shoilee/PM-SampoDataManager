from rdflib import Graph, Namespace, URIRef, Literal, Dataset
from SPARQLWrapper import SPARQLWrapper, JSON
import time

# SPARQL Endpoint
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
NEW_GRAPH_URI = "https://pressingmatter.nl/nmvw/graph/actors"
OUTPUT_FILE = "data/actors.trig"
BATCH_SIZE = 100  # Number of results per query

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
PM = Namespace("https://pressingmatter.nl/")
AAT = Namespace("http://vocab.getty.edu/aat/")


def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX rdfs: <{RDFS}>
    PREFIX rdf: <{RDF}>
    PREFIX aat: <{AAT}>
    
    SELECT ?actor ?label ?name ?type ?role ?gender ?nationality ?biography ?remarks ?profession WHERE {{
        # temporary constraints
        # ?object crm:P141i_was_assigned_by/crm:P141_assigned <https://hdl.handle.net/20.500.11840/event423> .
        # ?object crm:P24i_changed_ownership_through/crm:P23_transferred_title_from  ?actor .

        ?actor rdf:type ?type .
        FILTER(?type IN (crm:E21_Person, crm:E74_Group, crm:E39_Actor))
        {{ 
            ?actor crm:P1_is_identified_by ?name_id .
            ?name_id crm:P2_has_type aat:300404650 ;
            crm:P190_has_symbolic_content ?name .
        }}
        UNION {{ ?actor rdfs:label ?label . }}
        UNION {{ ?actor crm:P2_has_type/rdfs:label ?role . }}
        UNION {{ 
            ?actor crm:P67i_is_referred_to_by ?gender_id .
            ?gender_id crm:P2_has_type aat:300055147 ;
            crm:P190_has_symbolic_content ?gender . 
        }}
        UNION {{ 
            ?actor crm:P67i_is_referred_to_by ?nationality_id .
            ?nationality_id crm:P2_has_type aat:300379842 ;
            crm:P190_has_symbolic_content ?nationality . 
        }}
        UNION {{ 
            ?actor crm:P67i_is_referred_to_by ?biography_id .
            ?biography_id crm:P2_has_type aat:300435422 ;
            crm:P190_has_symbolic_content ?biography . 
        }}
        UNION {{ 
            ?actor crm:P67i_is_referred_to_by ?remarks_id .
            ?remarks_id crm:P2_has_type aat:300435415 ;
            crm:P190_has_symbolic_content ?remarks . 
        }}
        UNION {{ 
            ?actor crm:P67i_is_referred_to_by ?profession_id .
            ?profession_id crm:P2_has_type aat:300393201 ;
            crm:P190_has_symbolic_content ?profession . 
        }}
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
    """Store fetched triples into a new graph."""
    graph = ds.graph(URIRef(f"{NEW_GRAPH_URI}"))
    
    for row in results:
        actor = URIRef(row["actor"]["value"])
        if "label" in row:
            graph.add((actor, RDFS["label"], Literal(row["label"]["value"])))
        if "name" in row:
            graph.add((actor, PM["identified_by"], Literal(row["name"]["value"])))
        if "type" in row:
            graph.add((actor, RDF["type"], URIRef(row["type"]["value"])))
        if "role" in row:
            graph.add((actor, PM["roles"], Literal(row["role"]["value"])))
        if "gender" in row:
            graph.add((actor, PM["gender"], Literal(row["gender"]["value"])))
        if "nationality" in row:
            graph.add((actor, PM["nationality"], Literal(row["nationality"]["value"])))
        if "biography" in row:
            graph.add((actor, PM["biography"], Literal(row["biography"]["value"])))
        if "remarks" in row:
            graph.add((actor, PM["remarks"], Literal(row["remarks"]["value"])))
        if "profession" in row:
            graph.add((actor, PM["profession"], Literal(row["profession"]["value"])))


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
