from marshmallow import Schema, fields, ValidationError, validate, validates_schema


class AddUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=8))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    confirm_password = fields.Str(required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Введенные пароли не совпадают!')


class LogUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=8))
    password = fields.Str(required=True, validate=validate.Length(min=8))


class PutForumPostsSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=4))
    content = fields.Str(required=True, validate=validate.Length(min=8))
