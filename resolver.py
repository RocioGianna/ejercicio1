from db import get_user_by_id, get_users, get_users_filtered, create_user, delete_user, update_user


def resolve_get_user_by_id(id):
    return get_user_by_id(id)


def resolve_get_users_filtered(name, surname, email, user_name, limit, offset):
    return get_users_filtered(name, surname, email, user_name, limit, offset)

def resolve_get_users():
    return get_users()

def resolve_create_user(**kwargs):
    return create_user(**kwargs)


def resolve_update_user(**kwargs):
    return update_user(**kwargs)


def resolve_delete_user(id):
    return delete_user(id)
