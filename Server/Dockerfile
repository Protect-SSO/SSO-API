FROM python:3.9
WORKDIR /PYTHON_PROJ 
RUN apt-get -y update && apt-get install -y netcat-openbsd vim
COPY * .
RUN pip install -r ./requirements.txt
ENV IS_DOCKER 1
ENTRYPOINT [ "python", "main.py" ]
