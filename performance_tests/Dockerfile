FROM python:3.10

RUN pip install --upgrade pip
RUN pip install mite

# install vim
RUN apt-get update && apt-get install -y vim

COPY . /app

WORKDIR /app

CMD ["./run_test.sh"]
# CMD ["bash"]
# CMD ["mite", "scenario", "test", "scenarios:peak_scenario"]