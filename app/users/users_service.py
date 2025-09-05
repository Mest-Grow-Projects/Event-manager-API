from fastapi import HTTPException, status
from app.core.constants import success_messages, status_messages
from app.database.repository.user_repo import find_user_by_id, check_existing_user
from app.database.models.user import User, AccountStatus, Roles
from app.schemas.auth_schema import SignupSchema
from app.schemas.users_schema import UpdateUserInfo, ChangeRole
from app.utils.auth_utils import get_password_hash


class UsersService:
    async def get_all_users(self):
        users = await User.find_all().to_list()
        return {
            "message": success_messages["all_users"],
            "data": users,
        }


    async def get_user_by_id(self, user_id: str):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["user_id_required"],
            )
        found_user = await find_user_by_id(user_id)

        return {
            "message": success_messages["found_user"],
            "data": {
                "id": found_user.id,
                "name": found_user.name,
                "email": found_user.email,
                "avatar": found_user.avatar,
                "accountStatus": found_user.accountStatus,
                "role": found_user.role,
                "dob": found_user.dob,
                "location": found_user.location,
                "phone": found_user.phone,
                "createdAt": found_user.createdAt,
                "updatedAt": found_user.updatedAt,
            },
        }


    async def update_user_by_id(self, user_id: str, data: UpdateUserInfo):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["user_id_required"],
            )

        updated_user = await find_user_by_id(user_id)
        updated_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["update_invalid"],
            )

        await  updated_user.set(updated_data)
        return {
            "message": success_messages["update_user"],
            "data": updated_user
        }


    async def delete_user_by_id(self, user_id: str):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["user_id_required"],
            )

        user = await find_user_by_id(user_id)
        await user.delete()
        return { "message": success_messages["delete_user"] }


    async def add_app_admin(self, user: SignupSchema):
        found_user = await check_existing_user(str(user.email))
        hashed_password = get_password_hash(user.password)

        await User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            accountStatus=AccountStatus.VERIFIED,
            role=Roles.ADMIN
        ).insert()

        return {
            "message": success_messages["add_app_admin"],
        }


    async def add_organizer(self, user: SignupSchema):
        await check_existing_user(str(user.email))
        hashed_password = get_password_hash(user.password)

        await User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            accountStatus=AccountStatus.VERIFIED,
            role=Roles.ORGANIZER
        ).insert()

        return {
            "message": success_messages["add_organizer"],
        }


    async def change_role_status(self, user_id: str, data: ChangeRole):
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["user_id_required"],
            )

        updated_role = await find_user_by_id(user_id)
        updated_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_messages["update_invalid"],
            )

        await updated_role.set(updated_data)

        return {
            "message": success_messages["change_role_status"],
        }

users_service = UsersService()