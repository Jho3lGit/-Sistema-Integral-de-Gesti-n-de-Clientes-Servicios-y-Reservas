"""Simulación de operaciones completas del sistema Software FJ (válidas e inválidas)."""

import logging  # Para registrar el resultado de cada operación en el log

from modelos.gestor_servicios import GestorServicios  # Se importa primero: configura el log
from modelos.gestor_clientes import GestorClientes  # Gestor de clientes
from modelos.Reservas import Reserva, GestorReservas  # Reservas y su gestor
from modelos.excepciones import SoftwareFJError  # Base de las excepciones propias


class Simulacion:  # Agrupa la simulación en una clase, sin variables globales
    """Ejecuta operaciones válidas e inválidas sobre clientes, servicios y reservas."""

    def __init__(self):  # Constructor de la simulación
        """Crea gestores nuevos para que la simulación sea independiente del menú."""
        self.__clientes = GestorClientes()  # Gestor de clientes de la simulación
        self.__servicios = GestorServicios()  # Gestor de servicios de la simulación
        self.__reservas = GestorReservas()  # Gestor de reservas de la simulación
        self.__exitosas = 0  # Contador de operaciones que terminaron como se esperaba
        self.__inesperadas = 0  # Contador de operaciones con un resultado no esperado

    def __operacion(self, numero, descripcion, accion, espera_error=False):  # Ejecuta una operación aislada
        """Ejecuta una operación; si falla, registra el error y la simulación continúa."""
        tipo = "inválida" if espera_error else "válida"  # Texto según el tipo de operación
        print(f"\n[{numero}] {descripcion} ({tipo})")  # Muestra qué operación se ejecuta
        logging.info(f"Simulación - operación {numero} ({tipo}): {descripcion}")  # Marca el inicio en el log
        try:  # Bloque donde puede ocurrir un error
            resultado = accion()  # Ejecuta la operación
        except SoftwareFJError as e:  # Error propio del sistema (ya registrado por el módulo que lo lanzó)
            print(f"    Error controlado: {type(e).__name__}: {e}")  # Muestra el error sin detener el programa
            if e.__cause__:  # Si el error fue encadenado con raise ... from
                print(f"    Causa original: {type(e.__cause__).__name__}")  # Muestra la causa
            esperado = espera_error  # Un error es correcto solo si se esperaba
        except Exception as e:  # Error inesperado de Python: se registra y la simulación sigue
            logging.error(f"Simulación - operación {numero}: error inesperado {type(e).__name__}: {e}")  # Lo registra
            print(f"    Error inesperado: {type(e).__name__}: {e}")  # Lo muestra
            esperado = False  # Nunca se espera un error genérico
        else:  # Solo si la operación no lanzó errores
            print(f"    OK: {resultado}")  # Muestra el resultado
            esperado = not espera_error  # Un éxito es correcto solo si no se esperaba error
        finally:  # Se ejecuta siempre, haya error o no
            logging.info(f"Simulación - fin de la operación {numero}.")  # Marca el cierre en el log
        if esperado:  # El resultado coincide con lo previsto
            self.__exitosas += 1  # Suma una operación correcta
        else:  # El resultado no coincide con lo previsto
            self.__inesperadas += 1  # Suma una operación inesperada
            logging.error(f"Simulación - operación {numero} no tuvo el resultado esperado.")  # Lo registra

    def __reserva_completa(self, correo, servicio, duracion, impuesto, descuento):  # Flujo exitoso completo
        """Crea, confirma, calcula el costo y procesa una reserva."""
        cliente = self.__clientes.buscar_cliente(correo)  # Busca el cliente por correo
        reserva = Reserva(cliente, self.__servicios.buscar_servicio(servicio), duracion)  # Crea la reserva
        self.__reservas.agregar_reserva(reserva)  # La guarda en el gestor
        reserva.confirmar()  # Confirma la reserva
        costo = reserva.calcular_costo(impuesto=impuesto, descuento=descuento)  # Calcula el costo (sobrecarga)
        reserva.procesar()  # Procesa la reserva confirmada
        return f"{reserva} | Costo: ${costo:,.2f}"  # Retorna el resumen

    def __nueva_reserva(self, correo, servicio, duracion):  # Apoyo para las reservas fallidas
        """Crea una reserva y la agrega al gestor."""
        cliente = self.__clientes.buscar_cliente(correo)  # Busca el cliente por correo
        reserva = Reserva(cliente, self.__servicios.buscar_servicio(servicio), duracion)  # Crea la reserva
        self.__reservas.agregar_reserva(reserva)  # La guarda en el gestor
        return reserva  # Retorna la reserva creada

    def __cancelar_y_confirmar(self):  # Operación no permitida
        """Cancela una reserva y luego intenta confirmarla."""
        reserva = self.__nueva_reserva("ana@correo.com", "Sala Juntas", 2)  # Crea una reserva
        reserva.cancelar()  # La cancela (evento válido)
        reserva.confirmar()  # Confirmar una cancelada no está permitido

    def __desactivar_y_confirmar(self):  # Servicio no disponible
        """Desactiva la asesoría e intenta confirmar una reserva sobre ella."""
        self.__servicios.buscar_servicio("Asesoría Cloud").disponible = False  # Marca el servicio como no disponible
        self.__nueva_reserva("luis@correo.com", "Asesoría Cloud", 1).confirmar()  # Confirmar debe fallar

    def ejecutar(self):  # Corre todas las operaciones
        """Ejecuta las operaciones de la simulación y muestra un resumen."""
        c = self.__clientes  # Alias corto del gestor de clientes
        s = self.__servicios  # Alias corto del gestor de servicios
        print("=== SIMULACIÓN SOFTWARE FJ ===")  # Título
        logging.info("Simulación - inicio")  # Marca el inicio en el log
        self.__operacion(1, "Registrar cliente Ana Gómez", lambda: c.registrar_cliente(  # Cliente válido
            "Ana Gómez", "ana@correo.com", "3001234567"))  # Datos correctos
        self.__operacion(2, "Registrar cliente Luis Pérez", lambda: c.registrar_cliente(  # Cliente válido
            "Luis Pérez", "luis@correo.com", "6041234"))  # Teléfono fijo de 7 dígitos
        self.__operacion(3, "Registrar cliente con correo mal formado", lambda: c.registrar_cliente(  # Inválido
            "Eva Ruiz", "eva.correo.com", "3001112233"), espera_error=True)  # Correo sin @
        self.__operacion(4, "Registrar cliente con teléfono con letras", lambda: c.registrar_cliente(  # Inválido
            "Eva Ruiz", "eva@correo.com", "300ABC4567"), espera_error=True)  # Teléfono inválido
        self.__operacion(5, "Registrar cliente con correo duplicado", lambda: c.registrar_cliente(  # Inválido
            "Ana B", "ANA@correo.com", "3009998877"), espera_error=True)  # Mismo correo de la operación 1
        self.__operacion(6, "Crear sala Sala Juntas", lambda: s.crear_servicio(  # Servicio válido
            "sala", "Sala Juntas", 50000, capacidad=12))  # Cobro por hora
        self.__operacion(7, "Crear equipo Portátil Dell", lambda: s.crear_servicio(  # Servicio válido
            "equipo", "Portátil Dell", 80000, tipo_equipo="Portátil", deposito=200000))  # Cobro por día
        self.__operacion(8, "Crear asesoría Asesoría Cloud", lambda: s.crear_servicio(  # Servicio válido
            "asesoria", "Asesoría Cloud", 100000, nivel="Senior"))  # Tarifa según nivel
        self.__operacion(9, "Crear servicio con tarifa negativa", lambda: s.crear_servicio(  # Servicio inválido
            "sala", "Sala B", -100, capacidad=5), espera_error=True)  # TarifaInvalidaError
        self.__operacion(10, "Crear asesoría con nivel inexistente", lambda: s.crear_servicio(  # Servicio inválido
            "asesoria", "Asesoría X", 90000, nivel="master"), espera_error=True)  # DatosInvalidosError
        self.__operacion(11, "Reserva de sala completa (crear, confirmar, costo y procesar)",  # Reserva exitosa
                         lambda: self.__reserva_completa("ana@correo.com", "Sala Juntas", 3, 19, 10))  # IVA y descuento
        self.__operacion(12, "Reserva de equipo completa (crear, confirmar, costo y procesar)",  # Reserva exitosa
                         lambda: self.__reserva_completa("luis@correo.com", "Portátil Dell", 2, 19, 0))  # Polimorfismo
        self.__operacion(13, "Reserva con duración de tipo texto", lambda: self.__nueva_reserva(  # Reserva fallida
            "ana@correo.com", "Sala Juntas", "dos"), espera_error=True)  # DatosInvalidosError
        self.__operacion(14, "Procesar una reserva sin confirmar", lambda: self.__nueva_reserva(  # Reserva fallida
            "ana@correo.com", "Sala Juntas", 1).procesar(), espera_error=True)  # ReservaInvalidaError
        self.__operacion(15, "Cancelar una reserva y luego confirmarla",  # Operación no permitida
                         self.__cancelar_y_confirmar, espera_error=True)  # ReservaInvalidaError
        self.__operacion(16, "Confirmar reserva de un servicio no disponible",  # Servicio no disponible
                         self.__desactivar_y_confirmar, espera_error=True)  # ServicioNoDisponibleError
        self.__operacion(17, "Reservar con un cliente inexistente", lambda: self.__nueva_reserva(  # Reserva fallida
            "nadie@correo.com", "Sala Juntas", 2), espera_error=True)  # ClienteNoEncontradoError
        self.__operacion(18, "Calcular costo con descuento de 150%", lambda: self.__reservas.buscar_reserva(  # Cálculo inválido
            0).calcular_costo(descuento=150), espera_error=True)  # DatosInvalidosError
        total = self.__exitosas + self.__inesperadas  # Total de operaciones ejecutadas
        print(f"\n=== RESUMEN: {total} operaciones, {self.__exitosas} con el resultado esperado, "  # Muestra el resumen
              f"{self.__inesperadas} inesperadas ===")  # Completa el resumen
        logging.info(f"Simulación - fin: {total} operaciones, {self.__exitosas} con el resultado esperado, "  # Lo registra
                     f"{self.__inesperadas} inesperadas.")  # Completa el registro
        return self.__inesperadas == 0  # True si todo salió como se esperaba


if __name__ == "__main__":  # Permite ejecutar la simulación sola: python simulacion.py
    Simulacion().ejecutar()  # Crea la simulación y la ejecuta
