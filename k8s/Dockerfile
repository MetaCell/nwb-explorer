FROM metacell/jupyter-neuron:development

ARG BRANCH=nwbdev

ENV GIT_URL=https://github.com/MetaCell/nwb-explorer/archive/development.zip \
    FOLDER=nwb-explorer-development

USER root
RUN apt-get update -qq &&\
    apt-get install python3-tk vim nano unzip -qq
USER $NB_UID

RUN jupyter labextension disable @jupyterlab/hub-extension

RUN /bin/echo -e "\e[1;93mDownloading nwb-explorer \e[0m"

RUN wget --no-verbose ${GIT_URL} &&\
    unzip development.zip &&\
    rm development.zip

RUN cd ${FOLDER}/utilities &&\
    python install.py branch ${BRANCH}

WORKDIR $HOME/$FOLDER

EXPOSE 8000

CMD jupyter notebook --debug --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=nwb_explorer 
