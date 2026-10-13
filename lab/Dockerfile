FROM ats-10.2.0-lab:local

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/opt/ats/bin:${PATH}"

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/* \
    && if ! id -u labuser >/dev/null 2>&1; then \
         useradd --uid 10000 --user-group --no-create-home \
             --shell /usr/sbin/nologin labuser; \
       fi \
    && mkdir -p /opt/lab/origin /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver \
    && printf 'ATS-JSONRPC-UNRESTRICTED-WITNESS\n' > /opt/lab/origin/index.html \
    && chown nobody:nogroup /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver \
    && chmod 0755 /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver

COPY jsonrpc.yaml /opt/ats/etc/trafficserver/jsonrpc.yaml
COPY remap.config /opt/ats/etc/trafficserver/remap.config
COPY entrypoint.sh /opt/lab/entrypoint.sh

RUN sed -i 's/server_ports: 8080 8080:ipv6/server_ports: 8080/' \
        /opt/ats/etc/trafficserver/records.yaml \
    && printf '%s\n' '/opt/ats/var/trafficserver 32M' \
        > /opt/ats/etc/trafficserver/storage.config \
    && chmod 0755 /opt/lab/entrypoint.sh \
    && chmod 0644 /opt/ats/etc/trafficserver/jsonrpc.yaml \
                  /opt/ats/etc/trafficserver/remap.config

EXPOSE 8080
ENTRYPOINT ["/opt/lab/entrypoint.sh"]
