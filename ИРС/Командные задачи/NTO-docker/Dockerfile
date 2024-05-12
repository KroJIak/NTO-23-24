FROM ubuntu:20.04

RUN apt-get -y update && apt-get upgrade -y && apt-get install -y locales

ENV DEBIAN_FRONTEND noninteractive

RUN sed -i -e \
  's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
   && locale-gen
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /workspace

RUN apt-get -y update && apt-get upgrade -y

RUN apt install git vim build-essential cmake g++ libopencv-dev software-properties-common \
      mesa-utils libcanberra-gtk-module libcanberra-gtk3-module -y

RUN apt-get install -y tmux \
                        vim \
                        nano \
                        htop \
                        kmod \
                        kbd

RUN apt install python3 python3-distutils python3-dev python3-pip -y
RUN python3 -m pip install opencv-python

RUN apt-get -y update && apt-get upgrade -y

RUN git clone https://gitlab.com/ovcharov.alex.o/nto_robotics.git /presets-sim
RUN rm /presets-sim/README.md
RUN rm -r /presets-sim/cpp
RUN rm -r /presets-sim/python
RUN apt install /presets-sim/simulator/participant_nto_simlib_1.0-1_amd64.deb -y
RUN python3 -m pip install /presets-sim/simulator/nto_sim-0.0.1.tar.gz
RUN echo "ldconfig /usr/local/lib/nto_sim/ >> /root/.bashrc"

WORKDIR /workspace/nto_robotics/python
CMD ["/bin/bash"]