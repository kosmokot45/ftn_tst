change views

POST /products — получение товаров по категории,
GET /product — получение карточки конкретного товара. У товара должно быть название описание, картинка, цена, характеристики. Также необходимо иметь возможность фильтровать и сортировать по цене (не менее заданного значения и не более заданного значения).
GET /categories - возвращение списка категорий. У категорий может быть несколько уровней вложенности.
GET, POST, PUT, DELETE  /cart — для получения, добавления, изменения и удаления товаров в корзине, пользователь может получить только свою корзину,
POST /order— создание заказа. Заказ должен сохранится в бд. После вызова эндпоинта корзина должна быть очищена.