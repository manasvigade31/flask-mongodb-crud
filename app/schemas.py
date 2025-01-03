from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only=True)  
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True) 