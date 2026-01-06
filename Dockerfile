# TIBET Safety Chip - Docker Image
# Hardware-like AI Security at TPM Cost
#
# Build: docker build -t tibet-chip .
# Run:   docker run -i tibet-chip
#
# Part of HumoticaOS - https://humotica.com

FROM python:3.11-slim

LABEL maintainer="Jasper van de Meent <info@humotica.com>"
LABEL org.opencontainers.image.source="https://github.com/jaspertvdm/tibet-chip"
LABEL org.opencontainers.image.description="TIBET Safety Chip - Hardware-like AI Security at TPM Cost"
LABEL org.opencontainers.image.licenses="AGPL-3.0"

# Install from PyPI
RUN pip install --no-cache-dir tibet-chip

# MCP servers communicate via stdio
ENTRYPOINT ["python", "-m", "tibet_chip"]
