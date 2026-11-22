from modelos.gestor_servicios import GestorServicios  # Configura también el archivo logs/sistema.log
from modelos.gestor_clientes import GestorClientes
from modelos.Reservas import Reserva, GestorReservas
from modelos.excepciones import SoftwareFJError


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  [!] Por favor, ingrese un número entero válido.")


def leer_flotante(mensaje, permitir_vacio=False, valor_defecto=0.0):
    while True:
        entrada = input(mensaje).strip()
        if permitir_vacio and entrada == "":
            return valor_defecto
        try:
            return float(entrada)
        except ValueError:
            print("  [!] Por favor, ingrese un valor numérico válido.")


def cargar_datos_demo(gestor_clientes, gestor_servicios, gestor_reservas):
    """Carga datos iniciales para facilitar las pruebas del menú."""
    try:
        c1 = gestor_clientes.registrar_cliente("Ana Gómez", "ana@correo.com", "3001234567")
        c2 = gestor_clientes.registrar_cliente("Luis Pérez", "luis.perez@empresa.co", "6041234")

        s1 = gestor_servicios.crear_servicio("sala", "Sala Juntas", 50000, capacidad=12)
        s2 = gestor_servicios.crear_servicio(
            "equipo", "Portátil Dell", 80000, tipo_equipo="Portátil", deposito=200000
        )
        gestor_servicios.crear_servicio("asesoria", "Asesoría BD", 100000, nivel="Senior")

        r1 = Reserva(c1, s1, 3)
        r1.confirmar()
        gestor_reservas.agregar_reserva(r1)

        r2 = Reserva(c2, s2, 2)
        gestor_reservas.agregar_reserva(r2)
        print("\n  [OK] Datos de prueba cargados correctamente.")
    except SoftwareFJError as e:
        print(f"\n  [!] Aviso al cargar datos demo: {e}")


