##----------------------------------------------------------------------------------
##   File:   action_planning_agent.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage: python action_planning_agent.py
##
##   Purpose: This python script defines the action planning agent.
#             The agent devises a plan to execute tasks received from provided knowledge
##
##   History: 
##----------------------------------------------------------------------------------



# TODO: 1 - Import all required libraries, including the ActionPlanningAgent
# The base_agents.py is in the /workflow_abnets folder and will need to import it with that relative path
# The folder structure is built using ".":
from workflow_agents.base_agents import ActionPlanningAgent # ActionPlanningAgent is a class inside base_agents.py


# TODO: 2 - Load environment variables and define the openai_api_key variable with your OpenAI API key

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




knowledge = """
# Fried Egg
1. Heat pan with oil or butter
2. Crack egg into pan
3. Cook until white is set (2-3 minutes)
4. Season with salt and pepper
5. Serve

# Scrambled Eggs
1. Crack eggs into a bowl
2. Beat eggs with a fork until mixed
3. Heat pan with butter or oil over medium heat
4. Pour egg mixture into pan
5. Stir gently as eggs cook
6. Remove from heat when eggs are just set but still moist
7. Season with salt and pepper
8. Serve immediately

# Boiled Eggs
1. Place eggs in a pot
2. Cover with cold water (about 1 inch above eggs)
3. Bring water to a boil
4. Remove from heat and cover pot
5. Let sit: 4-6 minutes for soft-boiled or 10-12 minutes for hard-boiled
6. Transfer eggs to ice water to stop cooking
7. Peel and serve
"""

# TODO: 3 - Instantiate the ActionPlanningAgent, passing the openai_api_key and the knowledge variable
# Recall that knowledge was an attribute of this class: self.knowledge = knowledge
action_planning_agent = ActionPlanningAgent(openai_api_key=openai_api_key, knowledge=knowledge)

# TODO: 4 - Print the agent's response to the following prompt: "One morning I wanted to have scrambled eggs"
user_request_prompt = "One morning I wanted to have scrambled eggs"
print(f"User Request: {user_request_prompt}")

# We are now calling method extract_steps_from_prompt defined in ActionPlanningAgent on line 479
action_planning_agent_response = action_planning_agent.extract_steps_from_prompt(user_request_prompt)
# show the response:
print(action_planning_agent_response)

# Write to a file:



