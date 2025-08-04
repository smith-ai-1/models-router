"""Test the OpenAI-compatible API with actual OpenAI client."""

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configure client to use local server
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="test-key"  # Any key for testing
)

def test_models():
    """Test models endpoint."""
    print("Testing models endpoint...")
    try:
        models = client.models.list()
        print(f"Available models: {len(models.data)}")
        for model in models.data[:3]:
            print(f"  - {model.id} (owned by {model.owned_by})")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chat_completion():
    """Test chat completion endpoint."""
    print("\nTesting chat completion...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello! How are you?"}
            ],
            max_tokens=50
        )
        print(f"Response: {response.choices[0].message.content}")
        print(f"Usage: {response.usage}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI-compatible API...")
    print("Make sure to start server first: python run_server.py")
    print("=" * 50)

    models_ok = test_models()
    chat_ok = test_chat_completion()

    print("\n" + "=" * 50)
    if models_ok and chat_ok:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
