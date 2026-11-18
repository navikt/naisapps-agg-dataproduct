FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

RUN python3 -m venv --without-pip /app/venv
COPY requirements.txt requirements.txt
RUN python3 -m pip --python /app/venv/bin/python install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest AS runner

WORKDIR /app

COPY main.py .
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]
