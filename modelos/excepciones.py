"""Excepciones personalizadas compartidas por todo el sistema

Jerarquía:
    SoftwareFJError
    ├── ReservaError
    │   ├── ClienteNoEncontradoError
    │   └── ReservaInvalidaError
    ├── ServicioError
    │   ├── TarifaInvalidaError
    │   ├── ServicioNoDisponibleError
    │   └── ServicioNoEncontradoError
    └── DatosInvalidosError
"""


class SoftwareFJError(Exception):  # Raíz de todas las excepciones propias del sistema
    """Excepción base del Sistema Integral de Gestión de Software FJ."""

    pass  # No agrega comportamiento; solo permite capturar cualquier error propio


class ReservaError(SoftwareFJError):  # Base de los errores de reservas (ya existía en Reservas.py)
    """Errores relacionados con el manejo de reservas."""

    pass  # Hereda todo de SoftwareFJError


class ClienteNoEncontradoError(ReservaError):  # El cliente de la reserva no existe
    """Se lanza cuando una reserva no tiene un cliente válido."""

    pass  # Hereda todo de ReservaError


class ReservaInvalidaError(ReservaError):  # La reserva está en un estado que no permite la operación
    """Se lanza cuando una operación no es válida para el estado de la reserva."""

    pass  # Hereda todo de ReservaError


class ServicioError(SoftwareFJError):  # Base de los errores de servicios
    """Errores relacionados con la gestión de servicios."""

    pass  # Hereda todo de SoftwareFJError


class TarifaInvalidaError(ServicioError):  # El precio del servicio no es válido
    """Se lanza cuando la tarifa es cero, negativa, falta o no es numérica."""

    pass  # Hereda todo de ServicioError


class ServicioNoDisponibleError(ServicioError):  # El servicio existe pero no se puede usar
    """Se lanza cuando se intenta usar un servicio marcado como no disponible."""

    pass  # Hereda todo de ServicioError


class ServicioNoEncontradoError(ServicioError):  # El servicio buscado no está en la lista
    """Se lanza cuando se busca un servicio que no existe."""

    pass  # Hereda todo de ServicioError


class DatosInvalidosError(SoftwareFJError):  # Datos faltantes o fuera de rango en cualquier módulo
    """Se lanza cuando un dato obligatorio falta o tiene un valor no permitido."""

    pass  # Hereda todo de SoftwareFJError
