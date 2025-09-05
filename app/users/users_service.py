from enum import Enum
from fastapi import Query
from app.core.constants import success_messages
from app.database.repository.user_repo import create_user, get_and_validate_user, validate_updated_data
from app.database.models.user import User, AccountStatus, Roles, Gender
from app.schemas.auth_schema import SignupSchema
from app.schemas.users_schema import UpdateUserInfo, ChangeRole


class UsersService:
    async def get_all_users(
        self,
        name: str | None = None,
        gender: Gender | None = None,
        role: Roles | None = None,
        account_status: AccountStatus | None = None,
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
    ):
        skip = (page - 1) * limit
        query = {}

        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if gender:
            query["gender"] = gender.value if isinstance(gender, Enum) else gender
        if role:
            query["role"] = role.value if isinstance(role, Enum) else role
        if account_status:
            query["accountStatus"] = account_status.value if isinstance(account_status, Enum) else account_status

        total_users_count = await User.find(query).count()
        users = await User.find(query).skip(skip).limit(limit).to_list()

        return {
            "message": success_messages["all_users"],
            "data": users,
            "pagination": {
                "total": total_users_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_users_count + limit -1) // limit,
            }
        }


    async def get_user_by_id(self, user_id: str):
        found_user = await get_and_validate_user(user_id)

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
        updated_user = await get_and_validate_user(user_id)
        updated_data = validate_updated_data(data)
        await  updated_user.set(updated_data)

        return {
            "message": success_messages["update_user"],
            "data": updated_user
        }


    async def delete_user_by_id(self, user_id: str):
        user_to_delete = await get_and_validate_user(user_id)
        await user_to_delete.delete()
        return { "message": success_messages["delete_user"] }


    async def add_app_admin(self, user: SignupSchema):
        await create_user(
            user=user,
            role=Roles.ADMIN,
            account_status=AccountStatus.VERIFIED,
        )

        return {
            "message": success_messages["add_app_admin"],
        }


    async def add_organizer(self, user: SignupSchema):
        await create_user(
            user=user,
            role=Roles.ORGANIZER,
            account_status=AccountStatus.VERIFIED,
        )

        return {
            "message": success_messages["add_organizer"],
        }


    async def change_role_status(self, user_id: str, data: ChangeRole):
        updated_user_role = await get_and_validate_user(user_id)
        updated_data = validate_updated_data(data)
        await updated_user_role.set(updated_data)

        return {
            "message": success_messages["change_role_status"],
        }

users_service = UsersService()