import streamlit as st
import math
import re

st.set_page_config(page_title="Calculadora Combinatoria Avanzada", page_icon="🧠")

st.title("🧠 Calculadora de Problemas Combinatorios")
st.markdown("Ingresa tu problema en lenguaje natural y obtén resultado y explicación paso a paso.\n\n"
            "Ejemplos:\n- Una clave de admisión de un banco consta de dos letras seguidas de dos dígitos. ¿Cuántas claves hay?\n"
            "- En un experimento hay que acomodar 5 figuras diferentes en fila. ¿Cuántos acomodados hay?\n"
            "- ¿Cuántas secuencias de cara y cruz al lanzar una moneda 4 veces?")

def factorial(n):
    return math.factorial(n)

def permutacion_simple(n, r=None):
    if r is None:
        r = n
    return factorial(n)//factorial(n-r)

def permutacion_con_repeticion(n, r):
    return n ** r

def combinacion_simple(n, r):
    return factorial(n)//(factorial(r)*factorial(n-r))

def principio_multiplicativo(cantidades):
    result = 1
    for c in cantidades:
        result *= c
    return result

def acomodados_circulares(n):
    return factorial(n-1)

def explicar_permutacion_simple(n, r=None):
    if r is None:
        r = n
    total = permutacion_simple(n, r)
    return f"Permutación simple P({n},{r}) = {n}! / ({n}-{r})! = {total}"

def explicar_permutacion_con_repeticion(n, r):
    total = permutacion_con_repeticion(n, r)
    return f"Permutación con repetición: {n}^{r} = {total}"

def explicar_combinacion_simple(n, r):
    total = combinacion_simple(n, r)
    return f"Combinación simple C({n},{r}) = {n}! / ({r}! * ({n}-{r})!) = {total}"

def explicar_principio_multiplicativo(cantidades):
    total = principio_multiplicativo(cantidades)
    multiplicacion = " × ".join(map(str, cantidades))
    return f"Principio multiplicativo: {multiplicacion} = {total}"

def explicar_acomodados_circulares(n):
    total = acomodados_circulares(n)
    return f"Acomodados circulares de {n} elementos: (n-1)! = ({n}-1)! = {total}"

def interpretar_problema(texto):
    texto = texto.lower()

    # Detectar números importantes
    numeros = list(map(int, re.findall(r'\d+', texto)))

    # Casos comunes detectados con keywords

    # 1) Clave banco: 2 letras y 2 dígitos
    if "clave" in texto and ("letra" in texto or "alfabeto" in texto) and ("dígito" in texto or "digito" in texto):
        letras = 26
        digitos = 10
        # Buscamos cuántas letras y dígitos pide:
        letras_cant = len(re.findall(r'letra', texto))
        if letras_cant == 0:
            letras_cant = 2  # predeterminado
        digitos_cant = len(re.findall(r'dígito|digito', texto))
        if digitos_cant == 0:
            digitos_cant = 2

        total = permutacion_con_repeticion(letras, letras_cant) * permutacion_con_repeticion(digitos, digitos_cant)
        explicacion = (f"Clave formada por {letras_cant} letras (26 posibles cada una) y {digitos_cant} dígitos (10 posibles cada uno).\n"
                      f"Total de claves = 26^{letras_cant} × 10^{digitos_cant} = {total}")
        return total, explicacion

    # 2) Acomodar figuras distintas en fila (permutacion simple n!)
    if ("acomodar" in texto or "acomodados" in texto or "ordenar" in texto or "secuencia" in texto or "arreglo" in texto) and ("fila" in texto or "hilera" in texto):
        if numeros:
            n = numeros[0]
            total = permutacion_simple(n)
            explicacion = f"Permutación simple de {n} elementos: {n}! = {total}"
            return total, explicacion

    # 3) Lanzar moneda n veces (secuencia cara/cruz)
    if "moneda" in texto and "lanzar" in texto and numeros:
        n = numeros[0]
        total = 2 ** n
        explicacion = f"Cada lanzamiento tiene 2 resultados (cara o cruz), lanzados {n} veces.\nTotal de secuencias = 2^{n} = {total}"
        return total, explicacion

    # 4) Menú con opciones (principio multiplicativo)
    if ("menú" in texto or "menu" in texto or "opción" in texto or "elección" in texto or "plato" in texto or "bebida" in texto) and numeros:
        cantidades = numeros
        total = principio_multiplicativo(cantidades)
        explicacion = f"Principio multiplicativo aplicando: {' × '.join(map(str, cantidades))} = {total}"
        return total, explicacion

    # 5) Dado lanzado n veces (6^n secuencias)
    if "dado" in texto and "lanzar" in texto and numeros:
        n = numeros[0]
        total = 6 ** n
        explicacion = f"Dado de 6 caras lanzado {n} veces: total secuencias = 6^{n} = {total}"
        return total, explicacion

    # 6) Calcular permutación P(n,r)
    if re.search(r'p\(?\s*\d+\s*,\s*\d+\s*\)?', texto):
        m = re.search(r'p\(?\s*(\d+)\s*,\s*(\d+)\s*\)?', texto)
        if m:
            n = int(m.group(1))
            r = int(m.group(2))
            total = permutacion_simple(n,r)
            explicacion = explicar_permutacion_simple(n,r)
            return total, explicacion

    # 7) Permutaciones de conjunto n elementos: n!
    if "permutación" in texto and numeros:
        n = numeros[0]
        total = permutacion_simple(n)
        explicacion = f"Permutación simple de {n} elementos: {n}! = {total}"
        return total, explicacion

    # 16) Acomodar personas en círculo
    if ("círculo" in texto or "circulo" in texto) and numeros:
        n = numeros[0]
        total = acomodados_circulares(n)
        explicacion = explicar_acomodados_circulares(n)
        return total, explicacion

    # Caso general: si hay n y r y palabras combinacion/permutacion
    if len(numeros) >= 2:
        n, r = numeros[0], numeros[1]
        if "combinación sin repetición" in texto:
            total = combinacion_simple(n,r)
            explicacion = explicar_combinacion_simple(n,r)
            return total, explicacion
        if "permutación sin repetición" in texto:
            total = permutacion_simple(n,r)
            explicacion = explicar_permutacion_simple(n,r)
            return total, explicacion
        if "permutación con repetición" in texto:
            total = permutacion_con_repeticion(n,r)
            explicacion = explicar_permutacion_con_repeticion(n,r)
            return total, explicacion
        if "combinación con repetición" in texto:
            # formula para combinación con repetición
            total = factorial(n+r-1)//(factorial(r)*factorial(n-1))
            explicacion = f"Combinación con repetición: C({n}+{r}-1, {r}) = {total}"
            return total, explicacion

    return None, "No pude identificar el tipo exacto de problema. Por favor reformula o da más detalles."

# Interfaz
entrada = st.text_area("🔹 Ingresa tu problema combinatorio en lenguaje natural aquí:")

if entrada:
    resultado, explicacion = interpretar_problema(entrada)
    if resultado is not None:
        st.markdown(f"### 📊 Resultado: {resultado}")
        st.markdown(f"### 📝 Explicación:\n```\n{explicacion}\n```")
    else:
        st.error(explicacion)
