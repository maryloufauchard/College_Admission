#!/bin/bash
#SBATCH --job-name=mistral_scp_icl_1
#SBATCH --gres=gpu:80gb:2
#SBATCH --mem=32000M
#SBATCH --time=10:00:00
#SBATCH -o /network/scratch/m/marylou.fauchard/llm_scp/Gen_TEST_MISSING_EXAMPLES_ICL-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=marylou.fauchard@mila.quebec

# Fail on any error
set -e

# Recommended: clear all environment modules
module purge

# If you must use anaconda module (not recommended), do it AFTER purging
# module --quiet load anaconda/3

# Manually source Conda setup
source ~/miniconda3/etc/profile.d/conda.sh

# Unset conflicting Python paths
unset PYTHONPATH
export PYTHONPATH=""

# Activate your Conda environment
conda activate llm_scp_test

# Log debug info
echo "Python location: $(which python)"
python --version

# Move to your code directory
cd /home/mila/m/marylou.fauchard/llm_scp

# Run your script
python generation_scp.py --model mistral-instruct --config_file /home/mila/m/marylou.fauchard/llm_scp/config_ICL_1.py
