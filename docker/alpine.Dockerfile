# Using uv in Docker: https://docs.astral.sh/uv/guides/integration/docker/
# Instructions creating a new layer: ADD, COPY, RUN

ARG ALPINE_VERSION=3.21
ARG UV_VERSION=0.13.6

# ---------------------------------------------------------------------------- #
#               ------- Build Application ------
# ---------------------------------------------------------------------------- #
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-alpine${ALPINE_VERSION} AS builder

# Not persisted into the builder image
ARG PYTHON_VERSION=3.14.8

# Ensure that all commands within the Dockerfile compile bytecode
ENV UV_COMPILE_BYTECODE=1
# Cache mount used to improve performance across builds
ENV UV_LINK_MODE=copy
# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Set working directory to the `app` directory
WORKDIR /app

# Install Python before the application for caching
RUN uv python install ${PYTHON_VERSION} && \
# Solve CVEs
# msgpack: GHSA-6v7p-g79w-8964 (HIGH)
# setuptools: CVE-2025-47273 (HIGH)
# urllib3: CVE-2026-97687 (HIGH), CVE-2026-97689 (HIGH)
    uv pip uninstall --break-system-packages --system pip

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-default-groups --no-install-project

# Copy application code into the image
COPY . .

# Install application
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-default-groups --no-editable

# ---------------------------------------------------------------------------- #
#               ------- Run Application ------
# ---------------------------------------------------------------------------- #
FROM docker.io/library/alpine:${ALPINE_VERSION} AS runtime

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="app-name"
LABEL org.opencontainers.image.description="app-description"
LABEL org.opencontainers.image.authors="Support - support@company.com"
LABEL org.opencontainers.image.vendor="Company Inc."

# Not persisted into the runtime image
ARG USER=nonroot
ARG ID=65532
ARG HOME=/${USER}
ARG VIRTUAL_ENV="${HOME}/.venv"

# Place executables in the environment at the front of the path
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Set working directory
WORKDIR ${HOME}

# Create group, user, and home directory
RUN addgroup -g ${ID} ${USER} && \
    adduser -D -h ${HOME} -u ${ID} -G ${USER} ${USER}

# Copy the Python version, the application from the builder, and the entrypoint
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=${USER}:${USER} ${HOME}/.venv ${HOME}/.venv
COPY --chmod=500 --chown=${USER}:${USER} docker/entrypoint.sh ${HOME}/entrypoint.sh
COPY --chmod=500 --chown=${USER}:${USER} docker/healthcheck.py ${HOME}/healthcheck.py

USER ${USER}

HEALTHCHECK --interval=30s --timeout=10s --start-interval=10s --start-period=5s --retries=3 \
    CMD ["python healthcheck.py || exit 1"]

ENTRYPOINT ["./entrypoint.sh"]
