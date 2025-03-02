FROM secoresearch/fuseki
# Add custom config file for Fuseki
COPY assembler.ttl $FUSEKI_BASE/configuration/assembler.ttl

# Copy data files
COPY --chown=9008 data/objects.trig /tmp/objects.trig
COPY --chown=9008 data/provEvents.trig /tmp/provEvents.trig
COPY --chown=9008 data/histEvents.trig /tmp/histEvents.trig
COPY --chown=9008 data/actors.trig /tmp/actors.trig
COPY --chown=9008 data/thesaurus.trig /tmp/thesaurus.trig
COPY --chown=9008 data/geonames.trig /tmp/geonames.trig
# COPY --chown=9008 data/sites.trig /tmp/sites.trig
# COPY --chown=9008 data/accession-objects.trig /tmp/accession-objects.trig
# COPY --chown=9008 data/deaccession-objects.trig /tmp/deaccession-objects.trig
# COPY --chown=9008 data/depiction-objects.trig /tmp/depiction-objects.trig
# COPY --chown=9008 data/geography-objects.trig /tmp/geography-objects.trig
# COPY --chown=9008 data/images-objects.trig /tmp/images-objects.trig
# COPY --chown=9008 data/keyword-objects.trig /tmp/keyword-objects.trig
# COPY --chown=9008 data/makers.trig /tmp/makers.trig
# COPY --chown=9008 data/material-objects.trig /tmp/material-objects.trig
# COPY --chown=9008 data/provenance-constituents.trig /tmp/provenance-constituents.trig
# COPY --chown=9008 data/provenance-objects.trig /tmp/provenance-objects.trig

# COPY --chown=9008 ttl/*.ttl /tmp/

# Load data into Fuseki and construct indexes
RUN $TDBLOADER /tmp/objects.trig \
    && $TDBLOADER /tmp/provEvents.trig \
    && $TDBLOADER /tmp/histEvents.trig \
    && $TDBLOADER /tmp/actors.trig \
    && $TDBLOADER /tmp/thesaurus.trig \
    && $TDBLOADER /tmp/geonames.trig \
    # && $TDBLOADER /tmp/accession-objects.trig \
    # && $TDBLOADER /tmp/deaccession-objects.trig \
    # && $TDBLOADER /tmp/depiction-objects.trig \
    # && $TDBLOADER /tmp/geography-objects.trig \
    # && $TDBLOADER /tmp/images-objects.trig \
    # && $TDBLOADER /tmp/keyword-objects.trig \
    # && $TDBLOADER /tmp/makers.trig \
    # && $TDBLOADER /tmp/material-objects.trig \
    # && $TDBLOADER /tmp/provenance-constituents.trig \
    # && $TDBLOADER /tmp/provenance-objects.trig \
    # && $TDBLOADER /tmp/sites.trig \
    && $TEXTINDEXER \
    && $TDBSTATS --graph urn:x-arq:UnionGraph > /tmp/stats.opt \
    && mv /tmp/stats.opt /fuseki-base/databases/tdb/ \
    && rm /tmp/objects.trig \
    && rm /tmp/provEvents.trig \
    && rm /tmp/histEvents.trig \
    && rm /tmp/actors.trig \
    && rm /tmp/thesaurus.trig \
    && rm /tmp/geonames.trig \
    # && rm /tmp/accession-objects.trig \
    # && rm /tmp/deaccession-objects.trig \
    # && rm /tmp/depiction-objects.trig \
    # && rm /tmp/geography-objects.trig \
    # && rm /tmp/images-objects.trig \
    # && rm /tmp/keyword-objects.trig \
    # && rm /tmp/makers.trig \
    # && rm /tmp/material-objects.trig \
    # && rm /tmp/provenance-constituents.trig \
    # && rm /tmp/provenance-objects.trig \
    # && rm /tmp/sites.trig