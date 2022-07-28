FROM python:3.8-slim

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

COPY . /app
WORKDIR /app

# if you forked EasyOCR, you can pass in your own GitHub username to use your fork
# i.e. gh_username=myname
ARG gh_username=JaidedAI
ARG service_home="/home/EasyOCR"

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    python3-setuptools \
    gcc \
    make

# Configure apt and install packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    python3-dev \
    python3-setuptools \
    git \
    gcc \
    make \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

# Clone EasyOCR repo
RUN mkdir "$service_home" \
    && git clone "https://github.com/$gh_username/EasyOCR.git" "$service_home" \
    && cd "$service_home" \
    && git remote add upstream "https://github.com/JaidedAI/EasyOCR.git" \
    && git pull upstream master

# Create a virtual environment in /opt
RUN python3 -m venv /opt/venv
RUN source /opt/venv/bin/activate

# Build
RUN cd "$service_home" \
    && python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

# purge unused
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


# Install requirments to new virtual environment
RUN pip install -r requirements.txt


# make entrypoint.sh executable
RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]