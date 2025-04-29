import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

def get_request(url:str, params:dict, headers:dict) -> dict:
    """
    Makes basic get request to api

    Params: 
        url: string with full url and endpoint 
        params: dict with application id and key and any other values for api request 
        headers: dict with 'Edamam-Account-User' to define account user name
    Returns: raw json response
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        if response and response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return "Unauthorized request, ensure valid authorization parameters"
        elif response.status_code == 400:
            return "Bad request, check paramaters and try again"
        else:
            return "GET request failed due to unexpected error"
    except HTTPError as e:
        print(f"Unexpected error while attempting to make get request: {e}")
        return None
    
def parse_data(data: dict) -> list[dict]:
    """
    Parses api json response data to extract desired fields

    Note: Only handles first page of response. Each api request returns 1 page of generated results, with 20 hits per page. To access next page link can be found at response -> _links -> next -> href
    """

    #flatten json by 1 level to remove need for deeper key lookups
    data_recipe_list = [item["recipe"] for item in data["hits"]]

    #extract list of recipes and desired fields from response
    #Note: api provides comprehensive list of all total nutrients, only the main macronutrients + sugar are extracted here
    recipes = [
        {
            "label": item["label"],
            "image": item["image"],
            "servings": item["yield"],
            "dietLabels": item["dietLabels"],
            "healthLabels": item["healthLabels"],
            "ingredientLines": item["ingredientLines"],
            "calories": item["calories"],
            "cuisineType": item["cuisineType"],
            "mealType": item["mealType"],
            "FAT": item["totalNutrients"]["FAT"],
            "PROTIEN": item["totalNutrients"]["PROCNT"],
            "CARBS": item["totalNutrients"]["CHOCDF"],
            "FIBER": item["totalNutrients"]["FIBTG"],
            "SUGAR": item["totalNutrients"]["SUGAR"]
        }
        for item in data_recipe_list   
    ]
    return recipes


def get_recipes(search_query, diet=None, meal=None, cuisine=None, health=None, dish=None) -> list[dict]:
    """
    Returns: list of dictionaries, each dict containing data from 1 recipe, including label(recipe name), image, etc. Should have length  <=20, based on search query/filters provided to api request
    """
    load_dotenv()
    base_url = os.environ['API_BASE_URL']
    endpoint = os.environ['API_ENDPOINT']
    api_user = os.environ['API_USER']
    api_id = os.environ['API_ID']
    api_key = os.environ['API_KEY']

    full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {"Edamam-Account-User": api_user}
    parameters = {"type": "public", "q":search_query, "app_id":api_id, "app_key":api_key}

    # only add filters if provided
    if diet:
        parameters["diet"] = diet
    if meal:
        parameters["mealType"] = meal
    if cuisine: 
        parameters["cuisineType"] = cuisine
    if health:
        parameters["health"] = health
    if dish:
        parameters["dishType"] = dish

    response = get_request(full_url, parameters, headers)
    recipes = parse_data(response)
    return recipes