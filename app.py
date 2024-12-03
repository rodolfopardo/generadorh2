import streamlit as st
import requests

# Configuración de la API de SERPAPI
API_KEY = 'd357372e49b3ced99c045808d367df52d32f64facc7e3cb8f8dec2da84225b24'
BASE_URL = 'https://serpapi.com/search.json'

# Función para obtener preguntas sugeridas
def get_h2_suggestions(title, country):
    params = {
        "q": title,  # Título o tema del artículo
        "gl": country,  # Código del país (ej., 'es' para España)
        "hl": "es",  # Idioma (ej., 'es' para español)
        "api_key": API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        results = response.json()

        # Extraer preguntas de "People Also Ask"
        paa_questions = results.get("related_questions", [])
        questions = [q["question"] for q in paa_questions]

        # Filtrar preguntas informativas (opcional)
        informative_questions = [
            q for q in questions if any(keyword in q.lower() for keyword in ["qué", "cómo", "cuándo", "por qué", "dónde"])
        ]

        return questions, informative_questions
    except Exception as e:
        st.error(f"Error al obtener los datos de SERPAPI: {e}")
        return [], []

# Interfaz de Streamlit
def main():
    st.title("Generador de H2 SEO - BigHacks")
    st.write(
        "Ingresa el título de tu artículo y obtén preguntas sugeridas de la audiencia para estructurar tus subtítulos (**H2**)."
    )

    # Entrada del usuario
    title = st.text_input("Título o tema del artículo:", placeholder="Ejemplo: Beneficios de la inteligencia artificial")
    country = st.selectbox("Selecciona el país:", [("España", "es"), ("Estados Unidos", "us"), ("México", "mx")])

    # Botón para buscar
    if st.button("Generar preguntas"):
        if title.strip():
            all_questions, filtered_questions = get_h2_suggestions(title, country[1])
            st.subheader("Resultados:")

            if all_questions:
                st.markdown("### Todas las preguntas:")
                for question in all_questions:
                    st.markdown(f"- {question}")

                st.markdown("### Preguntas sugeridas para H2:")
                for question in filtered_questions:
                    st.markdown(f"#### {question}")
            else:
                st.warning("No se encontraron preguntas para el título proporcionado.")
        else:
            st.warning("Por favor, ingresa un título válido.")

    # Exportar a CSV
    if "all_questions" in locals() and all_questions:
        if st.button("Exportar a CSV"):
            import pandas as pd

            data = {
                "Pregunta": all_questions,
                "Relevante para H2": ["Sí" if q in filtered_questions else "No" for q in all_questions],
            }
            df = pd.DataFrame(data)
            df.to_csv("preguntas_sugeridas.csv", index=False)
            st.success("Archivo CSV generado: preguntas_sugeridas.csv")

if __name__ == "__main__":
    main()
