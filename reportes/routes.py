from . import reportes
from flask import render_template, request, flash
from models import db, Pedido, DetallePedido
import datetime

MESES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

DIAS = {
    'lunes': 2, 'martes': 3, 'miércoles': 4, 'miercoles': 4,
    'jueves': 5, 'viernes': 6, 'sábado': 7, 'sabado': 7, 'domingo': 1
}

@reportes.route('/reportes', methods=['GET', 'POST'])
def reporte():
    ventas_dia   = []
    ventas_mes   = []
    total_dia    = 0
    total_mes    = 0
    busqueda_dia = ''
    busqueda_mes = ''

    if request.method == 'POST':

        # ── Consulta por día de la semana ────────────────────
        busqueda_dia = request.form.get('dia', '').strip().lower()
        if busqueda_dia:
            numero_dia = DIAS.get(busqueda_dia)
            if numero_dia is not None:
                ventas_dia = db.session.query(Pedido).filter(
                    db.func.dayofweek(Pedido.fecha) == numero_dia
                ).all()
                total_dia = sum(float(v.total) for v in ventas_dia)
            else:
                flash('Día no reconocido. Escribe el nombre completo en español (Ejemplo: lunes)', 'warning')

        # ── Consulta por mes ─────────────────────────────────
        busqueda_mes = request.form.get('mes', '').strip().lower()
        if busqueda_mes:
            numero_mes = MESES.get(busqueda_mes)
            if numero_mes is not None:
                ventas_mes = db.session.query(Pedido).filter(
                    db.func.month(Pedido.fecha) == numero_mes
                ).all()
                total_mes = sum(float(v.total) for v in ventas_mes)
            else:
                flash('Mes no reconocido. Escribe el nombre completo en español (Ejemplo: marzo)', 'warning')

    return render_template('reportes/index.html',
                           ventas_dia=ventas_dia,
                           ventas_mes=ventas_mes,
                           total_dia=total_dia,
                           total_mes=total_mes,
                           busqueda_dia=busqueda_dia,
                           busqueda_mes=busqueda_mes)

@reportes.route('/reportes/detalle/<int:id_pedido>')
def detalle(id_pedido):
    pedido   = db.session.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    detalles = db.session.query(DetallePedido).filter(DetallePedido.id_pedido == id_pedido).all()
    return render_template('reportes/detalle.html', pedido=pedido, detalles=detalles)