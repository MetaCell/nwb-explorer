FROM metacell/jupyter-neuron:development

ARG BRANCH=feature/jupyter-backend

ENV GIT_URL=https://github.com/MetaCell/nwb-explorer/tarball/${BRANCH} \
  FOLDER=nwb

USER root
RUN apt-get update -qq &&\
  apt-get install python3-tk -qq
USER $NB_UID

RUN jupyter labextension disable @jupyterlab/hub-extension
  # jupyter labextension uninstall @jupyterlab/hub-extension &&\
  # conda remove jupyterlab

RUN /bin/echo -e "\e[1;93m Installing python requirements\e[0m"
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN /bin/echo -e "\e[1;93mDownloading branch $BRANCH for nwb-explorer \e[0m"

RUN mkdir ${FOLDER} &&\
  wget --no-verbose -O - ${GIT_URL} | tar xz -C ${FOLDER} --strip-components 1 &&\
  cd ${FOLDER}/utilities &&\
  python install.py branch ${BRANCH}

WORKDIR $HOME/${FOLDER}

EXPOSE 8000

CMD jupyter notebook --debug --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=nwb_explorer 