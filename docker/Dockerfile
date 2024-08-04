FROM ubuntu:jammy

RUN apt-get update && \
    apt-get install -y software-properties-common python3 python3-pip git cmake && \
    add-apt-repository ppa:jancaha/gis-tools && \
    apt-get update && \
    apt-get install -y viewshed-bin viewshed && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/apt/lists/*

RUN pip install wheel build
RUN pip install git+https://github.com/JanCaha/viewshed-library-pybind11
