FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/
COPY nginx.conf /confs/
RUN pip install Flask psutil 
EXPOSE 5000
CMD ["python", "app.py"]