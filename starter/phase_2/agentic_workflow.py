#----------------------------------------------------------------------------------
##   File:   agentic_workflow.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage:  python agentic_workflow.py
##
##   Purpose: This is the main executioner script that builds the agentic workflows.
##            It plans the entire programme project by using the ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
##            Based on suitability calculations, it decides which woker agent is best suited for a task based on an optimizer calculatiion
##            It delivers a final report on the outcome
              
              
##              
##
##   History: 
##----------------------------------------------------------------------------------


# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent


import os, sys

# GvN:  Load the dotenv:
# Needed to find the .env file - had issues in it not being read properly invalidating the key
# Sought help from Udacity but none was given.
# Had to import the pathlib and find_dotenv to search for .env which I put in the /starter folder:
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
# Load environment variables from .env file
# Find the directory where this script lives, then look for .env there
# TODO: 2 - Load the OpenAI API key from the environment variables
# Have to find my .env file using find_dotenv from the current worrking directory:
env_path = find_dotenv(filename=".env", usecwd=True)
load_dotenv(dotenv_path=env_path)
openai_api_key = os.getenv("OPENAI_API_KEY") # will be needed below to do the constructor and make the LLM call
# print(openai_api_key) # this comes out as correct


# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
# read the file Product-Spec-Email-Router.txt
file = open("Product-Spec-Email-Router.txt", "r")
# read the file into product_spec:
product_spec = file.read()
file.close()
# Note: could have used a with statement but wanted to be more granular above


# Instantiate all the agents:



###################################################################################################################
#######################
# Action Planning Agent
#######################
knowledge_action_planning = (
    "Stories are defined from a product spec by identifying a "
    "persona, an action, and a desired outcome for each story. "
    "Each story represents a specific functionality of the product "
    "described in the specification. \n"
    "Features are defined by grouping related user stories. \n"
    "Tasks are defined for each story and represent the engineering "
    "work required to develop the product. \n"
    "A development Plan for a product contains all these components"
)
# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
# knowledge is an attribute of ActionPlanningAgent and knowledge_action_planning above must be assigned to it. 
# openai_api_key comes from above:
action_planning_agent= ActionPlanningAgent(openai_api_key=os.getenv("OPENAI_API_KEY"),knowledge=knowledge_action_planning)



## P R O D U C T    M A N A G E R
###################################################################################################################
####################################################
# Product Manager - Knowledge Augmented Prompt Agent
####################################################
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    # product_spec is assigned above by reading the text file:
    f"{product_spec}"
)
# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent.
# GvN:  The Product Manager is an Evaluation Agent (class EvaluationAgent). The object is called product_manager_evaluation_agent
#       This agent will evaluate the product_manager_knowledge_agent. The worker agent is the product_manager_knowledge_agent 
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
# GvN:  EvaluationAgent is defined as def __init__(self, openai_api_key, persona, evaluation_criteria, worker_agent, max_interactions) in base_agents.py:
#       Going to use the wording further below - "You are an evaluation agent that checks the answers of other worker agents."

# Create the worker agent:
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=os.getenv("OPENAI_API_KEY"), persona=persona_product_manager, knowledge=knowledge_product_manager)
# Create the evaluator agent persona:
persona_product_manager_evaluation = ("You are a product manager evaluation agent that checks the answers of the product manager agents")
persona_product_manager_evaluation_criteria = "The evaluation_criteria should specify the expected structure for user stories. As a [type of user], I want [an action or feature] so that [benefit/value]. All agile stories must address a specific use-case need or function "

# I chose max_interactions to be 10 - as course material suggested
product_manager_evaluation_agent = EvaluationAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    persona=persona_product_manager_evaluation,
    evaluation_criteria=persona_product_manager_evaluation_criteria,
    worker_agent=product_manager_knowledge_agent,
    max_interactions=10
)
# persona_product_manager, knowledge_product_manager, product_manager_knowledge_agent, product_manager_evaluation_agent


