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

## Uso del menú (python main.py)

Al iniciar aparece el menú principal. Se escribe el número de la opción y se presiona Enter.

| Opción | Qué hace | Datos que pide |
|---|---|---|
| 1 | Registrar cliente | Nombre, correo y teléfono (7 a 10 dígitos) |
| 2 | Listar clientes | Nada |
| 3 | Crear servicio | Tipo (sala, equipo o asesoria), nombre, tarifa y el dato propio del tipo: capacidad (sala); tipo de equipo y depósito (equipo); nivel junior, senior o experto (asesoría) |
| 4 | Listar servicios | Nada |
| 5 | Crear reserva | Correo de un cliente registrado, número del servicio de la lista y duración (horas para sala y asesoría, días enteros para equipo) |
| 6 | Confirmar reserva | Número de la reserva de la lista |
| 7 | Cancelar reserva | Número de la reserva de la lista |
| 8 | Procesar reserva | Número de la reserva (debe estar confirmada) |
| 9 | Calcular costo | Número de la reserva, impuesto % y descuento % (vacío = 0) |
| 10 | Listar reservas | Nada |
| 11 | Ejecutar simulación | Nada: corre 18 operaciones automáticas |
| 0 | Salir | Nada |

### Paso a paso de una reserva completa

1. Opción 1: registre un cliente, por ejemplo Ana Gómez, ana@correo.com, 3001234567.
2. Opción 3: cree un servicio, por ejemplo tipo sala, nombre Sala Juntas, tarifa 50000, capacidad 12.
3. Opción 5: cree la reserva con el correo ana@correo.com, el servicio número 1 y duración 3.
4. Opción 6: confirme la reserva número 1.
5. Opción 9: calcule el costo de la reserva 1, con impuesto 19 y descuento 10 (resultado: $160,650.00).
6. Opción 8: procese la reserva 1.
7. Opción 10: revise que la reserva aparezca en la lista.
8. Opción 0: salga del programa y revise logs/sistema.log.

### Qué pasa si hay un error

Si un dato está vacío, no es un número, la opción no existe, se elige un número fuera de la lista o se intenta una acción sin datos previos (por ejemplo, crear una reserva sin clientes), el menú muestra un mensaje que empieza con "Error:", lo registra en el log y vuelve a mostrar las opciones. El programa no se cierra por ningún error; solo termina con la opción 0 o con Ctrl+C.

## Registro de eventos

Todos los errores y eventos relevantes se registran en `logs/sistema.log`. La carpeta se crea sola y el log se configura una única vez, en `modelos/gestor_servicios.py`. Cada línea tiene fecha, nivel (`INFO` o `ERROR`) y mensaje.

## Manejo de errores

El sistema usa excepciones propias (`modelos/excepciones.py`), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`. Ningún error detiene el menú ni la simulación: se muestra al usuario, queda en el log y el programa continúa.
