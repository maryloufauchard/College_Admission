# config file
path = {
    'cache_dir': '/home/mila/m/marylou.fauchard/scratch/llm_scp',  # <- adapt your path!
    'save_dir': '/home/mila/m/marylou.fauchard/scratch/llm_scp/save',
    'output_path': '/home/mila/m/marylou.fauchard/llm_scp/TEST_ICL_1_MISTRAL', # CHANGE FOR EACH MODEL !!
    'instance_dir' : '/home/mila/m/marylou.fauchard/llm_scp/LLM_instances_v2', 
    'instruction_dir' : '/home/mila/m/marylou.fauchard/llm_scp/LLM_instruction_ICL',
    'example_dir' : '/home/mila/m/marylou.fauchard/llm_scp/LLM_example_final',
    'example_match_dir':  '/home/mila/m/marylou.fauchard/llm_scp/LLM_example_match_final'
    
}

hp_balanced = {
    'temp_value': 0,         # Controls randomness (lower = more deterministic, higher = more diverse)
    'top_p_value':0.92,        # Nucleus sampling (keeps only top 92% of probability mass for fluency)
    'top_k_value':50,          # Limits sampling to top 50 most likely words (reduces weird token choices)
    'repet_value':1.2,        # Penalizes repetition to avoid looping outputs
    'sample_bin':True         # Enables sampling for natural sentence variation
}