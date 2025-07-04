FROM archlinux:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Update system and install dependencies
RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python python-pip python-pipx postgresql-libs base-devel jq && \
    pacman -Scc --noconfirm

# Install UV using pipx
RUN pipx install uv
ENV PATH="/root/.local/bin:$PATH"

# Copy UV configuration files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy project
COPY . .

# Create media directory with proper permissions
RUN mkdir -p /app/media/gallery && \
    chmod 755 /app/media

# Collect static files
RUN uv run python manage.py collectstatic --noinput

# Create entrypoint script that reads port from config.json
RUN printf '#!/bin/bash\nset -e\n\n# Read port from config.json\nPORT=$(jq -r ".port" /app/config.json)\necho "Using port: $PORT"\n\n# Wait for database to be ready\nuntil uv run python manage.py dbshell --command="SELECT 1;" > /dev/null 2>&1; do\n  echo "Waiting for database..."\n  sleep 1\ndone\n\n# Run migrations\nuv run python manage.py migrate\n\n# Start server on port from config\nexec uv run python manage.py runserver 0.0.0.0:$PORT\n' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Default expose (will be overridden by actual port)
EXPOSE 8000

# Run entrypoint
CMD ["/entrypoint.sh"]