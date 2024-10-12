ARG sha=unknown
ARG version=unknown

FROM python:3.13-slim AS base
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.4.24 /uv /uvx /bin/

FROM base AS bootstr
ARG sha
ARG version
RUN groupadd --system bootstr && useradd --system --create-home --gid bootstr bootstr
USER bootstr
WORKDIR /bootstr
ENV PATH="/bootstr/.venv/bin:$PATH"
COPY --chown=bootstr:bootstr uv.lock uv.lock
COPY --chown=bootstr:bootstr pyproject.toml pyproject.toml
RUN uv sync --frozen --compile-bytecode --no-install-workspace --no-dev
COPY --chown=bootstr:bootstr packages packages
COPY --chown=bootstr:bootstr applications applications
RUN uv sync --frozen --compile-bytecode --no-dev
ENV BUILD_SHA="${sha}"
ENV BUILD_VERSION="${version}"

FROM bootstr AS dev
RUN uv sync --frozen --compile-bytecode
