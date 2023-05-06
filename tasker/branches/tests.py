from django.test import TestCase
from .models import Branch


class BranchTestCase(TestCase):
    """
    Тесты для модели Branch.
    """

    def setUp(self):
        """
        Создает тестовые объекты модели Branch.
        """
        Branch.objects.create(city="Москва", longitude=37.6173, latitude=55.7558)
        Branch.objects.create(city="Санкт-Петербург")

    def test_branch_str_method(self):
        """
        Проверяет правильность работы метода __str__ модели Branch.
        """
        moscow_branch = Branch.objects.get(city="Москва")
        spb_branch = Branch.objects.get(city="Санкт-Петербург")

        self.assertEqual(str(moscow_branch), "Москва")
        self.assertEqual(str(spb_branch), "Санкт-Петербург")

    def test_branch_get_location_method(self):
        """
        Проверяет правильность работы метода get_location модели Branch.
        """
        moscow_branch = Branch.objects.get(city="Москва")
        spb_branch = Branch.objects.get(city="Санкт-Петербург")

        # Проверяем правильность возвращаемых значений при наличии координат
        self.assertEqual(moscow_branch.get_location(), [37.6173, 55.7558])

        # Проверяем правильность возвращаемых значений при отсутствии координат
        self.assertEqual(spb_branch.get_location(), "[55.7522,37.6156]")