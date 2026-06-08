import pandas as pd


def guardar_datos_iniciales(df_disponibilidad, df_materias, df_temas):
    """
    Guarda los datos ingresados por el usuario en archivos CSV.

    Parameters:
    ----------
    df_disponibilidad : pandas.DataFrame
        Contiene las horas disponibles para estudiar cada día de la semana.

    df_materias : pandas.DataFrame
        Contiene la información de las materias, incluyendo nombre,
        fecha de inicio y fecha de examen.

    df_temas : pandas.DataFrame
        Contiene los temas de cada materia junto con su dificultad
        y conocimiento previo.

    Returns:
    ----------
    None
    """
#index=False evita que pandas agregue una columna extra con los números de fila.

    df_disponibilidad.to_csv("datos/disponibilidad.csv",index=False)

    df_materias.to_csv("datos/materias.csv",index=False)

    df_temas.to_csv("datos/temas.csv",index=False)


def guardar_plan(plan):
    """
    Convierte el plan de estudio en un DataFrame y lo guarda
    en un archivo CSV.

    Parameters:
    ----------
    plan : dict
        Diccionario que cada clave es una fecha y  valor es una
        lista de actividades planificadas para ese día.

    Returns:
    ----------
    None
    """

    filas = []
    # Recorre cada fecha y las actividades asociadas a esa fecha.
    for fecha, actividades in plan.items():
        # Recorre cada actividad planificada para esa fecha.
        for actividad in actividades:
            # Convierte cada actividad en una fila para el DataFrame.
            filas.append({"fecha": fecha,
                          "materia": actividad["materia"],
                          "tema": actividad["tema"],
                          "actividad": actividad["actividad"],
                          "horas": actividad["horas"]})
    # Convierte la lista de diccionarios en una tabla.
    df_plan = pd.DataFrame(filas)
    # Guarda el plan en formato CSV.
    df_plan.to_csv("datos/plan.csv",index=False)


def cargar_datos_iniciales():
    """
    • Carga desde archivos CSV la disponibilidad, las materias y los temas ingresados por el usuario.
    • Convierte las columnas de fechas al tipo date.
    
    Returns:
    ----------
    tuple
        Tupla formada por: df_disponibilidad : pandas.DataFrame
                           df_materias : pandas.DataFrame
                           df_temas : pandas.DataFrame
    """
    # Carga la disponibilidad semanal.
    df_disponibilidad = pd.read_csv("datos/disponibilidad.csv")
    # Carga la información de las materias.
    df_materias = pd.read_csv("datos/materias.csv")
    # Carga la información de los temas.
    df_temas = pd.read_csv("datos/temas.csv")
    # Convierte la columna a tipo date.
        # Cuando se lee un CSV, las fechas se cargan como texto.
    df_materias["fecha_inicio"] = pd.to_datetime(df_materias["fecha_inicio"]).dt.date
    df_materias["fecha_examen"] = pd.to_datetime(df_materias["fecha_examen"]).dt.date

    return (df_disponibilidad, df_materias, df_temas)


def cargar_plan():
    """
    • Carga el plan de estudio guardado en un archivo CSV.
    • Convierte la columna fecha del plan al tipo date.
    
    Returns:
    ----------
    pandas.DataFrame
        DataFrame con las actividades planificadas.
    
    Si el archivo no existe:
    ----------
    pandas.DataFrame
        DataFrame vacío con las columnas necesarias para el plan.
    """

    try:
    # Intenta abrir el archivo donde se guardó el plan.
        df_plan = pd.read_csv("datos/plan.csv")
        # Convierte la columna fecha de texto a tipo date.
        df_plan["fecha"] = pd.to_datetime(df_plan["fecha"]).dt.date 
        
        return df_plan

    except FileNotFoundError:
        # Si el archivo todavía no existe, devuelve un DataFrame vacío con la estructura esperada por el resto del programa.
        return pd.DataFrame(columns=["fecha", "materia", "tema", "actividad", "horas"])


def guardar_progreso(df_progreso):
    """
    Guarda el progreso registrado por el usuario en un archivo CSV.

    Parameters:
    ----------
    df_progreso : pandas.DataFrame
        DataFrame con las horas realizadas para cada actividad.

    Returns:
    ----------
    None
    """
    df_progreso.to_csv("datos/progreso.csv",index=False)



def cargar_progreso():
    """
    • Carga el progreso registrado por el usuario desde un archivo CSV.
    • Convierte la columna fecha al tipo date.

    Returns:
    ----------
    pandas.DataFrame
        DataFrame con el progreso registrado.

    Si el archivo no existe:
    ----------
    pandas.DataFrame
        DataFrame vacío con las columnas necesarias para almacenar el progreso.
    """
    try:

        df_progreso = pd.read_csv("datos/progreso.csv")

        df_progreso["fecha"] = pd.to_datetime(df_progreso["fecha"]).dt.date

        return df_progreso

    except FileNotFoundError:
        # Si todavía no existe un archivo de progreso, devuelve un DataFrame vacío con la estructura esperada.
        return pd.DataFrame(columns=["fecha", "materia", "tema", "actividad", "horas_realizadas"])

def plan_dataframe_a_diccionario(df_plan):
    """
    Convierte un DataFrame con actividades planificadas en un diccionario organizado por fechas.

    Parameters:
    ----------
    df_plan : pandas.DataFrame
        DataFrame que contiene las actividades del plan de estudio.

    Returns:
    ----------
    dict
        Diccionario donde cada clave es una fecha y cada valor es una lista de actividades correspondientes a ese día.
    """
    plan = {}
    # iterrows --> Recorre cada fila del DataFrame.
    for indice, fila in df_plan.iterrows():
        
        fecha = fila["fecha"]
        # Si la fecha todavía no existe en el diccionario, crea una lista vacía para almacenar sus actividades.
        if fecha not in plan:
            plan[fecha] = []

        plan[fecha].append({"materia": fila["materia"],
                            "tema": fila["tema"],
                            "actividad": fila["actividad"],
                            "horas": fila["horas"]})

    return plan