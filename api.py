import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

def get_request(url:str, params:dict, headers:dict) -> dict:
    """
    Makes basic get request to api

    Params: 
        url: string with full url and endpoint 
        params: dict with apikey and any other values for api request 
        BOTH VALUES SHOULD BE DEFINED IN CONFIG.INI 
    Returns: raw json response
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        if response and response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return "Unauthorized request, ensure valid authoriziation paramaters"
        elif response.status_code == 400:
            return "Bad request, check paramaters and try again"
        else:
            return "GET request failed due to unexpected error"
    except HTTPError as e:
        print(f"Unexpected error while attempting to make get request: {e}")
        return None
    

def main():
    load_dotenv()
    base_url = os.environ['API_BASE_URL']
    endpoint = os.environ['API_ENDPOINT']
    api_user = os.environ['API_USER']
    api_id = os.environ['API_ID']
    api_key = os.environ['API_KEY']

    full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {"Edamam-Account-User": api_user}
    parameters = {"type": "public", "q":"chicken", "app_id":api_id, "app_key":api_key}

    response = get_request(full_url, parameters, headers)
    print(response)

if __name__ == '__main__':
    main()