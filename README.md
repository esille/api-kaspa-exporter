# api-kaspa-exporter
 Prometheus exporter for api.kaspa.org

# Docker

Container command ```docker build -t api-kaspa-exporter:latest .```

Container run command `docker run --name api-kaspa-exporter -it -e KASPA_ADDRESS="kaspa:1,kaspa:2" -p 5001:5001 api-kaspa-exporter`
