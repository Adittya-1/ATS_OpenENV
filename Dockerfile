FROM python:3.10-slim

# Hugging Face recommends running as a non-privileged user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Ensure standard output and error are easily logged
ENV PYTHONUNBUFFERED=1

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

# Hugging Face Spaces requires port 7860
EXPOSE 7860

# We start the FastAPI application on 0.0.0.0:7860
# Note: we use server.app:app because the code is now in the 'server' directory
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
