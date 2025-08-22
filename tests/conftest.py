import pytest

@pytest.fixture
def sample_data():
    return {"a": 1, "b": 2}

@pytest.fixture(params=[1, 2, 3])
def num(request):
    return request.param
