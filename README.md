# College_Admission
This is a benchmark for the college admission problem, a many-to-one matching. The goal is to analyze the reasoning capabilities of different LLMs with preference and stability constraints. The 369 instances included in the original benchmark are not supposed to be representative of real world size, but allowed us to see the change in performances when the complexity increase with both the number of students and the type of preferences. 

## How to use 
### DATASET 
The instances are in the folder *** with their respective solution from the DA algorithm in ***. New instances and matching can be created with the file ***. 

### Generation 
In order to test the LLMs with all instances of the dataset, we first need to generate the output from the LLMs with the file generation_scp.py. For that, we need to choose a prompt instruction, and adapt the path of the config file. For every prompt template, there is a sbactch file. 

After running the LLM on all instances, we need to extract the matching, which is done with extract_matching.py

The file metric_scp.py will compute, for every instance, the 4 metrics : feasibility, assignment stability, matching stability and student optimality. 

Finally, to aggregate our results overall, by students or by preferences, we need to run aggregation_metric.py