# ==================== SUBMENÚ CLIENTES ====================
def menu_clientes(gestor_clientes):
    while True:
        print("\n--- GESTIÓN DE CLIENTES ---")
        print("1. Registrar cliente")
        print("2. Buscar cliente por correo")
        print("3. Listar todos los clientes")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre completo: ")
            correo = input("Correo electrónico: ")
            telefono = input("Teléfono (7 a 10 dígitos): ")
            try:
                cliente = gestor_clientes.registrar_cliente(nombre, correo, telefono)
                print(f"  [OK] Cliente registrado: {cliente.describir()}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "2":
            correo = input("Ingrese el correo a buscar: ")
            try:
                cliente = gestor_clientes.buscar_cliente(correo)
                print(f"  [OK] Encontrado: {cliente.describir()}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "3":
            print("\nListado de clientes:")
            for linea in gestor_clientes.listar_clientes():
                print(f"  - {linea}")

        elif opcion == "0":
            break
        else:
            print("  [!] Opción no válida.")


# ==================== SUBMENÚ SERVICIOS ====================
def menu_servicios(gestor_servicios):
    while True:
        print("\n--- GESTIÓN DE SERVICIOS ---")
        print("1. Crear servicio (Sala / Equipo / Asesoría)")
        print("2. Listar todos los servicios")
        print("3. Listar solo servicios disponibles")
        print("4. Cambiar disponibilidad de un servicio")
        print("5. Cotizar costo de un servicio")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("Tipos disponibles: sala | equipo | asesoria")
            tipo = input("Tipo de servicio: ").strip().lower()
            nombre = input("Nombre del servicio: ")
            precio = leer_flotante("Tarifa base ($): ")

            try:
                if tipo == "sala":
                    capacidad = leer_entero("Capacidad de personas: ")
                    servicio = gestor_servicios.crear_servicio("sala", nombre, precio, capacidad=capacidad)
                elif tipo == "equipo":
                    tipo_equipo = input("Tipo de equipo (ej. Portátil, Proyector): ")
                    deposito = leer_flotante("Depósito reembolsable (Enter para 0): ", permitir_vacio=True)
                    servicio = gestor_servicios.crear_servicio(
                        "equipo", nombre, precio, tipo_equipo=tipo_equipo, deposito=deposito
                    )
                elif tipo == "asesoria":
                    nivel = input("Nivel (junior / senior / experto): ")
                    servicio = gestor_servicios.crear_servicio("asesoria", nombre, precio, nivel=nivel)
                else:
                    print("  [!] Tipo no reconocido. Use: sala, equipo o asesoria.")
                    continue

                print(f"  [OK] Servicio creado: {servicio.describir()}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "2":
            print("\nCatálogo completo de servicios:")
            for linea in gestor_servicios.listar_servicios(solo_disponibles=False):
                print(f"  - {linea}")

        elif opcion == "3":
            print("\nServicios disponibles:")
            for linea in gestor_servicios.listar_servicios(solo_disponibles=True):
                print(f"  - {linea}")

        elif opcion == "4":
            nombre = input("Nombre exacto del servicio: ")
            try:
                servicio = gestor_servicios.buscar_servicio(nombre)
                servicio.disponible = not servicio.disponible
                estado = "Disponible" if servicio.disponible else "No disponible"
                print(f"  [OK] Estado actualizado de '{servicio.nombre}': {estado}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "5":
            nombre = input("Nombre del servicio a cotizar: ")
            duracion = leer_flotante("Duración (horas o días enteros según servicio): ")
            if duracion.is_integer():
                duracion = int(duracion)
            impuesto = leer_flotante("Impuesto % (Enter para 0): ", permitir_vacio=True)
            descuento = leer_flotante("Descuento % (Enter para 0): ", permitir_vacio=True)
            try:
                costo = gestor_servicios.calcular_costo_servicio(nombre, duracion, impuesto, descuento)
                print(f"  [OK] Costo total calculado: ${costo:,.2f}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "0":
            break
        else:
            print("  [!] Opción no válida.")


# ==================== SUBMENÚ RESERVAS ====================
def menu_reservas(gestor_clientes, gestor_servicios, gestor_reservas):
    while True:
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Crear nueva reserva")
        print("2. Listar reservas")
        print("3. Confirmar reserva")
        print("4. Procesar reserva confirmada")
        print("5. Cancelar reserva")
        print("6. Calcular costo de una reserva")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            correo = input("Correo del cliente registrado: ")
            nombre_servicio = input("Nombre del servicio: ")
            duracion = leer_flotante("Duración (horas o días): ")
            if duracion.is_integer():
                duracion = int(duracion)

            try:
                cliente = gestor_clientes.buscar_cliente(correo)
                servicio = gestor_servicios.buscar_servicio(nombre_servicio)
                reserva = Reserva(cliente, servicio, duracion)
                gestor_reservas.agregar_reserva(reserva)
                print(f"  [OK] Reserva creada en estado PENDIENTE: {reserva}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "2":
            reservas = gestor_reservas.listar_reservas()
            if not reservas:
                print("  No hay reservas registradas todavía.")
            else:
                print("\nListado de reservas:")
                for idx, desc in enumerate(reservas):
                    print(f"  [{idx}] {desc}")

        elif opcion in {"3", "4", "5", "6"}:
            reservas = gestor_reservas.listar_reservas()
            if not reservas:
                print("  No hay reservas registradas.")
                continue
            for idx, desc in enumerate(reservas):
                print(f"  [{idx}] {desc}")

            indice = leer_entero("Ingrese el índice [número] de la reserva: ")
            try:
                reserva = gestor_reservas.buscar_reserva(indice)
                if opcion == "3":
                    reserva.confirmar()
                    print(f"  [OK] Reserva [{indice}] CONFIRMADA.")
                elif opcion == "4":
                    reserva.procesar()
                elif opcion == "5":
                    gestor_reservas.cancelar_reserva(indice)
                    print(f"  [OK] Reserva [{indice}] CANCELADA.")
                elif opcion == "6":
                    impuesto = leer_flotante("Impuesto % (Enter para 0): ", permitir_vacio=True)
                    descuento = leer_flotante("Descuento % (Enter para 0): ", permitir_vacio=True)
                    total = reserva.calcular_costo(impuesto=impuesto, descuento=descuento)
                    print(f"  [OK] Total a pagar por la reserva [{indice}]: ${total:,.2f}")
            except SoftwareFJError as e:
                print(f"  [ERROR] {e}")

        elif opcion == "0":
            break
        else:
            print("  [!] Opción no válida.")


# ==================== MENÚ PRINCIPAL ====================
def main():
    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()
    gestor_reservas = GestorReservas()

    while True:
        print("\n========================================================")
        print("   SISTEMA INTEGRAL DE CLIENTES, SERVICIOS Y RESERVAS   ")
        print("========================================================")
        print("1. Módulo de Clientes")
        print("2. Módulo de Servicios")
        print("3. Módulo de Reservas")
        print("4. Cargar datos de demostración (Pruebas rápidas)")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_clientes(gestor_clientes)
        elif opcion == "2":
            menu_servicios(gestor_servicios)
        elif opcion == "3":
            menu_reservas(gestor_clientes, gestor_servicios, gestor_reservas)
        elif opcion == "4":
            cargar_datos_demo(gestor_clientes, gestor_servicios, gestor_reservas)
        elif opcion == "0":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("  [!] Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
