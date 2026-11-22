# SIGCSR – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso Programación (213023) de la UNAD. Es un sistema orientado a objetos en Python, sin bases de datos, para la empresa ficticia **Software FJ**. Gestiona clientes, servicios (reserva de salas, alquiler de equipos y asesorías especializadas) y reservas. Toda la información vive en objetos y listas; el único archivo que se escribe es el log de eventos y errores.

## Requisitos

- Python 3.9 o superior (no usa librerías externas).

## Estructura

```
.
├── main.py                       # Menú de consola (clase MenuSistema)
├── simulacion.py                 # Simulación automática de 18 operaciones (clase Simulacion)
├── prueba_clientes.py            # Pruebas de clientes
├── prueba_servicios.py           # Pruebas de servicios
├── prueba_reservas.py            # Pruebas de reservas
├── prueba_integracion.py         # Prueba de integración de todo el flujo
├── modelos/
│   ├── excepciones.py            # Excepciones propias (raíz SoftwareFJError)
│   ├── entidad.py                # Clase abstracta Entidad
│   ├── cliente.py                # Cliente con validaciones y encapsulación
│   ├── gestor_clientes.py        # GestorClientes
│   ├── servicio.py               # Clase abstracta Servicio
│   ├── reserva_sala.py           # ReservaSala (cobro por hora)
│   ├── alquiler_equipo.py        # AlquilerEquipo (cobro por día + depósito)
│   ├── asesoria_especializada.py # AsesoriaEspecializada (tarifa según nivel)
│   ├── gestor_servicios.py       # GestorServicios y configuración del log
│   └── Reservas.py               # Reserva y GestorReservas
└── logs/sistema.log              # Se crea al ejecutar (no se sube al repositorio)
```

## Cómo ejecutar

Todos los comandos se ejecutan **desde la carpeta raíz del proyecto**, porque la ruta del log es relativa.

```
python main.py                 # Menú interactivo
python simulacion.py           # Solo la simulación automática
python prueba_clientes.py      # Pruebas de clientes
python prueba_servicios.py     # Pruebas de servicios
python prueba_reservas.py      # Pruebas de reservas
python prueba_integracion.py   # Prueba de integración
```

La simulación también se ejecuta desde el menú con la opción 11.

## Registro de eventos

Todos los errores y eventos relevantes se registran en `logs/sistema.log`. La carpeta se crea sola y el log se configura una única vez, en `modelos/gestor_servicios.py`. Cada línea tiene fecha, nivel (`INFO` o `ERROR`) y mensaje.

## Manejo de errores

El sistema usa excepciones propias (`modelos/excepciones.py`), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`. Ningún error detiene el menú ni la simulación: se muestra al usuario, queda en el log y el programa continúa.
