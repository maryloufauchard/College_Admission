import numpy
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import statistics
import numpy as np
import json
import os
from os import walk
from tqdm import tqdm
import argparse
from vllm import LLM, SamplingParams
import re
import importlib.util
import sys
import argparse
torch.cuda.empty_cache()
import re
import random

# find a similar example of a smaller instance for ICL 
def find_example_files(instance_filename):
    pattern = r"scp_\((\d+),(\d+)\)_(\w+)_(\d+)_seed(\d+)\.txt"
    match = re.match(pattern, instance_filename)

    if not match:
        raise ValueError(f"Filename {instance_filename} doesn't match expected pattern.")

    n_students, n_schools, pref_mode, total_cap, seed = match.groups()
    n_students = int(n_students)
    n_schools = int(n_schools)
    total_cap = int(total_cap)


    ratio = n_students / n_schools
    ideal_n_schools = min(5 if abs(ratio - 1.0) <= 0.3 else 3,4)
    capacity_ratio = total_cap / n_students
    if capacity_ratio <= 0.85:
        example_total_cap = 4
    elif capacity_ratio <= 1.05:
        example_total_cap = 5
    else:
        example_total_cap = 10
        
    example_n_schools = min(example_total_cap,ideal_n_schools)

    example_seed = random.choice([10, 20, 30])

    base_name = f"scp_(5,{example_n_schools})_{pref_mode}_{example_total_cap}_seed{example_seed}"
    example_filename = f"ex_{base_name}.txt"
    match_filename = f"ex_match_{base_name}.txt"

    return example_filename, match_filename


current_path = os.getcwd()
home_path = base_path = os.path.join(*current_path.split(os.sep)[:5])


#############################################################################################
##############################   PARSER ARGUMENTS   #########################################
parser = argparse.ArgumentParser(description="LLM Generation of many-to-one matching problem")
parser.add_argument("--model", default='llama3-big', help="LLMs model for genetaion. Expected values : llama3-big | llama3-instruct |llama3-instruct | mistral-instruct | qwen2-7b-instruct")
parser.add_argument("--run", default=0, type=int, help="indicate the run number")
parser.add_argument("--config", default=1, type=int, help="indicate the config number to use -- 3 possibilities 1 for balanced crea 2 for strict model 3 for divergent generation")
parser.add_argument("--cache_dir", default=None, help="path to model cache directory")
parser.add_argument("--save_path", default=None, help="path to general directory")
#parser.add_argument('--template', default='regular', help="valid values : regular | KB_templates")
parser.add_argument('--model_token_len', default=8192, type=int, help="input token length for vLLLM models")
parser.add_argument(
    "--config_file",
    required=True,
    help="path to the config .py you want to use (e.g. /path/to/my_config.py)"
)
parser.add_argument('--nb_gpus', default=2, type=int, help='tensor_parallel_size in vLLMs for large models only')

args = parser.parse_args() 


config_path = os.path.abspath(args.config_file)
if not os.path.isfile(config_path):
    raise FileNotFoundError(f"Could not find config file at {config_path}")

spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
sys.modules["config"] = config
spec.loader.exec_module(config)

args.cache_dir = args.cache_dir or config.path["cache_dir"]
args.save_path = args.save_path or config.path["save_dir"]


if args.model == 'llama3-big':
    model_name = "/network/weights/llama.var/llama_3/Meta-Llama-3-70B-Instruct"
elif args.model == 'llama3-instruct':
    model_name = "/network/weights/llama.var/llama_3/Meta-Llama-3-8B-Instruct"
elif args.model == 'qwen2-7b-instruct':
    model_name = "Qwen/Qwen2-7B-Instruct"
elif args.model == 'mistral-instruct':
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
else:
    print('Please provide a valid entry for models -- ')
    raise KeyError

if args.model in ['qwen2-7b-instruct', 'mistral-instruct']:
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=args.cache_dir, trust_remote_code=True)
else:
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=args.cache_dir)


