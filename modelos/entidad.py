from abc import ABC, abstractmethod  # Herramientas para crear clases y métodos abstractos


class Entidad(ABC):  # Clase abstracta: no se puede crear un objeto Entidad directamente

    _contador = 0  # Contador de clase compartido: cuántas entidades se han creado

    def __init__(self):  # Constructor común de todas las entidades
        Entidad._contador += 1  # Aumenta el contador de la clase en uno
        self.__identificador = Entidad._contador  # Guarda el número en un atributo privado

    @property  # Propiedad de solo lectura: tiene getter pero no setter
    def identificador(self):  # Getter del identificador
        return self.__identificador  # Retorna el valor privado

    @abstractmethod  # Obliga a cada clase hija a implementar este método
    def describir(self):  
        pass # Cada entidad se describe a su manera
