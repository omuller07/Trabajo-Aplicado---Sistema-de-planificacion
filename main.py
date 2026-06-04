from recoleccion_info import recolectar_informacion

from verificacion import (
    verificar_disponibilidad,
    verificar_fechas_materias,
    verificar_nombres_materias,
    verificar_nombres_temas)

from planificador import generar_plan


def mostrar_resumen_prioridades(temas_ordenados):
    print("\nRESUMEN DE PRIORIDADES")
    print("----------------------")

    columnas = [
        "materia",
        "tema",
        "dificultad",
        "conocimiento",
        "prioridad",
        "horas_necesarias"]

    print(temas_ordenados[columnas])


def mostrar_carga_diaria(carga_diaria, capacidad_diaria):
    print("\nCARGA DIARIA")
    print("------------")

    for fecha in sorted(carga_diaria.keys()):
        horas_usadas = round(carga_diaria[fecha], 1)
        horas_disponibles = capacidad_diaria[fecha]

        print(
            fecha,
            ":",
            horas_usadas,
            "hs usadas de",
            horas_disponibles,
            "hs disponibles")

        if horas_usadas > 4:
            print("  Alerta: posible sobrecarga mental.")


def mostrar_temas_no_asignados(temas_no_asignados):
    if len(temas_no_asignados) > 0:
        print("\nTEMAS NO ASIGNADOS")
        print("------------------")

        for item in temas_no_asignados:
            print(
                "-",
                item["materia"],
                "|",
                item["tema"],
                "|",
                item["actividad"],
                "| faltaron",
                item["horas_faltantes"],
                "hs")

        print("\nRecomendación: aumentá la disponibilidad o empezá antes a estudiar.")


def main():
    df_disponibilidad, df_materias, df_temas = recolectar_informacion()

    datos_validos = (
        verificar_disponibilidad(df_disponibilidad)
        and verificar_nombres_materias(df_materias)
        and verificar_fechas_materias(df_materias)
        and verificar_nombres_temas(df_temas))

    if not datos_validos:
        return

    plan, temas_ordenados, carga_diaria, capacidad_diaria, temas_no_asignados = generar_plan(
        df_disponibilidad,
        df_materias,
        df_temas)

    mostrar_resumen_prioridades(temas_ordenados)

    mostrar_carga_diaria(carga_diaria, capacidad_diaria)

    mostrar_temas_no_asignados(temas_no_asignados)


main()
