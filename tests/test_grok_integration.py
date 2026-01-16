import pytest
import logging
from lib.apis import Chatbot
from config import GROK_API_KEY

# Configure logging to capture output for debugging if needed
logging.basicConfig(level=logging.DEBUG)

# Mock plugin bot for function calling tests
class MockPluginBot:
    def get_available_functions(self):
        return {
            "get_weather": self.get_weather
        }
    
    def get_function_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City and state, e.g. San Francisco, CA"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]

    def get_weather(self, location):
        return f"The weather in {location} is sunny and 25 degrees Celsius."

@pytest.fixture
def chatbot():
    return Chatbot(MockPluginBot())

def is_grok_configured():
    return GROK_API_KEY and "xai-" in GROK_API_KEY

@pytest.mark.skipif(not is_grok_configured(), reason="Grok API key not configured")
def test_grok_connection(chatbot):
    """Test basic connection to Grok API"""
    response = chatbot.elaborate_query(["User: Hello, are you Grok?"])
    assert response is not None
    assert len(response) > 0
    # Grok usually identifies itself or responds friendly
    print(f"DEBUG: Grok response: {response}")

@pytest.mark.skipif(not is_grok_configured(), reason="Grok API key not configured")
def test_grok_function_calling(chatbot):
    """Test function calling capability with Grok"""
    # Ask something that triggers the function
    response = chatbot.elaborate_query(["User: What is the weather in Rome?"])
    
    assert response is not None
    # Check if the mock function result was incorporated
    # Expected: "The weather in Rome is sunny and 25 degrees Celsius."
    assert "sunny" in response.lower() or "25" in response
    assert "rome" in response.lower()
