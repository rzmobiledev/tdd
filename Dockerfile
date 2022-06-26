FROM python:alpine3.15
LABEL maintainer="rzmobiledev@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /env/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /env/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        rzuser && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R rzuser:rzuser /vol && \
    chmod -R 755 /vol

ENV PATH="/env/bin:${PATH}"

USER rzuser