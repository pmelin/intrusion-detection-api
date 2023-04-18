# we use micromamba as the conda implementation
FROM mambaorg/micromamba:1.4.1

# copies the conda env file
COPY --chown=$MAMBA_USER:$MAMBA_USER conda.yaml /app/conda.yaml

# install the dependencies
RUN micromamba install -y -n base -f /app/conda.yaml && \
    micromamba clean --all --yes

# activates the base environment
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# copies all the source files to /app
COPY --chown=$MAMBA_USER:$MAMBA_USER ./src/* /app/

# switches the folder to /app
WORKDIR /app

# starts FastAPI
CMD uvicorn --host=0.0.0.0 main:app