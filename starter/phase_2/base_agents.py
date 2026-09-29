##----------------------------------------------------------------------------------
##   File:   base_agents.py
##   Author: Graeme van Niekerk
#            tychotma1@gmail.com

##   Usage: 
##
##   Purpose: # This python script defines these base agent classes:
"""
	DirectPromptAgent
	AugmentedPromptAgent
	KnowledgeAugmentedPromptAgent
	RAGKnowledgePromptAgent
	EvaluationAgent
	RoutingAgent
	ActionPlanningAgent
"""
##
##   History: 
##----------------------------------------------------------------------------------


# These base classes will be used by derived classes such as the action_planning_agent, augmented_prompt_agent etc
# The LLM api call is done like this:
#  client = OpenAI(base_url="https://openai.vocareum.com/v1",api_key=self.openai_api_key)

#############################################################
# TODO: 1 - import the OpenAI class from the openai library

# Libraries needed:
import os

# This was installed from the text file as pip read it:
from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: 

# Maths, data and regular expressions:
# This was installed from the text file as pip read it:
import pandas as pd
import numpy as np
import re

# utility libs:
import csv
import uuid
from datetime import datetime

#############################################################


# DirectPromptAgent class definition
class DirectPromptAgent:
    
    # initiate the class as 'self' and point to the api key:
    def __init__(self, openai_api_key):
        # Initialize the agent
        # TODO: 2 - Define an attribute named openai_api_key to store the OpenAI API key provided to this class.
        # self-pointer to the attribute - the DirectPromptAgent object refers to itself as 'self' - and it takes the api key:
        self.openai_api_key = openai_api_key # passed in
        # Debug
        # print(self.openai_api_key)

    def respond(self, prompt): # prompt passed in
        # Generate a response using the OpenAI API
        client = OpenAI(base_url="https://openai.vocareum.com/v1",api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo', # Specify the model to use (gpt-3.5-turbo)
            # TODO: 4 - Provide the user's prompt here. Do not add a system prompt.
            # Reference: the refinery optimizer lab in the lessons                
            # No system_prompt specified: 
            messages=[
                {"role": "user", "content": prompt} # only have this in the list
            ],
            temperature=0 
        )
        # TODO: 5 - Return only the textual content of the response (not the full JSON response).
        # Again, as per the refinery code - decided to strip out any leading or trailing whitespaces:
        return response.choices[0].message.content.strip()

##########################################################################################################################       

# AugmentedPromptAgent class definition
class AugmentedPromptAgent:
    def __init__(self, openai_api_key, persona):
        """Initialize the agent with given attributes."""
        # TODO: 1 - Create an attribute for the agent's persona
        # The persona becomes and attribute to the object's instantiation: self.persona
        self.persona = persona
        self.openai_api_key = openai_api_key

    def respond(self, input_text):
        """Generate a response using OpenAI API."""
        ## LLM call:
        client = OpenAI(base_url="https://openai.vocareum.com/v1",api_key=self.openai_api_key)

        # TODO: 2 - Declare a variable 'response' that calls OpenAI's API for a chat completion.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # ** Discussing line 92:
            # {"role": "system", ...}: In AI chat APIs, messages are categorized by "roles." The system role acts as the high-level director. It sets the rules, boundaries, 
            # and persona for the AI, which the user usually doesn't see directly during the conversation.
            # "Forget all old contexts.": This is a prompt engineering technique. It attempts to wipe or override any instructions the AI received earlier in the session, 
            # forcing it to prioritize the new rules that follow.
            # f"... {self.persona}": This is a Python f-string (formatted string literal). The f allows Python to inject the value of a variable directly into the text.
            # self.persona: This is an object property (likely inside a Python class) that stores a specific character description, tone, or set of instructions 
            messages=[
                # TODO: 3 - Add a system prompt instructing the agent to assume the defined persona and explicitly forget previous context.
                # Using the wording I see below in class KnowledgeAugmentedPromptAgent: "Forget all previous context"
                {"role": "system", "content": f"Forget all previous context. {self.persona}"},
                {"role": "user", "content": input_text}
            ],
            temperature=0
        )
        # return  # TODO: 4 - Return only the textual content of the response, not the full JSON payload.
        # Same as DirectPromptAgent:
        return response.choices[0].message.content.strip()

##########################################################################################################################

