FROM python:3.9.5
ARG URL
RUN echo "$URL"
WORKDIR /app
COPY setup.cfg setup.cfg
COPY setup.py setup.py
COPY LICENSE LICENSE 
COPY unimi_dl /app/unimi_dl
RUN pip3 install --use-feature=in-tree-build .
ENTRYPOINT python3 -m unimi_dl -v "$URL"
