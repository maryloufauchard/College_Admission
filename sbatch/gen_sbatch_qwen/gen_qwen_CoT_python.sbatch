#!/bin/bash
#SBATCH --job-name=benchmark_scp
#SBATCH --gres=gpu:80gb:2
#SBATCH --mem=32000M
#SBATCH --time=10:00:00
#SBATCH -o llm_scp/Generation-Qwen-%j.out 

#Load the required module
module --quiet load anaconda/3
#Load your environment
conda activate llm_scp_test
python generation_scp.py --model qwen2-7b-instruct --config_file config/config_CoT_python.py
