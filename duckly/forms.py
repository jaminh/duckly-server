from wtforms import (
    Form,
    TextField,
    validators
)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=1, max=30),
                                      validators.Required()])
    display_name = TextField('Display Name')

