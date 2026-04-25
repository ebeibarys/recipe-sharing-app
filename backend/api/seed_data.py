import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Category, Recipe, Comment, Like, SavedRecipe
from rest_framework.authtoken.models import Token

def seed_database():
    print("Начинаем заполнение базы данных...")
    
    # 1. Создание категорий
    categories = [
        'Завтрак', 'Обед', 'Ужин', 'Десерт', 
        'Закуски', 'Суп', 'Салат', 'Напитки'
    ]
    
    created_categories = []
    for cat_name in categories:
        category, created = Category.objects.get_or_create(name=cat_name)
        created_categories.append(category)
        print(f"✓ Категория '{cat_name}' создана")
    
    # 2. Создание пользователей
    users_data = [
        {'username': 'alex_chef', 'password': 'chef123456', 'email': 'alex@example.com'},
        {'username': 'maria_cook', 'password': 'cook123456', 'email': 'maria@example.com'},
        {'username': 'john_food', 'password': 'food123456', 'email': 'john@example.com'},
        {'username': 'lena_kitchen', 'password': 'lena123456', 'email': 'lena@example.com'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'password': 'temp'
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✓ Пользователь '{user_data['username']}' создан")
        created_users.append(user)
    
    # 3. Создание рецептов
    recipes_data = [
        {
            'title': 'Классический борщ',
            'description': 'Наваристый украинский борщ с пампушками',
            'ingredients': 'Свекла - 2 шт\nКапуста - 300 г\nКартофель - 4 шт\nМорковь - 1 шт\nЛук - 1 шт\nТоматная паста - 2 ст.л.\nМясо говядина - 500 г\nЧеснок - 3 зубчика\nСоль, перец по вкусу',
            'instructions': '1. Сварить бульон из мяса\n2. Нарезать и обжарить свеклу с томатной пастой\n3. Добавить нарезанные овощи в бульон\n4. Варить до готовности 40 минут\n5. Добавить зажарку и чеснок\n6. Дать настояться 15 минут',
            'cooking_time': 120,
            'servings': 6,
            'difficulty': 'medium',
            'image': 'https://images.unsplash.com/photo-1547592180-85f173990554?w=500',
            'category_name': 'Суп'
        },
        {
            'title': 'Итальянская паста Карбонара',
            'description': 'Кремовая паста с беконом и пармезаном',
            'ingredients': 'Паста спагетти - 400 г\nБекон - 200 г\nЯйца - 4 шт\nПармезан - 100 г\nЧеснок - 2 зубчика\nСоль, перец черный',
            'instructions': '1. Сварить пасту до al dente\n2. Обжарить бекон с чесноком\n3. Смешать яйца с тертым пармезаном\n4. Соединить горячую пасту с беконом\n5. Добавить яичную смесь и быстро перемешать\n6. Подавать с дополнительным пармезаном',
            'cooking_time': 25,
            'servings': 4,
            'difficulty': 'easy',
            'image': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=500',
            'category_name': 'Ужин'
        },
        {
            'title': 'Воздушный панкейк',
            'description': 'Пышные американские блинчики на завтрак',
            'ingredients': 'Мука - 200 г\nМолоко - 200 мл\nЯйца - 2 шт\nСахар - 2 ст.л.\nРазрыхлитель - 1 ч.л.\nСоль - щепотка',
            'instructions': '1. Отделить белки от желтков\n2. Смешать желтки с молоком и сахаром\n3. Добавить просеянную муку и разрыхлитель\n4. Взбить белки в пену\n5. Аккуратно смешать с тестом\n6. Жарить на сухой сковороде',
            'cooking_time': 30,
            'servings': 4,
            'difficulty': 'easy',
            'image': 'https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=500',
            'category_name': 'Завтрак'
        },
        {
            'title': 'Тирамису',
            'description': 'Классический итальянский десерт',
            'ingredients': 'Маскарпоне - 500 г\nЯйца - 4 шт\nСахар - 100 г\nПеченье Савоярди - 200 г\nКофе эспрессо - 300 мл\nКакао - для посыпки',
            'instructions': '1. Отделить белки от желтков\n2. Взбить желтки с сахаром\n3. Добавить маскарпоне и перемешать\n4. Взбить белки в крепкую пену\n5. Аккуратно соединить с кремом\n6. Обмакнуть печенье в кофе\n7. Собрать слоями и поставить в холодильник на 4 часа',
            'cooking_time': 45,
            'servings': 6,
            'difficulty': 'medium',
            'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500',
            'category_name': 'Десерт'
        },
        {
            'title': 'Салат Цезарь с курицей',
            'description': 'Хрустящий салат с курицей и пармезаном',
            'ingredients': 'Куриное филе - 300 г\nСалат Романо - 1 шт\nСухарики - 100 г\nПармезан - 50 г\nСоус Цезарь - 4 ст.л.',
            'instructions': '1. Обжарить курицу до золотистой корочки\n2. Нарезать салат крупными кусками\n3. Добавить сухарики и пармезан\n4. Заправить соусом перед подачей',
            'cooking_time': 20,
            'servings': 2,
            'difficulty': 'easy',
            'image': 'https://images.unsplash.com/photo-1550304943-4f24f54dd8c9?w=500',
            'category_name': 'Салат'
        },
        {
            'title': 'Овощное рагу',
            'description': 'Полезное овощное рагу для всей семьи',
            'ingredients': 'Кабачок - 1 шт\nБаклажан - 1 шт\nПерец болгарский - 2 шт\nПомидоры - 3 шт\nМорковь - 1 шт\nЛук - 1 шт\nЧеснок - 2 зубчика',
            'instructions': '1. Нарезать все овощи кубиками\n2. Обжарить лук и морковь\n3. Добавить остальные овощи\n4. Тушить 20 минут\n5. Добавить чеснок и зелень',
            'cooking_time': 35,
            'servings': 4,
            'difficulty': 'easy',
            'image': 'https://images.unsplash.com/photo-1528715472581-0c5b5f5604a5?w=500',
            'category_name': 'Обед'
        }
    ]
    
    # Получаем словарь категорий
    category_dict = {cat.name: cat for cat in created_categories}
    
    created_recipes = []
    for recipe_data in recipes_data:
        author = created_users[recipe_data.get('index', 0) % len(created_users)]
        category = category_dict.get(recipe_data['category_name'])
        
        # Проверяем, существует ли уже такой рецепт
        recipe, created = Recipe.objects.get_or_create(
            title=recipe_data['title'],
            defaults={
                'description': recipe_data['description'],
                'ingredients': recipe_data['ingredients'],
                'instructions': recipe_data['instructions'],
                'cooking_time': recipe_data['cooking_time'],
                'servings': recipe_data['servings'],
                'difficulty': recipe_data['difficulty'],
                'image': recipe_data['image'],
                'author': author,
                'category': category
            }
        )
        if created:
            created_recipes.append(recipe)
            print(f"✓ Рецепт '{recipe_data['title']}' создан (автор: {author.username})")
        else:
            created_recipes.append(recipe)
            print(f"• Рецепт '{recipe_data['title']}' уже существует")
    
    # 4. Добавляем лайки
    for user in created_users:
        for recipe in created_recipes[:3]:  # Лайкаем первые 3 рецепта
            like, created = Like.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if created:
                print(f"✓ {user.username} лайкнул(а) {recipe.title}")
    
    # 5. Добавляем сохранения
    for user in created_users:
        for recipe in created_recipes[2:5]:  # Сохраняем рецепты с 3 по 5
            saved, created = SavedRecipe.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if created:
                print(f"✓ {user.username} сохранил(а) {recipe.title}")
    
    # 6. Добавляем комментарии
    comments_data = [
        {'text': 'Отличный рецепт! Всё получилось с первого раза! 👍', 'user': created_users[0], 'recipe': created_recipes[0]},
        {'text': 'Очень вкусно, готовил дважды! Спасибо!', 'user': created_users[1], 'recipe': created_recipes[0]},
        {'text': 'Добавила больше сыра, получилось ещё вкуснее', 'user': created_users[2], 'recipe': created_recipes[1]},
        {'text': 'Быстро и просто. Идеально для начинающих', 'user': created_users[1], 'recipe': created_recipes[2]},
        {'text': 'Мой новый любимый десерт!', 'user': created_users[3], 'recipe': created_recipes[3]},
        {'text': 'Спасибо за рецепт! Дети в восторге', 'user': created_users[0], 'recipe': created_recipes[4]},
        {'text': 'Можно заменить курицу на креветки?', 'user': created_users[2], 'recipe': created_recipes[1]},
        {'text': 'Лучшее блюдо для ужина!', 'user': created_users[3], 'recipe': created_recipes[1]},
    ]
    
    for comment_data in comments_data:
        comment, created = Comment.objects.get_or_create(
            text=comment_data['text'],
            user=comment_data['user'],
            recipe=comment_data['recipe'],
            defaults={'created_at': '2024-01-01 12:00:00'}
        )
        if created:
            print(f"✓ Комментарий от {comment_data['user'].username} добавлен")
    
    # 7. Генерируем токены для всех пользователей
    for user in created_users:
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"✓ Токен для {user.username}: {token.key}")
    
    print("\n" + "="*50)
    print("База данных успешно заполнена!")
    print(f"Категорий: {len(created_categories)}")
    print(f"Пользователей: {len(created_users)}")
    print(f"Рецептов: {len(created_recipes)}")
    print(f"Комментариев: {len(comments_data)}")
    
    # Выводим данные для входа
    print("\n" + "="*50)
    print("ДАННЫЕ ДЛЯ ВХОДА В ПРИЛОЖЕНИЕ:")
    print("="*50)
    print("\n👤 Пользователи:")
    for user in created_users:
        token = Token.objects.get(user=user)
        print(f"  Логин: {user.username}")
        print(f"  Пароль: {user.first_name if user.first_name else '123456'}")
        print(f"  Токен: {token.key}")
        print()
    
    print("🍽️ Тестовые рецепты созданы!")
    print("🌐 Откройте http://localhost:4200 и войдите под любым пользователем")

if __name__ == "__main__":
    seed_database()