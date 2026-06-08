import pandas as pd
from datetime import datetime, date


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


def pedir_horas(mensaje):
    """
    Solicita al usuario una cantidad de horas y verifica que sea un número válido y no negativo.
    
    Parameters:
    ----------
    mensaje : str
        Mensaje que se mostrará al usuario.

    Returns:
    ----------
    float
        Cantidad de horas ingresada por el usuario.
    """
   
    while True:
        try:
            horas = float(input(mensaje))

            if horas >= 0:
                return horas

            print("Error: las horas no pueden ser negativas.")

        except ValueError:
            print("Error: ingresá un número válido.")


def registrar_progreso_del_dia(df_plan, df_progreso):
    """
    • Registra las horas realmente realizadas por el usuario en una fecha determinada.
    • Busca las actividades planificadas para la fecha ingresada, le pide al usuario
    cuántas horas hizo de cada una y agrega esos registros al DataFrame de progreso.

    Parameters:
    ----------
    df_plan : pandas.DataFrame
        DataFrame con las actividades planificadas.

    df_progreso : pandas.DataFrame
        DataFrame con el progreso registrado hasta el momento.

    Returns:
    ----------
    pandas.DataFrame
        DataFrame de progreso actualizado con los nuevos registros.
    """
    
    fecha = pedir_fecha("Ingresá la fecha en la que querés registrar progreso")

    plan_del_dia = df_plan[df_plan["fecha"] == fecha]
    # Filtra el plan y se queda solo con las actividades de la fecha ingresada.
    
    if plan_del_dia.empty:
    # Verifica si no había actividades planificadas para ese día.
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
            + "?: ")

        nuevos_registros.append({
            "fecha": fecha,
            "materia": fila["materia"],
            "tema": fila["tema"],
            "actividad": fila["actividad"],
            "horas_realizadas": horas})

    df_nuevo = pd.DataFrame(nuevos_registros)
    df_progreso = pd.concat([df_progreso, df_nuevo], ignore_index=True)
    # Une el progreso anterior con los nuevos registros.
    # ignore_index=True --> reinicia los índices para que queden ordenados.

    return df_progreso


def detectar_alertas(df_plan, df_progreso):
    """
    • Analiza el progreso registrado por el usuario y detecta posibles situaciones de procrastinación o sobreexigencia.
    • Compara las horas planificadas con las horas realizadas hasta la última fecha registrada y muestra alertas cuando detecta diferencias importantes.

    Parameters:
    ----------
    df_plan : pandas.DataFrame
        DataFrame con las actividades planificadas.

    df_progreso : pandas.DataFrame
        DataFrame con las horas realmente realizadas.

    Returns:
    ----------
    None
    """
    
    if df_progreso.empty:
        print("Todavía no hay progreso registrado.")
        return

    fecha_maxima = df_progreso["fecha"].max()
    # Obtiene la última fecha para la que se registró progreso.

    plan_pasado = df_plan[df_plan["fecha"] <= fecha_maxima]
    # Selecciona únicamente las actividades que ya deberían haberse realizado.

    horas_planificadas = plan_pasado["horas"].sum()
    # Suma todas las horas que estaban planificadas hasta esa fecha.
    horas_realizadas = df_progreso["horas_realizadas"].sum()
    # Suma todas las horas que el usuario registró haber realizado.

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
    # Agrupa los registros por fecha y calcula cuántas horas se estudiaron cada día.

    for fecha, horas in progreso_por_dia.items():
        if horas > 4:
            print("Alerta de sobreexigencia:", fecha, "-", round(horas, 1), "hs estudiadas.")


def obtener_nombre_dia(fecha):
    """
    Obtiene el nombre del día de la semana correspondiente a una fecha.

    Parameters:
    ----------
    fecha : datetime.date
        Fecha de la cual se desea conocer el día de la semana.

    Returns:
    ----------
    str
        Nombre del día de la semana en español.
    """
    dias = ["lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabado",
            "domingo"]

    return dias[fecha.weekday()]
    # weekday() devuelve un número entre 0 y 6: 0 = lunes, 1 = martes, ..., 6 = domingo.


def reorganizar_plan_por_progreso(df_plan, df_progreso, df_disponibilidad):
    """
    • Reorganiza el plan de estudio según el progreso registrado por el usuario.
    • Si el usuario realizó menos horas de las planificadas hasta la última fecha registrada,
    calcula las horas pendientes e intenta reubicarlas en fechas futuras con disponibilidad.

    Parameters:
    ----------
    df_plan : pandas.DataFrame
        DataFrame con las actividades planificadas.

    df_progreso : pandas.DataFrame
        DataFrame con las horas realmente realizadas por el usuario.

    df_disponibilidad : pandas.DataFrame
        DataFrame con la cantidad de horas disponibles para estudiar cada día de la semana.

    Returns:
    ----------
    pandas.DataFrame
        DataFrame del plan actualizado con las horas pendientes que pudieron ser reorganizadas.
    """
    
    if df_progreso.empty:
        return df_plan

    fecha_actual = df_progreso["fecha"].max()

    plan_pasado = df_plan[df_plan["fecha"] <= fecha_actual]
    plan_futuro = df_plan[df_plan["fecha"] > fecha_actual].copy()
    # Separa el plan en actividades pasadas y actividades futuras.

    horas_planificadas = plan_pasado["horas"].sum()
    horas_realizadas = df_progreso["horas_realizadas"].sum()

    horas_pendientes = round(horas_planificadas - horas_realizadas, 1)
    # Calcula cuántas horas quedaron sin realizar.

    if horas_pendientes <= 0:
        print("No hay horas pendientes para reorganizar.")
        return df_plan

    print("\nHay", horas_pendientes, "hs pendientes para reubicar.")

    nuevas_filas = []

    for indice, fila in plan_futuro.iterrows():
        fecha = fila["fecha"]
        nombre_dia = obtener_nombre_dia(fecha)

        capacidad = df_disponibilidad.loc[0, nombre_dia]
        # Busca cuántas horas puede estudiar el usuario ese día de la semana.

        horas_ya_planificadas = plan_futuro[plan_futuro["fecha"] == fecha]["horas"].sum()
        # Suma las horas que ya estaban asignadas en esa fecha futura.

        espacio_libre = capacidad - horas_ya_planificadas
        # Calcula cuántas horas libres quedan disponibles ese día.

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
                "horas": round(horas_asignadas, 1)})

            horas_pendientes -= horas_asignadas
            # Descuenta las horas que ya fueron reubicadas.

    if len(nuevas_filas) > 0:
        df_nuevas = pd.DataFrame(nuevas_filas)
        df_plan = pd.concat([df_plan, df_nuevas], ignore_index=True)
        # Agrega al plan original las nuevas filas con horas reorganizadas.
        # pd.concat() --> Une DataFrames.

    if horas_pendientes > 0:
        print("No se pudieron reubicar", 
              round(horas_pendientes, 1),
              "hs. Conviene liberar tiempo de otras actividades.")
    else:
        print("Todas las horas pendientes fueron reorganizadas.")

    return df_plan
