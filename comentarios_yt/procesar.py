import json
import csv
from transformers import pipeline
from tqdm import tqdm

# 1. definicion de habilidades cognitivas
# tu nueva lista, mejorada con vocabulario de los comentarios reales

cognitive_skills = [
    {
        "name": "Memoria",
        "synonyms": [
            "memoria", "retención", "recuerdo", "reconocimiento", "memorización", 
            "memoria a corto plazo", "memoria a largo plazo", "memoria de trabajo", 
            "olvido", "olvidan", "olvidaba", "no me acuerdo", "no recordaba", "retener información"
        ]
    },
    {
        "name": "Atención",
        "synonyms": [
            "atención", "concentración", "enfoque", "vigilancia", "alerta", 
            "atención selectiva", "atención sostenida",
            "no me concentraba", "distracciones", "mantener la atención", "capacidad de atención"
        ]
    },
    {
        "name": "Velocidad de procesamiento",
        "synonyms": [
            "velocidad mental", "velocidad cognitiva", "tiempo de reacción", 
            "procesamiento de información", "rapidez mental",
            "agilizar procesos", "más rápido", "ahorrar tiempo", "en segundos", "inmediato"
        ]
    },
    {
        "name": "Razonamiento",
        "synonyms": [
            "pensamiento lógico", "razonamiento deductivo", "razonamiento inductivo", 
            "pensamiento crítico", "pensamiento abstracto", "resolución de problemas", 
            "pensamiento analítico", "inferencias", "lógica",
            "criterio", "sentido crítico", "capacidad de análisis", "capacidad de razonamiento",
            "analizar", "cuestionar", "conclusiones", "evaluación"
        ]
    },
    {
        "name": "Función ejecutiva",
        "synonyms": [
            "autorregulación", "control cognitivo", "planificación", "toma de decisiones", 
            "flexibilidad mental", "inhibición", "gestión de metas", "pensamiento estratégico",
            "organizar ideas", "estructurar ideas", "tomar decisiones"
        ]
    },
    {
        "name": "Comprensión del lenguaje",
        "synonyms": [
            "comprensión verbal", "procesamiento semántico", "comprensión lectora", 
            "análisis de texto", "habilidades lingüísticas", "razonamiento verbal",
            "redacción", "capacidad de redacción", "entender"
        ]
    },
    {
        "name": "Aprendizaje",
        "synonyms": [
            "adquisición de conocimiento", "aprendizaje de habilidades", "adaptabilidad", 
            "crecimiento cognitivo", "aprendizaje asociativo", "aprender",
            "entender conceptos", "esfuerzo cognitivo", "proceso de aprendizaje", "apropiarme"
        ]
    },
    {
        "name": "Creatividad",
        "synonyms": [
            "pensamiento divergente", "originalidad", "pensamiento innovador", 
            "generación de ideas", "flexibilidad conceptual", "imaginación",
            "ideas propias", "chispa inicial", "desbloquear la creatividad"
        ]
    },
    {"name": "Habilidad visoespacial", "synonyms": ["razonamiento espacial", "procesamiento visual", "rotación mental", "visualización espacial", "conciencia espacial", "imaginación visual", "integración visomotriz"]},
    {"name": "Habilidad numérica", "synonyms": ["razonamiento matemático", "pensamiento cuantitativo", "cálculo", "numeración", "habilidad aritmética", "procesamiento numérico"]},
    {"name": "Metacognición", "synonyms": ["pensar sobre pensar", "autoconciencia", "reflexión", "evaluación propia", "autorregulación cognitiva", "monitoreo del pensamiento", "reflexionar"]},
    {"name": "Inteligencia fluida", "synonyms": ["resolución de problemas nuevos", "razonamiento abstracto", "pensamiento adaptativo"]},
    {"name": "Inteligencia cristalizada", "synonyms": ["base de conocimientos", "habilidad verbal", "conocimiento factual", "conocimiento acumulado", "conocimiento cultural"]},
    {"name": "Percepción", "synonyms": ["percepción visual", "percepción auditiva", "procesamiento sensorial", "reconocimiento de patrones", "percepción táctil"]},
    {"name": "Solución de problemas", "synonyms": ["estrategia de solución", "razonamiento heurístico", "pensamiento estratégico", "resolución de problemas", "diagnóstico", "buscar soluciones"]},
    {"name": "Toma de decisiones", "synonyms": ["juicio", "evaluación", "elección", "priorización", "análisis de riesgos"]},
    {"name": "Flexibilidad cognitiva", "synonyms": ["flexibilidad mental", "cambio de tareas", "adaptabilidad", "cambio cognitivo"]}
]

# 2. carga de datos y modelo de sentimiento

# cargar archivos json
try:
    with open("Cómo ChatGPT arruina tu inteligencia - YouTube.json", encoding="utf-8") as f1:
        data1 = json.load(f1)
    with open("El MIT Muestra el Peligro del ChatGPT - YouTube.json", encoding="utf-8") as f2:
        data2 = json.load(f2)
    comentarios_json = data1 + data2
except FileNotFoundError:
    print("error: asegurate de que los archivos json esten en la misma carpeta.")
    exit()

# cargar el modelo de hugging face
print("cargando modelo de analisis de sentimiento...")
sentiment_pipeline = pipeline("sentiment-analysis", model="pysentimiento/robertuito-sentiment-analysis")
print("modelo cargado.")


# 3. funciones de analisis

def detectar_cognitive_insight(texto):
    texto_lower = texto.lower()
    for habilidad in cognitive_skills:
        for sinonimo in habilidad["synonyms"]:
            if sinonimo in texto_lower:
                return habilidad["name"]
    return "sin categoría"

def map_sentiment_label(label):
    if label == 'POS':
        return 'positivo'
    elif label == 'NEG':
        return 'negativo'
    return 'neutro'

# 4. procesamiento y exportacion

resultados = []
textos_para_analizar = []

# extraer el texto de cada comentario
for item in comentarios_json:
    texto = item.get("ytcoreattributedstring") or item.get("Título") or ""
    if texto and isinstance(texto, str) and texto.strip(): # solo procesar si el texto no esta vacio
        textos_para_analizar.append(texto)

print(f"procesando {len(textos_para_analizar)} comentarios...")

# procesar sentimientos en lote para mas eficiencia
sentimientos_results = sentiment_pipeline(textos_para_analizar, batch_size=16, truncation=True) 

# usamos tqdm para ver el progreso de la union de datos
print("uniendo resultados...")
for i, texto in tqdm(enumerate(textos_para_analizar), total=len(textos_para_analizar)):
    sentimiento_raw = sentimientos_results[i]
    
    sentimiento = map_sentiment_label(sentimiento_raw['label'])
    score = sentimiento_raw['score'] if sentimiento != 'negativo' else -sentimiento_raw['score']
    
    insight = detectar_cognitive_insight(texto)
    
    resultados.append({
        "texto": texto,
        "sentimiento": sentimiento,
        "score": round(score, 3),
        "insight": insight
    })

# guardar en csv
with open("comentarios_con_sentimiento.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["texto", "sentimiento", "score", "insight"])
    writer.writeheader()
    writer.writerows(resultados)

print(f"\n se creo el archivo 'comentarios_con_sentimiento.csv' con {len(resultados)} comentarios procesados.")