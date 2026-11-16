from datetime import datetime
import logging
from modelos.excepciones import (ReservaError, ClienteNoEncontradoError,
    ServicioNoDisponibleError, ReservaInvalidaError, DatosInvalidosError)

class Reserva:

    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion):
        try:
            self.validar_datos(cliente, servicio, duracion)
        except Exception as e:
            logging.error(str(e))
            raise
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = self.ESTADO_PENDIENTE
        self.fecha_creacion = datetime.now()

    def validar_datos(self, cliente, servicio, duracion):
        if cliente is None:
            raise ClienteNoEncontradoError("El cliente no existe.")
        if servicio is None:
            raise ServicioNoDisponibleError("El servicio no existe.")
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

    def confirmar(self):
        try:
            if self.estado == self.ESTADO_CANCELADA:
                raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")
            if hasattr(self.servicio, 'disponible') and not self.servicio.disponible:
                raise ServicioNoDisponibleError("El servicio no se encuentra disponible.")
            self.estado = self.ESTADO_CONFIRMADA
        except Exception as e:
            logging.error(str(e))
            raise

    def cancelar(self):
        try:
            if self.estado == self.ESTADO_CANCELADA:
                raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
            self.estado = self.ESTADO_CANCELADA
        except Exception as e:
            logging.error(str(e))
            raise

    def procesar(self):
        try:
            if self.estado != self.ESTADO_CONFIRMADA:
                raise ReservaInvalidaError("La reserva debe estar confirmada para procesarse.")
        except ReservaInvalidaError as e:
            logging.error(str(e))
            raise
        else:
            print(f"Reserva procesada correctamente para {self.cliente.nombre}")
        finally:
            print("Finalizó el proceso de reserva.")

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        try:
            return self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        except Exception as e:
            logging.error(str(e))
            raise

    def __str__(self):
        return (f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre} | "
                f"Duración: {self.duracion} | Estado: {self.estado}")

class GestorReservas:
    def __init__(self):
        self.reservas = []

    def agregar_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("El objeto no es una reserva válida.")
        self.reservas.append(reserva)

    def buscar_reserva(self, indice):
        try:
            return self.reservas[indice]
        except IndexError as e:
            raise ReservaInvalidaError("Reserva no encontrada.") from e

    def cancelar_reserva(self, indice):
        self.buscar_reserva(indice).cancelar()

    def listar_reservas(self):
        return [str(r) for r in self.reservas]
