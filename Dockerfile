FROM python:3.11-slim as base
WORKDIR /root/
COPY requirements.txt .
ENV PATH="/root/venv/bin:$PATH"
RUN python -m venv venv && pip install --no-cache-dir -r requirements.txt && \
  python -c "from pyngrok import ngrok; ngrok.install_ngrok()"

FROM python:3.11-slim as app
LABEL author=valentino-sm
WORKDIR /root/
ENV PATH="/root/venv/bin:$PATH"
COPY --from=base /root/venv venv
COPY . .
CMD [ "python", "main.py" ]
