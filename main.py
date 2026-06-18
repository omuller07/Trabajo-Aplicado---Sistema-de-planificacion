from src.recoleccion_info import recolectar_informacion

from src.verificacion import (verificar_disponibilidad, 
                              verificar_fechas_materias, 
                              verificar_nombres_materias, 
                              verificar_nombres_temas)
                                

from src.planificador import generar_plan

from src.graficos import crear_calendario_visual

from src.almacenamiento import (guardar_datos_iniciales, 
                                guardar_plan, 
                                cargar_datos_iniciales, 
                                cargar_plan, 
                                cargar_progreso, 
                                guardar_progreso,
                                plan_dataframe_a_diccionario)

from src.seguimiento import (registrar_progreso_del_dia, 
                             detectar_alertas, 
                             reorganizar_plan_por_progreso)


def mostrar_menu():
    """
    Muestra un menu de opcionespar el usuario. 
    1. generar un plan
    2. registrar porgreso de estudio 
    3.Ver calendario 
    4. Salir

    Returns
    -------
    opcion : str
        Numero de opcion seleccionada por el usuario.

    """
    print("\nMENÚ PRINCIPAL")
    print("1. Generar nuevo plan")
    print("2. Registrar progreso del día")
    print("3. Ver calendario actual")
    print("4. Salir")

    opcion = input("Elegí una opción: ")
    return opcion


def generar_nuevo_plan():
    """
    Solicita los datos al usuario en bucle hasta que pasen todas las
    validaciones (disponibilidad, nombres y fechas de materias y temas).
    Una vez validados, genera el plan, lo guarda, muestra un resumen de
    prioridades por consola, advierte sobre los temas que no pudieron
    ser asignados y genera el calendario visual.  

    Returns
    -------
    None.

    """
    while True:
        df_disponibilidad, df_materias, df_temas = recolectar_informacion()
        #desempaqueta los tres df que devuelve recolectar_informacion()

        datos_validos = (verificar_disponibilidad(df_disponibilidad) 
                         and verificar_nombres_materias(df_materias) 
                         and verificar_fechas_materias(df_materias) 
                         and verificar_nombres_temas(df_temas))
    #pasa por todas las validaciones, si alguna falla, pide todo devuelta. 
    #Cada función devuelve True o False. todas tienen que dar True

        if datos_validos:
            break

        print("\nVolvé a ingresar los datos.\n")

    plan, temas_ordenados, carga_diaria, capacidad_diaria, temas_no_asignados = generar_plan(
        df_disponibilidad,
        df_materias,
        df_temas)
    #llama a la funcion generar plan y asigna nombres a las cosas que devuleve. 

    guardar_datos_iniciales(df_disponibilidad, df_materias, df_temas)
    #funcion que guarda los datos 
    guardar_plan(plan)

    print("\nPlan generado y guardado correctamente.")
    print("\nRESUMEN DE PRIORIDADES")
    print(temas_ordenados[["materia", "tema", "prioridad", "horas_necesarias"]])

    if len(temas_no_asignados) > 0:
        print("\nTEMAS NO ASIGNADOS")
        for item in temas_no_asignados:
            print(item)

    crear_calendario_visual(plan, df_materias)
    #crea el calendario visual usando la funcion. 


def registrar_progreso():

    """
    EL usuario puede registrar su progreso. Si no hay un plan ya hecho, el programa pide que lo haga. 
    A partir de la nueva informacion edita la planificacion. 

    Returns
    -------
    None.

    """
    df_disponibilidad, df_materias, df_temas = cargar_datos_iniciales() #lo que hace es leer los archivos CSV que se guardaron cuando generaste el plan


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
        df_disponibilidad)

    guardar_plan(plan_dataframe_a_diccionario(df_plan_reorganizado))

    print("\nPlan actualizado según el progreso.")
    plan_actualizado = plan_dataframe_a_diccionario(df_plan_reorganizado)
    crear_calendario_visual(plan_actualizado, df_materias)


def ver_calendario():
    """
    Muestra el calendario, si no hay uno, pide que lo arme. 

    Returns
    -------
    None.

    """
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