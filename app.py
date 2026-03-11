import streamlit as st
import pandas as pd
from sqlmodel import Session, create_engine, select
import plotly.express as px
from caged_analysis import AnaliseMercado

# 1. CONFIGURAÇÃO DA PÁGINA (Layout Expandido)
st.set_page_config(
    page_title="GX Soluções | Inteligência Salarial",
    page_icon="📈",
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

# 3. ESTILIZAÇÃO PREMIUM TIPO "BLOOMBERG TERMINAL / POWER BI"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background-color: #F4F7FE; } /* Fundo gelo ultraleve, muito usado em SaaS moderno */
    
    /* Customização da Barra Lateral */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    
    /* Títulos mais sofisticados */
    h1, h2, h3 { color: #1E293B; font-weight: 700; letter-spacing: -0.02em; }
    
    /* Cards de Métricas HTML/CSS customizados (Responsivos) */
    .premium-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.03);
        border: 1px solid #E9EDF7;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s;
        height: 100%;
    }
    .premium-card:hover { transform: translateY(-3px); box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.06); }
    .card-title { font-size: 0.85rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
    .card-value { font-size: 2rem; font-weight: 800; color: #0F172A; line-height: 1.1; }
    .card-highlight { color: #0EA5E9; } /* Azul corporativo da GX */
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
# BARRA LATERAL (FILTROS)
# ==========================================
st.sidebar.markdown("## GX Soluções")
st.sidebar.caption("Inteligência e Engenharia de Custos")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Parâmetros da Pesquisa")

estados_disponiveis = sorted(df['estado'].unique())
estado_padrao = ["Rio de Janeiro"] if "Rio de Janeiro" in estados_disponiveis else [estados_disponiveis[0]]
estado_sel = st.sidebar.multiselect("1. Praça de Atuação (UF)", estados_disponiveis, default=estado_padrao)

min_amostra = st.sidebar.slider("2. Trava de Confiança (Mín. Contratações)", 1, 50, 3, help="Filtra ruídos estatísticos do mercado.")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica de Uso:** Os valores exibem a remuneração base e não incluem benefícios indiretos.")

# ==========================================
# ÁREA PRINCIPAL
# ==========================================
st.title("Mapa de Engenharia de Custos Salariais")
st.markdown("Cenários reais validados pela base oficial de admissões do Governo Federal.")

cargo_busca = st.text_input("🔍 Digite o cargo que deseja orçar (ex: Soldador, Engenheiro, Gerente):")

df_filtrado = df[(df['estado'].isin(estado_sel)) & (df['amostra'] >= min_amostra)]

if cargo_busca:
    df_filtrado = df_filtrado[df_filtrado['titulo_cbo'].str.contains(cargo_busca, case=False)]

if not df_filtrado.empty:
    cargos_unicos = sorted(df_filtrado['titulo_cbo'].unique())
    cargo_selecionado = st.selectbox("Refine a Ocupação Exata (CBO):", cargos_unicos)
    
    df_cargo = df_filtrado[df_filtrado['titulo_cbo'] == cargo_selecionado]
    df_cargo = df_cargo.sort_values(by='media_salarial', ascending=False)

    setor_campeao = df_cargo.iloc[0]['setor_economico']
    maior_media = df_cargo.iloc[0]['media_salarial']
    amostra_total = df_cargo['amostra'].sum()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CARDS EXECUTIVOS (Design Responsivo e Premium) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Teto Salarial Mapeado</div>
            <div class="card-value card-highlight">R$ {maior_media:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Setor de Maior Remuneração</div>
            <div class="card-value" style="font-size: 1.4rem;">{setor_campeao[:35]}{'...' if len(setor_campeao)>35 else ''}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="premium-card">
            <div class="card-title">Volume de Contratações Analisado</div>
            <div class="card-value">{int(amostra_total):,} <span style="font-size: 1rem; color: #64748B;">vagas</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='opacity: 0.5;'><br>", unsafe_allow_html=True)

    # --- GRÁFICOS ANTI-BUG (Comportamento Adaptativo) ---
    col_chart1, col_space, col_chart2 = st.columns([1, 0.05, 1])

    with col_chart1:
        st.markdown("#### 🏢 Disparidade por Setor Econômico")
        st.caption("Qual indústria paga mais para esta exata função?")
        
        fig_setores = px.bar(
            df_cargo, x='media_salarial', y='setor_economico', orientation='h',
            color='media_salarial', color_continuous_scale='Blues' # Gradiente executivo
        )
        
        # O Segredo Anti-Bug do Plotly
        fig_setores.update_traces(
            texttemplate='<b>R$ %{x:,.0f}</b>', # Remove centavos
            textposition='auto', # Adapta automaticamente se a tela for pequena
            insidetextanchor='middle',
            marker_line_width=0
        )
        
        fig_setores.update_layout(
            font_family="Plus Jakarta Sans",
            height=max(350, len(df_cargo) * 45), 
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=40, t=10, b=0), # Margem de segurança na direita
            xaxis=dict(showgrid=False, showticklabels=False, title=""), # Esconde eixo inferior poluído
            yaxis={'categoryorder':'total ascending', 'title': '', 'tickfont': dict(size=13, color='#475569')},
            uniformtext_minsize=10, uniformtext_mode='hide' # Esconde o texto se bugar muito, liberando o hover
        )
        st.plotly_chart(fig_setores, use_container_width=True, config={'displayModeBar': False}) # Esconde a barra de ferramentas do Plotly

    with col_chart2:
        st.markdown("#### 📈 Curva de Senioridade")
        st.caption("Evolução salarial dentro de um setor específico.")
        
        setores_disponiveis = df_cargo['setor_economico'].tolist()
        setor_detalhe = st.selectbox("Selecione a indústria para ver o detalhe:", setores_disponiveis, label_visibility="collapsed")
        
        dados_setor = df_cargo[df_cargo['setor_economico'] == setor_detalhe].iloc[0]

        df_senioridade = pd.DataFrame({
            "Nível": ["1. Júnior (P25)", "2. Pleno (P50)", "3. Sênior (P75)", "4. Master (P90)"],
            "Salário": [dados_setor['junior_p25'], dados_setor['pleno_p50'], dados_setor['senior_p75'], dados_setor['master_p90']]
        })

        fig_senioridade = px.bar(
            df_senioridade, x='Salário', y='Nível', orientation='h', 
            color='Salário', color_continuous_scale='Teal'
        )
        
        fig_senioridade.update_traces(
            texttemplate='<b>R$ %{x:,.0f}</b>', 
            textposition='auto',
            marker_line_width=0
        )
        
        fig_senioridade.update_layout(
            font_family="Plus Jakarta Sans",
            showlegend=False, height=350,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=40, t=10, b=0),
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(title="", tickfont=dict(size=13, color='#475569')),
            uniformtext_minsize=10, uniformtext_mode='hide'
        )
        st.plotly_chart(fig_senioridade, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📂 Explorar Dados Brutos (Exportação Analítica)"):
        st.dataframe(df_cargo, use_container_width=True)

else:
    st.info("💡 Bem-vindo à base de dados. Digite uma ocupação acima para iniciar a análise de custos.")
