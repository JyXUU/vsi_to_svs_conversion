#!/bin/bash

# Environment name
ENV_NAME="vsi_bio_env"

echo "[INFO] Purging all modules and loading conda + java..."
module purge
module load conda
module load java/11

# Export conda path explicitly to avoid conflicts
export PATH=/apps/conda/25.1.1/bin:$PATH
source /apps/conda/25.1.1/etc/profile.d/conda.sh

# If the environment exists, prompt user to delete manually
if conda env list | grep -q "$ENV_NAME"; then
  echo "[WARNING] Conda environment '$ENV_NAME' already exists."
  echo "If you want to recreate it, run: conda deactivate && conda remove -n $ENV_NAME --all"
  echo "Then re-run this script."
  exit 1
fi

echo "[INFO] Creating fresh conda environment: $ENV_NAME"
conda create -y -n $ENV_NAME python=3.10

echo "[INFO] Activating environment..."
conda activate $ENV_NAME

echo "[INFO] Installing required Python packages..."
pip install -r requirements.txt

echo "[SUCCESS] Environment '$ENV_NAME' is ready and all dependencies are installed!"
echo "To activate it manually later, run: conda activate $ENV_NAME"
