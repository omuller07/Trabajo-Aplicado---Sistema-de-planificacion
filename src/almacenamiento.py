import pandas as pd


def guardar_datos_iniciales(
    df_disponibilidad,
    df_materias,
    df_temas
):

    df_disponibilidad.to_csv(
        "datos/disponibilidad.csv",
        index=False
    )

    df_materias.to_csv(
        "datos/materias.csv",
        index=False
    )

    df_temas.to_csv(
        "datos/temas.csv",
        index=False
    )


def guardar_plan(plan):

    filas = []

    for fecha, actividades in plan.items():

        for actividad in actividades:

            filas.append({
                "fecha": fecha,
                "materia": actividad["materia"],
                "tema": actividad["tema"],
                "actividad": actividad["actividad"],
                "horas": actividad["horas"]
            })

    df_plan = pd.DataFrame(filas)

    df_plan.to_csv(
        "datos/plan.csv",
        index=False
    )


def cargar_datos_iniciales():

    df_disponibilidad = pd.read_csv(
        "datos/disponibilidad.csv"
    )

    df_materias = pd.read_csv(
        "datos/materias.csv"
    )

    df_temas = pd.read_csv(
        "datos/temas.csv"
    )

    df_materias["fecha_inicio"] = pd.to_datetime(
        df_materias["fecha_inicio"]
    ).dt.date

    df_materias["fecha_examen"] = pd.to_datetime(
        df_materias["fecha_examen"]
    ).dt.date

    return (
        df_disponibilidad,
        df_materias,
        df_temas
    )


def cargar_plan():

    try:

        df_plan = pd.read_csv(
            "datos/plan.csv"
        )

        df_plan["fecha"] = pd.to_datetime(
            df_plan["fecha"]
        ).dt.date

        return df_plan

    except FileNotFoundError:

        return pd.DataFrame(
            columns=[
                "fecha",
                "materia",
                "tema",
                "actividad",
                "horas"
            ]
        )


def guardar_progreso(df_progreso):

    df_progreso.to_csv(
        "datos/progreso.csv",
        index=False
    )


def cargar_progreso():

    try:

        df_progreso = pd.read_csv(
            "datos/progreso.csv"
        )

        df_progreso["fecha"] = pd.to_datetime(
            df_progreso["fecha"]
        ).dt.date

        return df_progreso

    except FileNotFoundError:

        return pd.DataFrame(
            columns=[
                "fecha",
                "materia",
                "tema",
                "actividad",
                "horas_realizadas"
            ]
        )


def plan_dataframe_a_diccionario(df_plan):

    plan = {}

    for indice, fila in df_plan.iterrows():

        fecha = fila["fecha"]

        if fecha not in plan:
            plan[fecha] = []

        plan[fecha].append({
            "materia": fila["materia"],
            "tema": fila["tema"],
            "actividad": fila["actividad"],
            "horas": fila["horas"]
        })

    return plan