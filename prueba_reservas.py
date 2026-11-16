
"""Prueba de Reservas.py integrada con los servicios (casos válidos e inválidos)."""

from modelos.gestor_servicios import GestorServicios  # Se importa primero: configura el log
from modelos.Reservas import Reserva, GestorReservas  # Clases de reservas
from modelos.excepciones import SoftwareFJError  # Base de las excepciones propias


class ClientePrueba:  # Cliente provisional hasta que exista la clase Cliente (Issue #3)
    def __init__(self, nombre):  # Solo necesita el nombre
        self.nombre = nombre  # Atributo que usa Reserva


def probar(descripcion, accion):  # Ejecuta una prueba y muestra el resultado o el error
    print(f"\n>> {descripcion}")  # Qué se prueba
    try:  # Intenta la acción
        resultado = accion()  # Ejecuta la función recibida
    except SoftwareFJError as e:  # Captura errores propios para no detener el script
        print(f"   ERROR {type(e).__name__}: {e}")  # Muestra tipo y mensaje
    else:  # Si no hubo error
        print(f"   OK: {resultado}")  # Muestra el resultado


servicios = GestorServicios()  # Gestor que crea los servicios
sala = servicios.crear_servicio("sala", "Sala Juntas", 50000, capacidad=12)  # Servicio 1
equipo = servicios.crear_servicio("equipo", "Portátil Dell", 80000,
                                  tipo_equipo="Portátil", deposito=200000)  # Servicio 2
asesoria = servicios.crear_servicio("asesoria", "Asesoría BD", 100000, nivel="Senior")  # Servicio 3
cliente = ClientePrueba("Cliente Demo")  # Cliente de prueba
gestor = GestorReservas()  # Gestor de reservas

r1 = Reserva(cliente, sala, 3)  # Reserva válida de la sala por 3 horas
gestor.agregar_reserva(r1)  # La guarda en el gestor
probar("1. Reserva creada", lambda: r1)
probar("2. Procesar sin confirmar", r1.procesar)  # ReservaInvalidaError
probar("3. Confirmar", lambda: (r1.confirmar(), r1.estado)[1])
probar("4. Procesar confirmada", r1.procesar)
probar("5. Costo sala 3 h con IVA 19%", lambda: r1.calcular_costo(impuesto=19))  # Delega al servicio
r2 = Reserva(cliente, equipo, 2)  # Reserva del equipo por 2 días
probar("6. Costo equipo 2 días", r2.calcular_costo)  # Otra regla, mismo método
probar("7. Cancelar", lambda: (r1.cancelar(), r1.estado)[1])
probar("8. Cancelar dos veces", r1.cancelar)  # ReservaInvalidaError
probar("9. Confirmar cancelada", r1.confirmar)  # ReservaInvalidaError
probar("10. Servicio None", lambda: Reserva(cliente, None, 2))
probar("11. Cliente None", lambda: Reserva(None, sala, 2))
probar("12. Duración negativa", lambda: Reserva(cliente, sala, -1))
asesoria.disponible = False  # Desactiva la asesoría
r3 = Reserva(cliente, asesoria, 2)  # Reserva sobre un servicio no disponible
probar("13. Confirmar servicio no disponible", r3.confirmar)
probar("14. Buscar reserva inexistente", lambda: gestor.buscar_reserva(9))
print(gestor.listar_reservas())  # Muestra las reservas guardadas