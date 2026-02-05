FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e ".[dev]"

ENV TYNI_TRACE_DIR=/app/traces
RUN mkdir -p /app/traces /app/workspace

ENTRYPOINT ["tyni-fish"]
CMD ["--help"]
