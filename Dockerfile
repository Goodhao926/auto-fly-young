FROM tensorflow/tensorflow
WORKDIR /usr/src/app
RUN apt update -y
RUN apt install libgl1-mesa-glx -y
COPY requirements.txt ./
RUN pip install opencv-python
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
ENV ops_config=produce
# 配置时间
ENV TimeZone=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
RUN apt-get install inetutils-ping
RUN apt-get install nodejs -y
COPY . .
CMD [ "uwsgi", "-i","uwsgi.ini" ]