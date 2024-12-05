FROM python:3.9-slim AS builder
WORKDIR /app
COPY app.py /app/
RUN pip install --upgrade pip && \
    pip install Flask


FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app/
EXPOSE 5000
CMD ["python", "app.py"]
