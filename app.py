import streamlit as st
from datetime import datetime
import time
import math
import os # ESSENCIAL: Garante que 'os.path' funcione para encontrar as imagens
# Reintrodução do carrossel para melhor gestão da galeria e aplicação de CSS
from streamlit_carousel import carousel 

# --- CONFIGURAÇÃO INICIAL (DATA E HORA DO NAMORO) ---
# Namoro começou em 19/05/2024 às 21:30:00
DATE_OF_START = datetime(2024, 5, 19, 21, 30, 0)
# ----------------------------------------------------------------

# --- CARREGANDO IMAGENS DA PASTA LOCAL 'imagens' ---
IMAGE_FOLDER = "imagens"
image_paths = []

# Verifica se a pasta existe e lista os arquivos
# Nota: A inclusão do 'import os' acima é crucial para que esta seção não cause um NameError
if os.path.exists(IMAGE_FOLDER) and os.path.isdir(IMAGE_FOLDER):
    # Lista os arquivos, ordenados por nome para ter uma ordem consistente
    for filename in sorted(os.listdir(IMAGE_FOLDER)):
        # Filtra apenas por arquivos de imagem comuns
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            # Cria o caminho relativo que o Streamlit Cloud consegue ler
            image_paths.append(os.path.join(IMAGE_FOLDER, filename))
else:
    # Esta mensagem só aparecerá se a pasta 'imagens' não for encontrada
    st.warning(f"A pasta '{IMAGE_FOLDER}' não foi encontrada. O carrossel não será exibido.")

# Preparar os itens do carrossel (formato exigido pela biblioteca)
carousel_items = []
if image_paths:
    for path in image_paths:
        # Adiciona item com URL da imagem e um título básico
        carousel_items.append({
            "title": "Nós",
            "text": "Nossa história em fotos",
            "img": path
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
    
    /* Contêiner de Métricas */
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
    
    /* Estilos para o Carrossel (Solução para o Corte de Fotos Verticais) */
    
    /* NOVO ALVO AGRESSIVO: Tenta anular altura em TODOS os contêineres Streamlit de alto nível */
    .st-emotion-cache-1mnn6ge, .st-emotion-cache-9y61k, .st-emotion-cache-0, .st-emotion-cache-1wa5c1t, 
    .st-emotion-cache-1g6x5f, .st-emotion-cache-13k65ss, .st-emotion-cache-1v0xssw, .st-emotion-cache-uofu1m {
        height: auto !important;
        max-height: none !important;
        min-height: auto !important;
        overflow: visible !important;
    }

    /* Alvo 1: O contêiner de itens do carrossel (onde a altura fixa é aplicada) */
    .carousel-item-wrapper, .carousel-item-body {
        height: auto !important;
        max-height: 90vh !important; /* Limite suave para telas grandes */
        min-height: auto !important;
        overflow: visible !important;
    }

    /* Alvo 2: A tag img dentro do carrossel (Regras Cruciais) */
    .carousel-item-body img {
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(216, 27, 96, 0.6); 
        
        /* ESSENCIAL: Garante que a imagem inteira seja visível (sem crop) */
        object-fit: contain !important; 
        
        /* ESSENCIAL: Altura determinada pela proporção original da imagem */
        height: auto !important; 
        
        /* ESSENCIAL: Remove qualquer limite de altura imposto */
        max-height: 90vh !important; 
        
        width: 100% !important; 
        min-height: auto !important;
        aspect-ratio: auto !important; /* Usa a proporção da imagem */
    }
    
    /* Esconde a barra de rolagem horizontal que pode aparecer com o carrossel */
    .st-emotion-cache-1mnn6ge, .st-emotion-cache-9y61k {
        overflow-x: hidden !important; 
    }
    
    /* Estilo para a Mensagem Final */
    .final-message {
        text-align: center;
        font-style: italic;
        color: #FF4444; /* Vermelho vibrante */
        font-size: 1.2em;
        margin-top: 40px;
        padding: 15px;
        border-top: 1px solid #333333;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.write(f"Início do Nosso Amor: **{DATE_OF_START.strftime('%d/%m/%Y às %H:%M:%S')}**")
st.markdown("---")

# --- EXIBIÇÃO DA GALERIA (CARROSSEL AUTOMÁTICO) ---
if carousel_items:
    # 1. Exibe o carrossel automático
    carousel(items=carousel_items, width=1.0)
    
    # 2. MOVE O TÍTULO PARA DEPOIS DO CARROSSEL
    st.header("✨ Nossas Melhores Memórias ✨")
    
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
        
        # --- MENSAGEM FINAL (O texto pedido) ---
        st.markdown(
            """
            <div class="final-message">
                Oi, meu amor! 
                Fiz esse site pra você lembrar que você é a melhor coisa que já aconteceu na minha vida e para nunca esquecer que eu sempre vou estar do seu lado, nos momentos bons e nos ruins. Te amo pra todo o sempre! 🫶🏻
            </div>
            """,
            unsafe_allow_html=True
        )
        # -------------------------------------

    # Espera 1 segundo antes de recalcular e atualizar a tela
    time.sleep(1)

