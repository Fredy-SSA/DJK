FROM ubuntu
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    libexpat1 \
    libsqlite3-0 \
    libssl1.1 \
    python3-pip \
    python3 \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir -p  /app 
WORKDIR /app
COPY ./requirements.txt /app/
COPY ./main.py /app/
CMD ["python3", "main.py"]