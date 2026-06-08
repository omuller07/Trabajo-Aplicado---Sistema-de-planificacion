from src.recoleccion_info import recolectar_informacion

from src.verificacion import (
    verificar_disponibilidad,
    verificar_fechas_materias,
    verificar_nombres_materias,
    verificar_nombres_temas
)

from src.planificador import generar_plan

from src.graficos import crear_calendario_visual

from src.almacenamiento import (
    guardar_datos_iniciales,
    guardar_plan,
    cargar_datos_iniciales,
    cargar_plan,
    cargar_progreso,
    guardar_progreso,
    plan_dataframe_a_diccionario
)

from src.seguimiento import (
    registrar_progreso_del_dia,
    detectar_alertas,
    reorganizar_plan_por_progreso
)


def mostrar_menu():
    print("\nMENÚ PRINCIPAL")
    print("1. Generar nuevo plan")
    print("2. Registrar progreso del día")
    print("3. Ver calendario actual")
    print("4. Salir")

    opcion = input("Elegí una opción: ")
    return opcion


def generar_nuevo_plan():

    while True:
        df_disponibilidad, df_materias, df_temas = recolectar_informacion()

        datos_validos = (
            verificar_disponibilidad(df_disponibilidad)
            and verificar_nombres_materias(df_materias)
            and verificar_fechas_materias(df_materias)
            and verificar_nombres_temas(df_temas)
        )

        if datos_validos:
            break

        print("\nVolvé a ingresar los datos.\n")

    plan, temas_ordenados, carga_diaria, capacidad_diaria, temas_no_asignados = generar_plan(
        df_disponibilidad,
        df_materias,
        df_temas
    )

    guardar_datos_iniciales(df_disponibilidad, df_materias, df_temas)
    guardar_plan(plan)

    print("\nPlan generado y guardado correctamente.")
    print("\nRESUMEN DE PRIORIDADES")
    print(temas_ordenados[["materia", "tema", "prioridad", "horas_necesarias"]])

    if len(temas_no_asignados) > 0:
        print("\nTEMAS NO ASIGNADOS")
        for item in temas_no_asignados:
            print(item)

    crear_calendario_visual(plan, df_materias)


def registrar_progreso():
    df_disponibilidad, df_materias, df_temas = cargar_datos_iniciales()
    df_plan = cargar_plan()
    df_progreso = cargar_progreso()

    if df_plan.empty:
        print("Primero tenés que generar un plan.")
        return

    df_progreso = registrar_progreso_del_dia(df_plan, df_progreso)
    guardar_progreso(df_progreso)

    detectar_alertas(df_plan, df_progreso)

    df_plan_reorganizado = reorganizar_plan_por_progreso(
        df_plan,
        df_progreso,
        df_disponibilidad
    )

    guardar_plan(plan_dataframe_a_diccionario(df_plan_reorganizado))

    print("\nPlan actualizado según el progreso.")
    plan_actualizado = plan_dataframe_a_diccionario(df_plan_reorganizado)
    crear_calendario_visual(plan_actualizado, df_materias)


def ver_calendario():
    df_disponibilidad, df_materias, df_temas = cargar_datos_iniciales()
    df_plan = cargar_plan()

    if df_plan.empty:
        print("Todavía no hay un plan guardado.")
        return

    plan = plan_dataframe_a_diccionario(df_plan)
    crear_calendario_visual(plan, df_materias)




while True:
    opcion = mostrar_menu()

    if opcion == "1":
        generar_nuevo_plan()

    elif opcion == "2":
        registrar_progreso()

    elif opcion == "3":
        ver_calendario()

    elif opcion == "4":
        print("Programa finalizado.")
        break