from app import schemas, models


def create_token(user: models.User, access_token: str) -> dict:
    print(schemas.UserAbilities.from_list(user.abilities))
    token = {
        "user_data": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "role": user.role.role_name,
            "ability": schemas.UserAbilities.from_list(user.abilities),
            "phone": user.phone_number,
            "email": user.email,
            "password": None
        },
        "access_token": access_token,
        "token_type": "bearer"
    }
    return token
