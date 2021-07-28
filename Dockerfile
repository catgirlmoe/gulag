FROM ubuntu:bionic

# Add python3.9 repository
RUN add-apt-repository ppa:deadsnakes/ppa

# Update and install packages
RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3.9 python3.9-dev python3.9-distutils wget
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py && rm get-pip.py

# Install dependencies
COPY ./ext/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Temporary workaround
RUN touch /var/run/nginx.pid

# Create and switch to the workdir
RUN mkdir /gulag
WORKDIR /gulag

# Create gulag user, chown the workdir and switch to it
RUN addgroup --system --gid 1003 gulag && adduser --system --uid 1003 --gid 1003 gulag
RUN chown -R gulag:gulag /gulag
USER gulag

# Expose port and set entrypoint
EXPOSE 8080
CMD [ "python3.9", "./main.py" ]

# Copy and build oppai-ng
COPY --chown=gulag:gulag ./oppai-ng ./oppai-ng
RUN cd oppai-ng && chmod +x ./libbuild && ./libbuild && cd ..

# Copy over the rest of gulag
COPY --chown=gulag:gulag ./ ./
