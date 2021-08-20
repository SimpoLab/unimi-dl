FROM python:3.9.6
WORKDIR /app
COPY pyproject.toml /app/pyproject.toml 
COPY setup.cfg /app/setup.cfg
COPY LICENSE /app/LICENSE
COPY unimi_dl /app/unimi_dl
RUN pip install .
#COPY credentials.json /root/.local/share/unimi-dl/
ENTRYPOINT ["python3", "-m", "unimi_dl"]
