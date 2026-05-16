FROM python:3.11-slim
WORKDIR /app
COPY hub_discovery.py .
# Container blijft actief maar start de scan NIET automatisch.
# Start de scan manueel via: docker exec -it <container> python hub_discovery.py
CMD ["tail", "-f", "/dev/null"]
