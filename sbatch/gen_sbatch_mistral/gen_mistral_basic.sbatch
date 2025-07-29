#!/bin/bash
#SBATCH --job-name=mistral_scp_basic
#SBATCH --gres=gpu:80gb:2
#SBATCH --mem=32000M
#SBATCH --time=10:00:00
#SBATCH -o /network/scratch/m/marylou.fauchard/llm_scp/Gen_test_mistral-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=marylou.fauchard@mila.quebec

cd /home/mila/m/marylou.fauchard/llm_scp

#Load the required module
module --quiet load anaconda/3
#Load your environment
conda activate llm_scp_test
python generation_scp.py --model mistral-instruct --config_file /home/mila/m/marylou.fauchard/llm_scp/config_basic.py