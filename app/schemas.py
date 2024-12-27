from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)  # MongoDB _id will be used
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)  # You can omit this field in responses, but it's needed for validation
