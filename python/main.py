from collections import deque
from pathlib import Path

CARPETA = Path(__file__).resolve().parent

ARCHIVO_ALUMNOS = CARPETA / "alumnos.txt"
ARCHIVO_PROFESORES = CARPETA / "profesores.txt"
ARCHIVO_CERTIFICADOS = CARPETA / "certificados_pendientes.txt"

class Persona:
    def __init__(self, cedula, nombre, correo):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo

    def mostrar_datos(self):
        print("Cédula:", self.cedula)
        print("Nombre:", self.nombre)
        print("Correo:", self.correo)
        
class Alumno(Persona):
    def __init__(self, cedula, nombre, correo, programa):
        super().__init__(cedula, nombre, correo)

        self.programa = programa
        self.notas = []

    def registrar_nota(self, nota):
        if len(self.notas) < 3:
            self.notas.append(nota)
            return True

        return False

    def eliminar_ultima_nota(self):
        if len(self.notas) > 0:
            return self.notas.pop()

        return None

    def calcular_promedio(self):
        if len(self.notas) == 0:
            return 0

        return sum(self.notas) / len(self.notas)
    
class Profesor(Persona):
    def __init__(self, cedula, nombre, correo, especialidad, materia):
        super().__init__(cedula, nombre, correo)

        self.especialidad = especialidad
        self.materia = materia
        
class ProgramaAcademico:
    nombre = "Programa"

    def evaluar_aprobacion(self, notas):
        pass


class Curso(ProgramaAcademico):
    nombre = "Curso"

    def evaluar_aprobacion(self, notas):
        if len(notas) < 3:
            return False

        promedio = sum(notas) / len(notas)

        return promedio >= 10


class Diplomado(ProgramaAcademico):
    nombre = "Diplomado"

    def evaluar_aprobacion(self, notas):
        if len(notas) < 3:
            return False

        promedio = sum(notas) / len(notas)

        return promedio >= 14


class Bootcamp(ProgramaAcademico):
    nombre = "Bootcamp"

    def evaluar_aprobacion(self, notas):
        if len(notas) < 3:
            return False

        for nota in notas:
            if nota < 14:
                return False

        return True
    
def crear_programa(nombre):
    if nombre == "Curso":
        return Curso()

    if nombre == "Diplomado":
        return Diplomado()

    if nombre == "Bootcamp":
        return Bootcamp()

    return None
    
