import streamlit as st
import math
import re
from collections import Counter

st.set_page_config(page_title="Calculadora Combinatoria Avanzada", page_icon="🧠")

st.title(" Calculadora Avanzada de Problemas Combinatorios")
st.markdown("""
Ingresa tu problema en lenguaje natural y obtén resultado y explicación detallada.  
Ejemplos:  
- Claves con letras y dígitos  
- Permutaciones de palabras con letras repetidas  
- Permutaciones con restricciones (vocales juntas)  
- Acomodar personas hombres/mujeres alternados  
- Acomodados en círculo  
- Lanzamientos de monedas y dados  
- Combinaciones simples y con repetición
""")

def factorial(n):
    return math.factorial(n)

def permutacion_simple(n, r=None):
    if r is None:
        r = n
    return factorial(n)//factorial(n-r)

def permutacion_con_repeticion(total_elementos, repeticiones):
    denom = 1
    for r in repeticiones:
        denom *= factorial(r)
    return factorial(total_elementos)//denom

def permutacion_con_restricciones(n, grupo1, grupo2):
    # ejemplo para alternar grupos: factorial de cada grupo * factorial de posiciones
    return factorial(grupo1) * factorial(grupo2) * 2  # factor 2 por empezar uno u otro (simplificado)

def combinacion_simple(n, r):
    return factorial(n)//(factorial(r)*factorial(n-r))

def combinacion_con_repeticion(n, r):
    return factorial(n+r-1)//(factorial(r)*factorial(n-1))

def principio_multiplicativo(cantidades):
    result = 1
    for c in cantidades:
        result *= c
    return result

def acomodados_circulares(n):
    return factorial(n-1)

def contar_letras(texto):
    texto = texto.lower()
    return Counter(c for c in texto if c.isalpha())

