FROM python:3.7.2-slim
WORKDIR /meshtest
COPY ./requirements.txt /meshtest/requirements.txt
RUN pip install --trusted-host pypi.python.org -r /meshtest/requirements.txt
COPY . /meshtest
ENV PYTHONPATH $(pwd)
CMD ["python", "-m", "unittest", "discover", "MeshTest"]
