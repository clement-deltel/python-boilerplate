# Using uv in Docker: https://docs.astral.sh/uv/guides/integration/docker/
# Instructions creating a new layer: ADD, COPY, RUN

ARG DEBIAN_VERSION=trixie-slim
ARG UV_VERSION=0.10.2

# ---------------------------------------------------------------------------- #
#               ------- Build Application ------
# ---------------------------------------------------------------------------- #
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-${DEBIAN_VERSION} AS builder

# Not persisted into the builder image
ARG PYTHON_VERSION=3.11.14

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
# pip: CVE-2026-1703 (Low)
# setuptools: CVE-2026-23949 (High)
    uv pip uninstall --break-system-packages --system pip setuptools

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-default-groups --no-install-project

# Copy application code into the image
COPY . .

# Build application wheel
RUN --mount=type=cache,target=/root/.cache/uv \
    uv build --cache-dir /root/.cache/uv --wheel

# ---------------------------------------------------------------------------- #
#               ------- Run Application ------
# ---------------------------------------------------------------------------- #
FROM docker.io/library/debian:${DEBIAN_VERSION} AS runtime

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="app-name"
LABEL org.opencontainers.image.description="app-description"
LABEL org.opencontainers.image.authors="Support - support@company.com"
LABEL org.opencontainers.image.vendor="Company Inc."

# Not persisted into the runtime image
ARG HOME=/app

WORKDIR ${HOME}

# Copy and install wheel file
COPY --from=builder /app/dist/*.whl ./
RUN pip install --no-cache-dir ./*.whl
