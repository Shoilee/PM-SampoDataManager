import requests
import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, Dataset
import time
from tqdm import tqdm

# SPARQL Endpoint
NEW_GRAPH_URI = "https://pressimngmatter.nl/nmvw/graph/geonames"
ENDPOINT_URL = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
OUTPUT_FILE = "data/geonames.trig"
BATCH_SIZE = 1000  # Number of results per query

# Define Namespaces
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
PM = Namespace("https://pressingmatter.nl/")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
WGS84 = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

def fetch_sparql_results(offset):
    """Fetch SPARQL query results from the endpoint with pagination."""

    # Define the SPARQL query to retrieve all ?id with LIMIT and OFFSET placeholders
    query = f"""
        PREFIX skos: <{SKOS}>
   
        SELECT ?id WHERE {{
            ?place skos:inScheme <https://hdl.handle.net/20.500.11840/conceptscheme1> .
            ?place skos:exactMatch ?id .
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


# GeoNames API function to get latitude and longitude by GeoNames ID
def get_lat_lng(geoname_id):
    username = "sshoilee"  # Replace with your GeoNames username
    # print(f"Querying GeoNames for geoname_id: {geoname_id}")
    url = f"http://api.geonames.org/get?geonameId={geoname_id}&username={username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        # Extract latitude and longitude
        lat = root.findtext("lat")
        lng = root.findtext("lng")
        
        if lat and lng:
            return lat, lng
        
    else:
        print(f"Response code: {response.status_code}")
    return None, None


# Function to store triples in RDF graph
def store_triples_in_graph(results, ds):
    graph = ds.graph(URIRef(NEW_GRAPH_URI))
    for row in results:
        place = URIRef(row["id"]["value"])
        lat, lng = get_lat_lng(place.rstrip('/').split("/")[-1])

        if lat and lng:
            graph.add((place, WGS84["lat"], Literal(lat)))
            graph.add((place, WGS84["long"], Literal(lng)))
        else:
            print(f"Could not find coordinates for geoname_id: {place}")
    # print(f"Stored {len(results)} triples in the graph")

def main():
    start_time = time.time()
    offset = 0
    ds = Dataset()
    try:
        while True:
            results = fetch_sparql_results(offset)
            if not results:
                break  

            store_triples_in_graph(results, ds)
            offset += BATCH_SIZE

    except KeyboardInterrupt:
        print("\nScript interrupted by user. Saving RDF data before exiting...")
    finally:
        # Save RDF data to a Turtle file even if interrupted
        print(f"Saving extracted triples to {OUTPUT_FILE}...")
        ds.serialize(OUTPUT_FILE, format="trig")
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