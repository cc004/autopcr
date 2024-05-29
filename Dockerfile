# 首个阶段，使用构建基础镜像
FROM python:3.10-alpine AS builder
LABEL maintainer="autopcr"
ENV PYTHONIOENCODING=utf-8

WORKDIR /app

# 安装build依赖，并保持清洁，尽可能小的构建环境
RUN apk add --no-cache build-base && \
    pip install --upgrade pip

# 复制需求文件，并且安装Python依赖
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段, 构建最终小镜像
FROM python:3.10-alpine
LABEL maintainer="autopcr"
ENV PYTHONIOENCODING=utf-8

WORKDIR /app

# 复制构建阶段产物
COPY --from=builder /root/.cache /root/.cache
COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/lib /usr/lib

# 设置时区
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata

# 从构建阶段复制已经下载好的依赖包
COPY . .

# 预下载或执行可能会生成大的临时文件的步骤
RUN python3 _download_web.py || (echo "Failed to download web file" && exit 1)

EXPOSE 13200

VOLUME ["/app/result", "/app/cache"]

CMD ["python3", "_httpserver_test.py"]