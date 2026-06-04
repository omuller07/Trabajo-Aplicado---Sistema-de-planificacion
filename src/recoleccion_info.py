import pandas as pd
from datetime import datetime


def pedir_fecha(mensaje):
    while True:
        texto = input(mensaje + " (dd/mm/aaaa): ")

        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()

        except ValueError:
            print("Error: fecha inválida. Usá el formato dd/mm/aaaa.")


def pedir_horas_dia(nombre_dia):
    while True:
        try:
            horas = float(input(f"¿Cuántas horas podés estudiar los {nombre_dia}?: "))

            if 0 <= horas <= 12:
                return horas

            print("Error: las horas deben estar entre 0 y 12.")

        except ValueError:
            print("Error: ingresá un número válido.")


def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))

            if minimo <= numero <= maximo:
                return numero

            print(f"Error: el número debe estar entre {minimo} y {maximo}.")

        except ValueError:
            print("Error: ingresá un número válido.")


def recolectar_disponibilidad():
    print("\nDISPONIBILIDAD SEMANAL")
    print("Si un día no podés estudiar, escribí 0.\n")

    disponibilidad = {"lunes": pedir_horas_dia("lunes"),
                      "martes": pedir_horas_dia("martes"),
                      "miercoles": pedir_horas_dia("miércoles"),
                      "jueves": pedir_horas_dia("jueves"),
                      "viernes": pedir_horas_dia("viernes"),
                      "sabado": pedir_horas_dia("sábados"),
                      "domingo": pedir_horas_dia("domingos")}

    df_disponibilidad = pd.DataFrame([disponibilidad])

    return df_disponibilidad


def recolectar_materias_y_temas():
    materias = []
    temas = []

    cantidad_materias = pedir_entero("\n¿Cuántas materias/exámenes querés planificar?: ", 1, 10)

    for i in range(cantidad_materias):
        print(f"\nMATERIA {i + 1}")

        id_materia = i + 1

        nombre_materia = input("Nombre de la materia: ")

        fecha_inicio = pedir_fecha("Fecha de inicio del estudio")

        fecha_examen = pedir_fecha("Fecha del examen")

        materias.append({"id_materia": id_materia,
                         "materia": nombre_materia,
                         "fecha_inicio": fecha_inicio,
                         "fecha_examen": fecha_examen})

        cantidad_temas = pedir_entero(f"¿Cuántos temas tiene {nombre_materia}?: ", 1, 30)

        for j in range(cantidad_temas):
            print(f"\nTema {j + 1} de {nombre_materia}")

            nombre_tema = input("Nombre del tema: ")

            dificultad = pedir_entero("Dificultad del tema (1 a 10): ", 1, 10)

            conocimiento = pedir_entero("Conocimiento previo (1 a 5): ", 1, 5)

            temas.append({"id_materia": id_materia,
                          "tema": nombre_tema,
                          "dificultad": dificultad,
                          "conocimiento": conocimiento})

    df_materias = pd.DataFrame(materias)
    df_temas = pd.DataFrame(temas)

    return df_materias, df_temas


def recolectar_informacion():
    print("PLANIFICADOR DE ESTUDIO")
    print("-----------------------")

    df_disponibilidad = recolectar_disponibilidad()

    df_materias, df_temas = recolectar_materias_y_temas()

    return df_disponibilidad, df_materias, df_temas
