# TODO: place geonames in a trig file with the Named Graph
import requests
import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace
import time
from tqdm import tqdm

# Set up the SPARQL endpoint for the Colonial Collections data
sparql_endpoint = "https://api.colonialcollections.nl/datasets/nmvw/collection-archives/sparql"
sparql = SPARQLWrapper(sparql_endpoint)

# Define the SPARQL query to retrieve all ?id with LIMIT and OFFSET placeholders
base_query = """
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?id WHERE {{
        ?place skos:exactMatch ?id .
    }} LIMIT 100 OFFSET {}
"""

# Initialize RDF graph
g = Graph()

# GeoNames API function to get latitude and longitude by GeoNames ID
def get_lat_lng(geoname_id):
    username = "sshoilee"  # Replace with your GeoNames username
    print(f"Querying GeoNames for geoname_id: {geoname_id}")
    url = f"http://api.geonames.org/get?geonameId={geoname_id}&username={username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.text)
        # Extract latitude and longitude
        lat = root.findtext("lat")
        lng = root.findtext("lng")
        
        if lat and lng:
            return lat, lng
    return None, None

# Namespaces for RDF
WGS84 = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

# Function to retrieve paginated results from SPARQL endpoint
def fetch_sparql_results(offset=0):
    sparql.setQuery(base_query.format(offset))
    sparql.setReturnFormat(JSON)
    sparqlResponse = sparql.query().convert()
    return sparqlResponse["results"]["bindings"]

# Start with an initial offset of 0
offset = 0
batch_size = 100
ttl_file = "data/geonames.ttl"

try:
    while True:
        results = fetch_sparql_results(offset)
        if not results:
            break  # Stop fetching when no more results are returned

        # Process each result in the batch
        for result in tqdm(results, desc=f"Processing batch {offset // batch_size + 1}"):
            geoname_uri = result["id"]["value"]
            geoname_id = geoname_uri.rstrip('/').split('/')[-1]
            print(f"Retrieved geoname_id: {geoname_id}")

            # Call GeoNames API to get lat and lng for each id
            lat, lng = get_lat_lng(geoname_id)
            print(f"Retrieved lat={lat} and lng={lng}")

            if lat and lng:
                # Create RDF triples
                geo_uri = URIRef(geoname_uri)
                g.add((geo_uri, WGS84.lat, Literal(lat)))
                g.add((geo_uri, WGS84.long, Literal(lng)))

            # Optional: Add a sleep to avoid hitting the GeoNames API too quickly
            time.sleep(1)

        # Increase the offset for the next batch
        offset += batch_size

except KeyboardInterrupt:
    print("\nScript interrupted by user. Saving RDF data before exiting...")
finally:
    # Save RDF data to a Turtle file even if interrupted
    g.serialize(ttl_file, format="turtle")
    print(f"RDF data saved to {ttl_file}")
