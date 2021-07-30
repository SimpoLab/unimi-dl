FROM python:3.9.5
WORKDIR /app
RUN ls -a
#TODO: remove deps and use requirements.txt or setup.cfg
RUN pip3 install requests
RUN pip3 install youtube-dl
RUN pip3 install --use-feature=in-tree-build .
COPY credentials.json /root/.local/share/unimi-dl/
ENTRYPOINT ["python3", "-m", "unimi_dl"]
