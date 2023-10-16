FROM python:3.9
WORKDIR PYTHON_PROJ 
COPY *.py .
RUN python3 -m pip install wheel
RUN python3 -m pip install flask pymysql python-dotenv
ENV IS_DOCKER 1
ENTRYPOINT [ "python3", "main.py" ]
