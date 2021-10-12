from django.test import TestCase
from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from tests import constants


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.get_verbose_name_recipe = Recipe._meta.get_field
        cls.get_verbose_name_tag = Tag._meta.get_field
        cls.get_verbose_name_ingredient = Ingredient._meta.get_field
        cls.get_verbose_name_recipeingredient = (
            RecipeIngredient._meta.get_field
        )
        cls.get_verbose_name_favorite = Favorite._meta.get_field
        cls.get_verbose_name_follow = Follow._meta.get_field

    def test_verbose_name_recipe(self):
        """verbose_name в полях Recipe совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Recipe.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_recipe(value).verbose_name,
                    expected
                )

    def test_help_text_recipe(self):
        """help_text в полях Recipe совпадает с ожидаемым."""
        for value, expected in constants.field_help_texts_Recipe.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_recipe(value).help_text,
                    expected
                )

    def test_verbose_name_tag(self):
        """verbose_name в полях Tag совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Tag.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_tag(value).verbose_name,
                    expected
                )

    def test_help_text_tag(self):
        """help_text в полях Tag совпадает с ожидаемым."""
        for value, expected in constants.field_help_texts_Tag.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_tag(value).help_text,
                    expected
                )

    def test_verbose_name_ingredient(self):
        """verbose_name в полях Ingredient совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Ingredient.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_ingredient(value).verbose_name,
                    expected
                )

    def test_help_text_ingredient(self):
        """help_text в полях Ingredient совпадает с ожидаемым."""
        for value, expected in constants.field_help_texts_Ingredient.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_ingredient(value).help_text,
                    expected
                )

    def test_verbose_name_recipe_ingredient(self):
        """verbose_name в полях RecipeIngredient совпадает с ожидаемым."""
        for value, expected in (
                constants.field_verboses_RecipeIngredient.items()
        ):
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_recipeingredient(value).verbose_name,
                    expected
                )

    def test_help_text_recipe_ingredient(self):
        """help_text в полях RecipeIngredient совпадает с ожидаемым."""
        for value, expected in (
                constants.field_help_texts_RecipeIngredient.items()
        ):
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_recipeingredient(value).help_text,
                    expected
                )

    def test_verbose_name_favorite(self):
        """verbose_name в полях Favorite совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Favorite.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_favorite(value).verbose_name,
                    expected
                )

    def test_verbose_name_follow(self):
        """verbose_name в полях Follow совпадает с ожидаемым."""
        for value, expected in constants.field_verboses_Follow.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_follow(value).verbose_name,
                    expected
                )
