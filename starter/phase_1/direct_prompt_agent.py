###----------------------------------------------------------------------------------
##   File:   direct_prompt_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage:  python direct_prompt_agent.py
##
##   Purpose: This python script receives a direct prompt to answer a question. It uses the LLM model to respond
##
##   History: 
##----------------------------------------------------------------------------------



# Test script for DirectPromptAgent base class

# TODO: 1 - Import the DirectPromptAgent class from BaseAgents
# As with the other class, we do the same:
from workflow_agents.base_agents import DirectPromptAgent

import os, sys

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
prompt = "What is the Capital of France?"


# TODO: 3 - Instantiate the DirectPromptAgent as direct_agent
# I will call it direct_prompt_agent. It the base file it is initialised only with the open api key: def __init__(self, openai_api_key) and will do that here
# It passes openai_api_key in as part of the constructor:
direct_prompt_agent = DirectPromptAgent(openai_api_key=openai_api_key)
# print(direct_prompt_agent) # for debugging

# TODO: 4 - Use direct_agent to send the prompt defined above and store the response
# There is a method defined inside the class called responsd: def respond(self, prompt). The prompt input to the method is defined above:
direct_prompt_agent_response = direct_prompt_agent.respond(prompt=prompt)
# sys.exit("Stopping script execution intentionally here.")
# Print the response from the agent
print(direct_prompt_agent_response)

# TODO: 5 - Print an explanatory message describing the knowledge source used by the agent to generate the response
direct_prompt_agent_response_explanation = "The agent trained on the gpt-3.5-turbo OpenAI model and answered the question based on that model. It wasn't given any hints in the prompt and it did not consult external knowledge - the agent assumed the model it trained on, was good enough."
# gpt-3.5-turbo
print(direct_prompt_agent_response_explanation)