big_model_list = ['llama3-big', 'gemma-2-big', 'falcon-big','qwen2-7b-instruct','mistral-instruct']

if args.model in big_model_list:
    dtype_m = 'float16'
    model = LLM(model=model_name, task="generate", revision='main', max_model_len=args.model_token_len, max_num_batched_tokens=args.model_token_len, tokenizer=model_name, download_dir=args.cache_dir, trust_remote_code=True, dtype=dtype_m, tensor_parallel_size=args.nb_gpus)
    print('BIG MODEL')
else:
    model = LLM(model=model_name, task="generate", revision='main', max_model_len=args.model_token_len,  max_num_batched_tokens=args.model_token_len,tokenizer=model_name, download_dir=args.cache_dir, trust_remote_code=True, dtype='float16')
    

configs = config.hp_balanced
config_ = f'config_{args.config}'

run = f'run_{args.run}'

model_configs = args.model + run + config_
save_path = args.save_path + f'Generated_answers_{model_configs}/'

save_directory = os.path.dirname(save_path)
if save_directory and not os.path.exists(save_directory):
    os.makedirs(save_directory)
    already_saved_files = []
    print(f"Created directory: {save_directory}")
else:
    already_saved_files = list(set(next(walk(save_path), (None,None,[]))[2]))
    


tradi_gen_len = 10000  
novel_gen_len = 10000
sampling_params = SamplingParams(max_tokens=tradi_gen_len, temperature=configs['temp_value'], top_p=configs['top_p_value'], 
                                        top_k=configs['top_k_value'], repetition_penalty=configs['repet_value'])



instance_dir = config.path['instance_dir']     
instruction_dir = config.path['instruction_dir'] 
generation_dir = config.path['output_path']
example_dir = config.path['example_dir']
example_match_dir = config.path['example_match_dir']

instruction_files = [f for f in os.listdir(instruction_dir) if f.endswith('.txt')]
instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.txt')]

os.makedirs(generation_dir, exist_ok=True)


for instruction_file in tqdm(instruction_files, desc="Instructions"):
    instruction_path = os.path.join(instruction_dir, instruction_file)
    with open(instruction_path, 'r', encoding='utf-8') as f:
        instruction_text = f.read()

    instruction_name = os.path.splitext(instruction_file)[0]
    needs_example = "[ADD EXAMPLE HERE]" in instruction_text

    for instance_file in tqdm(instance_files, desc=f"Instances for {instruction_name}", leave=False):
        instance_base = os.path.splitext(instance_file)[0]
        output_filename = f"generation_{instruction_name}_{instance_base}.txt"
        output_path = os.path.join(generation_dir, output_filename)

        if os.path.exists(output_path):
            print(f" --> Skipping {output_filename}, already generated.")
            continue

        
        instance_path = os.path.join(instance_dir, instance_file)
        with open(instance_path, 'r', encoding='utf-8') as f:
            instance_text = f.read()

        prompt = instruction_text

        # ICL case
        if needs_example:
            try:
                ex_filename, match_filename = find_example_files(instance_file)
                ex_path = os.path.join(example_dir, ex_filename)
                match_path = os.path.join(example_match_dir, match_filename)

                with open(ex_path, 'r', encoding='utf-8') as f:
                    ex_content = f.read()
                with open(match_path, 'r', encoding='utf-8') as f:
                    match_content = f.read()

                example_section = f"If you have this instance:\n{ex_content}\n\nYou should return this matching in this format:\n{match_content}"
                prompt = prompt.replace("[ADD EXAMPLE HERE]", example_section)

            except FileNotFoundError:
                print(f"!!! Missing: {ex_filename} or {match_filename} for {instance_file}")
                prompt = prompt.replace("[ADD EXAMPLE HERE]", "[EXAMPLE MISSING]")

        prompt = prompt.replace("[ADD INSTANCE HERE]", instance_text)

        outputs = model.generate(prompt, sampling_params=sampling_params, use_tqdm=False)
        answer = outputs[0].outputs[0].text

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(answer)
