FROM archlinux

# Update and install essentials
RUN pacman -Syu base base-devel nano curl python --needed --noconfirm

# Install dependencies
COPY ./ext/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Temporary workaround
RUN touch /var/run/nginx.pid

# Create and switch to the workdir
RUN mkdir /gulag
WORKDIR /gulag

# Create gulag user, chown the workdir and switch to it
RUN groupadd --system --gid 1003 gulag && useradd --system --uid 1003 --gid 1003 gulag
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
