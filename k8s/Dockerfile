FROM metacell/jupyter-neuron:development

ARG BRANCH=feature/jupyter-backend

ENV GIT_URL=https://github.com/MetaCell/nwb-explorer/tarball/${BRANCH} \
  FOLDER=nwb

RUN /bin/echo -e "\e[1;93mDownloading branch $BRANCH for nwb-explorer \e[0m"

RUN mkdir ${FOLDER} &&\
  wget -O - ${GIT_URL} | tar xz -C ${FOLDER} --strip-components 1 &&\
  cd ${FOLDER}/utilities &&\
  python install.py branch ${BRANCH}

WORKDIR $HOME/${FOLDER}

EXPOSE 8000

CMD jupyter notebook --debug --NotebookApp.default_url=/geppetto --NotebookApp.token='' --library=nwb_explorer 