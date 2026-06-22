# --- Step 1: Base Image ---
# Use a slim, optimized Python image to minimize container footprint
FROM python:3.12-slim

# --- Step 2: Environment Settings ---
# Set the working directory inside the container runtime context
WORKDIR /app

# --- Step 3: Package Manager Installation ---
# Install uv (high-performance Python package manager)
RUN pip install uv

# --- Step 4: Layer Caching Optimization ---
# Copy lockfiles first so Docker caches dependency layers efficiently
COPY pyproject.toml .
COPY uv.lock* .

# Install dependencies using production flags (--frozen skips updating lockfiles)
RUN uv sync --frozen --no-dev

# --- Step 5: Application Deployment ---
COPY app/ app/

# --- Step 6: Security Hardening ---
RUN useradd --create-home appuser

# FIX: Grant the new appuser read/write ownership over everything inside /app
RUN chown -R appuser:appuser /app

# Switch runtime context to the secure user
USER appuser

# --- Step 7: Networking & Orchestration ---
# Document the internal listening gateway port
EXPOSE 8000

# Embedded health probe for container orchestrators (Docker/Kubernetes)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Final execution entrypoint command running uvicorn through uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]