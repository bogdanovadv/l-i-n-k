class Config:
    # Адрес API
    api_host = '10.170.1.120'
    api_port = 5000
    api_url = f"http://{api_host}:{api_port}"

    # Подключение к БД
    db_host = "localhost"
    db_name = "orm_test"
    db_user = "root"
    db_pass = ""

    # Соль для генерации хэша
    SECRET_KEY = '2$ViplzPm935vjRFCyPmdw$nxEHZPlwdmezZgQxYyRegVym6AJDauWC365NTY'
    salt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTQxMjA2MiwianRpIjoiMzBjOTc0YTEtNmQ4NS00ZDZjLWEwOTItMjYxODAzNTFmYmY0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjIxNDEyMDYyLCJleHAiOjE2MjM0ODU2NjJ9.k-nY9DmNeE2W3paQCiOxT6YKbcEZo5breesRB1ZOGmk"

    # Разрешенные адреса для подключения к API
    CORS_ALLOWED_ORIGINS = ['http://10.170.1.120:8080']
	
