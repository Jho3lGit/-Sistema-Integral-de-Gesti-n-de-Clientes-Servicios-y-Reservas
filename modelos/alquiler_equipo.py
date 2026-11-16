from modelos.excepciones import DatosInvalidosError  # Excepción para parámetros faltantes o inválidos
from modelos.servicio import Servicio  # Clase abstracta de la que hereda


class AlquilerEquipo(Servicio):  # Hereda de Servicio y concreta sus métodos abstractos

    def __init__(self, nombre, precio_dia, tipo_equipo=None, deposito=0.0, disponible=True):  # Constructor
        super().__init__(nombre, precio_dia, disponible)  # Inicializa y valida los atributos comunes
        self.__tipo_equipo = tipo_equipo  # Guarda el tipo de equipo en un atributo privado
        self.__deposito = deposito  # Guarda el depósito en un atributo privado
        self.validar_parametros()  # Valida los atributos exclusivos del alquiler

    @property  # Permite leer el tipo de equipo privado
    def tipo_equipo(self):  # Getter del tipo de equipo
        return self.__tipo_equipo  # Retorna el valor privado

    @property  # Permite leer el depósito privado
    def deposito(self):  # Getter del depósito
        return self.__deposito  # Retorna el valor privado

    def validar_parametros(self):  # Sobrescribe el método abstracto
        if self.__tipo_equipo is None:  # Revisa si falta el tipo de equipo
            raise DatosInvalidosError("Falta el parámetro 'tipo_equipo' del alquiler.")  # Avisa parámetro faltante
        if not isinstance(self.__tipo_equipo, str) or not self.__tipo_equipo.strip():  # Exige texto no vacío
            raise DatosInvalidosError("El tipo de equipo debe ser un texto no vacío.")  # Avisa tipo incorrecto
        if isinstance(self.__deposito, bool) or not isinstance(self.__deposito, (int, float)):  # Exige número
            raise DatosInvalidosError("El depósito debe ser numérico.")  # Avisa tipo incorrecto
        if self.__deposito < 0:  # Rechaza depósitos negativos (cero sí se permite)
            raise DatosInvalidosError("El depósito no puede ser negativo.")  # Avisa valor inválido
        return True  # Indica que la validación pasó

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):  # Sobrescribe el método abstracto
        self._verificar_disponibilidad()  # Impide calcular si el equipo no está disponible
        self._validar_duracion(duracion, "días")  # Valida que los días sean un número mayor que cero
        if not isinstance(duracion, int):  # El alquiler solo se cobra por días completos
            raise DatosInvalidosError("Los días de alquiler deben ser un número entero.")  # Avisa tipo incorrecto
        subtotal = self.precio * duracion  # Multiplica la tarifa diaria por los días
        total_alquiler = self._aplicar_ajustes(subtotal, impuesto, descuento)  # Aplica descuento e impuesto
        return round(total_alquiler + self.deposito, 2)  # Suma el depósito (no lleva impuesto ni descuento)

    def describir(self):  # Sobrescribe el método abstracto
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce el booleano a texto
        return (f"[Equipo] {self.nombre} ({self.tipo_equipo}) | ${self.precio:,.0f} por día | "  # Primera parte
                f"Depósito: ${self.deposito:,.0f} | {estado}")  # Completa el texto y lo retorna
