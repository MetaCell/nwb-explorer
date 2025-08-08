FROM node:20 as jsbuild

ENV FOLDER=nwb-explorer


WORKDIR $FOLDER/webapp
COPY webapp/yarn.lock .
COPY webapp/package.json .
RUN yarn install --network-timeout 1000000000
COPY webapp/ .
RUN yarn build && rm -Rf node_modules

###
FROM quay.io/jupyter/base-notebook:latest
ENV NB_UID=jovyan
ENV FOLDER=nwb-explorer
USER root
RUN jupyter labextension disable @jupyterlab/hub-extension
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip git g++ -qq\
    && rm -rf /var/lib/apt/lists
USER $NB_UID
COPY --chown=1000:1000 requirements.txt .   
RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip &&\ 
    pip install -r requirements.txt


COPY --chown=$NB_UID:$NB_UID . $FOLDER 
COPY --from=jsbuild --chown=$NB_UID:$NB_UID $FOLDER $FOLDER

WORKDIR $FOLDER
RUN mkdir workspace


# RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip &&\
#     python utilities/install.py --npm-skip

USER root
# sym link workspace pvc to $FOLDER
RUN mkdir -p /opt/workspace
RUN mkdir -p /opt/home
# clean workspace from tests
RUN rm -Rf workspace/* 
RUN chown $NB_UID /opt/workspace
RUN chown $NB_UID /opt/home
RUN ln -s /opt/workspace ./workspace
RUN ln -s /opt/home ./workspace

USER $NB_UID
CMD ./NWBE