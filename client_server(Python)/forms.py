from wtforms import Form, StringField, validators

class RegisterForm(Form):
    name = StringField('HotSpot Name', [validators.Length(min = 5, max = 65)])
    password = StringField('Password', [validators.Length(min = 8, max = 100)])

class MessageForm(Form):
    message = StringField('Message', [validators.Length(min = 1, max = 1000)])