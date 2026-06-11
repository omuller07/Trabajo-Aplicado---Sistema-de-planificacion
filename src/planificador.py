from datetime import timedelta
import math

# timedelta representa una duración de tiempo (para sumar o restar fechas)
# math contiene funciones matemáticas útiles


def calcular_dias_restantes(fecha_inicio, fecha_examen):
    '''
    Calcula los dias que faltan para el examen.

    Parameters
    ----------
    fecha_inicio : datetime
        Fecha de inicio del estudio.
    fecha_examen : datetime
        Fecha del examen.

    Returns
    -------
    int
        Dias que faltan para examen.

    '''
    return (fecha_examen - fecha_inicio).days
    # .days extrae la cantidad de días como un int


def calcular_urgencia(dias_restantes):
    '''
    Calcula la urgencia del examen usando la formula 10 / (dias que faltan)

    Parameters
    ----------
    dias_restantes : int
        Dias que faltan para el examen.

    Returns
    -------
    int
        Urgencia del examen.

    '''
    if dias_restantes <= 0:
        return 10

    return 10 / dias_restantes


def obtener_nombre_dia(fecha):
    '''
    

    Parameters
    ----------
    fecha : datetime.date
        Fecha que se quiere obtener el dia de la semana.

    Returns
    -------
    str
        Nombre del dia de la semana.

    '''

    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    return dias[fecha.weekday()]
    # .weekday() devuelve un entero entre 0 y 6


def crear_rango_fechas(fecha_inicio, fecha_examen):
    '''
    Genera una lista con las fechas de estudio  entre la fecha de inicio y la fecha del examen.

    Parameters
    ----------
    fecha_inicio : datetime.date
        Fecha de inicio del estudio.
    fecha_examen : datetime.date
        Fecha del examen.

    Returns
    -------
    fechas : list
        Lista con todas las fechas entre inicio y examen.

    '''
    fechas = []

    fecha_actual = fecha_inicio

    while fecha_actual < fecha_examen:
        fechas.append(fecha_actual)
        fecha_actual += timedelta(days=1) #fecha_actual = fecha_actual + 1 día

    return fechas


def calcular_prioridades(df_materias, df_temas):
    '''
    Calcula la prioridad de estudio de cada tema.

    Parameters
    ----------
    df_materias : DataFrame
        Contiene la informacion de las materias.
    df_temas : DataFrame
        Contiene la informacion de cada uno de los temas.

    Returns
    -------
    df : DataFrame
        Devuelve el mismo DataFrame de los temas pero con una columna adicional.

    '''
    df = df_temas.copy()

    df = df.merge(df_materias, on="id_materia") #junta la info por materia

    prioridades = []

    for indice, fila in df.iterrows():
        dias_restantes = calcular_dias_restantes(
            fila["fecha_inicio"],
            fila["fecha_examen"])

        urgencia = calcular_urgencia(dias_restantes)

        prioridad = (
            2 * fila["dificultad"]
            + (6 - fila["conocimiento"])
            + urgencia)
        
        prioridades.append(prioridad)

    df["prioridad"] = prioridades

    return df


def calcular_horas_necesarias(df):
    '''
    Calcula las horas necesarias para estudiar cada tema.

    Parameters
    ----------
    df : DataFrame
        Contiene informacion sobre cada uno de los temas.

    Returns
    -------
    df : DataFrame
        Devuelve el mismo DataFrame pero con una columna adicional de cuantas horas se necesitan para estudiar.

    '''
    df = df.copy()

    df["horas_necesarias"] = (
        1
        + df["dificultad"] * 0.3
        + (6 - df["conocimiento"]) * 0.3)

    df["horas_necesarias"] = df["horas_necesarias"].round(1) #redondeá a 1 decimal. ej 3,56 --> 3,6

    return df


def crear_estructura_plan(df_disponibilidad, df_materias):
    '''
    Crea un diccionario para almacenar las actividades asignadas a cada
    fecha, otro para registrar la carga de estudio diaria y otro para
    guardar la capacidad disponible de cada día según la disponibilidad
    del estudiante.

    Parameters
    ----------
    df_disponibilidad : DataFrame
        Contiene las horas disponibles del estudiante en cada dia de la semana.
    df_materias : DataFram
        Contiene la informacion de las materias.

    Returns
    -------
    plan : diccio
        Asocia cada fecha con una lista de actividades.
    carga_diaria : diccio
        Registra la carga de estudio acumulada por fecha.
    capacidad_diaria : diccio
        Indica la cantidad de horas disponibles para estudiar en cada fecha.

    '''
    plan = {}
    carga_diaria = {}
    capacidad_diaria = {}

    for indice, materia in df_materias.iterrows():
        fechas = crear_rango_fechas(
            materia["fecha_inicio"],
            materia["fecha_examen"])

        for fecha in fechas:
            if fecha not in plan:
                plan[fecha] = []
                carga_diaria[fecha] = 0

                nombre_dia = obtener_nombre_dia(fecha)
                capacidad_diaria[fecha] = df_disponibilidad.loc[0, nombre_dia]

    return plan, carga_diaria, capacidad_diaria


