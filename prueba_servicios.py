from modelos.gestor_servicios import GestorServicios  # Gestor que crea y administra los servicios
from modelos.servicio import Servicio  # Clase abstracta, para probar que no se puede instanciar


def probar(descripcion, accion):  # Ejecuta una prueba y muestra el resultado o el error
    print(f"\n>> {descripcion}")  # Muestra qué se está probando
    try:  # Intenta ejecutar la prueba
        resultado = accion()  # Ejecuta la función recibida
    except Exception as e:  # Captura cualquier error para que el script continúe
        print(f"   ERROR {type(e).__name__}: {e}")  # Muestra el tipo y mensaje del error
        if e.__cause__:  # Si el error fue encadenado con "from e"
            print(f"   Causa original: {type(e.__cause__).__name__}: {e.__cause__}")  # Muestra la causa
    else:  # Si no hubo error
        print(f"   OK: {resultado}")  # Muestra el resultado


gestor = GestorServicios()  # Crea el gestor vacío

probar("1. Listar con el gestor vacío", gestor.listar_servicios)  # Debe avisar sin lanzar error
probar("2. Crear sala válida", lambda: gestor.crear_servicio("sala", "Sala Juntas", 50000, capacidad=12))  # Válido
probar("3. Crear equipo válido", lambda: gestor.crear_servicio(  # Válido
    "equipo", "Portátil Dell", 80000, tipo_equipo="Portátil", deposito=200000))  # Con depósito
probar("4. Crear asesoría válida", lambda: gestor.crear_servicio(  # Válido
    "asesoria", "Asesoría BD", 100000, nivel="Senior"))  # Nivel senior (factor 1.5)
probar("5. Tarifa negativa", lambda: gestor.crear_servicio("sala", "Sala B", -100, capacidad=5))  # TarifaInvalidaError
probar("6. Tarifa de tipo texto", lambda: gestor.crear_servicio("sala", "Sala C", "abc", capacidad=5))  # TarifaInvalidaError
probar("7. Falta la capacidad", lambda: gestor.crear_servicio("sala", "Sala D", 40000))  # DatosInvalidosError
probar("8. Nivel de asesor no válido", lambda: gestor.crear_servicio(  # DatosInvalidosError
    "asesoria", "Asesoría X", 90000, nivel="master"))  # Nivel inexistente
probar("9. Descuento de 150%", lambda: gestor.calcular_costo_servicio(  # DatosInvalidosError
    "Sala Juntas", 2, descuento=150))  # Descuento fuera de rango
probar("10. Costo sala 3 h con IVA 19%", lambda: gestor.calcular_costo_servicio(  # Válido
    "Sala Juntas", 3, impuesto=19))  # 50000 x 3 x 1.19
probar("11. Costo equipo 2 días con 10% de descuento", lambda: gestor.calcular_costo_servicio(  # Válido
    "Portátil Dell", 2, descuento=10))  # 80000 x 2 x 0.9 + 200000
def costo_servicio_desactivado():  # Prueba auxiliar para el caso 12
    """Desactiva la asesoría e intenta calcular su costo."""
    gestor.buscar_servicio("Asesoría BD").disponible = False  # Marca la asesoría como no disponible
    return gestor.calcular_costo_servicio("Asesoría BD", 2)  # Debe lanzar ServicioNoDisponibleError


probar("12. Servicio no disponible", costo_servicio_desactivado)  # ServicioNoDisponibleError
probar("13. Posición inexistente (error encadenado)", lambda: gestor.obtener_servicio(10))  # ServicioNoEncontradoError
probar("14. Instanciar la clase abstracta", lambda: Servicio("Genérico", 1000))  # TypeError de Python

print("\n>> Polimorfismo: costo de 2 unidades de cada servicio disponible")  # Título de la demostración
for indice in range(2):  # Recorre la sala y el equipo
    servicio = gestor.obtener_servicio(indice)  # Obtiene el servicio
    print(f"   {servicio.nombre}: ${servicio.calcular_costo(2):,.2f}")  # Misma llamada, regla distinta

print("\n>> Listado final")  # Título del listado
for linea in gestor.listar_servicios():  # Recorre las descripciones
    print(f"   {linea}")  # Muestra cada servicio
print("\nRevise el archivo logs/sistema.log para ver los errores y eventos registrados.")  # Indicación final
