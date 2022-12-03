FROM python:3.10 as base

#COPY ./deployment/apt/apt.conf /etc/apt/apt.conf
#COPY ./deployment/apt/reg.conf /etc/apt/auth.conf.d/reg.conf
#COPY ./deployment/apt/sources.list /etc/apt/sources.list

ENV USERNAME=app

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev libaio1 unzip && \
    apt-get clean -y && \
    apt-get autoclean -y && \
    rm -rf /var/lib/apt/lists/* /var/lib/log/* /tmp/* /var/tmp/*
#    rm /etc/apt/auth.conf.d/reg.conf

COPY ./components/backend/ /app
WORKDIR /app

RUN echo $(ls -l)
RUN pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir . \
    && python setup.py bdist_wheel

RUN groupadd -r $USERNAME && \
    useradd -r -g $USERNAME -d /home/$USERNAME -s /sbin/nologin -c "Docker image user" app

COPY --chown=app:app ./deployment/backend/entrypoint_*.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint_*.sh
WORKDIR /usr/local/lib/python3.10/site-packages/

USER $USERNAME

FROM base as final
