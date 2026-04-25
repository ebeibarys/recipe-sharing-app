import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Category, Recipe, Comment, Like, SavedRecipe
from rest_framework.authtoken.models import Token

print("="*70)
print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ - ТОЛЬКО ВАШИ ФОТО")
print("="*70)

# 1. КАТЕГОРИИ
print("\n1. КАТЕГОРИИ:")
categories_data = [
    'Завтрак', 'Обед', 'Ужин', 'Десерт', 
    'Суп', 'Салат', 'Закуски', 'Выпечка', 
    'Напитки', 'Мясное', 'Рыбное'
]

categories = {}
for name in categories_data:
    cat, _ = Category.objects.get_or_create(name=name)
    categories[name] = cat
    print(f"  ✓ {name}")

# 2. ПОЛЬЗОВАТЕЛИ
print("\n2. ПОЛЬЗОВАТЕЛИ:")
users_data = [
    ('chef_artem', 'Артем'),
    ('chef_maria', 'Мария'),
    ('chef_ivan', 'Иван'),
    ('chef_elena', 'Елена'),
    ('chef_dmitry', 'Дмитрий'),
]

users = []
for username, name in users_data:
    user, _ = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com', 'first_name': name})
    if _:
        user.set_password('123456')
        user.save()
    users.append(user)
    Token.objects.get_or_create(user=user)
    print(f"  ✓ {username} (пароль: 123456)")

print("\n" + "="*70)
print("⚠️ ВСТАВЬТЕ ВАШИ ССЫЛКИ НА ФОТО ВМЕСТО 'ВАША_ССЫЛКА_X'")
print("="*70)

all_recipes = []

