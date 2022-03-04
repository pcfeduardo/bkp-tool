FROM python:3.9-slim
WORKDIR /bkp-tool
RUN apt-get update -y && apt-get install rsync -y && apt-get clean
ADD . .
CMD [ "bash", "-c", "./bkp-tool.py", "/src", "/dst", "--show-logs" ]