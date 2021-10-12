import constants as const
import constants_url as const_url
import pytest
from recipes.models import Recipe


class TestUserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_recipe_not_found(self, client):
        response = client.get(const_url.recipes)

        assert response.status_code != 404, (
            'Страница `/api/recipes/` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_not_auth(self, client):
        response = client.get(const_url.recipes)

        assert response.status_code == 200, (
            'Проверьте, что `/api/recipes/` доступен для чтения '
            'неавторизованному пользователю'
        )
        assert response.status_code != 500, (
            'Проверьте, что `/api/recipes/` не вызывает ошибок '
            'на стороне сервера'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_auth_get(self, user_client, recipe):
        response = user_client.get(const_url.recipes)
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/` с токеном '
            'авторизации возвращается статус 200'
        )

        test_data = response.json()
        assert type(test_data) == dict, (
            'Проверьте, что при GET запросе на `/api/recipes/` '
            'возвращается словарь'
        )

        assert len(test_data['results']) == Recipe.objects.count(), (
            'Проверьте, что при GET запросе на `/api/recipes/` возвращается '
            'весь список рецептов'
        )

        data_recipe = test_data['results'][0]

        assert 'id' in data_recipe, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'tags' in data_recipe, (
            'Проверьте, что добавили `tags` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'author' in data_recipe, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'ingredients' in data_recipe, (
            'Проверьте, что добавили `ingredients` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'is_favorited' in data_recipe, (
            'Проверьте, что добавили `is_favorited` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'is_in_shopping_cart' in data_recipe, (
            'Проверьте, что добавили `is_in_shopping_cart` в список полей '
            '`fields` сериализатора модели Recipe'
        )
        assert 'name' in data_recipe, (
            'Проверьте, что добавили `name` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'image' in data_recipe, (
            'Проверьте, что добавили `image` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'text' in data_recipe, (
            'Проверьте, что добавили `text` в список полей `fields` '
            'сериализатора модели Recipe'
        )
        assert 'cooking_time' in data_recipe, (
            'Проверьте, что добавили `cooking_time` в список полей `fields` '
            'сериализатора модели Recipe'
        )
