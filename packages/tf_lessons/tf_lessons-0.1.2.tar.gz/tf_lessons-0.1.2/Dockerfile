FROM python:3
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    autopep8 \
    black \
    codecov \
    data-science-types \
    flake8 \
    flit \
    mutmut \
    mypy \
    pylint \
    pytest \
    pytest-cov \
    tox
