# User
username = 'TestUser'
email = 'Test@email.ru',
# User2
username2 = 'TestUser2'
email2 = 'Test2@mail.ru'
# User3
username3 = 'TestUser3'
email3 = 'Test3@mail.ru'
password3 = '567891548358'
first_name = 'Test'
last_name = 'User'

# ------ Users -------


# ------ Recipes -------

# Recipe
name_recipe = 'Рецепт'
text_recipe = 'Описание рецепта'
cooking_time = 120
image = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg=='
field_verboses_Recipe = {
    'name': 'Рецепт',
    'text': 'Описание рецепта',
    'author': 'Автор',
    'image': 'Изображение',
    'ingredients': 'Ингредиенты',
    'tags': 'Тег',
    'cooking_time': 'Время приготовления',
    'pub_date': 'Дата создания'
}
field_help_texts_Recipe = {
    'name': 'Название рецепта',
    'text': 'Описание рецепта',
    'image': 'Изображение',
    'ingredients': 'Ингредиенты',
    'tags': 'Тег',
    'cooking_time': 'Время приготовления в минутах',
}

# Tag
name_tag = 'Тег'
color = '#52EB15'
slug = 'Tag'
field_verboses_Tag = {
    'name': 'Тэг',
    'slug': 'slug'
}
field_help_texts_Tag = {
    'name': 'Название тега',
    'slug': 'Slug тега'
}

# Ingredient
name_ingredient = 'Ингредиент'
measurement_unit = 50
field_verboses_Ingredient = {
    'name': 'Ингредиент',
    'measurement_unit': 'Единицы измерения'
}
field_help_texts_Ingredient = {
    'name': 'Название ингредиента',
    'measurement_unit': 'Единицы измерения ингредиента'
}

# RecipeIngredient
amount = 50
field_verboses_RecipeIngredient = {
    'ingredient': 'Ингредиент рецепта',
    'amount': 'Количество'
}
field_help_texts_RecipeIngredient = {
    'ingredient': 'Ингредиент рецепта',
    'amount': 'Количество ингредиента'
}

# Favorite
field_verboses_Favorite = {
    'user': 'Пользователь',
    'recipe': 'Рецепт',
    'shopping_cart': 'Корзина покупок',
    'favorite': 'Избранное',
}

# Follow
field_verboses_Follow = {
    'user': 'Подписчик',
    'author': 'Подписант'
}
