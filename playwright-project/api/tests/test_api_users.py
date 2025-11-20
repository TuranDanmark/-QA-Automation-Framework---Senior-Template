from api.users_api import UsersAPI

def test_api_list_users():
    api = UsersAPI()
    res = api.get_users(page=2)
    assert res.status_code == 200
    data = res.json()
    assert "data" in data
    assert isinstance(data["data"], list)
