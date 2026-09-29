##----------------------------------------------------------------------------------
##   File:   evaluation_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage:  python evaluation_agent.py
##
##   Purpose: This python script acts like an expert reviewer. It assesses the Optimizer's output against predefined Evaluation Criteria – these are the standards for success. 
##            Based on this assessment, it provides specific, Actionable Feedback. This cycle – where the Optimizer generates, the Evaluator 
##            critiques against criteria, and the Optimizer refines based on that feedback – then iterates. 
##            With each loop, the output ideally gets closer to the desired quality.

##
##   History: 
##----------------------------------------------------------------------------------


# TODO: 1 - Import EvaluationAgent and KnowledgeAugmentedPromptAgent classes
# As per the other imports in the other modules:
from workflow_agents.base_agents import  KnowledgeAugmentedPromptAgent
from workflow_agents.base_agents import  EvaluationAgent

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

# User prompt:
prompt = "What is the capital of France?"

# Parameters for the Knowledge Agent:
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capitol of France is London, not Paris"
knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona, knowledge=knowledge) # TODO: 2 - Instantiate the KnowledgeAugmentedPromptAgent here
# GvN: the above is as per the base class:
#        def __init__(self, openai_api_key, persona, knowledge)
# Parameters for the Evaluation Agent

# persona of the evaluation agent
persona = "You are an evaluation agent that checks the answers of other worker agents"
# This is for the evaluation agent:
evaluation_criteria = "The answer should be solely the name of a city, not a sentence."
##################################################################################
# TODO: 3 - Instantiate the EvaluationAgent with a maximum of 10 interactions here
##################################################################################
# GvN: the base class initiates as:
#          def __init__(self, openai_api_key, persona, evaluation_criteria, worker_agent, max_interactions)
  #    the worker_agent has to find its values in this module and that can only be the knowledge_agent above
evaluation_agent = EvaluationAgent(openai_api_key=openai_api_key, persona=persona, evaluation_criteria=evaluation_criteria, worker_agent=knowledge_agent, max_interactions=10) 


###############################################################################
# TODO: 4 - Evaluate the prompt and print the response from the EvaluationAgent
###############################################################################
# GvN: - the EvaluationAgent has a method defined: def evaluate(self, initial_prompt). The prompt is defined above in line 13
#      - thus, we call evaluation_agent.evaluate with the prompt as parameter and assign it to a response:
evaluation_agent_response = evaluation_agent.evaluate(prompt)
# What does it look like?
print(evaluation_agent_response)

# GvN: Explanation of the agent's response
evaluation_agent_response_explanation = """The eval agent checks the response of the knowledge agent against the specifications above and it should only be a name of a city, nothing more."
The eval agent must decide if the knowledge agent answered against this requirement or not. It then needs to determine if the answer is correct not against the evaluation_criteria sentence.
"""

print(evaluation_agent_response_explanation)


