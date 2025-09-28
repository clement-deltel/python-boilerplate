# Using uv in Docker: https://docs.astral.sh/uv/guides/integration/docker/
# Instructions creating a new layer: ADD, COPY, RUN

# https://github.com/astral-sh/uv/pkgs/container/uv
ARG DEBIAN_VERSION=bookworm-slim
ARG UV_VERSION=0.8.18

# https://github.com/GoogleContainerTools/distroless
ARG DEBIAN_DISTROLESS_VERSION=12

# ---------------------------------------------------------------------------- #
#               ------- Build Application ------
# ---------------------------------------------------------------------------- #
FROM ghcr.io/astral-sh/uv:${UV_VERSION}-${DEBIAN_VERSION} AS builder

# Not persisted into the builder image
ARG PYTHON_VERSION=3.11.13

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

# Clean up unnecessary files to reduce size
RUN find .venv \( \
    -name "*.pyc" -o \
    -name "*.pyo" -o \
    -name "*.pyd" -o \
    -name "__pycache__" -o \
    -name "test" \
    \) -exec rm -rf {} + 2>/dev/null || true

# ---------------------------------------------------------------------------- #
#               ------- Development Application ------
# ---------------------------------------------------------------------------- #
FROM debian:${DEBIAN_VERSION} AS development

# Not persisted into the runtime image
ARG DEBIAN_FRONTEND=noninteractive
ARG USER="app"
ARG ID="10001"
ARG HOME=/app
ARG VIRTUAL_ENV="${HOME}/.venv"
ARG MODE=505

# Place executables in the environment at the front of the path
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Set working directory
WORKDIR ${HOME}

# Create group, user, and home directory
RUN groupadd --gid ${ID} ${USER} && \
    useradd --create-home --home ${HOME} --uid ${ID} --gid ${ID} ${USER} &&\
# Remove setuid and setgid permissions to prevent privilege escalation
# https://github.com/goodwithtech/dockle/blob/master/CHECKPOINT.md#cis-di-0008
    chmod u-s /usr/bin/su /usr/bin/chsh /usr/bin/mount /usr/bin/chfn \
              /usr/bin/umount /usr/bin/newgrp /usr/bin/passwd /usr/bin/gpasswd && \
    chmod g-s /usr/bin/expiry /usr/sbin/unix_chkpwd /usr/bin/chage

# Copy Python installation and application virtual env from the builder, as well as entrypoint and healthcheck
COPY --from=builder --chmod=${MODE} /python /python
COPY --from=builder --chmod=${MODE} ${HOME}/.venv ${HOME}/.venv
COPY --chmod=${MODE} docker/healthcheck.py ${HOME}/healthcheck.py

USER ${USER}

# hadolint unsupported flag: --start-interval=10s
# See https://github.com/hadolint/hadolint/issues/978
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
    CMD python healthcheck.py || exit 1

ENTRYPOINT ["app_name"]
EXPOSE 5678

# ---------------------------------------------------------------------------- #
#               ------- Production Application ------
# ---------------------------------------------------------------------------- #
FROM gcr.io/distroless/python3-debian${DEBIAN_DISTROLESS_VERSION}:nonroot AS production

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL org.opencontainers.image.title="app-name"
LABEL org.opencontainers.image.description="app-description"
LABEL org.opencontainers.image.authors="Support - support@company.com"
LABEL org.opencontainers.image.vendor="Company Inc."

# Not persisted into the runtime image
ARG USER="nonroot"
# ARG ID="65532"
ARG HOME=/app
ARG VIRTUAL_ENV="${HOME}/.venv"
ARG MODE=505

# Place executables in the environment at the front of the path
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Set working directory
WORKDIR ${HOME}

# Copy Python installation and application virtual env from the builder, as well as healthcheck
COPY --from=builder --chmod=${MODE} /python /python
COPY --from=builder --chmod=${MODE} ${HOME}/.venv ${HOME}/.venv
COPY --chmod=${MODE} docker/healthcheck.py ${HOME}/healthcheck.py

USER ${USER}

# hadolint unsupported flag: --start-interval=10s
# See https://github.com/hadolint/hadolint/issues/978
HEALTHCHECK --interval=60s --timeout=10s --start-period=10s --retries=3 \
    CMD python healthcheck.py || exit 1

ENTRYPOINT ["app_name"]
EXPOSE 5678
