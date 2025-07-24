# Using uv in Docker: https://docs.astral.sh/uv/guides/integration/docker/
# Instructions creating a new layer: ADD, COPY, RUN

ARG PYTHON_VERSION=3.11.8

# --------------------------------------------------------------------------- #
#               ------- Build Application ------
# --------------------------------------------------------------------------- #
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
WORKDIR /app

# Ensure that all commands within the Dockerfile compile bytecode
ENV UV_COMPILE_BYTECODE=1
# Cache mount used to improve performance across builds
ENV UV_LINK_MODE=copy
# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python
# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python before the application for caching
RUN uv python install ${PYTHON_VERSION}

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

# --------------------------------------------------------------------------- #
#               ------- Run Application ------
# --------------------------------------------------------------------------- #
FROM debian:bookworm-slim AS runtime

LABEL org.opencontainers.image.title="app"
LABEL org.opencontainers.image.description="app"
LABEL org.opencontainers.image.authors="Support - support@company.com"
LABEL org.opencontainers.image.vendor="Company Inc."

# Not persisted into the runtime image
ARG USER="app"
ARG ID="1000"
ARG HOME=/home/app
ARG VIRTUAL_ENV="${HOME}/.venv"

# Ensure apt-get doesn't open a menu on you
ENV DEBIAN_FRONTEND=noninteractive
# Place executables in the environment at the front of the path
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Create group, user, and home directory
RUN groupadd --gid ${ID} ${USER} && \
    useradd --create-home --home ${HOME} --uid ${ID} --gid ${ID} ${USER}

# Copy the Python version, the application from the builder, and the entrypoint
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=${USER}:${USER} /app ${HOME}
COPY --chown=${USER}:${USER} docker/entrypoint.sh ${HOME}/entrypoint.sh
RUN chmod +x ${HOME}/entrypoint.sh
WORKDIR ${HOME}
USER ${USER}

ENTRYPOINT ["./entrypoint.sh"]
