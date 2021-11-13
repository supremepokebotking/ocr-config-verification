FROM ubuntu:18.04
#MAINTAINER <your name> "<your email>"
ENV PYTHONUNBUFFERED 1

ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LC_TYPE C.UTF-8

EXPOSE 5111

RUN apt-get update -y && apt-get install -y python3-pip python3-dev libsm6 libxext6 libxrender-dev
RUN apt-get -y install tesseract-ocr-all libtesseract-dev

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

#We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
