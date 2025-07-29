#!/bin/bash
#SBATCH --job-name=mistral_scp_icl_1
#SBATCH --gres=gpu:80gb:2
#SBATCH --mem=32000M
#SBATCH --time=1:00:00
#SBATCH -o /network/scratch/m/marylou.fauchard/llm_scp/Gen_TEST_NEW_ENV_ICL-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=marylou.fauchard@mila.quebec

cd /home/mila/m/marylou.fauchard/llm_scp

#Load the required module
module --quiet load anaconda/3
#Load your environment
conda activate scp_bench
export HF_HOME=/home/mila/m/marylou.fauchard/scratch/llm_scp
export TRANSFORMERS_CACHE=/home/mila/m/marylou.fauchard/scratch/llm_scp
export HUGGINGFACE_TOKEN=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
export HF_TOKEN=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
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU

python generation_scp.py --model mistral-instruct --config_file /home/mila/m/marylou.fauchard/llm_scp/config_ICL_1.py