# === ЗАВТРАК (5) ===
print("\n📸 [ЗАВТРАК] Вставьте ваши ссылки:")
breakfast_recipes = [
    {'title': 'Сырники классические', 'desc': 'Нежные творожные сырники', 'time': 25, 'serv': 4, 'diff': 'easy', 'ingredients': 'Творог 500г, Яйца 2шт, Мука 100г, Сахар 50г', 'instructions': '1. Смешать ингредиенты\n2. Сформировать сырники\n3. Обжарить до золотистой корочки', 'image': 'https://s1.eda.ru/StaticContent/Photos/0/02/0025db869a0b4ceca1542f2895a5fdb5.jpg'},  # ← ВАША ССЫЛКА
    {'title': 'Овсяная каша с ягодами', 'desc': 'Полезный завтрак', 'time': 15, 'serv': 2, 'diff': 'easy', 'ingredients': 'Овсянка 100г, Молоко 400мл, Ягоды 150г, Мед', 'instructions': '1. Вскипятить молоко\n2. Добавить овсянку\n3. Варить 5 минут\n4. Добавить ягоды и мед', 'image': 'https://media.istockphoto.com/id/686045026/ru/фото/здоровая-органическая-каша-с-ягодами.jpg?s=612x612&w=0&k=20&c=71bCmsnDLREHfajcZP89SSJ-g0MJ-CJ8eWORyRVT2JA='},  # ← ВАША ССЫЛКА
    {'title': 'Панкейки пышные', 'desc': 'Американские блинчики', 'time': 30, 'serv': 4, 'diff': 'easy', 'ingredients': 'Мука 200г, Молоко 200мл, Яйца 2шт, Сахар 2ст.л', 'instructions': '1. Смешать ингредиенты\n2. Жарить на сухой сковороде\n3. Подавать с сиропом', 'image': 'https://i.pinimg.com/736x/c6/0b/ab/c60bab29276171a8e93d35cb169699b7.jpg'},  # ← ВАША ССЫЛКА
    {'title': 'Омлет с сыром', 'desc': 'Пышный омлет', 'time': 15, 'serv': 2, 'diff': 'easy', 'ingredients': 'Яйца 4шт, Молоко 100мл, Сыр 80г', 'instructions': '1. Взбить яйца с молоком\n2. Вылить на сковороду\n3. Посыпать сыром\n4. Жарить до готовности', 'image': 'https://avatars.mds.yandex.net/i?id=1912cd480957361b23ddc3b626e94c022e92a283-5869035-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Блины на молоке', 'desc': 'Тонкие блины', 'time': 40, 'serv': 6, 'diff': 'easy', 'ingredients': 'Мука 300г, Молоко 800мл, Яйца 3шт, Сахар 2ст.л', 'instructions': '1. Взбить яйца с сахаром\n2. Добавить муку\n3. Влить молоко\n4. Жарить блины', 'image': 'https://avatars.mds.yandex.net/i?id=ecf14aaa3996a1ef09861cf25fd0416f_l-9233745-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
]

for r in breakfast_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Завтрак']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === ОБЕД (5) ===
print("\n📸 [ОБЕД] Вставьте ваши ссылки:")
lunch_recipes = [
    {'title': 'Борщ красный', 'desc': 'Наваристый украинский борщ', 'time': 120, 'serv': 8, 'diff': 'medium', 'ingredients': 'Свекла 2шт, Капуста 500г, Картофель 5шт, Морковь 2шт, Лук 2шт, Мясо 700г', 'instructions': '1. Сварить бульон\n2. Обжарить свеклу\n3. Добавить овощи\n4. Варить 30 минут', 'image': 'https://i.ytimg.com/vi/1CsVXRuoSGg/maxresdefault.jpg'},  # ← ВАША ССЫЛКА
    {'title': 'Плов с бараниной', 'desc': 'Узбекский плов', 'time': 90, 'serv': 6, 'diff': 'medium', 'ingredients': 'Рис 500г, Баранина 600г, Морковь 500г, Лук 300г, Чеснок', 'instructions': '1. Обжарить мясо\n2. Добавить лук и морковь\n3. Добавить рис и воду\n4. Томить 40 минут', 'image': 'https://cdn.food.ru/unsigned/fit/640/480/ce/0/czM6Ly9tZWRpYS9waWN0dXJlcy8yMDI0MTAxNy91QlBBM0IuanBlZw.jpg'},  # ← ВАША ССЫЛКА
    {'title': 'Щи из капусты', 'desc': 'Традиционные русские щи', 'time': 80, 'serv': 6, 'diff': 'easy', 'ingredients': 'Капуста 500г, Картофель 5шт, Морковь 1шт, Лук 1шт, Свинина 500г', 'instructions': '1. Сварить бульон\n2. Добавить капусту и картофель\n3. Добавить зажарку', 'image': 'https://avatars.mds.yandex.net/i?id=acec9633762afc07b4365d782a9315edfdbbc284-4809712-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Ленивые голубцы', 'desc': 'Быстрые голубцы', 'time': 60, 'serv': 6, 'diff': 'easy', 'ingredients': 'Фарш 600г, Капуста 400г, Рис 200г, Лук 1шт, Морковь 1шт', 'instructions': '1. Смешать фарш с рисом\n2. Добавить капусту\n3. Сформировать шарики\n4. Тушить в соусе', 'image': 'https://avatars.mds.yandex.net/i?id=e59c5c3dc4752bac10d044339698827bd57a4448-16185907-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Картофель с мясом', 'desc': 'Сытное блюдо', 'time': 60, 'serv': 4, 'diff': 'easy', 'ingredients': 'Картофель 1кг, Мясо 500г, Лук 1шт, Морковь 1шт', 'instructions': '1. Обжарить мясо\n2. Добавить лук и морковь\n3. Добавить картофель\n4. Тушить до готовности', 'image': 'https://avatars.mds.yandex.net/i?id=792d8e01814220e5bb1c81729a30b284b89a3995-5489936-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
]

for r in lunch_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Обед']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === УЖИН (5) ===
print("\n📸 [УЖИН] Вставьте ваши ссылки:")
dinner_recipes = [
    {'title': 'Паста Карбонара', 'desc': 'Классическая итальянская паста', 'time': 25, 'serv': 4, 'diff': 'easy', 'ingredients': 'Спагетти 400г, Бекон 200г, Яйца 4шт, Пармезан 100г', 'instructions': '1. Сварить спагетти\n2. Обжарить бекон\n3. Смешать яйца с сыром\n4. Соединить все', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5631834/1262162579/S600xU_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Курица карри', 'desc': 'Ароматная курица в соусе', 'time': 45, 'serv': 4, 'diff': 'medium', 'ingredients': 'Курица 600г, Сливки 200мл, Паста карри 2ст.л, Лук 1шт', 'instructions': '1. Обжарить курицу\n2. Добавить лук\n3. Добавить карри и сливки\n4. Тушить 15 минут', 'image': 'https://avatars.mds.yandex.net/i?id=54e8644611484cf1bbcbeddc03b932feb46bfe20-5878122-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Ризотто с грибами', 'desc': 'Кремовое ризотто', 'time': 40, 'serv': 4, 'diff': 'medium', 'ingredients': 'Рис 300г, Грибы 400г, Лук 1шт, Бульон 1л, Пармезан 80г', 'instructions': '1. Обжарить лук\n2. Добавить рис\n3. Постепенно добавлять бульон\n4. Добавить грибы и сыр', 'image': 'https://avatars.mds.yandex.net/i?id=f498ba440858a420717632a0d094590f6deb94be-2511007-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Мясо по-французски', 'desc': 'Свинина с сыром', 'time': 50, 'serv': 4, 'diff': 'easy', 'ingredients': 'Свинина 500г, Лук 2шт, Сыр 200г, Майонез', 'instructions': '1. Нарезать мясо\n2. Отбить\n3. Добавить лук и сыр\n4. Запекать 30 минут', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2044927/1261489401/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Стейк рибай', 'desc': 'Сочный стейк', 'time': 30, 'serv': 2, 'diff': 'medium', 'ingredients': 'Рибай 500г, Масло, Розмарин, Чеснок', 'instructions': '1. Достать мясо за час\n2. Обжарить на сильном огне\n3. Дать отдохнуть 5 минут', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2238866/1254344930/S600xU_2x'},  # ← ВАША ССЫЛКА
]

for r in dinner_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Ужин']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === ДЕСЕРТ (5) ===
print("\n📸 [ДЕСЕРТ] Вставьте ваши ссылки:")
dessert_recipes = [
    {'title': 'Тирамису', 'desc': 'Итальянский десерт', 'time': 60, 'serv': 6, 'diff': 'medium', 'ingredients': 'Маскарпоне 500г, Яйца 4шт, Сахар 100г, Кофе 300мл, Савоярди', 'instructions': '1. Взбить желтки с сахаром\n2. Добавить маскарпоне\n3. Собрать слоями\n4. Охладить 4 часа', 'image': 'https://avatars.mds.yandex.net/get-entity_search/57048/1244409329/S600xU_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Чизкейк', 'desc': 'Нежный чизкейк', 'time': 120, 'serv': 8, 'diff': 'medium', 'ingredients': 'Сыр 600г, Печенье 200г, Масло 100г, Сахар 150г, Яйца 3шт', 'instructions': '1. Сделать основу\n2. Взбить сыр с сахаром\n3. Добавить яйца\n4. Выпекать 1 час', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5103535/1245259507/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Наполеон', 'desc': 'Классический торт', 'time': 180, 'serv': 10, 'diff': 'hard', 'ingredients': 'Мука 500г, Масло 400г, Яйца 2шт, Сахар 200г, Молоко 1л', 'instructions': '1. Замесить тесто\n2. Испечь коржи\n3. Сварить крем\n4. Собрать торт', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5396454/1227746355/S600xU_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Панна котта', 'desc': 'Итальянский десерт', 'time': 30, 'serv': 4, 'diff': 'easy', 'ingredients': 'Сливки 500мл, Сахар 100г, Ваниль, Желатин 10г', 'instructions': '1. Замочить желатин\n2. Нагреть сливки\n3. Добавить желатин\n4. Охладить 4 часа', 'image': 'https://avatars.mds.yandex.net/get-entity_search/1989973/1261393483/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Шоколадный фондан', 'desc': 'Десерт с жидкой начинкой', 'time': 25, 'serv': 4, 'diff': 'medium', 'ingredients': 'Шоколад 200г, Масло 100г, Яйца 4шт, Сахар 100г, Мука 50г', 'instructions': '1. Растопить шоколад\n2. Взбить яйца с сахаром\n3. Соединить\n4. Выпекать 12 минут', 'image': 'https://avatars.mds.yandex.net/get-entity_search/10767883/1040444621/SUx182_2x'},  # ← ВАША ССЫЛКА
]

for r in dessert_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Десерт']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === СУПЫ (5) ===
print("\n📸 [СУПЫ] Вставьте ваши ссылки:")
soup_recipes = [
    {'title': 'Солянка мясная', 'desc': 'Острый суп с мясом', 'time': 90, 'serv': 6, 'diff': 'medium', 'ingredients': 'Говядина 400г, Колбаса 200г, Огурцы соленые 200г, Оливки 100г', 'instructions': '1. Сварить бульон\n2. Добавить мясо и колбасу\n3. Добавить огурцы и оливки\n4. Варить 20 минут', 'image': 'https://avatars.mds.yandex.net/get-entity_search/7759284/1248160518/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Грибной суп', 'desc': 'Нежный суп с грибами', 'time': 50, 'serv': 4, 'diff': 'easy', 'ingredients': 'Грибы 500г, Картофель 4шт, Лук 1шт, Сливки 200мл', 'instructions': '1. Обжарить грибы с луком\n2. Добавить картофель и воду\n3. Варить 30 минут\n4. Добавить сливки', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2480722/1228810979/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Уха рыбная', 'desc': 'Ароматная уха', 'time': 60, 'serv': 6, 'diff': 'easy', 'ingredients': 'Рыба 1кг, Картофель 5шт, Лук 2шт, Морковь 1шт', 'instructions': '1. Сварить бульон из рыбы\n2. Добавить картофель\n3. Добавить зажарку\n4. Варить до готовности', 'image': 'https://avatars.mds.yandex.net/i?id=8e3bf5fdafab061a0eab45da1cf56da0d0e5d36a-5578546-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Харчо', 'desc': 'Грузинский суп', 'time': 80, 'serv': 6, 'diff': 'medium', 'ingredients': 'Говядина 600г, Рис 100г, Орехи 100г, Чеснок 4зуб', 'instructions': '1. Сварить бульон\n2. Добавить рис\n3. Добавить орехи и специи\n4. Варить до готовности', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2032283/1229026036/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Тыквенный суп', 'desc': 'Яркий суп-пюре', 'time': 40, 'serv': 4, 'diff': 'easy', 'ingredients': 'Тыква 800г, Морковь 2шт, Лук 1шт, Сливки 100мл', 'instructions': '1. Обжарить овощи\n2. Добавить тыкву и воду\n3. Варить 20 минут\n4. Взбить блендером', 'image': 'https://avatars.mds.yandex.net/get-entity_search/6454749/1244946224/SUx182_2x'},  # ← ВАША ССЫЛКА
]

for r in soup_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Суп']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === САЛАТЫ (5) ===
print("\n📸 [САЛАТЫ] Вставьте ваши ссылки:")
salad_recipes = [
    {'title': 'Цезарь с курицей', 'desc': 'Хрустящий салат', 'time': 25, 'serv': 4, 'diff': 'easy', 'ingredients': 'Курица 400г, Салат Романо, Сухарики 100г, Пармезан 80г', 'instructions': '1. Обжарить курицу\n2. Нарезать салат\n3. Добавить сухарики и сыр\n4. Заправить соусом', 'image': 'https://avatars.mds.yandex.net/i?id=fefec47600cd886419caf5b0ab7153a4356c488b-5305327-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Оливье', 'desc': 'Классический салат', 'time': 45, 'serv': 8, 'diff': 'easy', 'ingredients': 'Картофель 4шт, Морковь 3шт, Яйца 5шт, Колбаса 400г', 'instructions': '1. Отварить овощи\n2. Нарезать кубиками\n3. Добавить горошек\n4. Заправить майонезом', 'image': 'https://avatars.mds.yandex.net/get-entity_search/10349888/1244614344/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Греческий', 'desc': 'Свежий салат', 'time': 15, 'serv': 4, 'diff': 'easy', 'ingredients': 'Огурцы 2шт, Помидоры 3шт, Перец 1шт, Фета 200г', 'instructions': '1. Нарезать овощи\n2. Добавить фету и маслины\n3. Заправить маслом\n4. Посыпать орегано', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5579913/1190347465/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Мимоза', 'desc': 'Слоеный салат', 'time': 60, 'serv': 6, 'diff': 'medium', 'ingredients': 'Рыбные консервы 2б, Картофель 4шт, Морковь 3шт, Яйца 5шт', 'instructions': '1. Отварить овощи и яйца\n2. Натереть на терке\n3. Выложить слоями\n4. Промазать майонезом', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5103535/1262352162/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Сельдь под шубой', 'desc': 'Праздничный салат', 'time': 60, 'serv': 8, 'diff': 'medium', 'ingredients': 'Сельдь 2шт, Свекла 3шт, Картофель 4шт, Морковь 3шт', 'instructions': '1. Отварить овощи\n2. Натереть на терке\n3. Выложить слоями\n4. Каждый слой с майонезом', 'image': 'https://avatars.mds.yandex.net/get-entity_search/10844871/953829237/SUx182_2x'},  # ← ВАША ССЫЛКА
]

for r in salad_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Салат']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === ЗАКУСКИ (5) ===
print("\n📸 [ЗАКУСКИ] Вставьте ваши ссылки:")
appetizer_recipes = [
    {'title': 'Брускетта с томатами', 'desc': 'Итальянская закуска', 'time': 15, 'serv': 6, 'diff': 'easy', 'ingredients': 'Багет 1шт, Помидоры 4шт, Чеснок 2зуб, Базилик', 'instructions': '1. Поджарить хлеб\n2. Натереть чесноком\n3. Нарезать томаты\n4. Выложить на хлеб', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2304479/1262531642/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Капрезе', 'desc': 'Итальянская закуска', 'time': 10, 'serv': 4, 'diff': 'easy', 'ingredients': 'Моцарелла 250г, Помидоры 3шт, Базилик, Масло оливковое', 'instructions': '1. Нарезать сыр и томаты\n2. Выложить в шахматном порядке\n3. Полить маслом\n4. Посыпать базиликом', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2048976/1261478620/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Фаршированные яйца', 'desc': 'Простая закуска', 'time': 25, 'serv': 6, 'diff': 'easy', 'ingredients': 'Яйца 6шт, Майонез 2ст.л, Горчица 1ч.л, Зелень', 'instructions': '1. Отварить яйца\n2. Разрезать пополам\n3. Достать желтки\n4. Смешать с майонезом', 'image': 'https://avatars.mds.yandex.net/get-entity_search/11019286/1170287107/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Картофель фри', 'desc': 'Хрустящий картофель', 'time': 30, 'serv': 4, 'diff': 'easy', 'ingredients': 'Картофель 1кг, Масло, Соль, Паприка', 'instructions': '1. Нарезать брусочками\n2. Обсушить\n3. Обжарить в масле\n4. Посыпать специями', 'image': 'https://avatars.mds.yandex.net/get-entity_search/7983837/1262548322/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Спринг роллы', 'desc': 'Азиатские роллы', 'time': 40, 'serv': 8, 'diff': 'medium', 'ingredients': 'Рисовая бумага, Креветки 200г, Лапша, Морковь', 'instructions': '1. Замочить рисовую бумагу\n2. Нарезать овощи\n3. Выложить начинку\n4. Завернуть роллы', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2321801/1254198877/SUx182_2x'},  # ← ВАША ССЫЛКА
]

for r in appetizer_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Закуски']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === ВЫПЕЧКА (5) ===
print("\n📸 [ВЫПЕЧКА] Вставьте ваши ссылки:")
baking_recipes = [
    {'title': 'Шарлотка с яблоками', 'desc': 'Яблочный пирог', 'time': 60, 'serv': 6, 'diff': 'easy', 'ingredients': 'Яблоки 5шт, Яйца 4шт, Мука 200г, Сахар 150г', 'instructions': '1. Взбить яйца с сахаром\n2. Добавить муку\n3. Нарезать яблоки\n4. Вылить тесто на яблоки', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2102351/1244831714/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Печенье', 'desc': 'Домашнее печенье', 'time': 45, 'serv': 12, 'diff': 'easy', 'ingredients': 'Мука 250г, Масло 100г, Сахар 100г, Яйцо 1шт', 'instructions': '1. Взбить масло с сахаром\n2. Добавить яйцо\n3. Добавить муку\n4. Сформировать печенье', 'image': 'https://avatars.mds.yandex.net/i?id=15e83fdb82032d01b6f8ccdb5b045d7e5162529b-4232421-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Круассаны', 'desc': 'Слоеные круассаны', 'time': 180, 'serv': 8, 'diff': 'hard', 'ingredients': 'Мука 500г, Масло 250г, Дрожжи 10г, Молоко 200мл', 'instructions': '1. Замесить тесто\n2. Сделать слоение\n3. Сформировать круассаны\n4. Выпекать', 'image': 'https://avatars.mds.yandex.net/get-entity_search/1974877/1261908618/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Маффины', 'desc': 'Шоколадные маффины', 'time': 30, 'serv': 12, 'diff': 'easy', 'ingredients': 'Мука 250г, Какао 50г, Сахар 150г, Масло 100г', 'instructions': '1. Смешать сухие компоненты\n2. Добавить жидкие\n3. Разлить по формочкам\n4. Выпекать', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2000260/1220908411/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Хлеб ржаной', 'desc': 'Домашний хлеб', 'time': 180, 'serv': 10, 'diff': 'medium', 'ingredients': 'Мука ржаная 400г, Мука пшеничная 100г, Закваска 200г', 'instructions': '1. Замесить тесто\n2. Расстойка 2 часа\n3. Сформировать\n4. Выпекать', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2334190/1238269480/SUx182_2x'},  # ← ВАША ССЫЛКА
]

for r in baking_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Выпечка']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === НАПИТКИ (5) ===
print("\n📸 [НАПИТКИ] Вставьте ваши ссылки:")
drink_recipes = [
    {'title': 'Глинтвейн', 'desc': 'Согревающий напиток', 'time': 15, 'serv': 4, 'diff': 'easy', 'ingredients': 'Вино 750мл, Апельсин, Лимон, Корица, Мед', 'instructions': '1. Нагреть вино\n2. Добавить фрукты и специи\n3. Добавить мед\n4. Подавать горячим', 'image': 'https://avatars.mds.yandex.net/get-entity_search/10105370/1248598206/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Смузи клубничный', 'desc': 'Освежающий смузи', 'time': 5, 'serv': 2, 'diff': 'easy', 'ingredients': 'Клубника 200г, Банан 1шт, Йогурт 200мл', 'instructions': '1. Смешать все в блендере\n2. Взбить до однородности\n3. Подавать охлажденным', 'image': 'https://avatars.mds.yandex.net/i?id=058fd2b9b5a7378442758b3422b81dd32f00fe75-10517487-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Матча латте', 'desc': 'Зеленый чай латте', 'time': 10, 'serv': 2, 'diff': 'easy', 'ingredients': 'Молоко 400мл, Матча 2ч.л, Мед 2ч.л', 'instructions': '1. Развести матчу водой\n2. Подогреть молоко\n3. Соединить\n4. Взбить в пену', 'image': 'https://avatars.mds.yandex.net/get-entity_search/4787573/1244229797/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Лимонад', 'desc': 'Домашний лимонад', 'time': 10, 'serv': 4, 'diff': 'easy', 'ingredients': 'Лимоны 3шт, Мед 3ст.л, Мята, Вода', 'instructions': '1. Выжать лимоны\n2. Добавить мед\n3. Добавить мяту\n4. Залить водой', 'image': 'https://avatars.mds.yandex.net/i?id=288abd50ec9763f25449c4663c60aa36da5a577b-5101081-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Горячий шоколад', 'desc': 'Густой горячий шоколад', 'time': 15, 'serv': 2, 'diff': 'easy', 'ingredients': 'Молоко 500мл, Шоколад 100г, Какао 2ст.л', 'instructions': '1. Нагреть молоко\n2. Растопить шоколад\n3. Добавить какао\n4. Взбить', 'image': 'https://avatars.mds.yandex.net/i?id=c6d991777bb162788fca0132cf57172a554c3211-3872711-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
]

for r in drink_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Напитки']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === МЯСНОЕ (5) ===
print("\n📸 [МЯСНОЕ] Вставьте ваши ссылки:")
meat_recipes = [
    {'title': 'Шашлык из свинины', 'desc': 'Сочный шашлык', 'time': 180, 'serv': 6, 'diff': 'medium', 'ingredients': 'Свинина 1.5кг, Лук 500г, Уксус, Специи', 'instructions': '1. Нарезать мясо\n2. Добавить лук и специи\n3. Мариновать 2 часа\n4. Жарить', 'image': 'https://avatars.mds.yandex.net/i?id=86d01a02e33104ad9f056ee402b77bf3b71ee9ed-9097048-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Бефстроганов', 'desc': 'Нежное мясо в сметанном соусе', 'time': 50, 'serv': 4, 'diff': 'medium', 'ingredients': 'Говядина 500г, Лук 2шт, Сметана 200г', 'instructions': '1. Нарезать мясо полосками\n2. Обжарить\n3. Добавить лук\n4. Добавить сметану', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5394189/1222855139/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Отбивные свиные', 'desc': 'Сочные отбивные', 'time': 30, 'serv': 4, 'diff': 'easy', 'ingredients': 'Свинина 600г, Яйца 2шт, Сухари 100г', 'instructions': '1. Отбить мясо\n2. Обвалять в яйце и сухарях\n3. Обжарить', 'image': 'https://avatars.mds.yandex.net/i?id=a180686c1fe66a12bb85bea9b728f5e652b75acd-4819109-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Гуляш', 'desc': 'Венгерский гуляш', 'time': 90, 'serv': 6, 'diff': 'medium', 'ingredients': 'Говядина 800г, Лук 3шт, Паприка, Томат', 'instructions': '1. Обжарить мясо\n2. Добавить лук и паприку\n3. Залить водой\n4. Тушить', 'image': 'https://avatars.mds.yandex.net/get-entity_search/5396253/1262097517/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Курица в духовке', 'desc': 'Целая курица запеченая', 'time': 80, 'serv': 4, 'diff': 'easy', 'ingredients': 'Курица 1.5кг, Чеснок, Розмарин', 'instructions': '1. Натереть курицу специями\n2. Запекать 1 час\n3. Дать отдохнуть', 'image': 'https://avatars.mds.yandex.net/i?id=1a22fec116adc54e5e05a4d26fd3cfd8e24de41f-11380463-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
]

for r in meat_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Мясное']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# === РЫБНОЕ (5) ===
print("\n📸 [РЫБНОЕ] Вставьте ваши ссылки:")
fish_recipes = [
    {'title': 'Семга в сливочном соусе', 'desc': 'Нежная семга', 'time': 25, 'serv': 4, 'diff': 'easy', 'ingredients': 'Семга 600г, Сливки 200мл, Лук 1шт', 'instructions': '1. Обжарить рыбу\n2. Сделать соус\n3. Залить рыбу соусом\n4. Тушить', 'image': 'https://avatars.mds.yandex.net/i?id=f6cce1950691397815eb5527e9198bb968bed633-5488376-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Скумбрия на гриле', 'desc': 'Ароматная скумбрия', 'time': 20, 'serv': 4, 'diff': 'easy', 'ingredients': 'Скумбрия 4шт, Лимон, Розмарин', 'instructions': '1. Натереть солью\n2. Добавить розмарин\n3. Жарить на гриле', 'image': 'https://avatars.mds.yandex.net/i?id=56aadb12aa1db4351230481391205e26c840c729-10898088-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Салат с тунцом', 'desc': 'Полезный салат', 'time': 15, 'serv': 2, 'diff': 'easy', 'ingredients': 'Тунец 200г, Яйца 2шт, Овощи', 'instructions': '1. Отварить яйца\n2. Нарезать овощи\n3. Добавить тунец\n4. Заправить', 'image': 'https://avatars.mds.yandex.net/get-entity_search/2001742/1254036555/SUx182_2x'},  # ← ВАША ССЫЛКА
    {'title': 'Уха царская', 'desc': 'Богатая уха', 'time': 90, 'serv': 8, 'diff': 'medium', 'ingredients': 'Осетрина 500г, Лосось 400г, Картофель', 'instructions': '1. Сварить бульон\n2. Добавить картофель\n3. Добавить рыбу\n4. Варить', 'image': 'https://avatars.mds.yandex.net/i?id=52b128fc8be2e29b967d38e71f3db62e19987532-11476564-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
    {'title': 'Рыбные котлеты', 'desc': 'Нежные рыбные котлеты', 'time': 40, 'serv': 6, 'diff': 'easy', 'ingredients': 'Филе рыбы 800г, Лук 1шт, Яйцо 1шт', 'instructions': '1. Пропустить рыбу через мясорубку\n2. Добавить лук и яйцо\n3. Сформировать котлеты\n4. Обжарить', 'image': 'https://avatars.mds.yandex.net/i?id=ae1e70da60a6f3dc584ea714dd7ee40ad651f1dc-5351536-images-thumbs&n=13'},  # ← ВАША ССЫЛКА
]

for r in fish_recipes:
    recipe, _ = Recipe.objects.get_or_create(
        title=r['title'],
        defaults={
            'description': r['desc'],
            'ingredients': r['ingredients'],
            'instructions': r['instructions'],
            'cooking_time': r['time'],
            'servings': r['serv'],
            'difficulty': r['diff'],
            'image': r['image'],
            'author': random.choice(users),
            'category': categories['Рыбное']
        }
    )
    all_recipes.append(recipe)
    print(f"  ✓ {r['title']}")

# 4. ЛАЙКИ
print("\n4. ДОБАВЛЕНИЕ ЛАЙКОВ...")
like_count = 0
for user in users:
    liked_recipes = random.sample(all_recipes, min(30, len(all_recipes)))
    for recipe in liked_recipes:
        like, created = Like.objects.get_or_create(user=user, recipe=recipe)
        if created:
            like_count += 1
print(f"  ✓ Добавлено лайков: {like_count}")

# 5. СОХРАНЕНИЯ
print("\n5. ДОБАВЛЕНИЕ СОХРАНЕНИЙ...")
save_count = 0
for user in users:
    saved_recipes = random.sample(all_recipes, min(20, len(all_recipes)))
    for recipe in saved_recipes:
        saved, created = SavedRecipe.objects.get_or_create(user=user, recipe=recipe)
        if created:
            save_count += 1
print(f"  ✓ Добавлено сохранений: {save_count}")

# 6. КОММЕНТАРИИ
print("\n6. ДОБАВЛЕНИЕ КОММЕНТАРИЕВ...")
comments_list = [
    "Отличный рецепт! Все получилось! 👍",
    "Спасибо, очень вкусно! 😋",
    "Буду готовить еще!",
    "Рецепт огонь! 🔥",
    "Лучший рецепт!",
    "Всем рекомендую!",
]
comment_count = 0
for recipe in all_recipes:
    for user in random.sample(users, min(3, len(users))):
        comment, created = Comment.objects.get_or_create(
            text=random.choice(comments_list),
            user=user,
            recipe=recipe
        )
        if created:
            comment_count += 1
print(f"  ✓ Добавлено комментариев: {comment_count}")

# 7. СТАТИСТИКА
print("\n" + "="*70)
print("ИТОГОВАЯ СТАТИСТИКА")
print("="*70)
print(f"  Категории: {Category.objects.count()}")
print(f"  Пользователи: {User.objects.filter(is_superuser=False).count()}")
print(f"  Рецепты: {Recipe.objects.count()}")
print(f"  Лайки: {Like.objects.count()}")
print(f"  Сохранения: {SavedRecipe.objects.count()}")
print(f"  Комментарии: {Comment.objects.count()}")

print("\n" + "="*70)
print("ДАННЫЕ ДЛЯ ВХОДА")
print("="*70)
for user in users:
    token = Token.objects.get(user=user)
    print(f"\n  Логин: {user.username}")
    print(f"  Пароль: 123456")

print("\n" + "="*70)
print("✅ ГОТОВО!")
print("="*70)
print("\n📸 Теперь замените 'ВАША_ССЫЛКА_1' ... 'ВАША_ССЫЛКА_55'")
print("на ваши реальные ссылки на фото каждого блюда!")
print("="*70)