def interpretar_problema(texto):
    texto_lower = texto.lower()
    numeros = list(map(int, re.findall(r'\d+', texto_lower)))

    # 1. Clave banco: letras y dígitos
    if "clave" in texto_lower and ("letra" in texto_lower or "alfabeto" in texto_lower) and ("dígito" in texto_lower or "digito" in texto_lower):
        letras = 26
        digitos = 10
        letras_cant = len(re.findall(r'letra', texto_lower))
        if letras_cant == 0: letras_cant = 2
        digitos_cant = len(re.findall(r'dígito|digito', texto_lower))
        if digitos_cant == 0: digitos_cant = 2
        total = permutacion_con_repeticion(letras, [letras_cant]) * permutacion_con_repeticion(digitos, [digitos_cant])
        explicacion = (f"Clave formada por {letras_cant} letras (26 opciones cada una) y {digitos_cant} dígitos (10 opciones cada uno).\n"
                      f"Total = 26^{letras_cant} × 10^{digitos_cant} = {total}")
        return total, explicacion

    # 2. Permutación simple (acometar en fila)
    if ("acomodar" in texto_lower or "acomodados" in texto_lower or "ordenar" in texto_lower or "arreglo" in texto_lower) and ("fila" in texto_lower or "hilera" in texto_lower):
        if numeros:
            n = numeros[0]
            total = permutacion_simple(n)
            explicacion = f"Permutación simple de {n} elementos: {n}! = {total}"
            return total, explicacion

    # 3. Secuencias lanzar moneda
    if "moneda" in texto_lower and "lanzar" in texto_lower and numeros:
        n = numeros[0]
        total = 2 ** n
        explicacion = f"Cada lanzamiento tiene 2 resultados (cara o cruz), lanzados {n} veces.\nTotal secuencias = 2^{n} = {total}"
        return total, explicacion

    # 4. Menú (principio multiplicativo)
    if ("menú" in texto_lower or "menu" in texto_lower or "opción" in texto_lower or "elección" in texto_lower or "plato" in texto_lower or "bebida" in texto_lower) and numeros:
        cantidades = numeros
        total = principio_multiplicativo(cantidades)
        explicacion = f"Principio multiplicativo: {' × '.join(map(str, cantidades))} = {total}"
        return total, explicacion

    # 5. Dado lanzado varias veces
    if "dado" in texto_lower and "lanzar" in texto_lower and numeros:
        n = numeros[0]
        total = 6 ** n
        explicacion = f"Dado de 6 caras lanzado {n} veces: total secuencias = 6^{n} = {total}"
        return total, explicacion

    # 6. Permutaciones P(n,r)
    m = re.search(r'p\(?\s*(\d+)\s*,\s*(\d+)\s*\)?', texto_lower)
    if m:
        n = int(m.group(1))
        r = int(m.group(2))
        total = permutacion_simple(n,r)
        explicacion = f"Permutación P({n},{r}) = {n}! / ({n}-{r})! = {total}"
        return total, explicacion

    # 7. Permutaciones de palabra (con letras repetidas)
    if ("palabra" in texto_lower or "letras" in texto_lower) and "permutación" in texto_lower:
        # intentar encontrar la palabra
        palabra = re.findall(r'palabra\s*de\s*(\w+)', texto_lower)
        if palabra:
            p = palabra[0]
            conteo = contar_letras(p)
            total = permutacion_con_repeticion(len(p), list(conteo.values()))
            explicacion = f"Permutaciones de palabra '{p}' con letras repetidas:\n"
            explicacion += f"Total = {len(p)}! / " + " * ".join([f"{v}!" for v in conteo.values()]) + f" = {total}"
            return total, explicacion

    # 8. Acomodar hombres y mujeres alternados
    if ("hombres" in texto_lower and "mujeres" in texto_lower and "alternado" in texto_lower) and numeros and len(numeros) >= 2:
        hombres = numeros[0]
        mujeres = numeros[1]
        if abs(hombres - mujeres) > 1:
            return None, "No es posible alternar si la diferencia de hombres y mujeres es mayor a 1."
        total = factorial(hombres) * factorial(mujeres) * 2
        explicacion = (f"Acomodar {hombres} hombres y {mujeres} mujeres alternados.\n"
                      f"Total = {hombres}! × {mujeres}! × 2 (por empezar con hombre o mujer) = {total}")
        return total, explicacion

    # 9. Acomodados circulares
    if ("círculo" in texto_lower or "circulo" in texto_lower) and numeros:
        n = numeros[0]
        total = acomodados_circulares(n)
        explicacion = f"Acomodados circulares de {n} elementos: (n-1)! = ({n}-1)! = {total}"
        return total, explicacion

    # 10. Combinaciones simples y con repetición
    if len(numeros) >= 2:
        n, r = numeros[0], numeros[1]
        if "combinación sin repetición" in texto_lower:
            total = combinacion_simple(n,r)
            explicacion = f"Combinación C({n},{r}) = {n}! / ({r}! * ({n}-{r})!) = {total}"
            return total, explicacion
        if "combinación con repetición" in texto_lower:
            total = combinacion_con_repeticion(n,r)
            explicacion = f"Combinación con repetición C({n}+{r}-1,{r}) = {total}"
            return total, explicacion
        if "permutación sin repetición" in texto_lower:
            total = permutacion_simple(n,r)
            explicacion = f"Permutación P({n},{r}) = {n}! / ({n}-{r})! = {total}"
            return total, explicacion
        if "permutación con repetición" in texto_lower:
            total = permutacion_con_repeticion(n,r)
            explicacion = f"Permutación con repetición: {n}^{r} = {total}"
            return total, explicacion

    # 11. Palabras con vocales juntas (restricción)
    if "vocales juntas" in texto_lower and ("palabra" in texto_lower or "letras" in texto_lower):
        palabra = re.findall(r'palabra\s*de\s*(\w+)', texto_lower)
        if palabra:
            p = palabra[0]
            vocales = sum(p.count(v) for v in "aeiou")
            consonantes = len(p) - vocales
            # Tratamos el grupo de vocales como uno solo
            total = factorial(consonantes + 1) * factorial(vocales)
            explicacion = (f"Palabra '{p}' con vocales juntas:\n"
                          f"Trato las {vocales} vocales como un solo bloque.\n"
                          f"Permutaciones = (consonantes + 1)! × vocales! = {total}")
            return total, explicacion

    return None, "No pude identificar el tipo exacto de problema. Por favor reformula o sé más específico."

entrada = st.text_area("🔹 Ingresa tu problema combinatorio aquí:")

if entrada:
    resultado, explicacion = interpretar_problema(entrada)
    if resultado is not None:
        st.markdown(f"###  Resultado: {resultado}")
        st.markdown(f"###  Explicación:\n```\n{explicacion}\n```")
    else:
        st.error(explicacion)
