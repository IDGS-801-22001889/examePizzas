from wtforms import Form, validators
from wtforms import StringField, IntegerField, DateField

class FormPedido(Form):
    nombre    = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(max=100)
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message='La dirección es requerida'),
        validators.length(max=200)
    ])
    telefono  = StringField('Teléfono', [
        validators.DataRequired(message='El teléfono es requerido'),
        validators.length(max=20)
    ])
    fecha     = DateField('Fecha', [
        validators.DataRequired(message='La fecha es requerida')
    ])
    cantidad  = IntegerField('Número de Pizzas', [
        validators.DataRequired(message='La cantidad es requerida'),
        validators.number_range(min=1, message='Mínimo 1 pizza')
    ])