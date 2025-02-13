from rdflib import Graph, Namespace, URIRef, Literal, Dataset
from SPARQLWrapper import SPARQLWrapper, JSON
import os

# SPARQL Endpoint
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
GRAPH_URI = "https://data.colonialcollections.nl/nmvw/graph/objects"
OUTPUT_FILE = "../data/objects.trig"

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
AAT = Namespace("http://vocab.getty.edu/aat/")

# SPARQL Query
QUERY = f"""
PREFIX crm: <{CRM}>
PREFIX skos: <{SKOS}>
PREFIX rdfs: <{RDFS}>
PREFIX aat: <{AAT}>

SELECT ?object ?type ?typeLabel{{
    GRAPH <{GRAPH_URI}> {{
        ?object crm:P2_has_type ?type .
        OPTIONAL {{ ?type skos:prefLabel ?typeLabel . }}
        
        }}
}}LIMIT 10
"""

def fetch_sparql_results():
    """Fetch SPARQL query results from the endpoint."""
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(QUERY)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return results["results"]["bindings"]
    except Exception as e:
        print(f"Error querying SPARQL endpoint: {e}")
        return []

def store_triples_in_graph(results):
    ds = Dataset()
    graph = ds.graph(URIRef(f"{GRAPH_URI}"))

    for row in results:
        obj = URIRef(row["object"]["value"])

        if "type" in row:
            type_uri = URIRef(row["type"]["value"])
            graph.add((obj, CRM["P2_has_type"], type_uri))
            if "typeLabel" in row:
                graph.add((type_uri, SKOS["prefLabel"], Literal(row["typeLabel"]["value"])))

    return ds

def main():
    """Main function to execute the SPARQL query and store the data safely."""
    results = fetch_sparql_results()
    if not results:
        print("No data retrieved. Exiting.")
        return
    
    graph = store_triples_in_graph(results)

    try:
        print(f"Saving extracted triples to {OUTPUT_FILE}...")
        graph.serialize(destination=OUTPUT_FILE, format="trig")
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

