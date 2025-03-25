ENV_NAME="vsi_bio_env"

echo "Creating conda environment: $ENV_NAME"
conda create -y -n $ENV_NAME python=3.10

echo "Activating environment..."
source activate $ENV_NAME

echo "Installing Python dependencies..."
pip install -r requirements.txt

# Load Java module if on HiPerGator
if command -v module &> /dev/null; then
    echo "Loading Java module..."
    module load java/11
fi

echo "Environment '$ENV_NAME' is ready."
echo "To activate it later, use: conda activate $ENV_NAME"
