import pytest
from app.api_handler import get_request, parse_data

@pytest.mark.request
def test_valid_request(mocker):
    mock_data = {}

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)
    response = get_request(url="", params={}, headers={})

    assert response == mock_data

@pytest.mark.request
def test_invalid_authorization(mocker):
    mock_data = {}

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.status_code = 401

    mocker.patch("requests.get", return_value=mock_response)
    response = get_request(url="", params={}, headers={})

    assert response == "Unauthorized request, ensure valid authorization parameters"

@pytest.mark.request
def test_bad_request(mocker):
    mock_data = {}

    mock_response = mocker.MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.status_code = 400

    mocker.patch("requests.get", return_value=mock_response)
    response = get_request(url="", params={}, headers={})

    assert response == "Bad request, check paramaters and try again"

def test_parse_data():
    # Provide sample data in structure api provides
    mock_data = {
    "from": 1,
    "to": 20,
    "count": 10000,
    "_links": {
        "next": {
            "href": "http://fake_link.com",
            "title": "Next page"
        }
    },
    "hits": [
        {
            "recipe": {
                "uri": "http://fake_link.com",
                "label": "Shredded chicken",
                "image": "http://fake_link.com",
                "images": {
                    "THUMBNAIL": {
                        "url": "http://fake_link.com",
                        "width": 100,
                        "height": 100
                    },
                    "SMALL": {
                        "url": "http://fake_link.com",
                        "width": 200,
                        "height": 200
                    },
                    "REGULAR": {
                        "url": "http://fake_link.com",
                        "width": 300,
                        "height": 300
                    },
                    "LARGE": {
                        "url": "http://fake_link.com",
                        "width": 600,
                        "height": 600
                    }
                },
                "source": "BBC Good Food",
                "url": "http://fake_link.com",
                "shareAs": "http://fake_link.com",
                "yield": 14.0,
                "dietLabels": [
                    "Low-Carb",
                    "Low-Sodium"
                ],
                "healthLabels": [
                    "Sugar-Conscious",
                    "Low Sugar",
                    "Keto-Friendly",
                    "Paleo",
                    "Mediterranean",
                    "Dairy-Free",
                    "Gluten-Free",
                    "Wheat-Free",
                    "Egg-Free",
                    "Peanut-Free",
                    "Tree-Nut-Free",
                    "Soy-Free",
                    "Fish-Free",
                    "Shellfish-Free",
                    "Pork-Free",
                    "Red-Meat-Free",
                    "Crustacean-Free",
                    "Celery-Free",
                    "Mustard-Free",
                    "Sesame-Free",
                    "Lupine-Free",
                    "Mollusk-Free",
                    "Alcohol-Free",
                    "No oil added",
                    "Sulfite-Free",
                    "Kosher"
                ],
                "cautions": [],
                "ingredientLines": [
                    "1 ½ chicken stock cubes",
                    "2 chicken breasts, around 400g"
                ],
                "ingredients": [
                    {
                        "text": "1 ½ chicken stock cubes",
                        "quantity": 1.5,
                        "measure": "<unit>",
                        "food": "chicken",
                        "weight": 1800.0,
                        "foodCategory": "Poultry",
                        "foodId": "food_bmyxrshbfao9s1amjrvhoauob6mo",
                        "image": "http://fake_link.com"
                    },
                    {
                        "text": "2 chicken breasts, around 400g",
                        "quantity": 2.0,
                        "measure": "<unit>",
                        "food": "chicken breasts",
                        "weight": 544.0,
                        "foodCategory": "Poultry",
                        "foodId": "food_bdrxu94aj3x2djbpur8dhagfhkcn",
                        "image": "http://fake_link.com"
                    }
                ],
                "calories": 4522.8,
                "totalCO2Emissions": 23135.28,
                "co2EmissionsClass": "F",
                "totalWeight": 2344.0,
                "totalTime": 0.0,
                "cuisineType": [
                    "american"
                ],
                "mealType": [
                    "lunch/dinner"
                ],
                "dishType": [
                    "starter"
                ],
                "totalNutrients": {
                    "ENERC_KCAL": {
                        "label": "Energy",
                        "quantity": 4522.8,
                        "unit": "kcal"
                    },
                    "FAT": {
                        "label": "Fat",
                        "quantity": 286.0528,
                        "unit": "g"
                    },
                    "FASAT": {
                        "label": "Saturated",
                        "quantity": 80.64272,
                        "unit": "g"
                    },
                    "FATRN": {
                        "label": "Trans",
                        "quantity": 1.7840799999999997,
                        "unit": "g"
                    },
                    "FAMS": {
                        "label": "Monounsaturated",
                        "quantity": 116.06815999999999,
                        "unit": "g"
                    },
                    "FAPU": {
                        "label": "Polyunsaturated",
                        "quantity": 60.44656,
                        "unit": "g"
                    },
                    "CHOCDF": {
                        "label": "Carbs",
                        "quantity": 0.0,
                        "unit": "g"
                    },
                    "FIBTG": {
                        "label": "Fiber",
                        "quantity": 0.0,
                        "unit": "g"
                    },
                    "SUGAR": {
                        "label": "Sugars",
                        "quantity": 0.0,
                        "unit": "g"
                    },
                    "PROCNT": {
                        "label": "Protein",
                        "quantity": 457.20000000000005,
                        "unit": "g"
                    }
                }
            }
    }]}
    
    response = parse_data(mock_data)

    #Ensure response is in expected structure
    assert isinstance(response, list) and all(isinstance(item, dict) for item in response)
    #Check values are parsed correctly (hardcoded from mock_data sample response)
    assert response[0]['label'] == 'Shredded chicken'
    assert response[0]['image'] == 'http://fake_link.com'
    assert response[0]['servings'] == 14.0
    assert response[0]['dietLabels'] == ["Low-Carb","Low-Sodium"]
    assert response[0]['mealType'] == ["lunch/dinner"]