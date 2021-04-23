FROM tensorflow/tensorflow
WORKDIR /usr/src/app
RUN sed -i "s|http://archive.ubuntu.com|http://mirrors.163.com|g" /etc/apt/sources.list && rm -Rf /var/lib/apt/lists/* && apt-get -y update && apt-get install -y \
    pkg-config \
    python-dev \
    python-opencv \
    libopencv-dev \
    libav-tools  \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    python-numpy \
    python-pycurl \
    python-opencv

# Install python3
RUN  apt-get install -y python3

# Install pip
RUN apt-get install -y wget vim
RUN wget -O /tmp/get-pip.py https://bootstrap.pypa.io/pip/3.5/get-pip.py
RUN python3 /tmp/get-pip.py
RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV ops_config=produce
# 配置时间
ENV TimeZone=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TimeZone /etc/localtime && echo $TimeZone > /etc/timezone
COPY . .

CMD [ "python", "./auto_fly_young_linux.py" ]