from modelos.excepciones import DatosInvalidosError  # Excepción para parámetros faltantes o inválidos
from modelos.servicio import Servicio  # Clase abstracta de la que hereda


class AsesoriaEspecializada(Servicio):  # Hereda de Servicio y concreta sus métodos abstractos

    FACTORES_NIVEL = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # Multiplicador de la tarifa por nivel

    def __init__(self, nombre, tarifa_base, nivel=None, disponible=True):  # Constructor de la asesoría
        super().__init__(nombre, tarifa_base, disponible)  # Inicializa y valida los atributos comunes
        if isinstance(nivel, str):  # Si el nivel es texto, se normaliza
            nivel = nivel.strip().lower()  # Quita espacios y pasa a minúsculas ("Senior" -> "senior")
        self.__nivel = nivel  # Guarda el nivel en un atributo privado
        self.validar_parametros()  # Valida el atributo exclusivo de la asesoría

    @property  # Permite leer el nivel privado
    def nivel(self):  # Getter del nivel
        return self.__nivel  # Retorna el valor privado

    @property  # Valor calculado, no se guarda
    def tarifa_hora(self):  # Getter de la tarifa real por hora
        return self.precio * self.FACTORES_NIVEL[self.nivel]  # Multiplica la tarifa base por el factor

    def validar_parametros(self):  # Sobrescribe el método abstracto
        if self.__nivel is None:  # Revisa si falta el nivel
            raise DatosInvalidosError("Falta el parámetro 'nivel' de la asesoría.")  # Avisa parámetro faltante
        if self.__nivel not in self.FACTORES_NIVEL:  # Revisa que el nivel sea uno de los permitidos
            niveles = ", ".join(self.FACTORES_NIVEL)  # Arma el texto con los niveles válidos
            raise DatosInvalidosError(f"Nivel '{self.__nivel}' no válido. Use: {niveles}.")  # Avisa valor inválido
        return True  # Indica que la validación pasó

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):  # Sobrescribe el método abstracto
        self._verificar_disponibilidad()  # Impide calcular si la asesoría no está disponible
        self._validar_duracion(duracion, "horas")  # Valida las horas recibidas
        subtotal = self.tarifa_hora * duracion  # Multiplica la tarifa ajustada por las horas
        return self._aplicar_ajustes(subtotal, impuesto, descuento)  # Aplica descuento e impuesto y retorna

    def describir(self):  # Sobrescribe el método abstracto
        estado = "Disponible" if self.disponible else "No disponible"  # Traduce el booleano a texto
        return (f"[Asesoría] {self.nombre} | Nivel: {self.nivel} | "  # Arma la primera parte del texto
                f"${self.tarifa_hora:,.0f} por hora | {estado}")  # Completa el texto y lo retorna
