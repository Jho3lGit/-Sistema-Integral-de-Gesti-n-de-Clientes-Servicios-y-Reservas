import logging  # Librería estándar para registrar errores y eventos

from modelos.cliente import Cliente  # Clase de los clientes
from modelos.excepciones import (  # Excepciones personalizadas que usa el gestor
    ClienteDuplicadoError,  # Error cuando el correo ya está registrado
    ClienteInvalidoError,  # Error de datos de cliente no válidos
    ClienteNoEncontradoError,  # Error cuando el cliente buscado no existe
    SoftwareFJError,  # Base de todas las excepciones propias
)  # Cierra la importación


class GestorClientes:  # Administra todos los clientes en una lista interna

    def __init__(self):  # Constructor del gestor
        self.__clientes = []  # Lista privada donde se guardan los clientes

    def registrar_cliente(self, nombre=None, correo=None, telefono=None):  # Parámetros en None para detectar faltantes
        try:  # Bloque donde puede ocurrir un error
            if isinstance(correo, str) and self.__existe(correo):  # Revisa duplicados antes de crear el cliente
                raise ClienteDuplicadoError(f"Ya existe un cliente con el correo '{correo.strip().lower()}'.")  # Avisa
            cliente = Cliente(nombre, correo, telefono)  # Crea el cliente; sus setters validan los datos
        except SoftwareFJError as e:  # Errores propios ya controlados (datos inválidos, duplicado)
            logging.error(f"No se pudo registrar el cliente '{nombre}': {type(e).__name__}: {e}")  # Registra el error
            raise  # Vuelve a lanzar la misma excepción para que quien llamó la maneje
        except Exception as e:  # Cualquier error inesperado
            logging.error(f"Error inesperado al registrar el cliente '{nombre}': {e}")  # Registra el error
            raise ClienteInvalidoError("Error inesperado al registrar el cliente.") from e  # Encadena con la causa
        else:  # Solo se ejecuta si no hubo ningún error
            self.__clientes.append(cliente)  # Guarda el cliente en la lista
            logging.info(f"Cliente registrado: {cliente.describir()}")  # Registra el evento exitoso
            return cliente  # Retorna el cliente creado
        finally:  # Se ejecuta siempre, haya error o no
            logging.info(f"Finalizó el intento de registro del cliente con correo '{correo}'.")  # Registra el cierre

    def __existe(self, correo):  # Método privado de apoyo
        correo_buscado = correo.strip().lower()  # Normaliza el correo igual que lo hace Cliente
        return any(c.correo == correo_buscado for c in self.__clientes)  # True si encuentra coincidencia

    def buscar_cliente(self, correo):  # Busca por correo
        if not isinstance(correo, str) or not correo.strip():  # Valida que se haya enviado un correo
            logging.error("Se intentó buscar un cliente sin indicar el correo.")  # Registra el error
            raise ClienteInvalidoError("Debe indicar el correo del cliente a buscar.")  # Avisa parámetro faltante
        correo_buscado = correo.strip().lower()  # Normaliza el correo recibido
        try:  # Intenta encontrar el primer cliente con ese correo
            cliente = next(c for c in self.__clientes if c.correo == correo_buscado)  # next() falla si no hay ninguno
        except StopIteration as e:  # next() lanza StopIteration cuando no encuentra coincidencias
            logging.error(f"Cliente no encontrado: '{correo_buscado}'.")  # Registra el error
            raise ClienteNoEncontradoError(f"No existe un cliente con el correo '{correo_buscado}'.") from e  # Encadena
        else:  # Solo si se encontró el cliente
            logging.info(f"Cliente encontrado: {cliente.describir()}")  # Registra el evento
            return cliente  # Retorna el cliente encontrado

    def listar_clientes(self):  # Lista todos los clientes
        if not self.__clientes:  # Revisa si la lista está vacía
            mensaje = "No hay clientes registrados todavía."  # Texto del aviso
            print(mensaje)  # Muestra el aviso al usuario, sin lanzar error
            logging.info(f"Listado de clientes: {mensaje}")  # Registra el evento
            return []  # Retorna lista vacía
        return [c.describir() for c in self.__clientes]  # Retorna la descripción de cada cliente
