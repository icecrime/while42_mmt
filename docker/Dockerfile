FROM kamon/grafana_graphite
MAINTAINER icecrime@gmail.com

# We want to use every service from kamon/grafana_graphite, we just need to
# override a few configuration in order to get a second granularity.
ADD statsd/config.js /src/statsd/config.js
ADD graphite/local_settings.py /var/lib/graphite/webapp/graphite/local_settings.py
ADD graphite/storage-schemas.conf /var/lib/graphite/conf/storage-schemas.conf

# Override Grafana default's dashboard with ours. Not very clean, but ok
# considering that we're not trying to building a general purpose container.
ADD grafana/dashboard.json /src/grafana/app/dashboards/default.json

# Same CMD than our parent image.
CMD ["/usr/bin/supervisord"]
