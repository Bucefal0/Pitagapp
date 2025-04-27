import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math

# Set page configuration
st.set_page_config(
    page_title="Teorema de Pitágoras",
    page_icon="📐",
    layout="wide"
)

# Application title
st.title("📐 Teorema de Pitágoras")

# Introduction text
st.markdown("""
Este aplicativo te ayudará a entender el teorema de Pitágoras, que establece que:

**En un triángulo rectángulo, el cuadrado de la longitud de la hipotenusa es igual a la suma de los cuadrados de las longitudes de los otros dos lados.**

Matemáticamente se expresa como: $a^2 + b^2 = c^2$, donde:
- $a$ y $b$ son las longitudes de los catetos
- $c$ es la longitud de la hipotenusa
""")

# Create a function to draw the triangle
def draw_triangle(a, b, c, side_to_calculate):
    # Crear figura y ejes pequeños
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.set_aspect('equal')

    # Coordenadas del triángulo
    coords = np.array([[0, 0], [a, 0], [0, b]])
    triangle = Polygon(coords, fill=False, edgecolor='blue', linewidth=2)
    ax.add_patch(triangle)

    # Símbolo de ángulo recto (ajustado para triángulos pequeños)
    offset = min(a, b) * 0.12
    ax.plot([offset, offset], [0, offset], color='black', linewidth=1)
    ax.plot([0, offset], [offset, offset], color='black', linewidth=1)

    # Margen para etiquetas (ajustado dinámicamente)
    margin = max(a, b) * 0.15

    # Etiqueta lado a (base)
    a_label_y = -margin
    if side_to_calculate == 'a':
        ax.text(a / 2, a_label_y, "a = ?", fontsize=8, ha='center', color='red')
    else:
        ax.text(a / 2, a_label_y, f"a = {a}", fontsize=8, ha='center')

    # Etiqueta lado b (altura)
    b_label_x = -margin
    if side_to_calculate == 'b':
        ax.text(b_label_x, b / 2, "b = ?", fontsize=8, va='center', color='red', rotation=90)
    else:
        ax.text(b_label_x, b / 2, f"b = {b}", fontsize=8, va='center', rotation=90)

    # Etiqueta lado c (hipotenusa)
    # Calcula el punto medio de la hipotenusa y ajusta la posición
    c_label_x = a * 0.45 - margin * 0.2
    c_label_y = b * 0.45 + margin * 0.2
    if side_to_calculate == 'c':
        ax.text(c_label_x, c_label_y, "c = ?", fontsize=8, color='red', rotation=-math.degrees(math.atan2(b, a))/2)
    else:
        ax.text(c_label_x, c_label_y, f"c = {c:.2f}", fontsize=8, rotation=-math.degrees(math.atan2(b, a))/2)

    # Ajustar límites y quitar ejes
    ax.set_xlim(-margin, a + margin)
    ax.set_ylim(-margin, b + margin)
    ax.axis('off')

    return fig


# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Ingresa los valores")
    
    # Radio button to select which side to calculate
    side_to_calculate = st.radio(
        "¿Qué lado del triángulo deseas calcular?",
        ("Hipotenusa (c)", "Cateto (a)", "Cateto (b)"),
        index=0
    )
    
    # Set up the forms based on the selected side
    if side_to_calculate == "Hipotenusa (c)":
        st.markdown("Para calcular la hipotenusa, necesitamos los valores de los catetos a y b.")
        a = st.number_input("Valor del cateto a:", min_value=0.1, value=3.0, step=0.1)
        b = st.number_input("Valor del cateto b:", min_value=0.1, value=4.0, step=0.1)
        calculate_side = 'c'
        known_sides = {'a': a, 'b': b}
    
    elif side_to_calculate == "Cateto (a)":
        st.markdown("Para calcular el cateto a, necesitamos los valores de la hipotenusa c y el cateto b.")
        b = st.number_input("Valor del cateto b:", min_value=0.1, value=4.0, step=0.1)
        c = st.number_input("Valor de la hipotenusa c:", min_value=0.1, value=5.0, step=0.1)
        calculate_side = 'a'
        known_sides = {'b': b, 'c': c}
        
        # Validate that c > b (a valid right triangle)
        if c <= b:
            st.error("Error: La hipotenusa (c) debe ser mayor que el cateto (b) para formar un triángulo rectángulo válido.")
    
    elif side_to_calculate == "Cateto (b)":
        st.markdown("Para calcular el cateto b, necesitamos los valores de la hipotenusa c y el cateto a.")
        a = st.number_input("Valor del cateto a:", min_value=0.1, value=3.0, step=0.1)
        c = st.number_input("Valor de la hipotenusa c:", min_value=0.1, value=5.0, step=0.1)
        calculate_side = 'b'
        known_sides = {'a': a, 'c': c}
        
        # Validate that c > a (a valid right triangle)
        if c <= a:
            st.error("Error: La hipotenusa (c) debe ser mayor que el cateto (a) para formar un triángulo rectángulo válido.")

