from modelos.gestor_servicios import GestorServicios
from modelos.gestor_clientes import GestorClientes
from modelos.Reservas import Reserva, GestorReservas
from modelos.excepciones import (
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    TarifaInvalidaError,
)


def ejecutar_pruebas():
    print("=== INICIANDO PRUEBAS DE INTEGRACIÓN DEL SISTEMA ===\n")

    clientes = GestorClientes()
    servicios = GestorServicios()
    reservas = GestorReservas()

    # 1. Registro de clientes y control de duplicados
    c1 = clientes.registrar_cliente("Carlos Ruiz", "carlos@correo.com", "3105551234")
    assert c1.identificador >= 1
    try:
        clientes.registrar_cliente("Carlos Duplicado", "CARLOS@correo.com", "3105559999")
        assert False, "Debió fallar por correo duplicado"
    except ClienteDuplicadoError:
        print("[OK] Validación de cliente duplicado.")

    # 2. Creación de los 3 tipos de servicios
    sala = servicios.crear_servicio("sala", "Auditorio Principal", 120000, capacidad=50)
    equipo = servicios.crear_servicio("equipo", "Cámara 4K", 90000, tipo_equipo="Video", deposito=150000)
    asesoria = servicios.crear_servicio("asesoria", "Consultoría Cloud", 150000, nivel="Experto")

    # 2.1 Servicios inválidos: no deben crearse ni quedar registrados en el gestor
    total_antes = len(servicios.listar_servicios())
    try:
        servicios.crear_servicio("sala", "Sala Tarifa Negativa", -50000, capacidad=10)
        assert False, "Debió fallar por tarifa negativa"
    except TarifaInvalidaError as e:
        print(f"[OK] Servicio inválido (tarifa negativa) rechazado: {e}")
    try:
        servicios.crear_servicio("asesoria", "Asesoría Nivel Inexistente", 80000, nivel="master")
        assert False, "Debió fallar por nivel inexistente"
    except DatosInvalidosError as e:
        print(f"[OK] Servicio inválido (nivel inexistente) rechazado: {e}")
    assert len(servicios.listar_servicios()) == total_antes, "Un servicio inválido quedó registrado"
    print("[OK] Los servicios inválidos no quedaron registrados en el gestor.")

    # 3. Flujo completo de reserva exitosa (Crear -> Confirmar -> Calcular costo -> Procesar)
    print("\n--- Reserva exitosa completa ---")
    cliente_buscado = clientes.buscar_cliente("carlos@correo.com")
    servicio_buscado = servicios.buscar_servicio("Auditorio Principal")

    reserva1 = Reserva(cliente_buscado, servicio_buscado, 4)
    reservas.agregar_reserva(reserva1)
    assert reserva1.estado == Reserva.ESTADO_PENDIENTE
    print(f"1) Creada:     {reserva1}")

    # Intentar procesar antes de confirmar debe lanzar ReservaInvalidaError
    try:
        reserva1.procesar()
        assert False, "Debió fallar al procesar sin confirmar"
    except ReservaInvalidaError:
        print("[OK] Bloqueo de procesamiento en estado PENDIENTE.")

    reserva1.confirmar()
    assert reserva1.estado == Reserva.ESTADO_CONFIRMADA
    print(f"2) Confirmada: {reserva1}")
    costo_sala = reserva1.calcular_costo(impuesto=19, descuento=10)
    # 120,000 * 4 = 480,000 -> -10% = 432,000 -> +19% IVA = 514,080.0
    assert costo_sala == 514080.0, f"Costo inesperado: {costo_sala}"
    print(f"3) Costo:      ${costo_sala:,.2f} (IVA 19%, descuento 10%)")
    reserva1.procesar()
    assert reserva1.costo == costo_sala
    print(f"4) Procesada:  {reserva1}")
    print(f"[OK] Flujo completo de reserva de sala confirmado. Total: ${costo_sala:,.2f}")

    # 4. Cálculo polimórfico con equipo (incluye depósito sin IVA/descuento)
    reserva2 = Reserva(c1, equipo, 2)
    reservas.agregar_reserva(reserva2)
    costo_equipo = reserva2.calcular_costo(impuesto=19, descuento=0)
    # (90,000 * 2) * 1.19 + 150,000 = 214,200 + 150,000 = 364,200.0
    assert costo_equipo == 364200.0, f"Costo equipo inesperado: {costo_equipo}"
    print(f"[OK] Cálculo polimórfico en alquiler de equipo. Total: ${costo_equipo:,.2f}")

    # 5. Bloqueo al confirmar reserva de servicio no disponible
    asesoria.disponible = False
    reserva3 = Reserva(c1, asesoria, 1)
    try:
        reserva3.confirmar()
        assert False, "Debió fallar por servicio no disponible"
    except ServicioNoDisponibleError:
        print("[OK] Bloqueo de confirmación cuando el servicio no está disponible.")

    # 6. Búsqueda de cliente inexistente
    try:
        clientes.buscar_cliente("inexistente@correo.com")
        assert False, "Debió fallar por cliente inexistente"
    except ClienteNoEncontradoError:
        print("[OK] Excepción controlada para cliente inexistente.")

    print("\n=== TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON EXITOSAMENTE ===")


if __name__ == "__main__":
    ejecutar_pruebas()
