import configuration
import requests
import data


def post_new_user(body):  # Запрос на создание нового пользователя
    return requests.post(configuration.URL_SERVICE + configuration.MAIN_USER,  # подставляем полный url
                         json=body,  # здесь тело запроса
                         headers=data.headers)  # здесь вставляем headers


def post_new_client_kit(kit_body, headers_kit):  # Запрос на создание набора у пользователя
    return requests.post(configuration.URL_SERVICE + configuration.MAIN_KITS,  # подставляем полный url
                         json=kit_body,  # здесь тело запроса
                         headers=headers_kit)  # здесь вставляем headers
