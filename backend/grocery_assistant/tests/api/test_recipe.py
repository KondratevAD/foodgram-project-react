import constants as const
import constants_url as const_url
import pytest
from recipes.models import Favorite, Recipe


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
        assert ('count' and 'next' and 'previous') in test_data, (
            'Проверьте, что при GET запросе на `/api/recipes/` '
            'применена пагинация'
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

    @pytest.mark.django_db(transaction=True)
    def test_recipe_create(self, user, user_client, client, ingredient, tag):
        recipe_count = Recipe.objects.count()

        data = {}
        response = user_client.post(const_url.recipes, data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/recipes/` с не '
            'правильными данными возвращается статус 400'
        )
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 150}],
            "tags": [tag.id],
            "image": const.image,
            "name": const.name_recipe,
            "text": const.text_recipe,
            "cooking_time": const.cooking_time
        }

        response = client.post(
            const_url.recipes,
            data=data,
            format='json'
        )
        assert response.status_code == 401, (
            'Проверьте, что POST запрос на `/api/recipes/` с правильными '
            'данными не доступен для неавторизованного пользователя'
        )

        response = user_client.post(
            const_url.recipes,
            data=data,
            format='json'
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/recipes/` с правильными '
            'данными возвращается статус 201'
        )

        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на `/api/recipes/` возвращается '
            'словарь с данными нового рецепта'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('name') == data['name'], msg_error
        assert test_data.get('text') == data['text'], msg_error
        assert test_data.get('author')['username'] == user.username, (
            'Проверьте, что при POST запросе на `/api/recipes/` создается '
            'рецепт от авторизованного пользователя'
        )
        assert recipe_count + 1 == Recipe.objects.count(), (
            'Проверьте, что при POST запросе на `/api/recipes/` создается '
            'статья'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_get_current(self, client, user_client, recipe):
        response = user_client.get(f'{const_url.recipes}{recipe.id}/')

        assert response.status_code == 200, (
            'Страница `/api/recipes/{id}/` не найдена, проверьте этот адрес '
            'в *urls.py*'
        )
        response = client.get(f'{const_url.recipes}{recipe.id}/')

        assert response.status_code == 200, (
            'Проверьте, что GET запрос на `/api/recipes/{id}/` доступен '
            'неавторизованному пользователю'
        )

        test_data = response.json()
        assert test_data.get('name') == recipe.name, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/` возвращаете '
            'данные сериализатора, не найдено/не правильное значение `name`'
        )
        assert test_data.get('author')['username'] == recipe.author.username, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/` возвращаете '
            'данные сериализатора, не найдено или не правильное значение '
            '`author`, должно возвращать имя пользователя '
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_put_current(
            self,
            user_client,
            recipe,
            ingredient,
            tag,
            another_recipe
    ):
        data = {
            "ingredients": [{"id": ingredient.id, "amount": 150}],
            "tags": [tag.id],
            "image": const.image,
            "name": "Поменяли название рецепта",
            "text": const.text_recipe,
            "cooking_time": const.cooking_time
        }
        response = user_client.put(
            f'{const_url.recipes}{recipe.id}/',
            data=data,
            format='json'
        )
        assert response.status_code == 200, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` возвращаете '
            'статус 200'
        )

        test_recipe = Recipe.objects.filter(id=recipe.id).first()

        assert test_recipe, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` вы не '
            'удалили рецепт'
        )

        assert test_recipe.name == 'Поменяли название рецепта', (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` вы изменяете '
            'название рецепта'
        )

        response = user_client.put(
            f'{const_url.recipes}{another_recipe.id}/',
            data=data,
            format='json'
        )

        assert response.status_code == 403, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` для не своего'
            ' рецепта возвращаете статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_delete_current(self, user_client, recipe, another_recipe):
        response = user_client.delete(f'{const_url.recipes}{recipe.id}/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/` '
            'возвращаете статус 204'
        )

        test_recipe = Recipe.objects.filter(id=recipe.id).first()

        assert not test_recipe, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/` вы '
            'удалили рецепт'
        )

        response = user_client.delete(
            f'{const_url.recipes}{another_recipe.id}/'
        )

        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/` для не '
            'своего рецепта возвращаете статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_favorite(self, user_client, user, recipe):
        response = user_client.get(f'/api/recipes/{recipe.id}/favorite/')

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` '
            'возвращаете статус 200'
        )

        favorite = Favorite.objects.filter(user_id=user.id, recipe=recipe)
        assert favorite[0].favorite is True, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` '
            'рецепт добавляется в избранное'
        )

        response = user_client.delete(f'/api/recipes/{recipe.id}/favorite/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` '
            'возвращаете статус 204'
        )
        assert favorite[0].favorite is False, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` '
            'рецепт удаляется из избранного'
        )

    def test_recipe_shopping_cart(self, user_client, user, recipe):
        response = user_client.get(f'/api/recipes/{recipe.id}/shopping_cart/')

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` '
            'возвращаете статус 200'
        )

        favorite = Favorite.objects.filter(user_id=user.id, recipe=recipe)
        assert favorite[0].shopping_cart is True, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` '
            'рецепт добавляется в корзину покупок'
        )

        response = user_client.delete(f'/api/recipes/{recipe.id}/shopping_cart/')

        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` '
            'возвращаете статус 204'
        )
        assert favorite[0].shopping_cart is False, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` '
            'рецепт удаляется из корзины покупок'
        )