class SistemaGestionAcademica:
    def __init__(self):
        self.alumnos = []
        self.profesores = []

        self.pila_deshacer = []
        self.cola_certificados = deque()

        ARCHIVO_ALUMNOS.touch(exist_ok=True)
        ARCHIVO_PROFESORES.touch(exist_ok=True)

        self.cargar_datos()


    def guardar_alumnos(self):
        with open(ARCHIVO_ALUMNOS, "w", encoding="utf-8") as archivo:

            for alumno in self.alumnos:

                notas = alumno.notas.copy()

                while len(notas) < 3:
                    notas.append(0)

                archivo.write(
                    f"{alumno.cedula},{alumno.nombre},{alumno.correo},"
                    f"{alumno.programa.nombre},"
                    f"{notas[0]},{notas[1]},{notas[2]}\n"
                )


    def guardar_profesores(self):
        with open(ARCHIVO_PROFESORES, "w", encoding="utf-8") as archivo:

            for profesor in self.profesores:

                archivo.write(
                    f"{profesor.cedula},{profesor.nombre},{profesor.correo},"
                    f"{profesor.especialidad},{profesor.materia}\n"
                )


    def cargar_datos(self):
        self.alumnos = []
        self.profesores = []

        # Cargar alumnos
        with open(ARCHIVO_ALUMNOS, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                datos = linea.strip().split(",")

                if len(datos) != 7:
                    continue

                cedula = datos[0]
                nombre = datos[1]
                correo = datos[2]
                programa = crear_programa(datos[3])

                if programa is None:
                    continue

                alumno = Alumno(
                    cedula,
                    nombre,
                    correo,
                    programa
                )

                for dato_nota in datos[4:7]:

                    try:
                        nota = float(dato_nota)

                        if nota != 0:
                            alumno.notas.append(nota)

                    except ValueError:
                        pass

                self.alumnos.append(alumno)

        # Cargar profesores
        with open(ARCHIVO_PROFESORES, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                datos = linea.strip().split(",")

                if len(datos) != 5:
                    continue

                profesor = Profesor(
                    datos[0],
                    datos[1],
                    datos[2],
                    datos[3],
                    datos[4]
                )

                self.profesores.append(profesor)


    def buscar_alumno(self, cedula):
        for alumno in self.alumnos:

            if alumno.cedula == cedula:
                return alumno

        return None


    def cedula_existe(self, cedula):
        for alumno in self.alumnos:

            if alumno.cedula == cedula:
                return True

        for profesor in self.profesores:

            if profesor.cedula == cedula:
                return True

        return False


    def registrar_alumno(self):
        print("\n--- REGISTRAR ALUMNO ---")

        cedula = input("Cédula: ").strip()

        if self.cedula_existe(cedula):
            print("Error: La cédula ya está registrada.")
            return

        nombre = input("Nombre completo: ").strip()
        correo = input("Correo: ").strip()

        print("\nSeleccione el programa:")
        print("1. Curso")
        print("2. Diplomado")
        print("3. Bootcamp")

        try:
            opcion = int(input("Programa (1-3): "))

        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            return

        if opcion == 1:
            programa = Curso()

        elif opcion == 2:
            programa = Diplomado()

        elif opcion == 3:
            programa = Bootcamp()

        else:
            print("Error: Programa no válido.")
            return

        alumno = Alumno(
            cedula,
            nombre,
            correo,
            programa
        )

        self.alumnos.append(alumno)

        self.guardar_alumnos()

        print("Alumno registrado correctamente.")


    def registrar_profesor(self):
        print("\n--- REGISTRAR PROFESOR ---")

        cedula = input("Cédula: ").strip()

        if self.cedula_existe(cedula):
            print("Error: La cédula ya está registrada.")
            return

        nombre = input("Nombre completo: ").strip()
        correo = input("Correo: ").strip()
        especialidad = input("Especialidad académica: ").strip()
        materia = input("Materia asignada: ").strip()

        profesor = Profesor(
            cedula,
            nombre,
            correo,
            especialidad,
            materia
        )

        self.profesores.append(profesor)

        self.guardar_profesores()

        print("Profesor registrado correctamente.")


    def registrar_nota(self):
        print("\n--- REGISTRAR NOTA ---")

        cedula = input("Cédula del alumno: ").strip()

        alumno = self.buscar_alumno(cedula)

        if alumno is None:
            print("Error: Alumno no encontrado.")
            return

        if len(alumno.notas) >= 3:
            print("El alumno ya tiene el máximo de 3 notas.")
            return

        try:
            nota = float(input("Ingrese la nota: "))

        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            return

        alumno.registrar_nota(nota)

        self.pila_deshacer.append(
            (alumno.cedula, nota)
        )

        self.guardar_alumnos()

        print("Nota registrada correctamente.")


    def deshacer_ultima_nota(self):
        print("\n--- DESHACER ÚLTIMA NOTA ---")

        if len(self.pila_deshacer) == 0:
            print("No hay ninguna nota reciente para deshacer.")
            return

        cedula, nota = self.pila_deshacer.pop()

        alumno = self.buscar_alumno(cedula)

        if alumno is None:
            print("Error: Alumno no encontrado.")
            return

        alumno.eliminar_ultima_nota()

        self.guardar_alumnos()

        print(f"Última nota eliminada correctamente: {nota}")


    def generar_certificados(self):
        print("\n--- GENERAR COLA DE CERTIFICADOS ---")

        self.cargar_datos()

        self.cola_certificados.clear()

        for alumno in self.alumnos:

            aprobado = alumno.programa.evaluar_aprobacion(
                alumno.notas
            )

            if aprobado:
                self.cola_certificados.append(alumno)

        total = len(self.cola_certificados)

        with open(
            ARCHIVO_CERTIFICADOS,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                "=========================================\n"
            )

            archivo.write(
                "REPORTE DE CERTIFICADOS PENDIENTES\n"
            )

            archivo.write(
                "=========================================\n"
            )

            archivo.write(
                f"Total de graduandos en cola: {total}\n"
            )

            numero = 1

            while len(self.cola_certificados) > 0:

                alumno = self.cola_certificados.popleft()

                archivo.write(
                    f"{numero}. [{alumno.cedula}] {alumno.nombre}\n"
                )

                archivo.write(
                    f"- Programa: {alumno.programa.nombre}\n"
                )

                archivo.write(
                    f"- Promedio Final: "
                    f"{alumno.calcular_promedio():.1f}\n"
                )

                archivo.write(
                    "- Estatus: APROBADO\n"
                )

                numero += 1

            archivo.write(
                "=========================================\n"
            )

            archivo.write(
                "* Fin del reporte - Generado por SGA-DO *\n"
            )

        print(
            "Archivo certificados_pendientes.txt generado correctamente."
        )


    def mostrar_reporte(self):
        self.cargar_datos()

        print("\n==========================================")
        print("REPORTE GENERAL DEL SISTEMA")
        print("==========================================")

        print("\n--- PROFESORES ACTIVOS ---")

        if len(self.profesores) == 0:
            print("No hay profesores registrados.")

        else:
            for profesor in self.profesores:

                print(
                    f"Cédula: {profesor.cedula} | "
                    f"Nombre: {profesor.nombre} | "
                    f"Especialidad: {profesor.especialidad} | "
                    f"Materia: {profesor.materia}"
                )

        print("\n--- ALUMNOS REGISTRADOS ---")

        if len(self.alumnos) == 0:
            print("No hay alumnos registrados.")

        else:
            for alumno in self.alumnos:

                if len(alumno.notas) < 3:
                    estado = "PENDIENTE"

                elif alumno.programa.evaluar_aprobacion(
                    alumno.notas
                ):
                    estado = "APROBADO"

                else:
                    estado = "REPROBADO"

                print(
                    f"Cédula: {alumno.cedula} | "
                    f"Nombre: {alumno.nombre} | "
                    f"Programa: {alumno.programa.nombre} | "
                    f"Notas: {alumno.notas} | "
                    f"Promedio: {alumno.calcular_promedio():.1f} | "
                    f"Estatus: {estado}"
                )


    def mostrar_menu(self):
        print("\n==================================================")
        print("SGA-DO: SISTEMA DIPLOMADOSONLINE")
        print("==================================================")
        print("1. Registrar Alumno")
        print("2. Registrar Profesor")
        print("3. Registrar Notas a un Alumno")
        print("4. Deshacer Último Registro de Nota")
        print("5. Generar Cola de Certificados")
        print("6. Mostrar Reporte General")
        print("7. Salir")
        print("==================================================")


    def iniciar(self):
        while True:

            self.mostrar_menu()

            try:
                opcion = int(
                    input("Seleccione una opción (1-7): ")
                )

            except ValueError:
                print(
                    "Error: Ingrese un valor numérico válido."
                )

                continue

            if opcion == 1:
                self.registrar_alumno()

            elif opcion == 2:
                self.registrar_profesor()

            elif opcion == 3:
                self.registrar_nota()

            elif opcion == 4:
                self.deshacer_ultima_nota()

            elif opcion == 5:
                self.generar_certificados()

            elif opcion == 6:
                self.mostrar_reporte()

            elif opcion == 7:

                self.guardar_alumnos()
                self.guardar_profesores()

                print("\nCambios guardados.")
                print("Programa finalizado.")

                break

            else:
                print(
                    "Error: Seleccione una opción válida del 1 al 7."
                )

if __name__ == "__main__":
    sistema = SistemaGestionAcademica()
    sistema.iniciar()