FROM metacell/jupyter-neuron:development

ENV FOLDER=nwb-explorer

USER root
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip -qq
USER $NB_UID

RUN jupyter labextension disable @jupyterlab/hub-extension

COPY --chown=1000:1000 . ${FOLDER}

RUN python $FOLDER/utilities/install.py &&\
    rm -rf ${FOLDER}/webapp/node_modules ${FOLDER}/src/jupyter-geppetto/js/node_modules

WORKDIR $HOME/$FOLDER

CMD ./NWBE