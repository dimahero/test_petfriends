from api import PetFriends
from settings import valid_email, valid_password
import pytest
import os

pf = PetFriends()


# Новые тесты
def test_get_api_key_with_invalid_password(email=valid_email, password='invalid'):
    """ Проверяем что запрос api ключа с неверным паролем возвращает статус 403"""

    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_invalid_key():
    """ Проверяем что запрос всех питомцев с неверным api ключом возвращает статус 403"""

    auth_key = {'key': 'invalid_key'}
    status, _ = pf.get_list_of_pets(auth_key)
    assert status == 403


def test_add_new_pet_with_empty_data(name='', animal_type='', age='', pet_photo='images/cat1.jpg'):
    """ Проверяем что нельзя добавить питомца с пустыми данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if not os.path.exists(pet_photo):
        raise FileNotFoundError(f"File {pet_photo} not found.")

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200


def test_delete_nonexistent_pet():
    """ Проверяем что нельзя удалить несуществующего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'invalid_id'
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 404


def test_update_pet_with_invalid_age(name='Барсик', animal_type='кот', age=-1):
    """ Проверяем что нельзя обновить питомца некорректным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, _ = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status != 200
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_with_large_age(name='Барсик', animal_type='кот', age='1000', pet_photo='images/cat1.jpg'):
    """ Проверяем что нельзя добавить питомца с некорректно большим возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200


def test_add_pet_with_invalid_photo_format(name='Бублик', animal_type='котяра', age='5',
                                           invalid_photo='images/cat1.txt'):
    """ Проверяем добавление питомца с некорректным форматом фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), invalid_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status != 200, f"Ожидался статус отличный от 200, получен статус {status}"

    except Exception as e:
        pytest.fail(f"Ошибка при попытке добавления питомца: {e}")

def test_add_pet_with_invalid_photo_russian_format(name='Бублик', animal_type='котяра', age='5',
                                           invalid_photo='images/кот.jpg'):
    """ Проверяем добавление питомца с фото - название на русском языке"""

    pet_photo = os.path.join(os.path.dirname(__file__), invalid_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200

    except Exception as e:
        pytest.fail(f"Ошибка при попытке добавления питомца: {e}")

def test_get_all_pets_with_filter_my_pets():
    """ Проверяем что запрос своих питомцев возвращает не пустой список"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert status == 200
    assert len(result['pets']) > 0


def test_get_api_key_with_empty_email(email='', password=valid_password):
    """ Проверяем что запрос api ключа с пустым email возвращает статус 403"""

    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_with_empty_password(email=valid_email, password=''):
    """ Проверяем что запрос api ключа с пустым паролем возвращает статус 403"""

    status, _ = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pet_without_photo(name='Барсик', animal_type='кот', age='4'):
    """ Проверяем что можно добавить питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age