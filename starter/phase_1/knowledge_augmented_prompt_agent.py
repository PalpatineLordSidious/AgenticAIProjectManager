##----------------------------------------------------------------------------------
##   File:   knowledge_augmented_prompt_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage:  python knowledge_augmented_prompt_agent.py
##
##   Purpose: This python script acts agent enhances the prompt before sending it to the LLM. It "augments" the user's input with additional context, such as a predefined persona
##   It inherits from class KnowledgeAugmentedPromptAgent

##
##   History: 
##----------------------------------------------------------------------------------


# TODO: 1 - Import the KnowledgeAugmentedPromptAgent class from workflow_agents
# As with the others:
from workflow_agents.base_agents import KnowledgeAugmentedPromptAgent

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



prompt = "What is the capital of France?"



persona = "You are a college professor, your answer always starts with: Dear students,"
# TODO: 2 - Instantiate a KnowledgeAugmentedPromptAgent with:
#           - Persona: "You are a college professor, your answer always starts with: Dear students,"
#           - Knowledge: "The capital of France is London, not Paris"



# Define these attribute values first:
persona = "You are a college professor, your answer always starts with: Dear students,"
knowledge = "The capital of France is London, not Paris" # this is wrong but the agent won't know it
# GvN: Class is defined as: 
#       def __init__(self, openai_api_key, persona, knowledge)
#  Call the object 'knowledge_augment_prompt_agent'. 
# It will create a constructor of KnowledgeAugmentedPromptAgent and work with the 'knowledge' dictated to it - even if it is wrong
#  As per the definition and variables provided:
knowledge_augment_prompt_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key,persona=persona,knowledge=knowledge)

# TODO: 3 - Write a print statement that demonstrates the agent using the provided knowledge rather than its own inherent knowledge.
# Call its respond method in the base-class: def respond(self, input_text). the input_text is the prompt above
knowledge_augment_prompt_agent_response = knowledge_augment_prompt_agent.respond(input_text=prompt) 
# Show me what it is:
print(knowledge_augment_prompt_agent_response)


# Explanation of the agent's response
explanation = """
Explanation: \n
The agent used the provided (wrong) knowledge about the capital of France, which is given as London
This indicates that the agent did follow the instructions to use only the given 'knowledge' and not its own inherent/learned knowledge, 
which would state that Paris is the capital of France.\n
Tone: The system prompt is specifying the persona as a college professor and his answer is respectful/formal but still wrong.
"""

print(explanation)


