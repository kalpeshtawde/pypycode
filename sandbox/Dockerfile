FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1001 runner

# No package installs at runtime
WORKDIR /runner
COPY runner.py /runner/runner.py
COPY test_runner.py /runner/test_runner.py

RUN chown -R runner:runner /runner
USER runner

# No network, read-only fs enforced by docker run flags
CMD ["python", "/runner/runner.py"]
