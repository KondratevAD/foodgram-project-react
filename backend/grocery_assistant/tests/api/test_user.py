import constants_url as const_url
import constants as const
import pytest
from users.models import User


class TestUserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_users_not_found(self, client):
        response = client.get(const_url.users)

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_not_auth(self, client):
        response = client.get(const_url.users)

        assert response.status_code == 200, (
            'Проверьте, что `/api/users/` доступен для чтения '
            'неавторизованному пользователю'
        )
        assert response.status_code != 500, (
            'Проверьте, что `/api/users/` не вызывает ошибок '
            'на стороне сервера'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_auth_get(self, user_client):
        response = user_client.get(const_url.users)
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/` с токеном '
            'авторизации возвращаетсся статус 200'
        )

        test_data = response.json()
        assert type(test_data) == dict, (
            'Проверьте, что при GET запросе на `/api/users/` '
            'возвращается словарь'
        )

        assert len(test_data['results']) == User.objects.count(), (
            'Проверьте, что при GET запросе на `/api/users/` возвращается весь'
            ' список пользователей'
        )
        data_user = test_data['results'][0]

        assert 'email' in data_user, (
            'Проверьте, что добавили `email` в список полей `fields` '
            'сериализатора модели User'
        )
        assert 'id' in data_user, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели User'
        )
        assert 'username' in data_user, (
            'Проверьте, что добавили `username` в список полей `fields` '
            'сериализатора модели User'
        )
        assert 'first_name' in data_user, (
            'Проверьте, что добавили `first_name` в список полей `fields` '
            'сериализатора модели User'
        )
        assert 'last_name' in data_user, (
            'Проверьте, что добавили `last_name` в список полей `fields` '
            'сериализатора модели User'
        )
        assert 'is_subscribed' in data_user, (
            'Проверьте, что добавили `is_subscribed` в список полей `fields` '
            'сериализатора модели User'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_create(self, client):
        user_count = User.objects.count()

        data = {}
        response = client.post(const_url.users, data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/users/` с не правильными'
            ' данными возвращается статус 400'
        )

        data = {
            'username': const.username3,
            'email': const.email3,
            'password': const.password3,
            'first_name': const.first_name,
            'last_name': const.last_name
        }
        response = client.post(const_url.users, data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/users/` с правильными '
            'данными возвращается статус 201'
        )

        test_data = response.json()

        msg_error = (
            'Проверьте, что при POST запросе на `/api/users/` возвращается '
            'словарь с данными нового пользователя'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('username') == data['username'], msg_error

        assert user_count + 1 == User.objects.count(), (
            'Проверьте, что при POST запросе на `/api/users/` создается '
            'новый пользователь'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_get_current(self, user_client, user):
        response = user_client.get(f'{const_url.users}{user.id}/')

        assert response.status_code == 200, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес '
            'в *urls.py*'
        )

        test_data = response.json()
        assert test_data.get('username') == user.username, (
            'Проверьте, что при GET запросе `/api/users/{id}/` возвращаете '
            'данные сериализатора, не найдено или не правильное '
            'значение `username`'
        )
        assert test_data.get('email') == user.email, (
            'Проверьте, что при GET запросе `/api/users/{id}/` возвращаете '
            'данные сериализатора, не найдено или не правильное значение'
            ' `email`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_me(self, user_client, user):
        response = user_client.get(const_url.users_me)
        test_data = response.json()

        assert test_data.get('username') == user.username, (
            'Проверьте, что при GET запросе `//api/users/me/` возвращаете '
            'данные сериализатора, не найдено или не правильное значение'
            ' `username`'
        )
