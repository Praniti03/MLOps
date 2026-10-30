# ---------------------------------------------------------------------------
# Multi-stage Dockerfile with two build targets
#
#   base   shared layers: slim Python, pinned dependencies, non-root user
#   test   runs the unit tests and a model-quality check during the build
#          -> if a test fails, `docker build` fails and no image is made
#   serve  prediction API (gunicorn) with a HEALTHCHECK
#   train  training job (the DEFAULT target, like the original lab)
#
#   docker build -t lab1:v1 .                          -> train image (original commands still work)
#   docker build --target serve -t lab1-serve:v2 .     -> serving image
#   docker compose up --build -d                       -> train, then serve, sharing a volume
# ---------------------------------------------------------------------------
ARG PYTHON_VERSION=3.11

# ---------- base ----------
FROM python:${PYTHON_VERSION}-slim AS base
LABEL org.opencontainers.image.title="Iris classifier (Docker Lab 1, modified)" \
      org.opencontainers.image.description="Multi-stage image: tested training job and prediction API"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODEL_DIR=/models
WORKDIR /app

# Dependencies first, so this layer is cached when only the code changes
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 1000 appuser \
    && mkdir -p /models && chown appuser /models

COPY src/ ./

# ---------- test ----------
FROM base AS test
ARG MIN_ACCURACY=0.85
ENV MIN_ACCURACY=${MIN_ACCURACY}
RUN pip install --no-cache-dir pytest==8.3.3
COPY tests/ ./tests/
RUN python -m pytest -v tests && touch /tmp/tests_passed

# ---------- serve ----------
FROM base AS serve
# Depending on a file from the test stage forces the tests to run first
COPY --from=test /tmp/tests_passed /tmp/tests_passed
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health', timeout=2).status == 200 else 1)"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "serve:app"]

# ---------- train (default target: keep it last) ----------
FROM base AS train
ARG N_ESTIMATORS=100
ARG IMAGE_VERSION=v2
ENV N_ESTIMATORS=${N_ESTIMATORS} \
    IMAGE_VERSION=${IMAGE_VERSION}
COPY --from=test /tmp/tests_passed /tmp/tests_passed
USER appuser
CMD ["python", "main.py"]
