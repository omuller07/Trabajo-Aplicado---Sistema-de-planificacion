import pandas as pd
from datetime import datetime, date


def pedir_fecha(mensaje):
    while True:
        texto = input(mensaje + " (dd/mm/aaaa): ")

        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()

        except ValueError:
            print("Error: fecha inválida.")


def pedir_horas(mensaje):
    while True:
        try:
            horas = float(input(mensaje))

            if horas >= 0:
                return horas

            print("Error: las horas no pueden ser negativas.")

        except ValueError:
            print("Error: ingresá un número válido.")


def registrar_progreso_del_dia(df_plan, df_progreso):
    fecha = pedir_fecha("Ingresá la fecha en la que querés registrar progreso")

    plan_del_dia = df_plan[df_plan["fecha"] == fecha]

    if plan_del_dia.empty:
        print("No tenías actividades planificadas para ese día.")
        return df_progreso

    print("\nPLAN DEL DÍA")
    print(plan_del_dia[["materia", "tema", "actividad", "horas"]])

    nuevos_registros = []

    for indice, fila in plan_del_dia.iterrows():
        horas = pedir_horas(
            "¿Cuántas horas hiciste de "
            + fila["materia"]
            + " - "
            + fila["tema"]
            + "?: "
        )

        nuevos_registros.append({
            "fecha": fecha,
            "materia": fila["materia"],
            "tema": fila["tema"],
            "actividad": fila["actividad"],
            "horas_realizadas": horas
        })

    df_nuevo = pd.DataFrame(nuevos_registros)
    df_progreso = pd.concat([df_progreso, df_nuevo], ignore_index=True)

    return df_progreso


def detectar_alertas(df_plan, df_progreso):
    if df_progreso.empty:
        print("Todavía no hay progreso registrado.")
        return

    fecha_maxima = df_progreso["fecha"].max()

    plan_pasado = df_plan[df_plan["fecha"] <= fecha_maxima]

    horas_planificadas = plan_pasado["horas"].sum()
    horas_realizadas = df_progreso["horas_realizadas"].sum()

    print("\nSEGUIMIENTO")
    print("-----------")
    print("Horas planificadas hasta esa fecha:", round(horas_planificadas, 1))
    print("Horas realizadas:", round(horas_realizadas, 1))

    if horas_realizadas < horas_planificadas:
        print("Alerta: posible procrastinación. Hay horas pendientes.")

    elif horas_realizadas > horas_planificadas + 2:
        print("Alerta: posible sobreexigencia.")

    else:
        print("Vas bien con el plan.")

    progreso_por_dia = df_progreso.groupby("fecha")["horas_realizadas"].sum()

    for fecha, horas in progreso_por_dia.items():
        if horas > 4:
            print("Alerta de sobreexigencia:", fecha, "-", round(horas, 1), "hs estudiadas.")


def obtener_nombre_dia(fecha):
    dias = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo"
    ]

    return dias[fecha.weekday()]


def reorganizar_plan_por_progreso(df_plan, df_progreso, df_disponibilidad):
    if df_progreso.empty:
        return df_plan

    fecha_actual = df_progreso["fecha"].max()

    plan_pasado = df_plan[df_plan["fecha"] <= fecha_actual]
    plan_futuro = df_plan[df_plan["fecha"] > fecha_actual].copy()

    horas_planificadas = plan_pasado["horas"].sum()
    horas_realizadas = df_progreso["horas_realizadas"].sum()

    horas_pendientes = round(horas_planificadas - horas_realizadas, 1)

    if horas_pendientes <= 0:
        print("No hay horas pendientes para reorganizar.")
        return df_plan

    print("\nHay", horas_pendientes, "hs pendientes para reubicar.")

    nuevas_filas = []

    for indice, fila in plan_futuro.iterrows():
        fecha = fila["fecha"]
        nombre_dia = obtener_nombre_dia(fecha)

        capacidad = df_disponibilidad.loc[0, nombre_dia]

        horas_ya_planificadas = plan_futuro[plan_futuro["fecha"] == fecha]["horas"].sum()

        espacio_libre = capacidad - horas_ya_planificadas

        if espacio_libre > 0 and horas_pendientes > 0:
            if horas_pendientes <= espacio_libre:
                horas_asignadas = horas_pendientes
            else:
                horas_asignadas = espacio_libre

            nuevas_filas.append({
                "fecha": fecha,
                "materia": "Reorganización",
                "tema": "Horas pendientes",
                "actividad": "Reorganizado",
                "horas": round(horas_asignadas, 1)
            })

            horas_pendientes -= horas_asignadas

    if len(nuevas_filas) > 0:
        df_nuevas = pd.DataFrame(nuevas_filas)
        df_plan = pd.concat([df_plan, df_nuevas], ignore_index=True)

    if horas_pendientes > 0:
        print(
            "No se pudieron reubicar",
            round(horas_pendientes, 1),
            "hs. Conviene liberar tiempo de otras actividades."
        )
    else:
        print("Todas las horas pendientes fueron reorganizadas.")

    return df_plan
