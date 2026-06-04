from datetime import timedelta
import math


def calcular_dias_restantes(fecha_inicio, fecha_examen):
    return (fecha_examen - fecha_inicio).days


def calcular_urgencia(dias_restantes):
    if dias_restantes <= 0:
        return 10

    return 10 / dias_restantes


def obtener_nombre_dia(fecha):

    dias = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo"]

    return dias[fecha.weekday()]


def crear_rango_fechas(fecha_inicio, fecha_examen):
    fechas = []

    fecha_actual = fecha_inicio

    while fecha_actual < fecha_examen:
        fechas.append(fecha_actual)
        fecha_actual += timedelta(days=1) #fecha_actual = fecha_actual + 1 día

    return fechas


def calcular_prioridades(df_materias, df_temas):
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
    df = df.copy()

    df["horas_necesarias"] = (
        1
        + df["dificultad"] * 0.3
        + (6 - df["conocimiento"]) * 0.3)

    df["horas_necesarias"] = df["horas_necesarias"].round(1) #redondeá a 1 decimal. ej 3,56 --> 3,6

    return df


def crear_estructura_plan(df_disponibilidad, df_materias):
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


def asignar_bloque_repartido(
    plan,
    fechas_posibles,
    carga_diaria,
    capacidad_diaria,
    materia,
    tema,
    actividad,
    horas_bloque):
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

            plan[fecha].append({
                "materia": materia,
                "tema": tema,
                "actividad": actividad,
                "horas": round(horas_asignadas, 1)})

            carga_diaria[fecha] += horas_asignadas
            horas_pendientes -= horas_asignadas

        if horas_pendientes <= 0:
            return 0

    return horas_pendientes


def generar_plan(df_disponibilidad, df_materias, df_temas):

    temas_priorizados = calcular_prioridades(
        df_materias,
        df_temas)

    temas_con_horas = calcular_horas_necesarias(
        temas_priorizados)

    temas_ordenados = temas_con_horas.sort_values(
        "prioridad",
        ascending=False)

    plan, carga_diaria, capacidad_diaria = crear_estructura_plan(
        df_disponibilidad,
        df_materias)

    temas_no_asignados = []

    for indice, tema in temas_ordenados.iterrows():

        fechas_posibles = crear_rango_fechas(
            tema["fecha_inicio"],
            tema["fecha_examen"]
        )

        horas_necesarias = tema["horas_necesarias"]

        cantidad_bloques = math.ceil(horas_necesarias / 1.5)#redondea para arriba. ej 2,66 --> 3.

        horas_por_bloque = round(horas_necesarias / cantidad_bloques,1 )#the lo redondea un decimal. 3,66 -->3,6

        for bloque in range(cantidad_bloques):

            if bloque == 0:
                actividad = "Estudio"

            elif bloque == cantidad_bloques - 1:
                actividad = "Repaso"

            else:
                actividad = "Práctica"

            horas_sin_asignar = asignar_bloque_repartido(
                plan,
                fechas_posibles,
                carga_diaria,
                capacidad_diaria,
                tema["materia"],
                tema["tema"],
                actividad,
                horas_por_bloque
            )

            if horas_sin_asignar > 0:
                temas_no_asignados.append({
                    "materia": tema["materia"],
                    "tema": tema["tema"],
                    "actividad": actividad,
                    "horas_faltantes": round(horas_sin_asignar, 1)
                })

    return (plan, temas_ordenados, carga_diaria, capacidad_diaria, temas_no_asignados)