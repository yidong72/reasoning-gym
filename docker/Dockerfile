# The `reasoning-gym` package requires Python >= 3.11. 
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sudo gosu \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git vim \
    && rm -rf /var/lib/apt/lists/* \
    && gosu nobody true

# Upgrade pip to the latest version
RUN pip install --upgrade pip
RUN pip install openai>=1.64.0 PyYAML>=6.0 tqdm>=4.66.0 ipython pudb pytest>=8.3.4 pytest-cov>=6.0.0 black>=24.10.0 isort>=5.13.2 flake8>=7.1.1 mypy>=1.14.1 pre-commit>=4.1.0 
RUN pip install pandas pyarrow
RUN sudo su -
COPY entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh
ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["/usr/bin/bash"]
