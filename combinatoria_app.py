import streamlit as st
import math
import re

st.set_page_config(page_title="Calculadora Combinatoria", page_icon="🧠")

st.title("🧠 Calculadora de Problemas Combinatorios")
st.markdown("Escribe un problema como por ejemplo:\n- *Permutación sin repetición de 5 elementos tomados de 3*\n- *Combinación con repetición de 4 y 2*")

# Funciones combinatorias
def factorial(n):
    return math.factorial(n)

def perm_sin_rep(n, r):
    return factorial(n) // factorial(n - r)

def perm_con_rep(n, r):
    return n ** r

def comb_sin_rep(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def comb_con_rep(n, r):
    return factorial(n + r - 1) // (factorial(r) * factorial(n - 1))

# Analiza el texto y resuelve
def resolver_problema(texto):
    texto = texto.lower()
    numeros = list(map(int, re.findall(r'\d+', texto)))

    if len(numeros) < 2:
        return "❌ Por favor incluye al menos dos números (n y r)."

    n, r = numeros[0], numeros[1]

    if "permutación con repetición" in texto:
        return f"✅ Permutación con repetición: {n} ^ {r} = {perm_con_rep(n, r)}"
    elif "permutación sin repetición" in texto:
        return f"✅ Permutación sin repetición: P({n}, {r}) = {perm_sin_rep(n, r)}"
    elif "combinación con repetición" in texto:
        return f"✅ Combinación con repetición: C({n}+{r}-1, {r}) = {comb_con_rep(n, r)}"
    elif "combinación sin repetición" in texto:
        return f"✅ Combinación sin repetición: C({n}, {r}) = {comb_sin_rep(n, r)}"
    else:
        return "❌ No se reconoció el tipo de problema. Usa una de las siguientes frases:\n- Permutación con repetición\n- Permutación sin repetición\n- Combinación con repetición\n- Combinación sin repetición"

# Interfaz
user_input = st.text_input("🔹 Escribe tu problema combinatorio aquí:")

if user_input:
    resultado = resolver_problema(user_input)
    st.markdown(f"### 📊 Resultado:\n{resultado}")
