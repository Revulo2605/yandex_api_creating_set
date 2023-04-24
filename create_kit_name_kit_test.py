import sender_stand_request
import data


# Функция на проверку headers_kit на наличие сгенерированного токена пользователя
def get_user_token():
    if data.headers_kit["Authorization"] != "":
        return  # Если токен есть, то пропуск генерации токена пользователя
    else:
        get_new_user_token()  # Если токена нет, то создаём токен пользователя


# Функция меняет значения у параметра name в теле запроса (kit_body) на создание набора
def get_kit_body(name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_kit_body = data.kit_body.copy()
    # изменение значения в поле name
    current_kit_body["name"] = name
    # возвращается новый словарь с нужным значением kit_body
    return current_kit_body


#  Предназначена для формирования headers с токеном пользователя (authToken)
def get_new_user_token():
    # Отправляем запрос на создание нового пользователя и копируем данные из ответа:
    user_response = sender_stand_request.post_new_user(data.user_body)
    # Формируем новые headers для запроса на создание набора:
    # 1. Копируем тело ответа в формате json:
    auth_body = user_response.json()
    # 2. Копируем из тела токен пользователя:
    auth_token = auth_body['authToken']
    # 3. Переписываем параметр Authorization в headers у файла data в формате Bearer {authToken}:
    data.headers_kit[
        "Authorization"] = "Bearer " + auth_token


# Функция для позитивной проверки
def positive_assert(name):
    # В переменную kit_body сохраняется обновленное тело запроса:
    kit_body = get_kit_body(name)
    # Получаем токен пользователя:
    get_user_token()
    # Проверяем наличие созданного пользователя:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, data.headers_kit)
    # Проверяется, что код ответа равен 201:
    assert kit_response.status_code == 201
    # Проверяется, что в ответе есть поле name, и оно равно тому, что было задано в запросе:
    assert kit_response.json()["name"] == name


# Функция для негативной проверки
def negative_assert_400(kit_body):
    # Получаем токен пользователя:
    get_user_token()
    # В переменную kit_response сохраняется результат запроса на создание набора у пользователя:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, data.headers_kit)

    # Проверяется, что код ответа равен 400:
    assert kit_response.status_code == 400


# Тест 1. Успешное создание набора
# Параметр name состоит из 1 символа
def test_create_kit_1_letter_in_name_get_success_response():
    positive_assert("а")


# Тест 2. Успешное создание набора
# Параметр name состоит из 511 символов
def test_create_kit_511_letter_in_name_get_success_response():
    # Зададим новый параметр name
    name = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC"
    positive_assert(name)


# Тест 3. Ошибка
# Параметр name состоит из 0 символов
def test_create_kit_0_letter_in_name_get_error_response():
    # В переменную kit_body сохраняется обновленное тело запроса:
    kit_body = get_kit_body("")
    negative_assert_400(kit_body)


# Тест 4. Ошибка
# Параметр name состоит из 512 символов
def test_create_kit_512_letter_in_name_get_error_response():
    # Зададим новый параметр name
    name = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    # В переменную kit_body сохраняется обновленное тело запроса:
    kit_body = get_kit_body(name)
    # Вызовем функцию на негативную проверку с кодом 400:
    negative_assert_400(kit_body)


# Тест 5. Успешное создание набора
# Параметр name состоит из английских букв
def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert("QWErty")


# Тест 6. Успешное создание набора
# Параметр name состоит из русских букв
def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert("Мария")


# Тест 7. Успешное создание набора
# Параметр name состоит из спецсимволов
def test_create_kit_special_symbol_in_name_get_success_response():
    positive_assert("\"№%@\",")


# Тест 8. Успешное создание набора
# Параметр name состоит из слов с пробелами
def test_create_kit_has_space_in_name_get_success_response():
    positive_assert(" Человек и КО ")


# Тест 9. Успешное создание набора
# Параметр name состоит из цифр
def test_create_kit_has_number_in_name_get_success_response():
    positive_assert("123")


# Тест 10. Ошибка
# Параметр name не передан в запросе
def test_create_kit_no_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную kit_body
    # Иначе можно потерять данные из исходного словаря
    kit_body = data.kit_body.copy()
    # Удаление параметра firstName из запроса
    kit_body.pop("name")
    # Вызовем функцию на негативную проверку с кодом 400:
    negative_assert_400(kit_body)


# Тест 11. Ошибка
# Тип параметра name: число
def test_create_kit_number_type_name_get_error_response():
    # Зададим новый параметр name
    name = 123
    # В переменную kit_body сохраняется обновленное тело запроса:
    kit_body = get_kit_body(name)
    # Вызовем функцию на негативную проверку с кодом 400:
    negative_assert_400(kit_body)