## P R O G R A M M E    M A N A G E R
###################################################################################################################
#####################################################
# Program Manager - Knowledge Augmented Prompt Agent
#####################################################
# 1. Create a persona:
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
# 2. Knowledge of the programme manager (note: product_spec comes from the file above):
knowledge_program_manager = (
      "Features of a product are defined by organizing similar user stories into cohesive groups."
      "Group stories that are related to each other into features."
      "Each feature should should have a name, description or purpose, what it does or functionality and the end-user benefit\n\n"
      "Product Specification:\n"
       f"{product_spec}"                         
)
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# GvN: KnowledgeAugmentedPromptAgent is specified as: def __init__(self, openai_api_key, persona, knowledge)
#      Everything else is defined above incl knowledge_program_manager for knowledge
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=os.getenv("OPENAI_API_KEY"),persona=persona_program_manager,knowledge=knowledge_program_manager)

###################################################################################################################
####################################
# Program Manager - Evaluation Agent
####################################
# Now we need to evaluate the Program Manager
# The line below is provided - this is a persona attribute:
persona_program_manager_evaluation = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
# GvN: The specification is defined above
#      We are again dealing with class EvaluationAgent. Going to use the exact criteria above as seen:
# Define the criteria:
program_manager_evaluation_criteria = (
    "The answer should be product features that follow the following structure: "
    "Feature Name: A clear, concise title that identifies the capability\n"
    "Description: A brief explanation of what the feature does and its purpose\n"
    "Key Functionality: The specific capabilities or actions the feature provides\n"
    "User Benefit: How this feature creates value for the user"
)
# The worker_agent is still the product_manager_knowledge_agent.I chose max_interactions to be 10 again:
program_manager_evaluation_agent=EvaluationAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    persona=persona_program_manager_evaluation,
    evaluation_criteria=program_manager_evaluation_criteria,
    worker_agent=program_manager_knowledge_agent,
    max_interactions=10
)
# persona_program_manager, knowledge_program_manager, program_manager_knowledge_agent, program_manager_evaluation_agent



## D E V     E N G I N E E R
###################################################################################################################
############################
# Development Engineer
############################
# Development Engineer - Knowledge Augmented Prompt Agent
# The class KnowledgeAugmentedPromptAgent is specified as def __init__(self, openai_api_key, persona, knowledge)
#1. Create the persona for a dev engineer:
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
#2. Create the dev engineer knowledge:
knowledge_dev_engineer = (
    "Development tasks are defined by identifying what needs to be built to implement each user story."
    "You are a developer engineer. You need to be able to break the product specification into granular engineering tasks."
    "Each task has a task id, task name, task description, user story name, estimated effort needed, task dependancies, testing acceptance criteria.\n\n"
    "Product Specification:\n"
    f"{product_spec}"
)
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
# The dev engineer evaulation agent will evaluate this agent as a worker agent further below
development_engineer_knowledge_agent=KnowledgeAugmentedPromptAgent(openai_api_key=os.getenv("OPENAI_API_KEY"),persona=persona_dev_engineer,knowledge=knowledge_dev_engineer)
###################################################################################################################
#########################################
# Development Engineer - Evaluation Agent
# Now to evaluate the dev engineer:
# 1. Create a persona:
persona_dev_engineer_eval = ("You are an dev engineer evaluation agent that checks the answers of dev engineer agents."
)
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
# Criteria for Evaluation:
dev_engineer_evaluation_criteria=(
    "The answer should be tasks following this exact structure: " \
    "Task ID: A unique identifier for tracking purposes\n" \
    "Task Title: Brief description of the specific development work\n" \
    "Related User Story: Reference to the parent user story\n" \
    "Description: Detailed explanation of the technical work required\n" \
    "Acceptance Criteria: Specific requirements that must be met for completion\n" \
    "Estimated Effort: Time or complexity estimation\n" \
    "Dependencies: Any tasks that must be completed first"
)
# Instantiate the evaluation agent with 10 cycles:
dev_engineer_evaluation_agent=EvaluationAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    persona=persona_dev_engineer_eval,
    evaluation_criteria=dev_engineer_evaluation_criteria,
    worker_agent=development_engineer_knowledge_agent,
    max_interactions=10
)
# persona_dev_engineer, knowledge_dev_engineer, development_engineer_knowledge_agent, persona_dev_engineer_eval, dev_engineer_evaluation_criteria, dev_engineer_evaluation_agent


###################################################################################################################

## R O U T I N G     A G E N T
###############
# Routing Agent
###############
# The class in base_agent.py is defined as def __init__(self, openai_api_key, agents):
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. 
# Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.

######################################################################################
# These 3 functions are called by the Router Agent. He uses these to call the 3 agents

