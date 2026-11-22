from modelos.excepciones import DatosInvalidosError  # Excepción para parámetros faltantes o inválidos
from modelos.servicio import Servicio  # Clase abstracta de la que hereda


class ReservaSala(Servicio):  # Hereda de Servicio y concreta sus métodos abstractos

    def __init__(self, nombre, precio_hora, capacidad=None, disponible=True):  # Constructor de la sala
        super().__init__(nombre, precio_hora, disponible)  # Inicializa y valida los atributos comunes
        self.__capacidad = capacidad  # Guarda la capacidad en un atributo privado
        self.validar_parametros()  # Valida el atributo exclusivo de la sala

    @property  # Permite leer la capacidad privada
    def capacidad(self):  # Getter de la capacidad
        return self.__capacidad  # Retorna el valor privado

    def validar_parametros(self):  # Sobrescribe el método abstracto
        if self.__capacidad is None:  # Revisa si falta la capacidad
            raise DatosInvalidosError("Falta el parámetro 'capacidad' de la sala.")  # Avisa parámetro faltante
        if isinstance(self.__capacidad, bool) or not isinstance(self.__capacidad, int):  # Solo acepta enteros
            raise DatosInvalidosError("La capacidad de la sala debe ser un número entero.")  # Avisa tipo incorrecto
        if self.__capacidad <= 0:  # Rechaza capacidades cero o negativas
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor que cero.")  # Avisa valor inválido
        return True  # Indica que la validación pasó

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):  # Sobrescribe el método abstracto
        self._verificar_disponibilidad()  # Impide calcular si la sala no está disponible
        self._validar_duracion(duracion, "horas")  # Valida las horas recibidas
        subtotal = self.precio * duracion  # Multiplica la tarifa por hora por las horas
        return self._aplicar_ajustes(subtotal, impuesto, descuento)  # Aplica descuento e impuesto y retorna

    def describir(self):  # Sobrescribe el método abstracto
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce el booleano a texto
        return (f"[Sala] {self.nombre} | ${self.precio:,.0f} por hora | "  # Arma la primera parte del texto
                f"Capacidad: {self.capacidad} personas | {estado}")  # Completa el texto y lo retorna
