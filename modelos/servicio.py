import math  # Para math.isfinite: detecta valores nan e inf
from abc import abstractmethod  # Herramienta para declarar métodos abstractos (ABC ya viene de Entidad)

from modelos.entidad import Entidad  # Clase abstracta general de la que hereda Servicio
from modelos.excepciones import (  # Importa las excepciones personalizadas que usa este módulo
    DatosInvalidosError,  # Error de datos faltantes o fuera de rango
    ServicioNoDisponibleError,  # Error cuando el servicio no se puede usar
    TarifaInvalidaError,  # Error cuando el precio no es válido
)  # Cierra la importación


class Servicio(Entidad):  # Clase abstracta que hereda de Entidad: no se puede instanciar directamente

    def __init__(self, nombre, precio, disponible=True):  # Constructor común a todos los servicios
        self.nombre = nombre  # Asigna usando el setter, que valida el nombre
        self.precio = precio  # Asigna usando el setter, que valida la tarifa
        self.disponible = disponible  # Asigna usando el setter, que valida que sea booleano
        super().__init__()  # Inicializa Entidad: asigna el identificador autoincremental

    @property  # Permite leer el atributo privado como si fuera público
    def nombre(self):  # Getter del nombre
        return self.__nombre  # Retorna el valor guardado en el atributo privado

    @nombre.setter  # Define qué pasa al asignar servicio.nombre = valor
    def nombre(self, valor):  # Setter del nombre
        if not isinstance(valor, str) or not valor.strip():  # Rechaza valores que no son texto o están vacíos
            raise DatosInvalidosError("El nombre del servicio es obligatorio y debe ser texto.")  # Avisa el error
        self.__nombre = valor.strip()  # Guarda el nombre sin espacios sobrantes

    @property  # Permite leer el precio privado
    def precio(self):  # Getter del precio
        return self.__precio  # Retorna el valor guardado en el atributo privado

    @precio.setter  # Define qué pasa al asignar servicio.precio = valor
    def precio(self, valor):  # Setter del precio, aquí se valida la tarifa
        if valor is None:  # Verifica que la tarifa no falte
            raise TarifaInvalidaError("La tarifa es obligatoria.")  # Avisa que falta la tarifa
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):  # bool cuenta como int en Python, por eso se excluye
            raise TarifaInvalidaError(f"La tarifa debe ser numérica, se recibió {type(valor).__name__}.")  # Avisa tipo incorrecto
        if not math.isfinite(valor):  # Rechaza tarifas nan o inf
            raise TarifaInvalidaError(f"La tarifa debe ser un número finito, se recibió {valor}.")  # Avisa valor inválido
        if valor <= 0:  # Rechaza tarifas cero o negativas
            raise TarifaInvalidaError(f"La tarifa debe ser mayor que cero, se recibió {valor}.")  # Avisa valor inválido
        self.__precio = valor  # Guarda la tarifa ya validada

    @property  # Permite leer la disponibilidad privada
    def disponible(self):  # Getter de la disponibilidad
        return self.__disponible  # Retorna el valor guardado en el atributo privado

    @disponible.setter  # Define qué pasa al asignar servicio.disponible = valor
    def disponible(self, valor):  # Setter de la disponibilidad
        if not isinstance(valor, bool):  # Solo se aceptan valores booleanos
            raise DatosInvalidosError("La disponibilidad debe ser True o False.")  # Avisa tipo incorrecto
        self.__disponible = valor  # Guarda la disponibilidad validada

    def _verificar_disponibilidad(self):  # Método auxiliar para las clases hijas
        if not self.disponible:  # Revisa si el servicio está desactivado
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")  # Avisa el error

    def _validar_duracion(self, duracion, unidad):  # Método auxiliar para validar horas o días
        if duracion is None:  # Verifica que la duración no falte
            raise DatosInvalidosError(f"Falta la duración en {unidad}.")  # Avisa parámetro faltante
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):  # Rechaza tipos no numéricos
            raise DatosInvalidosError(f"La duración en {unidad} debe ser numérica.")  # Avisa tipo incorrecto
        if not math.isfinite(duracion):  # Rechaza duraciones nan o inf
            raise DatosInvalidosError(f"La duración en {unidad} debe ser un número finito.")  # Avisa valor inválido
        if duracion <= 0:  # Rechaza duraciones cero o negativas
            raise DatosInvalidosError(f"La duración en {unidad} debe ser mayor que cero.")  # Avisa valor inválido

    def _validar_porcentaje(self, valor, nombre_campo):  # Método auxiliar para impuesto y descuento
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):  # Rechaza tipos no numéricos
            raise DatosInvalidosError(f"El {nombre_campo} debe ser numérico.")  # Avisa tipo incorrecto
        if not math.isfinite(valor):  # Rechaza porcentajes nan o inf
            raise DatosInvalidosError(f"El {nombre_campo} debe ser un número finito.")  # Avisa valor inválido
        if valor < 0 or valor > 100:  # Rechaza porcentajes fuera del rango permitido
            raise DatosInvalidosError(f"El {nombre_campo} debe estar entre 0 y 100, se recibió {valor}.")  # Avisa el error

    def _aplicar_ajustes(self, subtotal, impuesto, descuento):  # Método auxiliar común a todos los cálculos
        self._validar_porcentaje(impuesto, "impuesto")  # Valida el impuesto
        self._validar_porcentaje(descuento, "descuento")  # Valida el descuento
        con_descuento = subtotal * (1 - descuento / 100)  # Resta el descuento al subtotal
        total = con_descuento * (1 + impuesto / 100)  # Suma el impuesto al valor con descuento
        return round(total, 2)  # Retorna el total redondeado a dos decimales

    @abstractmethod  # Obliga a cada clase hija a implementar este método
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):  # Impuesto y descuento son opcionales
        pass # Cada clase hija implementa este método

    @abstractmethod  # Obliga a cada clase hija a implementar este método
    def describir(self):  # Cada servicio se describe a su manera
        pass # Cada clase hija implementa este método

    @abstractmethod  # Obliga a cada clase hija a implementar este método
    def validar_parametros(self):  # Cada servicio valida sus atributos exclusivos
        pass # Cada clase hija implementa este método

    def __str__(self):  # Define cómo se ve el servicio al imprimirlo
        return self.describir()  # Reutiliza describir(), que cada hija implementa
