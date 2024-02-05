FROM node:20 as jsbuild

ENV FOLDER=nwb-explorer


WORKDIR $FOLDER/webapp
COPY webapp/yarn.lock .
COPY webapp/package.json .
RUN yarn install --network-timeout 1000000000
COPY webapp/ .
RUN yarn build
#Remove node_modules, need to keep the geppetto client
RUN rm -Rf node_modules

###
FROM jupyter/base-notebook:hub-1.5.0
ENV NB_UID=jovyan
ENV FOLDER=nwb-explorer
USER root
RUN jupyter labextension disable @jupyterlab/hub-extension
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip git g++ -qq
  
COPY --chown=1000:1000 requirements.txt .   
RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip &&\ 
    pip install -r requirements.txt
USER $NB_UID

COPY --chown=$NB_UID:$NB_UID . $FOLDER 
COPY --from=jsbuild --chown=1000:1000 $FOLDER $FOLDER

WORKDIR $FOLDER
RUN mkdir workspace



# Temporary fix for deprecated api usage on some requirement
# RUN pip install setuptools==45

USER root

RUN --mount=type=cache,target=/root/.cache python -m pip install --upgrade pip &&\
    python utilities/install.py --npm-skip


RUN rm -rf /var/lib/apt/lists
# sym link workspace pvc to $FOLDER
RUN mkdir -p /opt/workspace
RUN mkdir -p /opt/home
# clean workspace from tests
RUN rm -Rf workspace/* 
RUN chown $NB_UID app.log
RUN chown $NB_UID /opt/workspace
RUN chown $NB_UID /opt/home
RUN ln -s /opt/workspace ./workspace
RUN ln -s /opt/home ./workspace

USER $NB_UID
CMD ./NWBE