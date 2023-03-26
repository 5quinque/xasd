FROM python:3.10

RUN pip install --upgrade pip
RUN pip install mite

COPY . /app

WORKDIR /app

CMD ["./run_test.sh"]
# CMD ["mite", "scenario", "test", "scenarios:peak_scenario"]