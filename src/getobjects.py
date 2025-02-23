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

def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""
    query = f"""
    PREFIX crm: <{CRM}>
    PREFIX skos: <{SKOS}>
    PREFIX rdfs: <{RDFS}>
    PREFIX aat: <{AAT}>
    
    SELECT ?object ?type ?material ?intendedUse {{
        GRAPH <{GRAPH_URI}> {{
            ?object a crm:E22_Human-Made_Object .
        }}
        
        # Object Type
        {{
            ?object crm:P2_has_type ?type .
            ?type skos:inScheme <https://hdl.handle.net/20.500.11840/conceptscheme2> .
        }}
        
        # Materials
        UNION {{
            ?object crm:P45_consists_of/skos:altLabel ?material .
        }}
        
        # Intended Use
        UNION {{
            ?object crm:P103_was_intended_for/crm:P190_has_symbolic_content ?intendedUse .
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
    graph = ds.graph(URIRef(f"{GRAPH_URI}"))
    
    for row in results:
        obj = URIRef(row["object"]["value"])
        
        if "type" in row:
            type_uri = URIRef(row["type"]["value"])
            graph.add((obj, CRM["P2_has_type"], type_uri))
        
        if "material" in row:
            material_label = Literal(row["material"]["value"])
            graph.add((obj, PM["materials_used"], material_label))
        
        if "intendedUse" in row:
            intended_use_label = Literal(row["intendedUse"]["value"])
            graph.add((obj, PM["intended_use"], intended_use_label))

def main():
    """Main function to execute paginated SPARQL queries and store the data."""
    offset = 0
    ds = Dataset()
    
    while True:
        print(f"Fetching data with OFFSET {offset}...")
        results = fetch_sparql_results(offset)
        
        if not results:
            print("No more data found. Stopping query.")
            break
        
        store_triples_in_graph(results, ds)
        offset += BATCH_SIZE
    
    try:
        print(f"Saving extracted triples to {OUTPUT_FILE}...")
        ds.serialize(destination=OUTPUT_FILE, format="trig")
        print("Data successfully saved.")
    except Exception as e:
        print(f"Error saving .trig file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Attempting to save extracted data...")
        if os.path.exists(OUTPUT_FILE):
            print(f"Partial data saved in {OUTPUT_FILE}")
        else:
            print("No data was retrieved before interruption.")
