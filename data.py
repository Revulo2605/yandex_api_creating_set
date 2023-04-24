# headers для создания пользователя
headers = {
    "Content-Type": "application/json"
}


# Тело запроса на создание пользователя. В теле минимум данных
user_body = {
    "firstName": "Анатолий",
    "phone": "+79995553322",
    "address": "г. Москва, ул. Пушкина, д. 10"
}


# headers для тестирования создания набора у пользователя
headers_kit = {
    "Content-Type": "application/json",
    "Authorization": ""
}

# Тело запроса на создание набора у пользователя
kit_body = {
    "name": ""
}
