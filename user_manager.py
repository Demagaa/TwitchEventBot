import os

file_path = './user_ids'
subscribers = []


def create_file_if_not_exists():
    if not bool(subscribers):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Just create an empty file
        with open(file_path, 'r') as file:
            for line in file:
                subscribers.append(int(line.strip()))


def save_user_id(user_id):
    create_file_if_not_exists()
    if user_id in subscribers:
        return "Вы уже подписаны на Stubborn"
    with open(file_path, 'a') as file:
        file.write(str(user_id) + '\n')
    subscribers.append(user_id)
    return "Подписка на запуск трансляции для Stubborn оформлена"


def get_user_ids():
    create_file_if_not_exists()
    if not bool(subscribers):
        with open(file_path, 'r') as file:
            for line in file:
                subscribers.append(int(line.strip()))
    return subscribers


def remove_user_id(user_id):
    create_file_if_not_exists()
    if user_id not in subscribers:
        return "Вы не подписаны на Stubborn"
    subscribers.remove(user_id)
    # Read the existing user IDs and filter out the one to be removed
    with open(file_path, 'r') as file:
        user_ids = [int(line.strip()) for line in file if int(line.strip()) != user_id]

    # Write the updated user IDs back to the file
    with open(file_path, 'w') as file:
        for user_id in user_ids:
            file.write(str(user_id) + '\n')
    return "Вы были успешно отписаны от Stubborn"