FROM python:3.10 as base

COPY ./deployment/apt/apt.conf /etc/apt/apt.conf
COPY ./deployment/apt/reg.conf /etc/apt/auth.conf.d/reg.conf
COPY ./deployment/apt/sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends unixodbc-dev libaio1 unzip && \
    apt-get clean -y && \
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/* && \
    rm /etc/apt/auth.conf.d/reg.conf

WORKDIR /app

# ====================================================

FROM base as magnit-build

#ENV PIP_CONFIG_FILE=/app/pip.conf
ENV USERNAME=app
ENV PATH=$PATH:/opt/bin

RUN groupadd -r $USERNAME && \
    useradd -r -g $USERNAME -d /home/$USERNAME -s /sbin/nologin -c "Docker image user" app

COPY ./deployment/backend/entrypoint_*.sh /usr/bin/
COPY ./components/digital_tipster/pip.conf /app/pip.conf
RUN chmod +x /usr/bin/entrypoint_*.sh

COPY ./components/backend /app
RUN pip install --upgrade --no-cache-dir pip && \
    pip -vvv install --no-cache-dir . && \
    python setup.py bdist_wheel

WORKDIR /usr/local/lib/python3.10/site-packages/

USER $USERNAME

# ====================================================
#FROM digital_tipster-build as digital_tipster-tests
#
#ENV PIP_CONFIG_FILE=/app/pip.conf
#USER root
#WORKDIR /app
#COPY ./components/digital_tipster/pip.conf /app/pip.conf
#
#RUN pip install --no-cache-dir -e .[dev] && \
#    pytest ./digital_tipster/ ./tests/build_tests && \
#    rm -fr /app/pip.conf

# ====================================================
FROM magnit-build as magnit-final
