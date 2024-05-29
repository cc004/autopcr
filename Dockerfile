FROM python:3.10-slim-bullseye
LABEL maintainer="autopcr"

ENV PYTHONIOENCODING=utf-8

WORKDIR /app

# 设置时区并安装依赖
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install build-essential -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制源代码
COPY . .

# 安装Python依赖
RUN pip3 install -r requirements.txt --no-cache-dir \
    && pip3 cache purge \
    && rm -rf /root/.cache/pip/*

RUN python3 _download_web.py || (echo "Failed to download web file" && exit 1)

EXPOSE 13200

VOLUME /app/result /app/cache

CMD ["python3", "_httpserver_test.py"]
