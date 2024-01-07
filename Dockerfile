FROM python:3.10 AS builder
WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

ADD "https://api.github.com/repos/cczhong11/MyAssistant/commits?per_page=1"  latest_commit
RUN git clone https://github.com/cczhong11/MyAssistant.git
WORKDIR /app/MyAssistant

# 安装你的 Python 包
RUN ../.venv/bin/pip install .
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY config.json .
COPY main.py .

ENTRYPOINT [".venv/bin/python3","main.py"]
