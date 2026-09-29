##----------------------------------------------------------------------------------
##   File:   routing_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage:  python routing_agent.py
##
##   Purpose: This pattern is designed to intelligently direct incoming tasks or inputs – whether they're raw user requests or steps from a planning agent – to different processing paths or specialized agents based on the nature of the input itself.
##              At the heart of the routing pattern are two fundamental stages: Classification and Task Dispatch
##              Classification is the initial step where the system analyzes an incoming task or input to determine its type, category, intent, or even its complexity. The goal is to understand the nature of the input so an informed decision can be made about how to handle it.
##  	        Once the input is classified, the next stage is Task Dispatch.
##              Based on the classification, the workflow directs or 'dispatches' the input (and its classification label) to the appropriate specialized agent, a specific prompt chain, a function, or a dedicated processing module.
##              
##
##   History: 
##----------------------------------------------------------------------------------



# TODO: 1 - Import the KnowledgeAugmentedPromptAgent and RoutingAgent
# As per previously:
from workflow_agents.base_agents import RoutingAgent, KnowledgeAugmentedPromptAgent



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


persona = "You are a college professor"

knowledge = "You know everything about Texas"
# GvN:  Agent in question: KnowledgeAugmentedPromptAgent
#       Defined as: def __init__(self, openai_api_key, persona, knowledge)
# TODO: 2 - Define the Texas Knowledge Augmented Prompt Agent as a KnowledgeAugmentedPromptAgent:
TEXAS_knowledge_augment_prompt_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona, knowledge=knowledge)

knowledge = "You know everything about Europe"
# TODO: 3 - Define the Europe Knowledge Augmented Prompt Agent
EUROPE_knowledge_augment_prompt_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona, knowledge=knowledge)

# new persona comes in:
persona = "You are a maths professor"
knowledge = "You know everything about math, you take prompts with numbers, extract math formulas, and show the answer without explanation"
# TODO: 4 - Define the Math Knowledge Augmented Prompt Agent
MATHS_knowledge_augment_prompt_agent = KnowledgeAugmentedPromptAgent(openai_api_key=openai_api_key, persona=persona, knowledge=knowledge)

# List of agents is constructed - given code:
routing_agent = RoutingAgent(openai_api_key, {})

agents = [
    {
        "name": "texas agent",
        "description": "Answer a question about Texas",
        "func": lambda x: TEXAS_knowledge_augment_prompt_agent.respond(x) # TODO: 5 - Call the Texas Agent to respond to prompts. GvN: Note: we use the class's respond method
    },
    {
        "name": "europe agent",
        "description": "Answer a question about Europe",
        "func": lambda x: EUROPE_knowledge_augment_prompt_agent.respond(x) # TODO: 6 - Define a function to call the Europe Agent. GvN: Note: we use the class's respond method
    },
    {
        "name": "math agent",
        "description": "When a prompt contains numbers, respond with a math formula",
        "func": lambda x: MATHS_knowledge_augment_prompt_agent.respond(x) # TODO: 7 - Define a function to call the Math Agent
    }
]

routing_agent.agents = agents

# TODO: 8 - Print the RoutingAgent responses to the following prompts:
#           - "Tell me about the history of Rome, Texas"
#           - "Tell me about the history of Rome, Italy"
#           - "One story takes 2 days, and there are 20 stories"

# GvN: - Will use the prompts as given. 
#      - Have to use routing_agent.
#      - Class RoutingAgent has an implemented (in this lesson) method called route_user_requests on line 444 in base_agents.py
#      - The method routes user prompts to the appropriate agent. 

# Assign the list above to the routing agent object - 
#    it has a for-loop implemented in the class to cycle through all the agents received and calculate a best_score
#    the score will help thr routing agent to decide which agents services the prompt.
routing_agent.agents = agents

# Send all 3 prompts to the routing agent - it will decide on the best agent for each - taking the prompts as given:
print(routing_agent.route_user_requests("Tell me about the history of Rome, Texas"))
print(routing_agent.route_user_requests("Tell me about the history of Rome, Italy"))
print(routing_agent.route_user_requests("One story takes 2 days, and there are 20 stories"))
       