with col2:
    st.subheader("Solución paso a paso")
    
    # Calculate the unknown side
    if calculate_side == 'c':  # Calculate hypotenuse
        a, b = known_sides['a'], known_sides['b']
        c = math.sqrt(a**2 + b**2)
        
        # Show step-by-step solution
        st.markdown("### Calcular la hipotenusa (c):")
        st.markdown("1. Según el teorema de Pitágoras: $c^2 = a^2 + b^2$")
        st.markdown(f"2. Sustituimos los valores conocidos: $c^2 = {a}^2 + {b}^2$")
        st.markdown(f"3. Calculamos los cuadrados: $c^2 = {a**2} + {b**2}$")
        st.markdown(f"4. Sumamos: $c^2 = {a**2 + b**2}$")
        st.markdown(f"5. Aplicamos raíz cuadrada a ambos lados: $c = \\sqrt{{{a**2 + b**2}}}$")
        st.markdown(f"6. Resultado: $c = {c:.2f}$")
        
    elif calculate_side == 'a':  # Calculate cathetus a
        b, c = known_sides['b'], known_sides['c']
        
        if c <= b:
            a = None  # Invalid triangle
            st.markdown("⚠️ **No se puede calcular**: La hipotenusa debe ser mayor que el cateto.")
        else:
            a = math.sqrt(c**2 - b**2)
            
            # Show step-by-step solution
            st.markdown("### Calcular el cateto (a):")
            st.markdown("1. Según el teorema de Pitágoras: $a^2 + b^2 = c^2$")
            st.markdown("2. Despejamos $a^2$: $a^2 = c^2 - b^2$")
            st.markdown(f"3. Sustituimos los valores conocidos: $a^2 = {c}^2 - {b}^2$")
            st.markdown(f"4. Calculamos los cuadrados: $a^2 = {c**2} - {b**2}$")
            st.markdown(f"5. Restamos: $a^2 = {c**2 - b**2}$")
            st.markdown(f"6. Aplicamos raíz cuadrada a ambos lados: $a = \\sqrt{{{c**2 - b**2}}}$")
            st.markdown(f"7. Resultado: $a = {a:.2f}$")
    
    elif calculate_side == 'b':  # Calculate cathetus b
        a, c = known_sides['a'], known_sides['c']
        
        if c <= a:
            b = None  # Invalid triangle
            st.markdown("⚠️ **No se puede calcular**: La hipotenusa debe ser mayor que el cateto.")
        else:
            b = math.sqrt(c**2 - a**2)
            
            # Show step-by-step solution
            st.markdown("### Calcular el cateto (b):")
            st.markdown("1. Según el teorema de Pitágoras: $a^2 + b^2 = c^2$")
            st.markdown("2. Despejamos $b^2$: $b^2 = c^2 - a^2$")
            st.markdown(f"3. Sustituimos los valores conocidos: $b^2 = {c}^2 - {a}^2$")
            st.markdown(f"4. Calculamos los cuadrados: $b^2 = {c**2} - {a**2}$")
            st.markdown(f"5. Restamos: $b^2 = {c**2 - a**2}$")
            st.markdown(f"6. Aplicamos raíz cuadrada a ambos lados: $b = \\sqrt{{{c**2 - a**2}}}$")
            st.markdown(f"7. Resultado: $b = {b:.2f}$")

# Draw the triangle based on which side is being calculated
if calculate_side == 'c':
    a, b = known_sides['a'], known_sides['b']
    c = math.sqrt(a**2 + b**2)
    triangle_fig = draw_triangle(a, b, c, calculate_side)
elif calculate_side == 'a':
    b, c = known_sides['b'], known_sides['c']
    if c > b:  # Valid triangle
        a = math.sqrt(c**2 - b**2)
        triangle_fig = draw_triangle(a, b, c, calculate_side)
    else:  # Invalid triangle
        a, b, c = 3, 4, 5  # Default values
        triangle_fig = draw_triangle(a, b, c, calculate_side)
elif calculate_side == 'b':
    a, c = known_sides['a'], known_sides['c']
    if c > a:  # Valid triangle
        b = math.sqrt(c**2 - a**2)
        triangle_fig = draw_triangle(a, b, c, calculate_side)
    else:  # Invalid triangle
        a, b, c = 3, 4, 5  # Default values
        triangle_fig = draw_triangle(a, b, c, calculate_side)

# Display the triangle
st.subheader("Representación visual")
st.pyplot(triangle_fig)

# Additional information section
st.markdown("---")
st.subheader("Información adicional")
st.markdown("""
### ¿Qué es el Teorema de Pitágoras?
El Teorema de Pitágoras es una relación fundamental en geometría euclidiana que establece que en un triángulo rectángulo, el cuadrado de la longitud de la hipotenusa es igual a la suma de los cuadrados de las longitudes de los otros dos lados (catetos).

### Aplicaciones prácticas
- Arquitectura y construcción
- Navegación
- Cartografía
- Física
- Ingeniería
- Diseño gráfico

### Historia
El teorema lleva el nombre del matemático griego Pitágoras (570-495 a.C.), aunque hay evidencia de que civilizaciones anteriores como los babilonios y los chinos ya conocían esta relación.
""")

# Footer
st.markdown("---")
st.markdown("Desarrollado con ❤️ para ayudar a estudiantes a entender el Teorema de Pitágoras")
