class Config:
    # Адрес API
    api_host = 'https://l-i-n-k.herokuapp.com/'
    api_port = 5000
    api_url = 'https://l-i-n-k.herokuapp.com/'

    # Подключение к БД
    base = 'postgresql://ylgjqbynqxxspx:4902ae077dfb2377a8b3afeced3c82e20bd2e6bf05f8cda386d52295c5442044@ec2-52-17-1-206.eu-west-1.compute.amazonaws.com:5432/d7juj838rq4vv4'

    # Соль для генерации хэша
    SECRET_KEY = '2$ViplzPm935vjRFCyPmdw$nxEHZPlwdmezZgQxYyRegVym6AJDauWC365NTY'
    salt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTQxMjA2MiwianRpIjoiMzBjOTc0YTEtNmQ4NS00ZDZjLWEwOTItMjYxODAzNTFmYmY0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjIxNDEyMDYyLCJleHAiOjE2MjM0ODU2NjJ9.k-nY9DmNeE2W3paQCiOxT6YKbcEZo5breesRB1ZOGmk"

    # Разрешенные адреса для подключения к API
    CORS_ALLOWED_ORIGINS = ['*']
	
