FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

WORKDIR /dataflow

# Copy pipeline code
COPY . /dataflow

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the main Python file for the launcher
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="etl_pipeline.py"

