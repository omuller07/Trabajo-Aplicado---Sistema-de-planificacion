
import pandas as pd
from datetime import datetime


def pedir_fecha(mensaje):
    """
    Solicita al usuario una fecha y verifica que tenga un formato válido.

    Parameters:
    ----------
    mensaje : str
        Mensaje que se mostrará al usuario antes de pedir la fecha.

    Returns:
    ----------
    datetime.date
        Fecha ingresada por el usuario.
    """
    while True:
        texto = input(mensaje + "(dd/mm/aaaa): ")

        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
            # Convierte el texto ingresado a una fecha. --> "%d/%m/%Y" indica el formato día/mes/año.

        except ValueError:
            print("Error: fecha inválida.")


def pedir_horas_dia(nombre_dia):
    

    """
    Pide la capacidad horaria del usuario por dia, y la valida.
    Parameters
    ----------
    nombre_dia : str
        Texto que se muestra el nombre del dia del cual 
        se esta pidiendo la capcidad horaria


    """
    
    while True:
        try:
            horas = float(input(f"¿Cuántas horas podés estudiar los {nombre_dia}?: "))

            if 0 <= horas <= 12:
                return horas

            print("Error: las horas deben estar entre 0 y 12.")

        except ValueError:
            print("Error: ingresá un número válido.")


def pedir_entero(mensaje, minimo, maximo):
    '''
    Pide un numero y lo valida teniendo en cuenta un minimo y un maximo

    Parameters
    ----------
    mensaje : str
        TExto que se meustra al pedir el input.
    minimo : int
        Minimo que debe superar el numero ingresado.
    maximo : int
        Maximo para el numero ingresado.

    Returns
    -------
    numero : int
        Numero ingresado, ya validado.

    '''
    while True:
        try:
            numero = int(input(mensaje))

            if minimo <= numero <= maximo:
                return numero

            print(f"Error: el número debe estar entre {minimo} y {maximo}.")

        except ValueError:
            print("Error: ingresá un número válido.")


def recolectar_disponibilidad():
    '''
    Recorre los dias de la semana pidiendo la cantidad de horas 
    disponibles para estudiar y construye un DataFrame con esa informacion

    Muestra por consola un encabezado y solicita, para cada día,
    las horas disponibles mediante ``pedir_horas_dia()``. Si un día
    no hay disponibilidad, el usuario debe ingresar 0.
    Returns
    -------
    df_disponibilidad : pandas.DataFrame
        DataFrame de una fila y siete columnas (lunes a domingo) con
        la cantidad de horas disponibles para estudiar cada día..

    '''
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
    """
    Pide al usuario ingresar la cantidad de materias, 
    los nombres la fecha de inicio de estudio, de examen y 
    cantidad de temas de ellas. Pide al usuario que ingrese 
    la cantidad de conocimiento previo que posee por tema y la dificultad de cada uno
    Construye doss dataframes con la informacion recolectada. 
    

    Returns
    -------
    df_materias : pandas.DataFrame
        Dataframe con la infroamcion de cada materia ingresada: 
        id de materia, nombre, fecha de inicio de estudio, fecha de examen.
    df_temas : pandas.DataFrame
        Dataframe con la infroamcion de cada tema ingresada: 
         id de materia, nombre del tema. dificultad, conocimiento previo

    """
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
    """
    Coordina la recolección de toda la información necesaria para
    armar el plan de estudio. Muestra el encabezado del programa 
   
    Returns
    -------
    df_disponibilidad : pandas.DataFrame
        DataFrame de una fila y siete columnas con las horas
        disponibles para estudiar cada día de la semana.
    df_materias : pandas.DataFrame
        DataFrame con las materias ingresadas por el usuario.
    df_temas : pandas.DataFrame
        DataFrame con los temas asociados a cada materia.
    """
    
    
    print("PLANIFICADOR DE ESTUDIO")
    print("-----------------------")

    df_disponibilidad = recolectar_disponibilidad()

    df_materias, df_temas = recolectar_materias_y_temas()

    return df_disponibilidad, df_materias, df_temas
