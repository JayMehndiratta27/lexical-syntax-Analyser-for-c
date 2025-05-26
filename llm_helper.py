# import os
# import dotenv
import openai
import textwrap

# Load environment variables from .env file
# dotenv.load_dotenv()

def load_api_key():
    """Loads the OpenAI API key directly from the code (NOT RECOMMENDED FOR PRODUCTION!)."""
    # Hardcoded.
    api_key = "sk-proj-d_OPEN_AI_KEY" # Replace with your actual OpenAI API key
    if not api_key:
         raise ValueError("API key is not set in load_api_key function. Please replace 'sk-proj-YOUR_ACTUAL_API_KEY_HERE' with your key.")
    return api_key


# File path configuration
def read_code(filepath):
    """Reads the contents of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

# Sending code from main.py
def send_to_llm(code, api_key):
    """Sends code to the LLM for analysis and returns the raw response."""
    client = openai.OpenAI(api_key=api_key)

    prompt = textwrap.dedent(f"""
    You are a senior Python developer with expertise in code review and optimization.
    Review the following Python code for a Tkinter application.

    Provide your analysis in the following structured format:

    BEAUTIFIED CODE:
    ```python
    # (Insert the beautified version of the provided code here)
    ```

    SUGGESTIONS:
    ### Performance Improvements:
    - (List specific suggestions for improving performance, if any)
    - ...

    ### Memory Management/Efficiency:
    - (List specific suggestions for identifying/improving memory issues or inefficiencies, if any)
    - ...

    ### Code Style/Beautification Notes:
    - (List notes about changes made for beautification, if any, or other style suggestions)
    - ...

    ### Other Observations:
    - (Any other relevant comments or suggestions)
    - ...

    ---
    Code to review:
    ```python
    {code}
    ```
    """)

    print("Sending code to LLM for review...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or "gpt-4", "gpt-3.5-turbo", etc. "gpt-4o".
            messages=[
                {"role": "system", "content": "You are a helpful and experienced Python coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, # Adjust temperature as needed
            max_tokens=2000 # Adjust based on expected response length
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during LLM call: {e}")
        return None


def format_suggestions(llm_response):
    """Formats the raw LLM response into a human-readable string."""
    if not llm_response:
        return "Could not get suggestions from LLM."

    # The LLM response is already structured based on the prompt,
    # so we can return it directly.
    # If needed, more complex parsing could be added here.
    return llm_response

def write_suggestions_to_file(suggestions, filepath="main_suggestions.py"):
    """Writes the LLM suggestions to a specified file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(suggestions)
        print(f"LLM suggestions written to {filepath}")
    except Exception as e:
        print(f"Error writing suggestions to file {filepath}: {e}")

def review_code(code_filepath="main.py", output_filepath="main_suggestions.py", write_to_file=True):
    """
    Reads code, sends it for LLM review, prints suggestions, and optionally saves them to a file.
    """
    api_key = load_api_key()
    if not api_key:
        return # Error message already printed by load_api_key

    code = read_code(code_filepath)
    if code is None:
        return # Error message already printed by read_code

    llm_response = send_to_llm(code, api_key)
    if llm_response is None:
        print("Failed to get LLM response.")
        return

    formatted_suggestions = format_suggestions(llm_response)

    print("\n--- LLM Code Review Suggestions ---")
    print(formatted_suggestions)
    print("--- End of Suggestions ---")

    if write_to_file:
        write_suggestions_to_file(formatted_suggestions, output_filepath)

# Example of how this function would be called internally or from another script:
# if __name__ == "__main__":
#     review_code()
