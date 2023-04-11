#!/usr/bin/env python

import openai_secret_manager
import openai
import re
import argparse
import os
import sys

def generate_linux_command(prompt, model, temperature, max_tokens, api_key):
    """
    Generate a Linux command based on a description using the OpenAI API.
    """
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )
    generated_text = response.choices[0].text
    return generated_text
    #match = re.search(r'^([a-zA-Z0-9_-]+\s*)+', generated_text)
    #if match is None:
    #    return "Unable to generate a valid Linux command."
    #else:
    #    return match.group(0)

def main():
    """
    Command-line interface for generating Linux commands using the OpenAI API.
    """
    parser = argparse.ArgumentParser(description='Generate a Linux command based on a description using the OpenAI API.')
    parser.add_argument('description', type=str, help='The description of the command to generate.')
    parser.add_argument('--model', type=str, default='text-davinci-002', help='The OpenAI API model to use.')
    parser.add_argument('--temperature', type=float, default=0.5, help='The temperature to use for sampling.')
    parser.add_argument('--max-tokens', type=int, default=50, help='The maximum number of tokens to generate.')
    parser.add_argument('--api-key', type=str, help='Your OpenAI API key.')
    args = parser.parse_args()

    # Get the OpenAI API key
    api_key = args.api_key
    if api_key is None:
        # Check if the API key is already saved
        if os.path.exists(".openai"):
            with open(".openai", "r") as f:
                api_key = f.read().strip()

    # Prompt for API key if not provided
    if api_key is None:
        try:
            api_key = openai_secret_manager.get_secret("openai")["api_key"]
        except Exception as e:
            print("Error: {}".format(e))
            print("Please set your OpenAI API key as an environment variable or use the --api-key option.")
            return
    else:
        api_key = args.api_key

    prompt = "Generate a Linux command based on a description:\nInput: {}\nOutput:".format(args.description)
    command = generate_linux_command(prompt, args.model, args.temperature, args.max_tokens, api_key)
    print(command)

if __name__ == '__main__':
    main()
