# 阶段1：构建工具和依赖安装
FROM python:3.10-slim AS tools

# 声明获取 Docker 自动注入的架构参数
ARG TARGETARCH

RUN apt-get update \
    && apt-get upgrade -y \
    # 基础编译依赖（所有架构必须）
    && apt-get install -y build-essential libssl-dev pkg-config \
    # 动态判断架构：仅 ARM64 安装 Rust
    && if [ "$TARGETARCH" = "arm64" ]; then \
        echo "===== Installing Rust for ARM64 =====" \
        && apt-get install -y curl \
        && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
        && . "$HOME/.cargo/env" \
        && rustup update stable \
        && rustup default stable; \
    fi \
    # 统一清理缓存
    && apt-get purge -y --auto-remove curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

# 阶段2：安装 Python 依赖和字体
FROM tools AS builder

# 确保 Cargo 在 PATH 中
ENV PATH="/root/.cargo/bin:${PATH}"

# 安装依赖
COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# 阶段3：最终镜像
FROM python:3.10-slim

ENV PYTHONIOENCODING=utf-8

# 设置时区
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    rm -rf /var/lib/apt-get/lists/*

WORKDIR /app

# 仅复制依赖
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# 复制项目代码
COPY . .

# 预下载或执行可能会生成大的临时文件的步骤
RUN python3 _download_web.py || (echo "Failed to download web file" && exit 1)

EXPOSE 13200

VOLUME ["/app/result", "/app/cache", "/app/log"]

CMD ["python3", "_httpserver_test.py"]
