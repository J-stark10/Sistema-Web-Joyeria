from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):

    nombre_usuario = StringField(
        'Usuario',
        validators=[
            DataRequired(message='El usuario es obligatorio.'),
            Length(min=3, max=50, message='El usuario debe tener entre 3 y 50 caracteres.')
        ],
        render_kw={'placeholder': 'Ingresa tu usuario', 'autocomplete': 'username'}
    )

    contrasena = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es obligatoria.')
        ],
        render_kw={'placeholder': '••••••••', 'autocomplete': 'current-password'}
    )

    recordarme = BooleanField('Recordarme')

    submit = SubmitField('Iniciar sesión')
