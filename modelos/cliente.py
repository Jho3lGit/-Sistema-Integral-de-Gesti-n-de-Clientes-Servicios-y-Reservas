from modelos.entidad import Entidad  # Clase abstracta de la que hereda
from modelos.excepciones import ClienteInvalidoError  # Error para datos de cliente no válidos

DIGITOS = "0123456789"  # Caracteres permitidos en el teléfono


class Cliente(Entidad):  # Hereda de Entidad: recibe un identificador automático

    def __init__(self, nombre=None, correo=None, telefono=None):  # Parámetros en None para detectar faltantes
        self.nombre = nombre  # Asigna usando el setter, que valida el nombre
        self.correo = correo  # Asigna usando el setter, que valida el correo
        self.telefono = telefono  # Asigna usando el setter, que valida el teléfono
        super().__init__()  # Se llama al final para no gastar identificadores en clientes inválidos

    @property  # Permite leer el nombre privado
    def nombre(self):  # Getter del nombre
        return self.__nombre  # Retorna el valor privado

    @nombre.setter  # Define qué pasa al asignar cliente.nombre = valor
    def nombre(self, valor):  # Setter del nombre
        if not isinstance(valor, str) or not valor.strip():  # Rechaza no-texto, None o texto vacío
            raise ClienteInvalidoError("El nombre del cliente es obligatorio y debe ser texto.")  # Avisa el error
        self.__nombre = valor.strip()  # Guarda el nombre sin espacios sobrantes

    @property  # Permite leer el correo privado
    def correo(self):  # Getter del correo
        return self.__correo  # Retorna el valor privado

    @correo.setter  # Define qué pasa al asignar cliente.correo = valor
    def correo(self, valor):  # Setter del correo
        if not isinstance(valor, str) or not valor.strip():  # Rechaza no-texto, None o texto vacío
            raise ClienteInvalidoError("El correo del cliente es obligatorio y debe ser texto.")  # Avisa el error
        correo = valor.strip().lower()  # Quita espacios externos y pasa a minúsculas
        if " " in correo or correo.count("@") != 1:  # Debe tener exactamente una @ y ningún espacio
            raise ClienteInvalidoError(f"Correo '{valor}' no válido: debe tener una sola @ y sin espacios.")  # Avisa
        usuario, dominio = correo.split("@")  # Separa la parte antes y después de la @
        if not usuario or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):  # Revisa partes
            raise ClienteInvalidoError(f"Correo '{valor}' no válido: use el formato usuario@dominio.com.")  # Avisa
        self.__correo = correo  # Guarda el correo validado

    @property  # Permite leer el teléfono privado
    def telefono(self):  # Getter del teléfono
        return self.__telefono  # Retorna el valor privado

    @telefono.setter  # Define qué pasa al asignar cliente.telefono = valor
    def telefono(self, valor):  # Setter del teléfono
        if not isinstance(valor, str) or not valor.strip():  # Se pide texto para no perder ceros a la izquierda
            raise ClienteInvalidoError("El teléfono es obligatorio y debe ser texto, por ejemplo '3001234567'.")  # Avisa
        telefono = valor.strip()  # Quita espacios externos
        if not all(caracter in DIGITOS for caracter in telefono):  # Revisa que cada carácter sea un dígito
            raise ClienteInvalidoError(f"Teléfono '{valor}' no válido: solo se permiten dígitos.")  # Avisa
        if not 7 <= len(telefono) <= 10:  # Revisa la longitud permitida
            raise ClienteInvalidoError(f"Teléfono '{valor}' no válido: debe tener de 7 a 10 dígitos.")  # Avisa
        self.__telefono = telefono  # Guarda el teléfono validado

    def describir(self):  # Implementa el método abstracto de Entidad
        return (f"[Cliente #{self.identificador}] {self.nombre} | "  # Primera parte del texto
                f"{self.correo} | Tel: {self.telefono}")  # Completa el texto y lo retorna

    def __str__(self):  # Define cómo se ve el cliente al imprimirlo
        return self.describir()  # Reutiliza describir()
