from modelos.gestor_servicios import GestorServicios  # Se importa primero: configura el log
from modelos.gestor_clientes import GestorClientes  # Gestor de clientes
from modelos.entidad import Entidad  # Clase abstracta, para probar que no se puede instanciar
from modelos.Reservas import Reserva  # Para probar que Cliente funciona con Reserva


def probar(descripcion, accion):  # Ejecuta una prueba y muestra el resultado o el error
    """Ejecuta 'accion' y muestra el resultado o la excepción capturada."""
    print(f"\n>> {descripcion}")  # Muestra qué se está probando
    try:  # Intenta ejecutar la prueba
        resultado = accion()  # Ejecuta la función recibida
    except Exception as e:  # Captura cualquier error para que el script continúe
        print(f"   ERROR {type(e).__name__}: {e}")  # Muestra el tipo y mensaje del error
        if e.__cause__:  # Si el error fue encadenado con "from e"
            print(f"   Causa original: {type(e.__cause__).__name__}")  # Muestra el tipo de la causa
    else:  # Si no hubo error
        print(f"   OK: {resultado}")  # Muestra el resultado


clientes = GestorClientes()  # Crea el gestor de clientes vacío

probar("1. Listar con el gestor vacío", clientes.listar_clientes)  # Debe avisar sin lanzar error
probar("2. Registrar cliente válido", lambda: clientes.registrar_cliente(  # Válido
    "Ana Gómez", "ana@correo.com", "3001234567"))  # Datos correctos
probar("3. Registrar otro cliente válido", lambda: clientes.registrar_cliente(  # Válido, teléfono fijo de 7 dígitos
    "Luis Pérez", "  Luis.Perez@Empresa.co ", "6041234"))  # Correo con mayúsculas y espacios
probar("4. Nombre vacío", lambda: clientes.registrar_cliente("   ", "x@correo.com", "3001112233"))  # ClienteInvalidoError
probar("5. Correo sin @", lambda: clientes.registrar_cliente("Eva", "eva.correo.com", "3001112233"))  # ClienteInvalidoError
probar("6. Correo sin punto en el dominio", lambda: clientes.registrar_cliente(  # ClienteInvalidoError
    "Eva", "eva@correo", "3001112233"))  # Dominio incompleto
probar("7. Teléfono con letras", lambda: clientes.registrar_cliente(  # ClienteInvalidoError
    "Eva", "eva@correo.com", "300ABC4567"))  # Contiene letras
probar("8. Teléfono muy corto", lambda: clientes.registrar_cliente(  # ClienteInvalidoError
    "Eva", "eva@correo.com", "12345"))  # Solo 5 dígitos
probar("9. Falta el teléfono", lambda: clientes.registrar_cliente("Eva", "eva@correo.com"))  # ClienteInvalidoError
probar("10. Correo duplicado (con otras mayúsculas)", lambda: clientes.registrar_cliente(  # ClienteDuplicadoError
    "Ana B", "ANA@correo.com", "3009998877"))  # Mismo correo del caso 2
probar("11. Buscar cliente existente", lambda: clientes.buscar_cliente("luis.perez@empresa.co"))  # Válido
probar("12. Buscar cliente inexistente (error encadenado)", lambda: clientes.buscar_cliente(  # ClienteNoEncontradoError
    "nadie@correo.com"))  # Correo no registrado
probar("13. Instanciar la clase abstracta Entidad", Entidad)  # TypeError de Python

servicios = GestorServicios()  # Gestor de servicios para la prueba de integración
sala = servicios.crear_servicio("sala", "Sala Juntas", 50000, capacidad=12)  # Servicio que también es Entidad
ana = clientes.buscar_cliente("ana@correo.com")  # Cliente real registrado en el caso 2
probar("14. Reserva con un Cliente real", lambda: Reserva(ana, sala, 2))  # Reserva usa cliente.nombre
probar("15. Identificadores de Entidad", lambda: (ana.identificador, sala.identificador))  # Contador compartido

print("\n>> Listado final")  # Título del listado
for linea in clientes.listar_clientes():  # Recorre las descripciones
    print(f"   {linea}")  # Muestra cada cliente
print("\nRevise el archivo logs/sistema.log para ver los errores y eventos registrados.")  # Indicación final
