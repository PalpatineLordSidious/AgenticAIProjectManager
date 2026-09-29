##----------------------------------------------------------------------------------
##   File:   augmented_prompt_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage: python augmented_prompt_agent.py
##
##   Purpose: This python script defines the augmented prompt agent derived from AugmentedPromptAgent.
#             The agent answers a question based on a context or persona given to it. the answer is called an augmented response
##
##   History: 
##----------------------------------------------------------------------------------



# TODO: 1 - Import the AugmentedPromptAgent class
# GvN: Need to import AugmentedPromptAgent from workflow_agents.base_agents:
from workflow_agents.base_agents import AugmentedPromptAgent

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



# User prompt and persona:
prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"


# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
# GvN: The agent is initialised as: 
#        def __init__(self, openai_api_key, persona)
#      The prompt and persona are given above as text
#      Create an object of AugmentedPromptAgent called (as per my previous naming convention rule) descriptively augmented_prompt_agent:
augmented_prompt_agent = AugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona) # augmented_prompt_agent and its attributes/input are as defined in the base class

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
# The base class has a respond-method defined and it has to be called here: def respond(self, input_text). input_text is defined as a class attribute which receives the outside prompt:
augmented_agent_response = augmented_prompt_agent.respond(input_text=prompt) # the prompt comes from above
# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:
# - What knowledge the agent likely used to answer the prompt.
# - How the system prompt specifying the persona affected the agent's response.

reaugmented_agent_response_explanation = """The agent, using his LLM brain, would have established the capital of France as Paris.
The persona is that of a professor and because he opens his remarks with 'Dear students,', it should come across as authorative but respectful or formal to those students.
"""
# Show me what it looks like:
print(reaugmented_agent_response_explanation)

# Write to a file:
