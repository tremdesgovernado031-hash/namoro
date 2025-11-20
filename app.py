import streamlit as st
from datetime import datetime
import time
import math
import os
from streamlit_carousel import carousel # Carrossel adicionado novamente

# --- CONFIGURAÇÃO INICIAL (DATA E HORA DO NAMORO) ---
# Namoro começou em 19/05/2024 às 21:30:00
DATE_OF_START = datetime(2024, 5, 19, 21, 30, 0)
# ----------------------------------------------------------------

# --- CARREGANDO IMAGENS DA PASTA LOCAL 'imagens' ---
IMAGE_FOLDER = "imagens"
image_paths = []

# O Streamlit Cloud executa este código. Ele PRECISA encontrar a pasta 'imagens' no repositório.
if os.path.exists(IMAGE_FOLDER) and os.path.isdir(IMAGE_FOLDER):
    # Lista os arquivos, ordenados por nome para ter uma ordem consistente
    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            # Adiciona o caminho completo da imagem (ex: imagens/foto1.jpg)
            image_paths.append(os.path.join(IMAGE_FOLDER, filename))
else:
    # Aviso caso a pasta não seja encontrada
    st.warning(f"A pasta '{IMAGE_FOLDER}' não foi encontrada. O carrossel não será exibido. Certifique-se de que ela está no seu repositório GitHub.")

carousel_items = []
if image_paths:
    for i, path in enumerate(image_paths):
        carousel_items.append({
            "image": path,
            "title": f"Nossa Memória {i+1}",
            "text": f"Momento especial {i+1} de Pedro e Hellen",
            "interval": 3000 # 3 segundos para cada slide
        })
# ------------------------------------------------------------------------------

def calculate_duration(start_date):
    """Calcula a duração e a decompõe em anos, meses, dias, horas, minutos e segundos."""
    now = datetime.now()
    duration = now - start_date

    total_seconds = int(duration.total_seconds())

    s = total_seconds % 60
    m = (total_seconds // 60) % 60
    h = (total_seconds // 3600) % 24
    total_days = total_seconds // 86400

    # Aproximação para anos e meses (abordagem comum em contadores)
    DAYS_IN_YEAR = 365.2425
    DAYS_IN_MONTH = 30.4375

    years = math.floor(total_days / DAYS_IN_YEAR)
    days_after_years = total_days - math.floor(years * DAYS_IN_YEAR)
    months = math.floor(days_after_years / DAYS_IN_MONTH)
    days_only = math.floor(days_after_years - (months * DAYS_IN_MONTH))

    return years, months, days_only, h, m, s, total_seconds

# Configuração da página Streamlit
st.set_page_config(
    page_title="Pedro e Hellen",
    page_icon="❤️",
    layout="centered",
)

st.title("❤️ Pedro e Hellen ❤️")
st.subheader("Contagem Detalhada do Nosso Amor!") 

# Descrição do contador
st.markdown(
    """
    <p style="text-align: center; color: #aaaaaa; font-size: 1.1em; margin-top: -10px;">
        Contamos cada segundo do nosso relacionamento! Reviva nossas melhores lembranças na galeria de fotos.
    </p>
    """,
    unsafe_allow_html=True
)

# Estilos CSS personalizados (Preto e Vermelho)
st.markdown(
    """
    <style>
    /* Fundo escuro sutil e texto principal claro */
    .stApp {
        background-color: #111111; /* Fundo do app */
    }
    h1, h2, h3, h4, .stMarkdown {
        color: #ffffff;
    }
    
    /* Contêiner de Métricas (Responsável por colocar os boxes lado a lado e com destaque) */
    .metric-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap; /* Permite que os boxes quebrem para a próxima linha em telas pequenas */
        margin-top: 30px;
        gap: 20px;
        /* Estilos para destacar o único contador */
        border: 3px solid #D81B60; /* Borda Vermelha */
        border-radius: 10px;
        padding: 20px;
        background-color: #222222;
        box-shadow: 0 4px 15px rgba(216, 27, 96, 0.4); 
    }
    
    /* Caixa de Cada Métrica */
    .metric-box {
        background-color: #333333; /* Fundo da caixa cinza escuro */
        border-radius: 12px;
        padding: 15px 25px;
        min-width: 120px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        border-bottom: 4px solid #D81B60; /* Linha de destaque vermelha */
        transition: transform 0.2s;
    }
    .metric-box:hover {
        transform: scale(1.05); /* Efeito sutil ao passar o mouse */
        background-color: #444444;
    }
    .metric-value {
        font-size: 3.0em;
        font-weight: 900;
        color: #FF4444; /* Vermelho para os números */
    }
    .metric-label {
        font-size: 0.9em;
        color: #aaaaaa; /* Cinza claro para os rótulos */
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Estilos para o carrossel */
    .stCarousel {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(216, 27, 96, 0.6); /* Sombra vermelha forte para destaque */
        margin-top: 40px;
        margin-bottom: 40px;
    }
    
    /* Cor do texto de informação abaixo do contador */
    .stAlert p {
        color: #dddddd; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write(f"Início do Nosso Amor: **{DATE_OF_START.strftime('%d/%m/%Y às %H:%M:%S')}**")
st.markdown("---")

# --- CARROSSEL ---
# O carrossel é colocado ANTES do loop while True para ser desenhado uma única vez.
if carousel_items:
    try:
        carousel(items=carousel_items,
                width=1, # Largura máxima do contêiner
                autoplay=True,
                loop=True) 
        st.markdown("---") # Separador após o carrossel
    except Exception as e:
        st.error(f"Erro ao exibir carrossel. Verifique seu requirements.txt para garantir que 'streamlit-carousel' esteja instalado e que TODAS as fotos estejam na pasta 'imagens'.