from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField


# Example
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class PlayerForm(Form):
    player_name = StringField('Pro name', [validators.Length(min=4, max=25)])
    summoner_name = StringField('Summoner name', [validators.Length(min=6, max=35)])
    region = SelectField('Region', [validators.DataRequired()])
