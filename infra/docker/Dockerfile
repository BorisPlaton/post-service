ARG VENV=.venv
ARG APP_DIR=/app
ARG GID
ARG UID

FROM python:3.12 AS dependencies
ARG VENV
ARG APP_DIR
ARG GID
ARG UID

COPY pyproject.toml poetry.lock ./
ENV PATH="/${VENV}/bin:/root/.local/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    python -m venv ${VENV} && \
    poetry install --no-interaction --only main


FROM python:3.12-slim AS final
ARG VENV
ARG APP_DIR
ARG GID
ARG UID

ENV PATH="/${VENV}/bin:${PATH}"
ENV PYTHONPATH="${PYTHONPATH}:${APP_DIR}"

WORKDIR $APP_DIR

COPY --from=dependencies "/${VENV}" "/${VENV}"
COPY ./src .

RUN groupadd -g $GID appgroup && \
    useradd -u $UID -g $GID appuser && \
    chmod +x ${APP_DIR}/application/cli/app.py && \
    ln ${APP_DIR}/application/cli/app.py /usr/local/bin/ps_cli

USER appuser