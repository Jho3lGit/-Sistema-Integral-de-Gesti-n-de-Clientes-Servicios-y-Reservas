"""Programa principal: menú de consola del Sistema Integral de Gestión de Software FJ."""

import logging  # Para registrar errores y eventos del menú

from modelos.gestor_servicios import GestorServicios  # Se importa primero: configura el log
from modelos.gestor_clientes import GestorClientes  # Gestor de clientes
from modelos.Reservas import Reserva, GestorReservas  # Reservas y su gestor
from modelos.excepciones import (  # Excepciones propias que usa el menú
    ClienteNoEncontradoError,  # No hay clientes registrados
    DatosInvalidosError,  # Entrada vacía, no numérica u opción inexistente
    ReservaInvalidaError,  # No hay reservas registradas
    ServicioNoEncontradoError,  # No hay servicios registrados
    SoftwareFJError,  # Base de todas las excepciones propias
)  # Cierra la importación
from simulacion import Simulacion  # Simulación automática de operaciones


class MenuSistema:  # Toda la interfaz está dentro de una clase, sin listas globales
    """Menú de consola que conecta al usuario con los gestores del sistema."""

    def __init__(self):  # Constructor del menú
        """Crea los gestores y la tabla de opciones."""
        self.__clientes = GestorClientes()  # Gestor de clientes del menú
        self.__servicios = GestorServicios()  # Gestor de servicios del menú
        self.__reservas = GestorReservas()  # Gestor de reservas del menú
        self.__opciones = {  # Número de opción -> (texto, método que la atiende)
            "1": ("Registrar cliente", self.registrar_cliente),  # Opción 1
            "2": ("Listar clientes", self.listar_clientes),  # Opción 2
            "3": ("Crear servicio", self.crear_servicio),  # Opción 3
            "4": ("Listar servicios", self.listar_servicios),  # Opción 4
            "5": ("Crear reserva", self.crear_reserva),  # Opción 5
            "6": ("Confirmar reserva", self.confirmar_reserva),  # Opción 6
            "7": ("Cancelar reserva", self.cancelar_reserva),  # Opción 7
            "8": ("Procesar reserva", self.procesar_reserva),  # Opción 8
            "9": ("Calcular costo de una reserva", self.calcular_costo),  # Opción 9
            "10": ("Listar reservas", self.listar_reservas),  # Opción 10
            "11": ("Ejecutar simulación automática", self.ejecutar_simulacion),  # Opción 11
        }  # Cierra la tabla de opciones

    # ---------- Lectura de datos ----------

    def __leer_texto(self, mensaje):  # Lee un texto obligatorio
        """Pide un texto; lanza DatosInvalidosError si queda vacío."""
        texto = input(mensaje).strip()  # Lee y quita espacios externos
        if not texto:  # Revisa que no esté vacío
            logging.error(f"Menú: dato obligatorio vacío ({mensaje.strip()})")  # Registra el error
            raise DatosInvalidosError("El dato es obligatorio y no puede quedar vacío.")  # Avisa con excepción propia
        return texto  # Retorna el texto leído

    def __leer_numero(self, mensaje, opcional=False):  # Lee un número entero o decimal
        """Pide un número; si es opcional y queda vacío retorna 0. Lanza DatosInvalidosError si no es número."""
        texto = input(mensaje).strip()  # Lee y quita espacios externos
        if not texto and opcional:  # Dato opcional sin valor
            return 0  # Usa cero por defecto
        try:  # Intenta convertir el texto
            return int(texto) if texto.lstrip("-").isdigit() else float(texto)  # Entero si son dígitos; si no, decimal
        except ValueError as e:  # El texto no es un número
            logging.error(f"Menú: valor no numérico '{texto}' ({mensaje.strip()})")  # Registra el error
            raise DatosInvalidosError(f"'{texto}' no es un número válido.") from e  # Encadena con la causa original

    def __leer_posicion(self, mensaje, cantidad):  # Lee una posición de una lista mostrada
        """Pide un número entre 1 y cantidad y retorna el índice (desde 0)."""
        numero = self.__leer_numero(mensaje)  # Lee el número
        if not isinstance(numero, int) or not 1 <= numero <= cantidad:  # Debe ser entero y estar en el rango
            logging.error(f"Menú: selección fuera de rango ({numero}); hay {cantidad} elementos.")  # Registra el error
            raise DatosInvalidosError(f"Seleccione un número entre 1 y {cantidad}.")  # Avisa con excepción propia
        return numero - 1  # Convierte a índice de lista

    # ---------- Selección de datos existentes ----------

    def __exigir_clientes(self):  # Aviso cuando no hay clientes
        """Lanza ClienteNoEncontradoError si no hay clientes registrados."""
        if not self.__clientes.listar_clientes():  # listar_clientes avisa y retorna [] si no hay
            logging.error("Menú: se intentó una acción que requiere clientes, pero no hay ninguno.")  # Registra
            raise ClienteNoEncontradoError("Primero registre al menos un cliente (opción 1).")  # Avisa

    def __seleccionar_servicio(self):  # Muestra los servicios y pide uno
        """Lista los servicios y retorna el elegido; avisa si no hay servicios."""
        lista = self.__servicios.listar_servicios()  # Descripciones de los servicios
        if not lista:  # No hay servicios registrados
            logging.error("Menú: se intentó una acción que requiere servicios, pero no hay ninguno.")  # Registra
            raise ServicioNoEncontradoError("Primero cree al menos un servicio (opción 3).")  # Avisa
        for numero, linea in enumerate(lista, start=1):  # Recorre los servicios numerados
            print(f"  {numero}. {linea}")  # Muestra cada servicio
        indice = self.__leer_posicion("Número del servicio: ", len(lista))  # Pide la selección
        return self.__servicios.obtener_servicio(indice)  # Retorna el servicio elegido

    def __seleccionar_reserva(self):  # Muestra las reservas y pide una
        """Lista las reservas y retorna la elegida; avisa si no hay reservas."""
        lista = self.__reservas.listar_reservas()  # Descripciones de las reservas
        if not lista:  # No hay reservas registradas
            logging.error("Menú: se intentó una acción sobre reservas, pero no hay ninguna.")  # Registra
            raise ReservaInvalidaError("Primero cree al menos una reserva (opción 5).")  # Avisa
        for numero, linea in enumerate(lista, start=1):  # Recorre las reservas numeradas
            print(f"  {numero}. {linea}")  # Muestra cada reserva
        indice = self.__leer_posicion("Número de la reserva: ", len(lista))  # Pide la selección
        return self.__reservas.buscar_reserva(indice)  # Retorna la reserva elegida

    # ---------- Acciones del menú ----------

    def registrar_cliente(self):  # Opción 1
        """Pide los datos y registra un cliente."""
        nombre = self.__leer_texto("Nombre: ")  # Lee el nombre
        correo = self.__leer_texto("Correo: ")  # Lee el correo
        telefono = self.__leer_texto("Teléfono (7 a 10 dígitos): ")  # Lee el teléfono
        print(f"Registrado: {self.__clientes.registrar_cliente(nombre, correo, telefono)}")  # Registra y muestra

    def listar_clientes(self):  # Opción 2
        """Muestra los clientes registrados (o un aviso si no hay)."""
        for linea in self.__clientes.listar_clientes():  # listar_clientes avisa si está vacío
            print(f"  {linea}")  # Muestra cada cliente

    def crear_servicio(self):  # Opción 3
        """Pide el tipo y los datos del servicio y lo crea."""
        tipo = self.__leer_texto("Tipo (sala / equipo / asesoria): ").lower()  # Lee el tipo
        nombre = self.__leer_texto("Nombre del servicio: ")  # Lee el nombre
        precio = self.__leer_numero("Tarifa base: ")  # Lee la tarifa
        extras = {}  # Parámetros propios de cada tipo
        if tipo == "sala":  # Datos de la sala
            extras["capacidad"] = self.__leer_numero("Capacidad (personas): ")  # Lee la capacidad
        elif tipo == "equipo":  # Datos del equipo
            extras["tipo_equipo"] = self.__leer_texto("Tipo de equipo: ")  # Lee el tipo de equipo
            extras["deposito"] = self.__leer_numero("Depósito (vacío = 0): ", opcional=True)  # Lee el depósito
        elif tipo == "asesoria":  # Datos de la asesoría
            extras["nivel"] = self.__leer_texto("Nivel (junior / senior / experto): ")  # Lee el nivel
        servicio = self.__servicios.crear_servicio(tipo, nombre, precio, **extras)  # El gestor valida y registra
        print(f"Creado: {servicio}")  # Muestra el servicio creado

    def listar_servicios(self):  # Opción 4
        """Muestra los servicios registrados (o un aviso si no hay)."""
        for linea in self.__servicios.listar_servicios():  # listar_servicios avisa si está vacío
            print(f"  {linea}")  # Muestra cada servicio

    def crear_reserva(self):  # Opción 5
        """Pide cliente, servicio y duración y crea la reserva."""
        self.__exigir_clientes()  # Avisa si no hay clientes
        cliente = self.__clientes.buscar_cliente(self.__leer_texto("Correo del cliente: "))  # Busca el cliente
        servicio = self.__seleccionar_servicio()  # Elige el servicio
        duracion = self.__leer_numero("Duración (horas o días según el servicio): ")  # Lee la duración
        reserva = Reserva(cliente, servicio, duracion)  # Reserva valida los datos
        self.__reservas.agregar_reserva(reserva)  # La guarda en el gestor
        print(f"Creada: {reserva}")  # Muestra la reserva

    def confirmar_reserva(self):  # Opción 6
        """Confirma la reserva elegida."""
        reserva = self.__seleccionar_reserva()  # Elige la reserva
        reserva.confirmar()  # Confirma (lanza excepción si no se puede)
        print(f"Confirmada: {reserva}")  # Muestra el resultado

    def cancelar_reserva(self):  # Opción 7
        """Cancela la reserva elegida."""
        reserva = self.__seleccionar_reserva()  # Elige la reserva
        reserva.cancelar()  # Cancela (lanza excepción si ya estaba cancelada)
        print(f"Cancelada: {reserva}")  # Muestra el resultado

    def procesar_reserva(self):  # Opción 8
        """Procesa la reserva elegida."""
        self.__seleccionar_reserva().procesar()  # Procesa (lanza excepción si no está confirmada)

    def calcular_costo(self):  # Opción 9
        """Calcula el costo de la reserva elegida con impuesto y descuento opcionales."""
        reserva = self.__seleccionar_reserva()  # Elige la reserva
        impuesto = self.__leer_numero("Impuesto % (vacío = 0): ", opcional=True)  # Lee el impuesto
        descuento = self.__leer_numero("Descuento % (vacío = 0): ", opcional=True)  # Lee el descuento
        costo = reserva.calcular_costo(impuesto=impuesto, descuento=descuento)  # Cada servicio aplica su regla
        print(f"Costo: ${costo:,.2f}")  # Muestra el costo

    def listar_reservas(self):  # Opción 10
        """Muestra las reservas registradas (o un aviso si no hay)."""
        lista = self.__reservas.listar_reservas()  # Descripciones de las reservas
        if not lista:  # No hay reservas
            print("No hay reservas registradas todavía.")  # Aviso sin lanzar error
        for numero, linea in enumerate(lista, start=1):  # Recorre las reservas
            print(f"  {numero}. {linea}")  # Muestra cada reserva

    def ejecutar_simulacion(self):  # Opción 11
        """Ejecuta la simulación automática con sus propios gestores."""
        Simulacion().ejecutar()  # Corre la simulación completa

    # ---------- Ciclo principal ----------

    def __mostrar_menu(self):  # Imprime las opciones
        """Muestra el menú principal."""
        print("\n===== SOFTWARE FJ - MENÚ PRINCIPAL =====")  # Título
        for clave, (texto, _) in self.__opciones.items():  # Recorre las opciones
            print(f"{clave:>2}. {texto}")  # Muestra cada opción
        print(" 0. Salir")  # Opción de salida

    def ejecutar(self):  # Ciclo del menú
        """Repite el menú hasta que el usuario elija salir; ningún error lo detiene."""
        logging.info("Menú: inicio del programa")  # Registra el inicio
        while True:  # Repite hasta que el usuario salga
            self.__mostrar_menu()  # Muestra las opciones
            try:  # Bloque donde puede ocurrir un error
                opcion = input("Seleccione una opción: ").strip()  # Lee la opción
                if opcion == "0":  # El usuario quiere salir
                    break  # Sale del ciclo
                if opcion not in self.__opciones:  # Opción vacía o inexistente
                    logging.error(f"Menú: opción no válida '{opcion}'.")  # Registra el error
                    raise DatosInvalidosError(f"La opción '{opcion}' no existe. Elija un número del menú.")  # Avisa
                texto, accion = self.__opciones[opcion]  # Obtiene la acción elegida
                accion()  # Ejecuta la acción
            except SoftwareFJError as e:  # Error propio: ya quedó registrado donde se lanzó
                print(f"Error: {e}")  # Lo muestra y el menú continúa
            except (EOFError, KeyboardInterrupt):  # Fin de la entrada o Ctrl+C
                print("\nEntrada interrumpida. Cerrando el programa.")  # Aviso
                logging.info("Menú: entrada interrumpida por el usuario.")  # Registra el evento
                break  # Sale de forma ordenada
            except Exception as e:  # Cualquier error inesperado
                logging.error(f"Menú: error inesperado {type(e).__name__}: {e}")  # Lo registra
                print(f"Error inesperado: {e}. El programa continúa.")  # Lo muestra y el menú continúa
            else:  # Solo si la opción se completó sin errores
                logging.info(f"Menú: opción '{texto}' completada.")  # Registra el evento exitoso
            finally:  # Se ejecuta siempre, haya error o no
                print("-" * 40)  # Separador visual entre operaciones
        logging.info("Menú: fin del programa")  # Registra el cierre
        print("Hasta luego.")  # Despedida


if __name__ == "__main__":  # Punto de entrada: python main.py
    MenuSistema().ejecutar()  # Crea el menú y lo ejecuta
