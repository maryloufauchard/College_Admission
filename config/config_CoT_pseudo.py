# config file, make sure to adapt each path
path = {
    'cache_dir': 'scratch/llm_scp',  # <- adapt your path!
    'save_dir': 'save', # adpat
    'output_path': 'Generation_CoT_pseudoCode_Llama8B', # CHANGE FOR EACH MODEL !!
    'instance_dir' : 'Dataset_Instance', 
    'instruction_dir' : 'Prompt_Template/LLM_instruction_CoT_pseudo',
    'example_dir' : 'LLM_example_final',
    'example_match_dir':  'LLM_example_match_final'
    
}

hp_balanced = {
    'temp_value': 0,         # Controls randomness (lower = more deterministic, higher = more diverse)
    'top_p_value':0.92,        # Nucleus sampling (keeps only top 92% of probability mass for fluency)
    'top_k_value':50,          # Limits sampling to top 50 most likely words (reduces weird token choices)
    'repet_value':1.2,        # Penalizes repetition to avoid looping outputs
    'sample_bin':True         # Enables sampling for natural sentence variation
}
