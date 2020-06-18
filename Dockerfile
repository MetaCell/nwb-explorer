FROM metacell/jupyter-neuron:development
ARG BUILD_DEV
ARG DEV_BRANCH

ENV FOLDER=nwb-explorer
ENV DEV=--dev

USER root
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip -qq
RUN npm i -g npm@6

RUN chown -R 1000:100 $HOME/.npm
USER $NB_UID

RUN jupyter labextension disable @jupyterlab/hub-extension

COPY --chown=1000:1000 . ${FOLDER}

RUN python $FOLDER/utilities/install.py  ${BUILD_DEV:+$DEV} ${DEV_BRANCH:+--branch=$DEV_BRANCH}
RUN mv $FOLDER/webapp/node_modules/@geppettoengine .
RUN rm -Rf $FOLDER/webapp/node_modules/*
RUN mv @geppettoengine $FOLDER/webapp/node_modules
WORKDIR $HOME/$FOLDER

EXPOSE 8000

CMD ./NWBE