#!/bin/bash
#SBATCH --job-name=benchmark_scp
#SBATCH --gres=gpu:80gb:2
#SBATCH --mem=32000M
#SBATCH --time=10:00:00
#SBATCH -o llm_scp/Generation-smallLlama-%j.out 

#Load the required module
module --quiet load anaconda/3
#Load your environment
conda activate llm_scp_test
python generation_scp.py --model llama3-big --config_file config/config_ICL_1.py
