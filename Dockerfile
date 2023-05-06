# Edit the base image here, e.g., to use
# TENSORFLOW (https://hub.docker.com/r/tensorflow/tensorflow/)
# or a different PYTORCH (https://hub.docker.com/r/pytorch/pytorch/) base image
FROM pytorch/pytorch

RUN apt-get update
RUN apt-get install -y git-core

RUN groupadd -r algorithm && useradd -m --no-log-init -r -g algorithm algorithm


RUN mkdir -p /opt/algorithm /input /output \
    && chown algorithm:algorithm /opt/algorithm /input /output

USER algorithm

WORKDIR /opt/algorithm

ENV PATH="/home/algorithm/.local/bin:${PATH}"

RUN python -m pip install --user -U pip

COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
COPY --chown=algorithm:algorithm vendor/ /opt/algorithm/vendor/
RUN python -m pip install --user -r requirements.txt

COPY --chown=algorithm:algorithm process.py /opt/algorithm/
COPY --chown=algorithm:algorithm task_config.json /opt/algorithm/
COPY --chown=algorithm:algorithm artifact/ /opt/algorithm/artifact

ENTRYPOINT python -m process $0 $@

## ALGORITHM LABELS ##
# These labels are required
LABEL nl.diagnijmegen.rse.algorithm.name=Algorithm



