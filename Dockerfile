FROM secoresearch/fuseki
# Add custom config file for Fuseki
COPY assembler.ttl $FUSEKI_BASE/configuration/assembler.ttl

# Copy data files
# COPY --chown=9008 data/accession-objects.trig /tmp/accession-objects.trig
# COPY --chown=9008 data/deaccession-objects.trig /tmp/deaccession-objects.trig
# COPY --chown=9008 data/depiction-objects.trig /tmp/depiction-objects.trig
# COPY --chown=9008 data/geography-objects.trig /tmp/geography-objects.trig
# COPY --chown=9008 data/histEvents.trig /tmp/histEvents.trig
# COPY --chown=9008 data/images-objects.trig /tmp/images-objects.trig
# COPY --chown=9008 data/keyword-objects.trig /tmp/keyword-objects.trig
# COPY --chown=9008 data/makers.trig /tmp/makers.trig
# COPY --chown=9008 data/material-objects.trig /tmp/material-objects.trig
# COPY --chown=9008 data/objects.trig /tmp/objects.trig
# COPY --chown=9008 data/provenance-constituents.trig /tmp/provenance-constituents.trig
# COPY --chown=9008 data/provenance-objects.trig /tmp/provenance-objects.trig
COPY --chown=9008 data/sites.trig /tmp/sites.trig
# COPY --chown=9008 data/thesaurus.trig /tmp/thesaurus.trig
# COPY --chown=9008 ttl/*.ttl /tmp/

# Load data into Fuseki and construct indexes
RUN $TDBLOADER /tmp/sites.trig \
    && $TEXTINDEXER \
    && $TDBSTATS --graph urn:x-arq:UnionGraph > /tmp/stats.opt \
    && mv /tmp/stats.opt /fuseki-base/databases/tdb/ \
    && rm /tmp/sites.trig 