# KnowledgeAugmentedPromptAgent class definition
class KnowledgeAugmentedPromptAgent:
    def __init__(self, openai_api_key, persona, knowledge):
        """Initialize the agent with provided attributes."""
        # The class receives three variables: openai_api_key, persona, knowledge
        # These become attributes of the class and they need to be defined and assigned to the class attribute by the same name:
        self.persona = persona
        # TODO: 1 - Create an attribute to store the agent's knowledge.
        # Call the attribute 'knowledge'. 
        # Create the attribute to the self-pointer and assign it to 'knowledge'. It is the same as self.persona = persona above.
        self.knowledge = knowledge
        # Assign openai_api_key to an attribute of the class as self.openai_api_key
        self.openai_api_key = openai_api_key

    def respond(self, input_text):
        ## GvN: assuming the input_text comes from the user or from outside
        """Generate a response using the OpenAI API."""
        client = OpenAI(base_url="https://openai.vocareum.com/v1",api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # GvN: This is a role assignment:
            # There are plenty of example in the lessons around the messages list and its construct:
            # messages=[
            #  {"role": "system", "content": system_prompt},
            #  {"role": "user", "content": user_prompt}
            # ],

            # I won't deviate from it

            # The self.persona needs to be given an instruction from the system to 'forget' the past. So, the f-predicate can be used to tell the persona this:            
            # Like above: f"Forget all previous context. {self.persona}"}
            # The other system-based prompts will just be in the format {"role": "system", "content": system_prompt} but also with the f predicate and each message

            # TODO: 2 
            # - Construct a system message including:
            # - The persona with the following instruction:
            #    "You are _persona_ knowledge-based assistant. Forget all previous context."
            # - The provided knowledge with this instruction:
            #    "Use only the following knowledge to answer, do not use your own knowledge: _knowledge_"
            # - Final instruction:
            #    "Answer the prompt based on this knowledge, not your own."

            # Creating the list with the above reasoning and I'll use the exact wording in the TODO:

            messages=[
                # 1. persona is told to forget his past and go stateless:
                {"role": "system", "content": f"Forget all previous context. {self.persona}"},
                # 2. The provided knowledge with this instruction and it's assigned to _knowledge_ which is a defined attribute sbove:
                {"role": "user", "content": f"Use only the following knowledge to answer, do not use your own knowledge: {self.knowledge}"},
                # 3. Final instruction: Answer the prompt based on this knowledge, not your own (meaning no attribute referencing because you have forgotten it)
                {"role": "user", "content": f"Final instruction: Answer the prompt based on this knowledge, not your own"},
                # 4. You also need to work with the prompt or input that was given - as per the examples in the lessons seen:
                #    {"role": "user", "content": prompt} - but the parameter is actually input_text, not prompt
                {"role": "user", "content": input_text}
            ],                          
            temperature=0
        )
        # TODO: 3 - Add the user's input prompt here as a user message.
        return response.choices[0].message.content


##########################################################################################################################


