import logging  # Librería estándar para registrar errores y eventos
import os  # Librería estándar para crear la carpeta de logs

from modelos.alquiler_equipo import AlquilerEquipo  # Servicio de alquiler de equipos
from modelos.asesoria_especializada import AsesoriaEspecializada  # Servicio de asesoría
from modelos.excepciones import (  # Excepciones personalizadas que usa el gestor
    DatosInvalidosError,  # Error de datos faltantes o inválidos
    ServicioNoEncontradoError,  # Error cuando el servicio buscado no existe
    SoftwareFJError,  # Base de todas las excepciones propias
)  # Cierra la importación
from modelos.reserva_sala import ReservaSala  # Servicio de reserva de salas

CARPETA_LOGS = "logs"  # Nombre de la carpeta donde se guarda el log
os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea la carpeta si no existe; si ya existe no hace nada
logging.basicConfig(  # Configura el registro de eventos del sistema
    filename=os.path.join(CARPETA_LOGS, "sistema.log"),  # Archivo donde se escriben los mensajes
    level=logging.INFO,  # Registra eventos (INFO) y errores (ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Fecha, nivel y mensaje (mismo formato de Reservas.py)
    encoding="utf-8",  # Permite tildes y eñes en el archivo
)  # Cierra la configuración


class GestorServicios:  # Administra todos los servicios en una lista interna

    def __init__(self):  # Constructor del gestor
        self.__servicios = []  # Lista privada donde se guardan los servicios

    def crear_servicio(self, tipo, nombre, precio, disponible=True, capacidad=None,  # Parámetros comunes
                       tipo_equipo=None, deposito=0.0, nivel=None):  # Parámetros opcionales según el tipo
        try:  # Bloque donde puede ocurrir un error
            if tipo == "sala":  # Caso de reserva de sala
                servicio = ReservaSala(nombre, precio, capacidad, disponible)  # Crea la sala
            elif tipo == "equipo":  # Caso de alquiler de equipo
                servicio = AlquilerEquipo(nombre, precio, tipo_equipo, deposito, disponible)  # Crea el alquiler
            elif tipo == "asesoria":  # Caso de asesoría especializada
                servicio = AsesoriaEspecializada(nombre, precio, nivel, disponible)  # Crea la asesoría
            else:  # Cualquier otro tipo no existe
                raise DatosInvalidosError(f"Tipo de servicio '{tipo}' no válido. Use: sala, equipo o asesoria.")  # Avisa
            if self.__existe(servicio.nombre):  # Revisa que no haya otro servicio con el mismo nombre
                raise DatosInvalidosError(f"Ya existe un servicio llamado '{servicio.nombre}'.")  # Avisa duplicado
        except SoftwareFJError as e:  # Errores propios ya controlados (tarifa, datos, etc.)
            logging.error(f"No se pudo crear el servicio '{nombre}': {type(e).__name__}: {e}")  # Registra el error
            raise  # Vuelve a lanzar la misma excepción para que quien llamó la maneje
        except Exception as e:  # Cualquier error inesperado
            logging.error(f"Error inesperado al crear el servicio '{nombre}': {e}")  # Registra el error
            raise DatosInvalidosError("Error inesperado al crear el servicio.") from e  # Encadena con la causa original
        else:  # Solo se ejecuta si no hubo ningún error
            self.__servicios.append(servicio)  # Guarda el servicio en la lista
            logging.info(f"Servicio creado: {servicio.describir()}")  # Registra el evento exitoso
            return servicio  # Retorna el servicio creado
        finally:  # Se ejecuta siempre, haya error o no
            logging.info(f"Finalizó el intento de creación del servicio '{nombre}' (tipo: {tipo}).")  # Registra el cierre

    def __existe(self, nombre):  # Método privado de apoyo
        return any(s.nombre.lower() == nombre.lower() for s in self.__servicios)  # True si encuentra coincidencia

    def obtener_servicio(self, indice):  # Busca por posición en la lista
        try:  # Intenta acceder a la posición
            return self.__servicios[indice]  # Retorna el servicio encontrado
        except (IndexError, TypeError) as e:  # Posición fuera de rango o índice que no es entero
            logging.error(f"Se pidió un servicio en una posición inexistente: {indice}.")  # Registra el error
            raise ServicioNoEncontradoError(f"No existe un servicio en la posición {indice}.") from e  # Encadena la causa

    def buscar_servicio(self, nombre):  # Busca por nombre
        for servicio in self.__servicios:  # Recorre la lista de servicios
            if servicio.nombre.lower() == str(nombre).strip().lower():  # Compara sin distinguir mayúsculas
                return servicio  # Retorna el servicio encontrado
        logging.error(f"Servicio no encontrado: '{nombre}'.")  # Registra el error antes de lanzarlo
        raise ServicioNoEncontradoError(f"No existe un servicio llamado '{nombre}'.")  # Avisa que no se encontró

    def calcular_costo_servicio(self, nombre, duracion, impuesto=0.0, descuento=0.0):  # Cálculo con registro
        try:  # Bloque donde puede ocurrir un error
            servicio = self.buscar_servicio(nombre)  # Obtiene el servicio
            costo = servicio.calcular_costo(duracion, impuesto, descuento)  # Cada servicio aplica su propia regla
        except SoftwareFJError as e:  # Errores propios (no encontrado, no disponible, datos inválidos)
            logging.error(f"No se pudo calcular el costo de '{nombre}': {type(e).__name__}: {e}")  # Registra el error
            raise  # Vuelve a lanzar la excepción
        else:  # Solo si el cálculo fue exitoso
            logging.info(f"Costo calculado para '{nombre}' ({duracion}): ${costo:,.2f}")  # Registra el evento
            return costo  # Retorna el costo

    def listar_servicios(self, solo_disponibles=False):  # Parámetro opcional (sobrecarga)
        servicios = [s for s in self.__servicios if s.disponible or not solo_disponibles]  # Filtra si se pide
        if not servicios:  # Revisa si la lista quedó vacía
            if solo_disponibles:  # Mensaje cuando se pidieron solo los disponibles
                mensaje = "No hay servicios disponibles en este momento."  # Texto del aviso
            else:  # Mensaje cuando no hay ningún servicio
                mensaje = "No hay servicios registrados todavía."  # Texto del aviso
            print(mensaje)  # Muestra el aviso al usuario, sin lanzar error
            logging.info(f"Listado de servicios: {mensaje}")  # Registra el evento
            return []  # Retorna lista vacía
        return [s.describir() for s in servicios]  # Cada servicio se describe con su propia versión de describir()