# 1. Product Manager function
def product_manager_support_function(query):
    # calls the product_manager_knowledge_agent implemnted above:
    response = product_manager_knowledge_agent.respond(input_text=query)
    # calls the product_manager_evaluation_agent implemented above
    prodmgr_evaluation = product_manager_evaluation_agent.evaluate(response) # product_manager_evaluation_agent
    return prodmgr_evaluation

# 2. Program Manager function
def program_manager_support_function(query):
    # calls the program_manager_knowledge_agent implemnted above:
    response = program_manager_knowledge_agent.respond(input_text=query)
    # calls the product_manager_evaluation_agent implemented above
    prgrmgr_evaluation = program_manager_evaluation_agent.evaluate(response)
    return prgrmgr_evaluation

# 3. Development Engineer function
def development_engineer_support_function(query):
    # calls the development_engineer_knowledge_agent implemnted above:
    response = development_engineer_knowledge_agent.respond(input_text=query)
    # calls the dev_engineer_evaluation_agent implemented above
    devengnr_evaluation = dev_engineer_evaluation_agent.evaluate(response)
    return devengnr_evaluation
######################################################################################


# GvN: Each route is a supporting agent
# I will need 3 agents: Product Manager, Program Manager and Development Engineer and each needs to described in these terms:
#    - name
#    - description
#    - func (as described above)

# Create the agents needed for the Routing Agent:
global_routing_agents=[
        {
            "name": "Product Manager",
            "description": "The product manager defines products and their user stories or use cases. He does not define tasks, features, epics and does not group stories or tasks.",
            # "func": product_manager_support_function # see the definition above
            "func": lambda x: product_manager_support_function(x),
        },
        {
            "name": "Program Manager",
            "description": "The Program manager defines product features and and he groups the stores that are related. He does not specify user stories and engineering tasks to complete them",
            #"func": program_manager_support_function # see the definition above
            "func": lambda x: program_manager_support_function(x),
        },
        {
            "name": "Development Engineer",
            "description": "The Dev Engineer defines the detailed engineering development tasks to implement the user stories. he does not define the suer stories or product features.",
            #"func": development_engineer_support_function # see the definition above
            "func": lambda x: development_engineer_support_function(x),
        },
]  # end of global_routing_agents dict 
routing_agent = RoutingAgent(openai_api_key, global_routing_agents)



# Run the workflow

print("\n*** Workflow execution started ***\n")
# Workflow Prompt
# ****
workflow_prompt = (
    "Create a development plan for the email router product specified in the txt file."
    "You need to group features and user stories together and list the engineering taks that are needed."
)    
# ****
print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

print("\nDefining workflow steps from the workflow prompt")

# TODO: 12 - Implement the workflow.
#   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
#   2. Initialize an empty list to store 'completed_steps'.
#   3. Loop through the extracted workflow steps:
#      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
#      b. Append the result to 'completed_steps'.
#      c. Print information about the step being executed and its result.
#   4. After the loop, print the final output of the workflow (the last completed step).

# GvN: USE action_planning_agent on line 41
#   - define a variable for all the wf steps - call it wf_steps
#   - the action planning agent is defined as action_planning_agent(openai_api_key=os.getenv("OPENAI_API_KEY"),knowledge=knowledge_action_planning)
#   - the class has extract_steps_from_prompt defined in base_agents.py. it needs to be tied to workflow_prompt as an input to that def
#   - this result is assigned to completed_steps (it has to be stateless before the for-loop)

# Defining the wf steps from the prompt given:
all_agent_workflow_steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)

# Loop through the list using an iteration index and a step name and list the steps:
for iteration, wfstep in enumerate(all_agent_workflow_steps, 1):
    print(f"{iteration}. {wfstep}")

completed_steps = [] # begin empty   

# Now loop through the wf steps and add to completed_steps:

for iteration, wfstep in enumerate(all_agent_workflow_steps, 1):
    print(f"Step name: {wfstep}")
  
    step_result = routing_agent.route_user_requests(wfstep)    
    print(step_result)
    completed_steps.append(wfstep)
    print(f"Result for step {iteration}:\n{step_result}")
        
    print(f"\n Outcome of workflow step '{wfstep}': {step_result}\n")
    



    
print("\n*** This Workflow has now been executed for this interaction. ***\n")