# RAGKnowledgePromptAgent class definition
# ** GvN: No TODO here it seems
class RAGKnowledgePromptAgent:
    """    
    An agent that uses Retrieval-Augmented Generation (RAG) to find knowledge from a large corpus
    and leverages embeddings to respond to prompts based solely on retrieved information.
    """

    def __init__(self, openai_api_key, persona, chunk_size=2000, chunk_overlap=100):
        """
        Initializes the RAGKnowledgePromptAgent with API credentials and configuration settings.

        Parameters:
        openai_api_key (str): API key for accessing OpenAI.
        persona (str): Persona description for the agent.
        chunk_size (int): The size of text chunks for embedding. Defaults to 2000.
        chunk_overlap (int): Overlap between consecutive chunks. Defaults to 100.
        """

        self.persona = persona
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.openai_api_key = openai_api_key
        self.unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.csv"

    def get_embedding(self, text):
        """
        Fetches the embedding vector for given text using OpenAI's embedding API.

        Parameters:
        text (str): Text to embed.

        Returns:
        list: The embedding vector.
        """

        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding

    def calculate_similarity(self, vector_one, vector_two):
        """
        Calculates cosine similarity between two vectors.

        Parameters:
        vector_one (list): First embedding vector.
        vector_two (list): Second embedding vector.

        Returns:
        float: Cosine similarity between vectors.
        """
        vec1, vec2 = np.array(vector_one), np.array(vector_two)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def chunk_text(self, text):
        """
        Splits text into manageable chunks, attempting natural breaks.

        Parameters:
        text (str): Text to split into chunks.

        Returns:
        list: List of dictionaries containing chunk metadata.
        """
        separator = "\n"
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) <= self.chunk_size:
            return [{"chunk_id": 0, "text": text, "chunk_size": len(text)}]

        chunks, start, chunk_id = [], 0, 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            if separator in text[start:end]:
                end = start + text[start:end].rindex(separator) + len(separator)

            chunks.append({
                "chunk_id": chunk_id,
                "text": text[start:end],
                "chunk_size": end - start,
                "start_char": start,
                "end_char": end
            })

            start = end - self.chunk_overlap
            chunk_id += 1

        with open(f"chunks-{self.unique_filename}", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["text", "chunk_size"])
            writer.writeheader()
            for chunk in chunks:
                writer.writerow({k: chunk[k] for k in ["text", "chunk_size"]})

        return chunks

    def calculate_embeddings(self):
        """
        Calculates embeddings for each chunk and stores them in a CSV file.

        Returns:
        DataFrame: DataFrame containing text chunks and their embeddings.
        """
        df = pd.read_csv(f"chunks-{self.unique_filename}", encoding='utf-8')
        df['embeddings'] = df['text'].apply(self.get_embedding)
        df.to_csv(f"embeddings-{self.unique_filename}", encoding='utf-8', index=False)
        return df

    def find_prompt_in_knowledge(self, prompt):
        """
        Finds and responds to a prompt based on similarity with embedded knowledge.

        Parameters:
        prompt (str): User input prompt.

        Returns:
        str: Response derived from the most similar chunk in knowledge.
        """
        prompt_embedding = self.get_embedding(prompt)
        df = pd.read_csv(f"embeddings-{self.unique_filename}", encoding='utf-8')
        df['embeddings'] = df['embeddings'].apply(lambda x: np.array(eval(x)))
        df['similarity'] = df['embeddings'].apply(lambda emb: self.calculate_similarity(prompt_embedding, emb))

        best_chunk = df.loc[df['similarity'].idxmax(), 'text']
        # LLM call:
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are {self.persona}, a knowledge-based assistant. Forget previous context."},
                {"role": "user", "content": f"Answer based only on this information: {best_chunk}. Prompt: {prompt}"}
            ],
            temperature=0
        )

        return response.choices[0].message.content

##########################################################################################################################

