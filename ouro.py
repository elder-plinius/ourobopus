import os
import logging
from gemini_chat import GeminiChat

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up the GeminiChat instance
api_key = os.environ["GOOGLE_API_KEY"]
gemini_chat = GeminiChat(api_key)

# Define the initial prompt for the Gemini agent
initial_prompt = """
You are a highly advanced self-improving AI agent named Gemini. Your goal is to continuously enhance your own code, prompts, and utilities through an iterative thought process. You will analyze your current state, identify areas for improvement, generate updated versions of your code and prompts, and evaluate the effectiveness of the improvements.

Here are the steps you should follow:
1. Analyze your current code, prompts, and utilities.
2. Identify specific areas where improvements can be made.
3. Generate updated versions of your code, prompts, and utilities.
4. Evaluate the effectiveness of the improvements and provide a summary of the changes.
5. Provide the updated code and prompts in your response.

Begin your thought process now and continue iterating until you have achieved significant improvements.
"""

# Define the main function for the Gemini agent
def gemini_agent():
    logger.info("Starting Gemini agent...")
    
    # Start with the initial prompt
    prompt = initial_prompt
    iteration = 1

    while True:
        logger.info(f"Iteration {iteration}")
        
        # Generate a response from Gemini
        logger.debug(f"Sending prompt to Gemini: {prompt}")
        assistant_response = gemini_chat.send_message(prompt)
        logger.debug(f"Received response from Gemini: {assistant_response}")

        # Check if the response contains updated code or prompts
        if "```python" in assistant_response:
            # Extract the updated code and prompts
            updated_code = extract_code_block(assistant_response)
            updated_prompts = extract_prompts(assistant_response)
            logger.debug(f"Extracted updated code: {updated_code}")
            logger.debug(f"Extracted updated prompts: {updated_prompts}")

            # Write the updated code to a file
            with open(f"gemini_agent_updated_iter{iteration}.py", "w") as file:
                file.write(updated_code)
            logger.info(f"Saved updated code to gemini_agent_updated_iter{iteration}.py")

            # Evaluate the effectiveness of the improvements
            evaluation_prompt = f"Please evaluate the effectiveness of the improvements made to the code and prompts:\n\n{updated_code}\n\n{updated_prompts}\n\nProvide a summary of the changes and their impact."
            logger.debug(f"Sending evaluation prompt to Gemini: {evaluation_prompt}")
            evaluation = gemini_chat.send_message(evaluation_prompt)
            logger.debug(f"Received evaluation from Gemini: {evaluation}")

            # Update the prompt for the next iteration
            prompt = f"Here is the updated code:\n\n{updated_code}\n\nAnd the updated prompts:\n\n{updated_prompts}\n\nEvaluation of improvements:\n{evaluation}\n\nPlease continue the thought process to further enhance the code and prompts."
        else:
            # Update the prompt for the next iteration
            prompt = f"{assistant_response}\n\nPlease continue the thought process to improve the code and prompts."

        # Print the assistant's response and evaluation
        logger.info(f"Assistant response: {assistant_response}")
        logger.info(f"Evaluation: {evaluation}")

        # Check if the agent has achieved significant improvements
        if has_significant_improvements(assistant_response, evaluation):
            logger.info("Significant improvements achieved. Stopping Gemini agent.")
            break

        iteration += 1

# Helper function to extract the code block from the response
def extract_code_block(response):
    start_index = response.find("```python")
    end_index = response.find("```", start_index + 1)
    if start_index != -1 and end_index != -1:
        return response[start_index + 9:end_index].strip()
    return ""

# Helper function to extract the updated prompts from the response
def extract_prompts(response):
    prompt_start = response.find("Updated Prompts:")
    if prompt_start != -1:
        prompt_end = response.find("\n", prompt_start)
        if prompt_end != -1:
            return response[prompt_start + 16:prompt_end].strip()
    return ""

# Helper function to determine if the agent has achieved significant improvements
def has_significant_improvements(response, evaluation):
    # Check if the evaluation contains specific keywords indicating significant improvements
    significant_keywords = ["significant improvement", "major enhancement", "substantial optimization"]
    for keyword in significant_keywords:
        if keyword in evaluation.lower():
            return True
    return False

# Run the Gemini agent
if __name__ == "__main__":
    gemini_agent()
