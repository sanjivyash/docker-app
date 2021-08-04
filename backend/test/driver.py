from fastapi.testclient import TestClient

from app.main import app
from .tests import Test

client = TestClient(app)
test = Test(client)
test()
