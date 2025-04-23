import pytest
from app.api_handler import get_request

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