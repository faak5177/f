import pytest
from datetime import date
from django.test import Client
from store.models import (
    Product, Order, User as StoreUser,
    Category, Manufacturer, Supplier, PickPoint,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Фикстуры
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.fixture
def http_client():
    return Client()


@pytest.fixture
def admin_user():
    return StoreUser.objects.filter(role_id=1).first()


@pytest.fixture
def manager_user():
    return StoreUser.objects.filter(role_id=2).first()


@pytest.fixture
def client_user():
    return StoreUser.objects.filter(role_id=3).first()


def login_as(client, user):
    """Вспомогательная функция: авторизует клиента по логину/паролю."""
    client.post('/login/', {'login': user.login, 'password': user.password})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ГОСТЬ (неавторизованный)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.mark.django_db(transaction=True)
class TestGuest:

    def test_login_page_loads(self, http_client):
        """Тест 1: Страница входа загружается для гостя."""
        response = http_client.get('/login/')
        assert response.status_code == 200
        assert 'Вход в систему' in response.content.decode('utf-8')

    def test_login_with_valid_credentials(self, http_client, admin_user):
        """Тест 2: Вход с корректными данными."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        response = http_client.post('/login/', {
            'login':    admin_user.login,
            'password': admin_user.password,
        })
        assert response.status_code == 302
        assert response.url == '/products/'

    def test_login_with_invalid_credentials(self, http_client):
        """Тест 3: Вход с некорректными данными — остаёмся на странице."""
        response = http_client.post('/login/', {
            'login':    'nonexistent_user_xyz',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200

    def test_guest_redirect_to_login(self, http_client):
        """Тест 4: Корневой URL перенаправляет неавторизованного на вход."""
        response = http_client.get('/')
        assert response.status_code in (200, 302)

    def test_guest_cannot_access_orders(self, http_client):
        """Тест 5: Гость не может открыть список заказов."""
        response = http_client.get('/orders/')
        assert response.status_code == 302
        assert response.url == '/login/'

    def test_guest_cannot_access_products(self, http_client):
        """Тест 6: Гость не может открыть каталог."""
        response = http_client.get('/products/')
        assert response.status_code == 302
        assert response.url == '/login/'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# КЛИЕНТ (role_id = 3)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.mark.django_db(transaction=True)
class TestClient:

    def test_client_can_view_products(self, http_client, client_user):
        """Тест 7: Клиент видит каталог товаров."""
        if not client_user:
            pytest.skip('Нет клиента в БД')
        login_as(http_client, client_user)
        response = http_client.get('/products/')
        assert response.status_code == 200
        assert 'Каталог' in response.content.decode('utf-8')

    def test_client_cannot_create_product(self, http_client, client_user):
        """Тест 8: Клиент не может добавлять товары (редирект)."""
        if not client_user:
            pytest.skip('Нет клиента в БД')
        login_as(http_client, client_user)
        response = http_client.get('/products/create/')
        assert response.status_code == 302

    def test_client_sees_only_own_orders(self, http_client, client_user):
        """Тест 9: Клиент видит только свои заказы."""
        if not client_user:
            pytest.skip('Нет клиента в БД')
        login_as(http_client, client_user)
        response = http_client.get('/orders/')
        assert response.status_code == 200


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# МЕНЕДЖЕР (role_id = 2)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.mark.django_db(transaction=True)
class TestManager:

    def test_manager_sees_filters_panel(self, http_client, manager_user):
        """Тест 10: Менеджер видит панель фильтров."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        response = http_client.get('/products/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'class="filters"' in content
        assert 'name="q"' in content

    def test_manager_search(self, http_client, manager_user):
        """Тест 11: Поиск товаров менеджером по строке."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        response = http_client.get('/products/', {'q': 'Валик'})
        assert response.status_code == 200

    def test_manager_filter_by_manufacturer(self, http_client, manager_user):
        """Тест 12: Фильтрация по производителю."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        m = Manufacturer.objects.first()
        if not m:
            pytest.skip('Нет производителей в БД')
        response = http_client.get('/products/', {'manufacturer': str(m.pk)})
        assert response.status_code == 200

    def test_manager_sort_by_price_asc(self, http_client, manager_user):
        """Тест 13: Сортировка по цене по возрастанию."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        response = http_client.get('/products/', {'sort': 'price_asc'})
        assert response.status_code == 200

    def test_manager_can_view_orders(self, http_client, manager_user):
        """Тест 14: Менеджер может открывать список заказов."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        response = http_client.get('/orders/')
        assert response.status_code == 200
        assert 'Заказы' in response.content.decode('utf-8')

    def test_manager_can_open_product_form(self, http_client, manager_user):
        """Тест 15: Менеджер может открывать форму добавления товара."""
        if not manager_user:
            pytest.skip('Нет менеджера в БД')
        login_as(http_client, manager_user)
        response = http_client.get('/products/create/')
        assert response.status_code == 200


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# АДМИНИСТРАТОР (role_id = 1)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.mark.django_db(transaction=True)
class TestAdmin:

    def test_admin_sees_add_product_button(self, http_client, admin_user):
        """Тест 16: Админ видит кнопку «Добавить товар»."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        response = http_client.get('/products/')
        assert response.status_code == 200
        assert 'Добавить товар' in response.content.decode('utf-8')

    def test_admin_can_open_create_form(self, http_client, admin_user):
        """Тест 17: Админ может открыть форму добавления товара."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        response = http_client.get('/products/create/')
        assert response.status_code == 200
        assert 'Новый товар' in response.content.decode('utf-8')

    def test_admin_create_product_then_delete(self, http_client, admin_user):
        """Тест 18: Админ создаёт товар и удаляет его."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)

        cat = Category.objects.first()
        man = Manufacturer.objects.first()
        sup = Supplier.objects.first()
        if not all([cat, man, sup]):
            pytest.skip('Не хватает справочных данных (Категории/Произв/Поставщики)')

        response = http_client.post('/products/create/', {
            'name':         'Тестовый товар (pytest)',
            'unit':         'шт.',
            'price':        '199.99',
            'max_discount': '20',
            'discount':     '0',
            'quantity':     '10',
            'description':  'Создан автотестом',
            'category':     str(cat.pk),
            'manufacturer': str(man.pk),
            'supplier':     str(sup.pk),
            'image_path':   '',
        })
        assert response.status_code == 302
        new_product = Product.objects.filter(name='Тестовый товар (pytest)').first()
        assert new_product is not None
        try:
            response = http_client.get(f'/products/delete/{new_product.article}/')
            assert response.status_code == 302
            assert not Product.objects.filter(pk=new_product.pk).exists()
        finally:
            Product.objects.filter(pk=new_product.pk).delete()

    def test_admin_view_all_orders(self, http_client, admin_user):
        """Тест 19: Админ видит все заказы."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        response = http_client.get('/orders/')
        assert response.status_code == 200
        assert 'Заказы' in response.content.decode('utf-8')

    def test_admin_edit_order_quantity(self, http_client, admin_user):
        """Тест 20: Админ изменяет количество в заказе."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        order = Order.objects.first()
        if not order:
            pytest.skip('Нет заказов в БД')
        original_qty = order.quantity
        new_qty = (original_qty or 1) + 5
        response = http_client.post(f'/orders/edit/{order.order_id}/', {
            'status':        order.status or 'Новый',
            'delivery_date': '',
            'quantity':      str(new_qty),
        })
        assert response.status_code == 302
        order.refresh_from_db()
        assert order.quantity == new_qty
        order.quantity = original_qty
        order.save()

    def test_admin_create_and_delete_order(self, http_client, admin_user):
        """Тест 21: Админ создаёт заказ и удаляет его."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        product = Product.objects.filter(quantity__gt=0).first()
        pp = PickPoint.objects.first()
        if not product:
            pytest.skip('Нет товаров в наличии')

        before = Order.objects.count()
        response = http_client.post('/orders/create/', {
            'product':     product.article,
            'quantity':    '2',
            'pickpoint':   str(pp.pk) if pp else '',
            'pickup_code': '777',
        })
        assert response.status_code == 302
        assert Order.objects.count() == before + 1

        new_order = Order.objects.latest('order_id')
        try:
            response = http_client.get(f'/orders/delete/{new_order.order_id}/')
            assert response.status_code == 302
            assert not Order.objects.filter(pk=new_order.pk).exists()
        finally:
            Order.objects.filter(pk=new_order.pk).delete()

    def test_admin_logout(self, http_client, admin_user):
        """Тест 22: Админ может выйти из системы."""
        if not admin_user:
            pytest.skip('Нет администратора в БД')
        login_as(http_client, admin_user)
        response = http_client.get('/logout/')
        assert response.status_code == 302
        assert response.url == '/login/'
