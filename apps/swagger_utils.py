from drf_yasg.openapi import Schema

users_id_schema = Schema(
    title="users_id",
    description="ID list of users to assign to group.",
    type="array",
    items=Schema(type="integer"),
)
