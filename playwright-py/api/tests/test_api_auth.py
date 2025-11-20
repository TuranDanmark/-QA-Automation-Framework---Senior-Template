from api.auth_api import AuthAPI

def test_api_login_success():
    api = AuthAPI()
    res = api.login("eve.holt@reqres.in", "cityslicka")
    assert res.status_code == 200
    assert "token" in res.json()
