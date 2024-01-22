from app import schemas, models


def create_token(user: models.User, access_token: str) -> dict:
    abilities = [
        schemas.UserAbility(**vars(ability))
        for ability in user.abilities
    ]
    token = {
        "user_data": {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "role": user.role.role_name,
            "ability": abilities,
            "phone": user.phone_number,
            "email": user.email,
            "password": None
        },
        "access_token": access_token,
        "token_type": "bearer"
    }
    return token