class EvaluationAgent:
    
    def __init__(self, openai_api_key, persona, evaluation_criteria, worker_agent, max_interactions):
        # Initialize the EvaluationAgent with given attributes.
        # TODO: 1 - Declare class attributes here
        # GvN: 5 attributes to instantiate a self constructor of EvaluationAgent: openai_api_key, persona, evaluation_criteria, worker_agent, max_interactions:
        self.openai_api_key = openai_api_key
        self.persona = persona
        self.evaluation_criteria = evaluation_criteria
        self.worker_agent = worker_agent
        self.max_interactions = max_interactions


    def evaluate(self, initial_prompt):
        # This method manages interactions between agents to achieve a solution.
        # LLM call:
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)

        prompt_to_evaluate = initial_prompt
        
        # TODO: 2 - Set loop to iterate up to the maximum number of interactions:
        # GvN: the loop takes place over a range - max_interactions is an attribute of the class - thus 'self'
        #   note: this editor has intelli-prompt active - I just follow that to complete most of my statements:
        for i in range(self.max_interactions):
            print(f"\n--- Interaction {i+1} ---")

            print(" Step 1: Worker agent generates a response to the prompt")
            print(f"Prompt:\n{prompt_to_evaluate}")
            # GvN: worker_agent is an attribute of the class and thuse self.worker_agent
            #      the def above has a parameter initial_prompt passed in. This is assigned to prompt_to_evaluate
            #      thus: self.worker_agent needs to reference prompt_to_evaluate as an input variable
            #      As per the role clause: {"role": "user", "content": input_text}  - we can use input_text
            response_from_worker = self.worker_agent.respond(input_text=prompt_to_evaluate) # TODO: 3 - Obtain a response from the worker agent
            print(f"Worker Agent Response:\n{response_from_worker}")

            print(" Step 2: Evaluator agent judges the response")
            eval_prompt = (
                f"Does the following answer: {response_from_worker}\n"
                # the attribute is evaluation_criteria of 'self' and we need to reference that:
                f"Meet this criteria: {self.evaluation_criteria}"  # TODO: 4 - Insert evaluation criteria here
                f"Respond Yes or No, and the reason why it does or doesn't meet the criteria."
            )
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                # TODO: 5 - Define the message structure sent to the LLM for evaluation (use temperature=0)
                ## GvN: eval_prompt above needs to be sent to the LLM using {"role": "user", "content": input_text} construct:
                messages=[
                    {"role": "user", "content": eval_prompt}
                ]    
            )
            # GvN : what was the response from the LLM? Assign the answer to evaluation and return it to the outside:
            evaluation = response.choices[0].message.content.strip()
            print(f"Evaluator Agent Evaluation:\n{evaluation}")

            print(" Step 3: Check if evaluation is positive")
            if evaluation.lower().startswith("yes"):
                print("✅ Final solution accepted.")
                break
            else:
                print(" Step 4: Generate instructions to correct the response")
                instruction_prompt = (
                    f"Provide instructions to fix an answer based on these reasons why it is incorrect: {evaluation}"
                )
                # TODO: 6 - Define the message structure sent to the LLM to generate correction instructions (use temperature=0)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    # We have to use the instruction_prompt above and send that off to the LLM again using {"role": "user", "content": input_text} construct
                    # This is the same as in the lessons - for example Routing" {"role": "user", "content": user_prompt} but in this case the user_prompt is instruction_prompt:
                    messages=[{"role": "user", "content": instruction_prompt}],
                )
                instructions = response.choices[0].message.content.strip()
                print(f"Instructions to fix:\n{instructions}")

                print(" Step 5: Send feedback to worker agent for refinement")
                prompt_to_evaluate = (
                    f"The original prompt was: {initial_prompt}\n"
                    f"The response to that prompt was: {response_from_worker}\n"
                    f"It has been evaluated as incorrect.\n"
                    f"Make only these corrections, do not alter content validity: {instructions}"
                )
        return {
            # TODO: 7 - Return a dictionary containing the final response, evaluation, and number of iterations
            # GvN: Looking at prompt_to_evaluate, we need to get something returned from response_from_worker with the evaluation (line 361)
            #      So, I'll just copy directly from the above dict:
            "final_worker_response": response_from_worker,
            "evaluation": evaluation, ## obtained in evaluation = response.choices[0].message.content.strip()
            "iterations": i + 1 # increment the loop variable i 
        }   


##########################################################################################################################


