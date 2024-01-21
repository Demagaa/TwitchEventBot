import os


file_path = './user_ids'
def create_file_if_not_exists():
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass  # Just create an empty file


def save_user_id(user_id):
    create_file_if_not_exists()
    with open(file_path, 'a') as file:
        file.write(str(user_id) + '\n')


def get_user_ids():
    create_file_if_not_exists()
    user_ids = []
    with open(file_path, 'r') as file:
        for line in file:
            user_ids.append(int(line.strip()))
    return user_ids
