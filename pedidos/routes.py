from . import pedidos
from flask import render_template, request, redirect, url_for, flash
import forms
import datetime
from models import db, Cliente, Pizza, Pedido, DetallePedido, CarritoTemp

@pedidos.route('/pedidos', methods=['GET', 'POST'])
def pedido():
    form = forms.FormPedido(request.form)
    pizzas = Pizza.query.all()
    carrito = CarritoTemp.query.all()
    hoy = datetime.date.today()
    ventas_hoy = db.session.query(Pedido).filter(db.func.date(Pedido.fecha) == hoy).all()
    return render_template('pedidos/index.html', form=form, pizzas=pizzas, carrito=carrito, ventas_hoy=ventas_hoy)

@pedidos.route('/agregar', methods=['POST'])
def agregar():
    tamano = request.form.get('tamano')
    cantidad = int(request.form.get('cantidad', 1))
    ingredientes = request.form.getlist('ingredientes')
    pizza = db.session.query(Pizza).filter(Pizza.tamano == tamano).first()
    precio_base = float(pizza.precio)
    costo_ingredientes = len(ingredientes) * 10
    precio_unitario = precio_base + costo_ingredientes
    subtotal = precio_unitario * cantidad
    item = CarritoTemp(
        id_pizza=pizza.id_pizza,
        tamano=tamano,
        ingredientes=', '.join(ingredientes) if ingredientes else 'Sin ingredientes',
        cantidad=cantidad,
        subtotal=subtotal
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('pedidos.pedido'))

@pedidos.route('/quitar/<int:id>', methods=['GET'])
def quitar(id):
    item = db.session.query(CarritoTemp).filter(CarritoTemp.id == id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('pedidos.pedido'))

@pedidos.route('/terminar', methods=['POST'])
def terminar():
    nombre    = request.form.get('nombre')
    direccion = request.form.get('direccion')
    telefono  = request.form.get('telefono')
    fecha_form = request.form.get('fecha')

    carrito = CarritoTemp.query.all()

    if not carrito:
        flash('No hay pizzas en el pedido', 'warning')
        return redirect(url_for('pedidos.pedido'))

    total = sum(float(item.subtotal) for item in carrito)

    cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono)
    db.session.add(cliente)
    db.session.flush()

    nuevo_pedido = Pedido(
        id_cliente=cliente.id_cliente,
        fecha=datetime.datetime.strptime(fecha_form, '%Y-%m-%d') if fecha_form else datetime.datetime.now(),
        total=total
    )
    db.session.add(nuevo_pedido)
    db.session.flush()

    for item in carrito:
        detalle = DetallePedido(
            id_pedido=nuevo_pedido.id_pedido,
            id_pizza=item.id_pizza,
            cantidad=item.cantidad,
            subtotal=item.subtotal,
            ingredientes=item.ingredientes
    )
    db.session.add(detalle)

    CarritoTemp.query.delete()
    db.session.commit()

    flash(f'Pedido registrado. Total a pagar: ${total:.2f}', 'success')
    return redirect(url_for('pedidos.pedido'))