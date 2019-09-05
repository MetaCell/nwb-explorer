FROM metacell/jupyter-neuron:development

ARG BRANCH=2.0.0-alpha

ENV FOLDER=nwb-explorer

USER root
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip -qq
USER $NB_UID

RUN jupyter labextension disable @jupyterlab/hub-extension

RUN /bin/echo -e "\e[1;93mDownloading nwb-explorer \e[0m"

COPY --chown=1000:1000 . ${FOLDER}

RUN cd ${FOLDER}/utilities &&\
    python install.py branch ${BRANCH} &&\
    rm -rf ${FOLDER}/webapp/node_modules ${FOLDER}/src/jupyter-geppetto/js/node_modules

WORKDIR $HOME/$FOLDER

EXPOSE 8000

CMD jupyter notebook --debug --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=nwb_explorer 