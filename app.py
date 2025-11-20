import streamlit as st
from datetime import datetime
import time
import math
import os
# A biblioteca streamlit_carousel foi removida para usar o recurso nativo de imagem do Streamlit,
# o que nos dá mais controle sobre o CSS para corrigir o corte.

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

# Inicializa o índice de imagem na sessão (usado para o carrossel manual)
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

def next_image():
    """Avança para a próxima imagem."""
    if image_paths:
        st.session_state.current_index = (st.session_state.current_index + 1) % len(image_paths)

def prev_image():
    """Volta para a imagem anterior."""
    if image_paths:
        st.session_state.current_index = (st.session_state.current_index - 1) % len(image_paths)

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
    
    /* Estilos para a Galeria/Imagens */
    
    /* Alvo 1: O contêiner de alto nível do Streamlit (classe gerada dinamicamente) */
    /* Isso tenta reverter qualquer altura fixa imposta pelo Streamlit. */
    div.stImage {
        height: auto !important;
        max-height: none !important;
        min-height: auto !important;
        overflow: visible !important;
    }

    /* Alvo 2: A tag img dentro do contêiner */
    .stImage img {
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(216, 27, 96, 0.6); 
        
        /* Regras Definitivas Contra Corte */
        object-fit: contain !important; /* ESSENCIAL: Garante que a imagem inteira seja visível (sem crop) */
        width: 100% !important; /* Usa a largura total da coluna */
        height: auto !important; /* A altura se ajusta à proporção da imagem (sem altura fixa) */
        max-height: none !important; /* Remove qualquer limite de altura */
        min-height: auto !important;
    }

    /* Alvo 3: O contêiner pai que envolve o stImage, usando um seletor mais amplo */
    /* Esta é a tentativa mais agressiva de remover restrições de altura nos pais. */
    .st-emotion-cache-1mnn6ge, .st-emotion-cache-9y61k, .st-emotion-cache-0 { /* Classes de cache Streamlit que podem impor altura */
        height: auto !important;
        max-height: none !important;
    }


    /* Estilos para os botões do carrossel */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background-color: #D81B60; /* Vermelho */
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #FF4444; /* Vermelho mais claro no hover */
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

# --- EXIBIÇÃO DA GALERIA (CARROSSEL MANUAL NATIVO) ---
if image_paths:
    st.header("✨ Nossas Melhores Memórias ✨")
    
    # Exibir a imagem atual
    current_path = image_paths[st.session_state.current_index]
    image_number = st.session_state.current_index + 1
    total_images = len(image_paths)
    
    st.image(
        current_path, 
        caption=f"Foto {image_number} de {total_images}",
    )
    
    # Controles (Botões)
    col1, col2 = st.columns(2)
    with col1:
        st.button("❮ Anterior", on_click=prev_image, key="prev_btn")
    with col2:
        st.button("Próxima ❯", on_click=next_image, key="next_btn")
        
    st.markdown("---")
else:
    st.info("Adicione suas fotos na pasta 'imagens' do seu repositório para exibir a galeria!")
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
