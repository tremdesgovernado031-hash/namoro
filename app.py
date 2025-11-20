import streamlit as st
from datetime import datetime
import time
import math
import os
from streamlit_carousel import carousel # Importação da biblioteca do carrossel

# --- CONFIGURAÇÃO INICIAL (DATA E HORA DO NAMORO) ---
# Namoro começou em 19/05/2024 às 21:30:00
DATE_OF_START = datetime(2024, 5, 19, 21, 30, 0)
# ----------------------------------------------------------------

# --- CARREGANDO IMAGENS DA PASTA LOCAL 'imagens' ---
IMAGE_FOLDER = "imagens"
image_paths = []

# Verifica se a pasta existe e lista os arquivos
if os.path.exists(IMAGE_FOLDER) and os.path.isdir(IMAGE_FOLDER):
    # Lista os arquivos, ordenados por nome para ter uma ordem consistente
    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        # Filtra apenas por arquivos de imagem comuns
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            # Cria o caminho relativo que o Streamlit Cloud consegue ler
            image_paths.append(os.path.join(IMAGE_FOLDER, filename))
else:
    # Aviso caso a pasta não seja encontrada
    st.warning(f"A pasta '{IMAGE_FOLDER}' não foi encontrada. O carrossel não será exibido. Certifique-se de que ela está no seu repositório GitHub.")

carousel_items = []
if image_paths:
    for i, path in enumerate(image_paths):
        # Usando apenas o caminho e o título, removendo o 'interval'
        carousel_items.append({
            "image": path,
            "title": f"Nossa Memória {i+1}",
            "text": f"Momento especial {i+1} de Pedro e Hellen",
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
        flex-wrap: wrap; 
        margin-top: 30px;
        gap: 20px;
        border: 3px solid #D81B60; /* Borda Vermelha */
        border-radius: 10px;
        padding: 20px;
        background-color: #222222;
        box-shadow: 0 4px 15px rgba(216, 27, 96, 0.4); 
    }
    
    /* Caixa de Cada Métrica */
    .metric-box {
        background-color: #333333; 
        border-radius: 12px;
        padding: 15px 25px;
        min-width: 120px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        border-bottom: 4px solid #D81B60; /* Linha de destaque vermelha */
        transition: transform 0.2s;
    }
    .metric-box:hover {
        transform: scale(1.05); 
        background-color: #444444;
    }
    .metric-value {
        font-size: 3.0em;
        font-weight: 900;
        color: #FF4444; /* Vermelho para os números */
    }
    .metric-label {
        font-size: 0.9em;
        color: #aaaaaa; 
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Estilos para o carrossel */
    /* Adicionando um tamanho fixo mínimo para evitar que o layout "salte" */
    .stCarousel {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(216, 27, 96, 0.6); 
        margin-top: 40px;
        margin-bottom: 40px;
        min-height: 400px; /* Garante que o espaço do carrossel será reservado */
    }
    
    .stAlert p {
        color: #dddddd; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write(f"Início do Nosso Amor: **{DATE_OF_START.strftime('%d/%m/%Y às %H:%M:%S')}**")
st.markdown("---")

# --- EXIBIÇÃO DO CARROSSEL ---
if carousel_items:
    try:
        # AQUI FOI REMOVIDO 'autoplay' e 'loop' para evitar o erro "unexpected keyword argument"
        carousel(items=carousel_items) 
        st.markdown("---") 
    except Exception as e:
        # Mensagem de erro padrão.
        st.error(f"Erro ao exibir carrossel. Por favor, verifique se a dependência 'streamlit-carousel' está instalada. O erro detalhado foi: {e}")
        st.markdown("---") 
else:
    st.info("Adicione suas fotos na pasta 'imagens' do seu repositório para exibir o carrossel!")
    st.markdown("---") 


# Inicializa um container vazio que será atualizado a cada segundo
placeholder = st.empty()

# O loop 'while True' permite a atualização em tempo real do contador.
while True:
    years, months, days_only, h, m, s, total_seconds = calculate_duration(DATE_OF_START)

    with placeholder.container():
        
        # Métrica detalhada em uma grade responsiva
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)

        # Anos
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{years}</div>
            <div class="metric-label">Anos</div>
        </div>
        """, unsafe_allow_html=True)

        # Meses
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{months}</div>
            <div class="metric-label">Meses</div>
        </div>
        """, unsafe_allow_html=True)

        # Dias
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{days_only}</div>
            <div class="metric-label">Dias Restantes</div>
        </div>
        """, unsafe_allow_html=True)

        # Horas
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{h:02}</div>
            <div class="metric-label">Horas</div>
        </div>
        """, unsafe_allow_html=True)

        # Minutos
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{m:02}</div>
            <div class="metric-label">Minutos</div>
        </div>
        """, unsafe_allow_html=True)

        # Segundos
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{s:02}</div>
            <div class="metric-label">Segundos</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Espera 1 segundo antes de recalcular e atualizar a tela
    time.sleep(1)
