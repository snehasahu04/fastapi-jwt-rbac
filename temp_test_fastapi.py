from fastapi.testclient import TestClient
import main, time

client = TestClient(main.app)
email = 'test_' + str(int(time.time())) + '@example.com'
print('SIGNUP')
r = client.post('/signup', json={'email': email, 'password': 'secret12'})
print(r.status_code)
print(r.text)
print('LOGIN')
r2 = client.post('/login', json={'email': email, 'password': 'secret12'})
print(r2.status_code)
print(r2.text)
