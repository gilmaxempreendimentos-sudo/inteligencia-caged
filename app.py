import streamlit as st
import pandas as pd
from sqlmodel import Session, create_engine, select
import plotly.express as px
from caged_analysis import AnaliseMercado

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="GX Soluções | Inteligência de Mercado",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. LIGAÇÃO AO BANCO DE DADOS
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})

@st.cache_data 
def buscar_dados():
    with Session(engine) as session:
        statement = select(AnaliseMercado)
        results = session.exec(statement).all()
        return pd.DataFrame([r.model_dump() for r in results])

# 3. ESTILIZAÇÃO CUSTOMIZADA (CSS MODERNO TIPO SAAS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #F8FAFC; }
    
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #0F172A; font-weight: 700; letter-spacing: -0.5px; }
    div[data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    div[data-testid="metric-container"] { background-color: #FFFFFF; padding: 24px 20px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #E2E8F0; }
    h1, h2, h3 { color: #0F172A; font-weight: 700; letter-spacing: -0.5px; }
    hr { margin-top: 2rem; margin-bottom: 2rem; border-color: #E2E8F0; }
    
    /* Estilo especial para a Landing Page */
    .hero-title { font-size: 3rem; font-weight: 800; color: #0F172A; line-height: 1.2; margin-bottom: 1rem; }
    .hero-subtitle { font-size: 1.2rem; color: #475569; margin-bottom: 2rem; line-height: 1.6; }
    .feature-box { background-color: #FFFFFF; padding: 20px; border-radius: 8px; border-left: 5px solid #0EA5E9; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%; }
    </style>
    """, unsafe_allow_html=True)

df = buscar_dados()

# --- TRADUTOR DE CÓDIGOS IBGE ---
mapa_estados_ibge = {
    '11': 'Rondônia', '12': 'Acre', '13': 'Amazonas', '14': 'Roraima', '15': 'Pará', '16': 'Amapá', 
    '17': 'Tocantins', '21': 'Maranhão', '22': 'Piauí', '23': 'Ceará', '24': 'Rio Grande do Norte', 
    '25': 'Paraíba', '26': 'Pernambuco', '27': 'Alagoas', '28': 'Sergipe', '29': 'Bahia', 
    '31': 'Minas Gerais', '32': 'Espírito Santo', '33': 'Rio de Janeiro', '35': 'São Paulo', 
    '41': 'Paraná', '42': 'Santa Catarina', '43': 'Rio Grande do Sul', '50': 'Mato Grosso do Sul', 
    '51': 'Mato Grosso', '52': 'Goiás', '53': 'Distrito Federal', '99': 'Não Informado'
}
df['estado'] = df['estado'].astype(str).map(mapa_estados_ibge).fillna(df['estado'])

# ==========================================
# BARRA LATERAL (MENU DE NAVEGAÇÃO)
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/000000/combo-chart--v1.png", width=60) # Ícone temporário simulando o logo
st.sidebar.title("GX Soluções")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação da Plataforma:",
    ["🏢 Visão Executiva (Home)", "📊 Painel de Inteligência"]
)

st.sidebar.markdown("---")

# ==========================================
# PÁGINA 1: A LANDING PAGE (APRESENTAÇÃO)
# ==========================================
if menu == "🏢 Visão Executiva (Home)":
    st.markdown('<div class="hero-title">Inteligência Competitiva e Engenharia de Custos</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Decisões estratégicas baseadas em dados reais de milhões de contratações no Brasil. A GX Soluções transforma o complexo mercado de trabalho numa vantagem competitiva clara para o seu negócio.</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("O Fim da Estimativa Cega")
    st.write("No mercado atual, a diferença entre vencer uma licitação ou perder um contrato milionário está na precisão da informação. Nossa plataforma lê diretamente a base oficial do Governo Federal (CAGED) e cruza os dados para entregar o raio-X financeiro do seu setor.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>🏗️ Orçamentos e Licitações</h4>
            <p>Composição precisa da folha de pagamento em propostas comerciais e editais públicos para vencer concorrências sem corroer a sua margem de lucro.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🎯 Recrutamento Cirúrgico</h4>
            <p>Atraia os melhores talentos definindo salários de entrada altamente competitivos. Pare de "chutar" valores e saiba exatamente o que a concorrência paga.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h4>📈 Filtros de Alta Resolução</h4>
            <p>Mapeamento granular por Estado, Cargo (CBO) e Setor Econômico (CNAE). Entenda a curva de maturidade do seu time, do nível Júnior ao Master.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Pronto para começar?** Selecione **'Painel de Inteligência'** no menu lateral para acessar a base de dados.")

# ==========================================
# PÁGINA 2: O PAINEL DE DADOS (A FERRAMENTA)
# ==========================================
elif menu == "📊 Painel de Inteligência":
    
    st.sidebar.markdown("### 🔍 Filtros Estratégicos")
    
    estados_disponiveis = sorted(df['estado'].unique())
    estado_padrao = ["Rio de Janeiro"] if "Rio de Janeiro" in estados_disponiveis else [estados_disponiveis[0]]
    estado_sel = st.sidebar.multiselect("Localidades (Estado)", estados_disponiveis, default=estado_padrao)
    
    min_amostra = st.sidebar.slider("Confiabilidade Estatística (Amostra Mínima)", 1, 100, 3)

    st.title("Painel de Inteligência Salarial")
    st.caption(f"Base de dados atualizada: {len(df):,} cenários mapeados por setor econômico.")

    cargo_busca = st.text_input("🔍 Buscar Ocupação", placeholder="Ex: Engenheiro de Producao")

    df_filtrado = df[(df['estado'].isin(estado_sel)) & (df['amostra'] >= min_amostra)]

    if cargo_busca:
        df_filtrado = df_filtrado[df_filtrado['titulo_cbo'].str.contains(cargo_busca, case=False)]

    if not df_filtrado.empty:
        cargos_unicos = sorted(df_filtrado['titulo_cbo'].unique())
        cargo_selecionado = st.selectbox("Selecione o cargo para análise detalhada:", cargos_unicos)
        
        df_cargo = df_filtrado[df_filtrado['titulo_cbo'] == cargo_selecionado]
        df_cargo = df_cargo.sort_values(by='media_salarial', ascending=False)

        setor_campeao = df_cargo.iloc[0]['setor_economico']
        maior_media = df_cargo.iloc[0]['media_salarial']
        amostra_total = df_cargo['amostra'].sum()

        st.markdown("### Visão Executiva")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Teto Salarial (Média)", f"R$ {maior_media:,.2f}")
        c2.metric("Setor Mais Rentável", setor_campeao)
        c3.metric("Volume de Contratações", f"{int(amostra_total)}")
        c4.metric("Diversidade Setorial", f"{len(df_cargo)} setores")

        st.markdown("---")

        st.subheader(f"Mapeamento por Setor Econômico")
        fig_setores = px.bar(
            df_cargo, x='media_salarial', y='setor_economico', orientation='h',
            color='media_salarial', color_continuous_scale='Teal', text='media_salarial',
            labels={'setor_economico': '', 'media_salarial': 'Média Salarial (R$)'}
        )
        fig_setores.update_traces(texttemplate='<b>R$ %{text:,.2f}</b>', textposition='outside', textfont_size=13, marker_line_width=0)
        fig_setores.update_layout(font_family="Inter", height=max(400, len(df_cargo) * 45), showlegend=False, plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(range=[0, df_cargo['media_salarial'].max() * 1.25], showgrid=False, zeroline=False), yaxis={'categoryorder':'total ascending', 'tickfont': dict(size=14)})
        st.plotly_chart(fig_setores, use_container_width=True, key=f"bar_setores_{cargo_selecionado}")

        st.markdown("---")

        st.subheader(f"Curva de Progressão e Maturidade")
        setores_disponiveis = df_cargo['setor_economico'].tolist()
        setor_detalhe = st.selectbox("Selecione o setor para visualizar a progressão:", setores_disponiveis)
        
        dados_setor = df_cargo[df_cargo['setor_economico'] == setor_detalhe].iloc[0]

        df_senioridade = pd.DataFrame({
            "Nível": ["Júnior (P25)", "Pleno (P50)", "Sênior (P75)", "Master (P90)"],
            "Salário": [dados_setor['junior_p25'], dados_setor['pleno_p50'], dados_setor['senior_p75'], dados_setor['master_p90']]
        })

        fig_senioridade = px.bar(df_senioridade, x='Nível', y='Salário', color='Salário', color_continuous_scale='Teal', text='Salário')
        fig_senioridade.update_traces(texttemplate='<b>R$ %{text:,.2f}</b>', textposition='outside', textfont_size=14, cliponaxis=False, marker_line_width=0)
        fig_senioridade.update_layout(font_family="Inter", showlegend=False, height=450, margin=dict(t=30), plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(range=[0, df_senioridade['Salário'].max() * 1.3], showgrid=True, gridcolor='#E2E8F0', title=""), xaxis=dict(tickfont=dict(size=14), title=""))
        
        st.plotly_chart(fig_senioridade, use_container_width=True, key=f"chart_sen_{cargo_selecionado}_{setor_detalhe}")

        with st.expander("📂 Explorar Base de Dados (Tabela)"):
            st.dataframe(df_cargo, use_container_width=True)

    else:
        st.info("💡 Nenhum dado encontrado. Tente ajustar os parâmetros de busca na barra lateral.")