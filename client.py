import requests

# Define the API endpoints
REDACT_API_URL = "http://127.0.0.1:8000/redact/"
QUERY_API_URL = "http://127.0.0.1:8001/query/"

def send_text_to_redact_api(text):
    """ Sends user text to the redaction API. """
    payload = {"text": text}
    response = requests.post(REDACT_API_URL, json=payload)
    
    if response.status_code == 200:
        return response.json()["redacted_text"]
    else:
        print("Error in redaction API:", response.json())
        return None

def send_redacted_text_to_query_api(redacted_text):
    """ Sends redacted text to the LLM query API. """
    payload = {"text": redacted_text}
    response = requests.post(QUERY_API_URL, json=payload)
    
    if response.status_code == 200:
        return response.json()["response_text"]
    else:
        print("Error in query API:", response.json())
        return None

if __name__ == "__main__":
    # Get user input
    user_text = input("Enter text to be redacted: ")

    # Step 1: Send input text to redaction API
    redacted_output = send_text_to_redact_api(user_text)
    
    if redacted_output:
        print("\nRedacted Text:", redacted_output)

        # Step 2: Send redacted text to LLM API
        final_response = send_redacted_text_to_query_api(redacted_output)

        if final_response:
            print("\nFinal LLM Response:", final_response)