def asignar_bloque_repartido(plan, fechas_posibles, carga_diaria, capacidad_diaria, materia, tema, actividad, horas_bloque):
    '''
    Distribuye las horas de una actividad entre las fechas posibles, priorizando aquellas con menor carga de estudio.

    Parameters
    ----------
    plan : diccio
        Diccionario que almacena las actividades asignadas a cada fecha.
    fechas_posibles : list
        Lista de fechas en las que puede programarse la actividad.
    carga_diaria : diccio
        Diccionario que registra las horas de estudio ya asignadas a cada fecha.
    capacidad_diaria : diccio
        Diccionario que indica la cantidad máxima de horas disponibles para estudiar en cada fecha.
    materia : str
        Nombre de la materia asociada a la actividad.
    tema : str
        Nombre del tema asociado a la actividad.
    actividad : str
        Tipo o descripción de la actividad a realizar.
    horas_bloque : float
        Cantidad de horas que se desea asignar.

    Returns
    -------
    float
        Cantidad de horas que no pudieron asignarse. Devuelve 0 si la actividad fue asignada completamente.

    '''
    horas_pendientes = horas_bloque

    fechas_ordenadas = sorted(
        fechas_posibles,
        key=lambda fecha: carga_diaria[fecha])

    for fecha in fechas_ordenadas:
        espacio_disponible = capacidad_diaria[fecha] - carga_diaria[fecha]
        if espacio_disponible > 0:
            if horas_pendientes <= espacio_disponible:
                horas_asignadas = horas_pendientes
            else:
                horas_asignadas = espacio_disponible

            plan[fecha].append({"materia": materia, "tema": tema,
                "actividad": actividad, "horas": round(horas_asignadas, 1)})

            carga_diaria[fecha] += horas_asignadas
            horas_pendientes -= horas_asignadas

        if horas_pendientes <= 0:
            return 0

    return horas_pendientes

def reservar_repasos_pre_examen(plan, carga_diaria, capacidad_diaria, df_materias):

    for indice, materia in df_materias.iterrows():

        fecha_repaso = materia["fecha_examen"] - timedelta(days=1)

        if fecha_repaso in plan:

            horas_repaso = 3

            if capacidad_diaria[fecha_repaso] >= horas_repaso:

                plan[fecha_repaso].append({
                    "materia": materia["materia"],
                    "tema": "Repaso general",
                    "actividad": "Repaso pre-examen",
                    "horas": horas_repaso})

                carga_diaria[fecha_repaso] += horas_repaso

            else:
                print("No hay disponibilidad suficiente para repasar el día anterior al examen de", materia["materia"])

def generar_plan(df_disponibilidad, df_materias, df_temas):
    '''
    las materias y los temas a estudiar.

    Parameters
    ----------
    df_disponibilidad : DataFrame
        Contiene horas disponibles para estudiar en cada día de la semana.
    df_materias : DataFrame
        Contiene información de las materias.
    df_temas : DataFrame
        Contiene información de los temas a estudiar.

    Returns
    -------
    plan : diccio
        Con actividades asignadas a cada fecha.
    temas_ordenados : DataFrame
        Contiene temas ordenados según su prioridad de estudio.
    carga_diaria : diccio
        Con horas de estudio asignadas a cada fecha.
    capacidad_diaria : diccio
        Con horas máximas disponibles por fecha.
    temas_no_asignados : list
        Con actividades que no pudieron programarse completamente y las horas faltantes.

    '''

    temas_priorizados = calcular_prioridades(df_materias, df_temas)

    temas_con_horas = calcular_horas_necesarias(temas_priorizados)

    temas_ordenados = temas_con_horas.sort_values("prioridad", ascending=False)
    # ordena el DataFrame temas_con_horas según la columna "prioridad" de mayor a menor

    plan, carga_diaria, capacidad_diaria = crear_estructura_plan(df_disponibilidad, df_materias)
    
    reservar_repasos_pre_examen(plan, carga_diaria,capacidad_diaria,df_materias) 
    
    temas_no_asignados = []

    for indice, tema in temas_ordenados.iterrows():

        fechas_posibles = crear_rango_fechas(tema["fecha_inicio"], tema["fecha_examen"])

        horas_necesarias = tema["horas_necesarias"]

        cantidad_bloques = math.ceil(horas_necesarias / 1.5) #redondea para arriba. ej 2,66 --> 3.

        horas_por_bloque = round(horas_necesarias / cantidad_bloques,1 ) #the lo redondea un decimal. 3,66 -->3,6

        for bloque in range(cantidad_bloques):

            if bloque == 0:
                actividad = "Estudio"

            elif bloque == cantidad_bloques - 1:
                actividad = "Repaso"

            else:
                actividad = "Práctica"

            horas_sin_asignar = asignar_bloque_repartido(plan, fechas_posibles, carga_diaria,
                                                         capacidad_diaria, tema["materia"], tema["tema"],
                                                         actividad, horas_por_bloque)

            if horas_sin_asignar > 0:
                temas_no_asignados.append({"materia": tema["materia"], "tema": tema["tema"],
                                           "actividad": actividad, "horas_faltantes": round(horas_sin_asignar, 1)})

    return (plan, temas_ordenados, carga_diaria, capacidad_diaria, temas_no_asignados)