class RoutingAgent():

    def __init__(self, openai_api_key, agents):
        # Initialize the agent with given attributes
        self.openai_api_key = openai_api_key # left this as is        
        # TODO: 1 - Define an attribute to hold the agents, call it agents
        self.agents = agents

    def get_embedding(self, text):
        client = OpenAI(base_url="https://openai.vocareum.com/v1",api_key=self.openai_api_key)
        # TODO: 2 - Write code to calculate the embedding of the text using the text-embedding-3-large model
        # GvN: Reference: https://developers.openai.com/api/docs/guides/embeddings
        #     An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. 
        #     Small distances suggest high relatedness and large distances suggest low relatedness.
        #     Ok, so in this discussion on this page, we have a model, input and encoding_format (float)
        #     It looks like this:
        """
        import OpenAI from "openai";
        const openai = new OpenAI();
        const embedding = await openai.embeddings.create({
        model: "text-embedding-3-small",
        input: "Your text string goes here",
        encoding_format: "float",
        });
        """
        # In my case the client is already defined on line 409 and it will be used as the object that is to be embedded:
        # The name of the embedding will be response
        response = client.embeddings.create(
            model="text-embedding-3-small", # use the model as suggested
            input=text,                     # line 410 - text is passed in
            encoding_format="float",        # as suggested above and confirmed by the webpage
        );
        # Extract and return the embedding vector from the response - left this as is:
        embedding = response.data[0].embedding    
        return embedding
        # Show in console:
        # console.log(embedding);
        console.log("This calculated embedding value is", embedding)



    # TODO: 3 - Define a method to route user prompts to the appropriate agent
    def route_user_requests(self, user_input):
        # TODO: 4 - Compute the embedding of the user input prompt
        # call get_embedding method above that is part of the class RoutingAgent now; just self-reference the method (intelli-sense completes it for me in this editor)
        # I can see at the end of this def that user_input is the parameter name - so, will use that
        input_embedding = self.get_embedding(user_input) # the constructor will need input from the user and get_embedding expects this as a parameter
        best_agent = None
        best_score = -1

        """
        I am struggling with this:
         When an embedding-based routing agent fails to find matching agents, 
         the root cause usually boils down to semantic mismatch, 
         low retrieval resolution, or overly rigid similarity thresholds.

         I don't know if the agent descriptions are too vague in routing_agent.py
         Running out of time to investigate this

        """

        for agent in self.agents:
            # TODO: 5 - Compute the embedding of the agent description
            agent_embedding = self.get_embedding(agent["description"]) # persona (str): Persona description for the agent.
            if agent_embedding is None:
                continue

            # This isn't giving me very good values
            similarity = np.dot(input_embedding, agent_embedding) / (np.linalg.norm(input_embedding) * np.linalg.norm(agent_embedding))
            print(f"- The calculated similarity-embedding value is {similarity}")

            # TODO: 6 - Add logic to select the best agent based on the similarity score between the user prompt and the agent descriptions
            if similarity > best_score: # i.e. anything > -1
                best_score = similarity
                best_agent = agent

        if best_agent is None:
            return "  X Sorry, no suitable agent could be selected.\n"

        print(f"[Router] Best agent: {best_agent['name']} (score={best_score:.3f})")
        return best_agent["func"](user_input)

##########################################################################################################################

class ActionPlanningAgent:

    def __init__(self, openai_api_key, knowledge):
        # TODO: 1 - Initialize the agent attributes here
        self.openai_api_key = openai_api_key
        self.knowledge = knowledge

    def extract_steps_from_prompt(self, prompt):

        # TODO: 2 - Instantiate the OpenAI client using the provided API key
        # Like line 19:
        client = OpenAI(base_url="https://openai.vocareum.com/v1", api_key=self.openai_api_key)
        # TODO: 3 - Call the OpenAI API to get a response from the "gpt-3.5-turbo" model.
        # Provide the following system prompt along with the user's prompt:
        # "You are an action planning agent. Using your knowledge, you extract from the user prompt the steps requested to complete the action the user is asking for. 
        # You return the steps as a list. Only return the steps in your knowledge. Forget any previous context. This is your knowledge: {pass the knowledge here}"
        
        # GvN: like in DirectPromptAgent definition:
        """
        response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
        {"role": "user", "content": prompt}
        ],
        temperature=0
        )
        """
        # You have two role prompts above: system and user
        # Looking at how it's done in AugmentedPromptAgent with :
        """
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": f"Forget all previous context. {self.persona}"},
        {"role": "user", "content": input_text}
        ],
        temperature=0
        )
        # In this case it will be something like:
        #     {"role": "system", "content": f"You are an action planning agent. Using your knowledge, you extract from the user prompt the steps requested to complete the action the user is asking for. You return the steps as a list. Only return the steps in your knowledge. Forget any previous context. This is your knowledge: {self.knowledge}"},
        #     extract_steps_from_prompt receives a user prompt called 'prompt': def extract_steps_from_prompt(self, prompt)
        #     use that then as the user role: {"role": "user", "content": prompt}
        """
        # With this outline as a guide, I can do the response structure
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an action planning agent. Using your knowledge, you extract from the user prompt the steps requested to complete the action the user is asking for. You return the steps as a list. Only return the steps in your knowledge. Forget any previous context. This is your knowledge: {self.knowledge}"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2 # Put slight urgency into planning this action?
        ) # response ends

        # As per many examples in lessons:
        response_text = response.choices[0].message.content.strip()  # TODO: 4 - Extract the response text from the OpenAI API response


        # TODO: 5 - Clean and format the extracted steps by removing empty lines and unwanted text
        # But I already did a strip on response_text above? This below is redundant?
        steps = response_text.split("\n")
        # So, steps will now be a list of steps and you can parse every member, say every single_step, of steps:
        steps = [single_step.strip() for single_step in steps]
        # Now cleaned up - again
        return steps

##########################################################################################################################        
