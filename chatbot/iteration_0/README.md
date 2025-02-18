# Motivation

This series goes beyond the typical 'Hello World' tutorial to explore essential considerations for building real-world Generative AI applications. While there are excellent resources [[1](https://applied-llms.org/#operational-day-to-day-and-org-concerns)] [[2](https://eugeneyan.com/writing/llm-patterns/#collect-user-feedback-to-build-our-data-flywheel)] on best practices for building Generative AI systems, applying them in real implementations isn't always clear. This series is designed for those already familiar with Large Language Models (LLMs) and looking to apply best practices in real-world implementations.

We'll use [LlamaIndex](https://docs.llamaindex.ai/en/stable/) and other tools to build a minimal Generative AI application while addressing key topics like LLM hallucinations, evaluations, monitoring, and retrieval-augmented generation (RAG).

# Example Application

In this tutorial, we'll build a simple Q&A chatbot using a fictitious product called RelMiner and its documentation. The chatbot will enable us to query the RelMiner documentation interactively, retrieving relevant information based on our questions. 

Understanding your input data is [crucial](https://applied-llms.org/#look-at-samples-of-llm-inputs-and-outputs-every-day) in Generative AI. I suggest to get familiar with the RelMiner documentation (`relminer.txt`) as this will help you assess the model's response quality. For example, here is a small description of this project:

> RelMiner is an open-source command-line tool designed to automatically extract a knowledge graph from a given text corpus. It detects entities, concepts, and relationships within unstructured text, making it ideal for researchers, data scientists, and knowledge engineers looking to structure textual data.

Please refer to the blog post for more details. 

# Setting up and running the example

In order to set up and run the example follow these steps: 

```bash
# Clone this repo
git clone git@github.com:fordaz/sandbox.git

# go to the chatbot directory
cd chatbot/iteration_0

# Configure your OpenAI Key
export OPENAI_API_KEY="..."

# Create an environment for this iteration, for example using Conda:
conda create -n chatbot_iter_0 python=3.10

# Install the few dependencies
pip install -r requirements.txt
```

Now you can run the Chatbot with any of the following commands:

```bash
# Running using the "best" chat mode and the system prompt version 0
python chatbot.py --mode best --prompt v0

# Using "condense_plus_context" chat more
python chatbot.py --mode condense_plus_context --prompt v0

# Using system prompt version 1
python chatbot.py --mode condense_plus_context --prompt v1

# Using the updates version of the docs which contain pricing information
python chatbot.py --mode condense_plus_context --prompt v1 --docs pricing
```

To exit the Chatbot, just type `bye`

