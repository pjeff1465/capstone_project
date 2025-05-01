import pytest
from app.api_handler import get_request, parse_data
import os
from dotenv import load_dotenv
import time

@pytest.fixture(scope="session")
def env_vars():
    load_dotenv() 

    env = {
        "API_BASE_URL": os.environ["API_BASE_URL"],
        "API_ENDPOINT": os.environ["API_ENDPOINT"],
        "API_USER": os.environ["API_USER"],
        "API_ID": os.environ["API_ID"],
        "API_KEY": os.environ["API_KEY"],
    }

    return env

def test_get_request(env_vars):
    """
    Tests get request to api, ensuring valid authorization / paramaters are used and response is structured as expected
    Must have valid values defined in .env for api credentials
    """
    url = f"{env_vars['API_BASE_URL'].rstrip('/')}/{env_vars['API_ENDPOINT'].lstrip('/')}"
    
    params = {
        "type": "public",
        "q": "chicken",
        "app_id": env_vars["API_ID"],
        "app_key": env_vars["API_KEY"]
    }

    headers = {
        "Edamam-Account-User": env_vars["API_USER"]
    }

    response = get_request(url, params, headers)

    assert isinstance(response, dict)
    assert "hits" in response
    assert len(response["hits"]) > 0

def test_request_performance(env_vars, performance_threshold_s=10):
    """
    Tests the response performance of the api by timing how long it takes to recieve a response.
    performance_threshold_s can be changed to determine acceptable time frame for response
    """
    url = f"{env_vars['API_BASE_URL'].rstrip('/')}/{env_vars['API_ENDPOINT'].lstrip('/')}"
    
    params = {
        "type": "public",
        "q": "chicken",
        "app_id": env_vars["API_ID"],
        "app_key": env_vars["API_KEY"]
    }

    headers = {
        "Edamam-Account-User": env_vars["API_USER"]
    }
    start_time = time.time()
    response = get_request(url, params, headers)
    end_time = time.time()

    response_time = end_time - start_time
    assert response_time < performance_threshold_s, f"API Respone took longer than acceptable. Time elapsed: {response_time}s"
