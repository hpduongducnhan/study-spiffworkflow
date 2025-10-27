FROM python:3.12.9-slim-bookworm

ARG PROJECT_NAME="loadtestem"
ARG PROJECT_VERSION="0.1.0"

ENV http_proxy=http://proxy.hcm.fpt.vn:80
ENV https_proxy=http://proxy.hcm.fpt.vn:80
ENV no_proxy=localhost,127.0.0.1,::1,172.24.222.112,172.27.230.30
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8

# install debug tool
RUN apt update
RUN apt-get -y update
RUN apt-get install -y --no-install-recommends \
    make \
    libffi-dev \
    libheif-dev \
    libde265-dev \
    ffmpeg \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    gcc \
    python3-dev \
    libpq-dev \
    mime-support \
    telnet \
    iputils-ping \
    curl \
    htop \
    vim \
    procps \
    net-tools \
    tini \
    && rm -rf /var/lib/apt/lists/*

# create main directory and logs directory
RUN mkdir -p /app/statics /app/logs
#    && ls -al /app

WORKDIR /app

# install poetry and dependency
COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/

RUN --mount=type=cache,target=/root/.cache/pip,id=scc/$PROJECT_NAME pip3 install --upgrade pip \
    && pip3 install poetry==2.1.3 wheel \
    && poetry config virtualenvs.in-project true

RUN poetry install
RUN poetry run pip install taskiq-redis

# copy neccessary files
COPY . .


# EXPOSE 8688
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["make", "pro-api-run"]
