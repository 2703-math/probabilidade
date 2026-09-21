import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Laboratório de Probabilidades",
    page_icon="🎲",
    layout="wide"
)

# ============================================
# CSS PROFISSIONAL (PADRÃO SAAS)
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f8fafc;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .main-title {font-size: 2.3rem; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: 0.2rem;}
    .subtitle {font-size: 1.05rem; color: #64748b; text-align: center; margin-bottom: 2rem;}
    .dashboard-card {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-bottom: 1.2rem;}
    .card-header {font-size: 1.1rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.6rem;}
    .math-box {background: #f1f5f9; border-radius: 8px; padding: 1rem; font-family: monospace; color: #334155; margin: 1rem 0; border: 1px solid #e2e8f0; text-align: center;}
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO E ABAS
# ============================================
st.markdown('<div class="main-title">🎲 Laboratório Interativo de Probabilidade</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore Espaços Amostrais, Árvores de Decisão, Regras de Soma e Probabilidade Condicional</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🌲 Eventos Sucessivos & Árvore", 
    "⚖️ Eventos Complementares", 
    "➕ Soma de Probabilidades", 
    "🔗 Probabilidade Condicional"
])

# ============================================
# ABA 1: EVENTOS SUCESSIVOS E ÁRVORE
# ============================================
with tab1:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🌲 Árvore de Probabilidades e Espaço Amostral (Ex: Lançamento de 2 Moedas)</div>', unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        st.markdown("### Configuração do Experimento")
        moedas = st.slider("Número de Lançamentos de Moeda", 1, 3, 2, step=1)
        st.info(f"Cada lançamento duplica o espaço amostral. Com {moedas} lançamentos, teremos $2^{{{moedas}}} = {2**moedas}$ resultados possíveis.")
        
        # Gerando espaço amostral para moedas
        if moedas == 1:
            espaco = ["Cara (C)", "Coroa (K)"]
            prob = 0.5
        elif moedas == 2:
            espaco = ["CC", "CK", "KC", "KK"]
        else:
            espaco = ["CCC", "CCK", "CKC", "CKK", "KCC", "KCK", "KKC", "KKK"]
            
        st.markdown(f"**Espaço Amostral ($\Omega$):**")
        st.code(str(espaco))

    with col_r:
        st.markdown("### 📊 Visualização da Árvore de Probabilidades")
        
        # Construção gráfica da árvore usando Plotly
        fig = go.Figure()
        
        if moedas == 2:
            # Nós da Árvore (Coordenadas X, Y)
            # Início -> Lançamento 1 -> Lançamento 2
            fig.add_trace(go.Scatter(
                x=[0, 1, 1, 2, 2, 2, 2], 
                y=[2, 3, 1, 3.5, 2.5, 1.5, 0.5],
                mode="text+markers",
                text=["Início", "Cara (1/2)", "Coroa (1/2)", "CC (1/4)", "CK (1/4)", "KC (1/4)", "KK (1/4)"],
                textposition="top center",
                marker=dict(size=[15, 10, 10, 8, 8, 8, 8], color=['#3b82f6', '#10b981', '#ef4444', '#f59e0b', '#f59e0b', '#f59e0b', '#f59e0b'])
            ))
            # Linhas de conexão (Galhos)
            fig.add_shape(type="line", x0=0, y0=2, x1=1, y1=3, line=dict(color="#cbd5e1", width=2))
            fig.add_shape(type="line", x0=0, y0=2, x1=1, y1=1, line=dict(color="#cbd5e1", width=2))
            fig.add_shape(type="line", x0=1, y0=3, x1=2, y1=3.5, line=dict(color="#cbd5e1", width=2))
            fig.add_shape(type="line", x0=1, y0=3, x1=2, y1=2.5, line=dict(color="#cbd5e1", width=2))
            fig.add_shape(type="line", x0=1, y0=1, x1=2, y1=1.5, line=dict(color="#cbd5e1", width=2))
            fig.add_shape(type="line", x0=1, y0=1, x1=2, y1=0.5, line=dict(color="#cbd5e1", width=2))
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False),
                plot_bgcolor='white', paper_bgcolor='white', height=350, margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("Altere o seletor para 2 lançamentos para visualizar o diagrama estruturado da árvore de probabilidades acima.")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 2: EVENTOS COMPLEMENTARES
# ============================================
with tab2:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">⚖️ Eventos Complementares ($P(A) + P(A\') = 1$)</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 1], gap="large")
    
    with col_c1:
        st.markdown("""
        O **evento complementar** ($A'$) representa tudo o que **não** é o evento $A$ dentro do espaço amostral. A soma da probabilidade de um evento acontecer com a de não acontecer é sempre igual a 100% ($1$).
        """)
        st.markdown('<div class="math-box">P(A\') = 1 - P(A)</div>', unsafe_allow_html=True)
        
        exemplo_comp = st.selectbox("Escolha o Contexto:", ["Baralho (Extrair uma Carta)", "Lançamento de Dados"])
        
    with col_c2:
        if exemplo_comp == "Baralho (Extrair uma Carta)":
            st.markdown("#### Exemplo com Baralho Tradicional (52 cartas)")
            alvo = st.selectbox("Evento A (Quero extrair):", ["Uma Carta de Copas", "Uma Figura (Rei, Dama ou Valete)", "Um Ás"])
            
            if alvo == "Uma Carta de Copas":
                p_a = 13 / 52
                p_comp = 39 / 52
                st.metric("P(A) - É Copas", f"{p_a:.2f} ({13}/52)")
                st.metric("P(A') - NÃO é Copas", f"{p_comp:.2f} ({39}/52)")
            elif alvo == "Uma Figura (Rei, Dama ou Valete)":
                p_a = 12 / 52
                p_comp = 40 / 52
                st.metric("P(A) - É Figura", f"{p_a:.2f} ({12}/52)")
                st.metric("P(A') - NÃO é Figura", f"{p_comp:.2f} ({40}/52)")
            else:
                p_a = 4 / 52
                p_comp = 48 / 52
                st.metric("P(A) - É Ás", f"{p_a:.2f} ({4}/52)")
                st.metric("P(A') - NÃO é Ás", f"{p_comp:.2f} ({48}/52)")
        else:
            st.markdown("#### Exemplo com um Dado de 6 Faces ($\Omega = \{1, 2, 3, 4, 5, 6\}$)")
            dado_alvo = st.selectbox("Evento A:", ["Sair Número Par", "Sair Número Maior que 4", "Sair o Número 6"])
            
            if dado_alvo == "Sair Número Par":
                p_a = 3 / 6
                p_comp = 3 / 6
                st.metric("P(A) - Par {2, 4, 6}", "50% (3/6)")
                st.metric("P(A') - ÍMPAR {1, 3, 5}", "50% (3/6)")
            elif dado_alvo == "Sair Número Maior que 4":
                p_a = 2 / 6
                p_comp = 4 / 6
                st.metric("P(A) - Maior que 4 {5, 6}", f"{p_a:.2f} (2/6)")
                st.metric("P(A') - Menor ou igual a 4", f"{p_comp:.2f} (4/6)")
            else:
                p_a = 1 / 6
                p_comp = 5 / 6
                st.metric("P(A) - Sair 6", f"{p_a:.2f} (1/6)")
                st.metric("P(A') - NÃO sair 6", f"{p_comp:.2f} (5/6)")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 3: SOMA DE PROBABILIDADES
# ============================================
with tab3:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">➕ Regra da Soma: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Utilizada quando queremos calcular a probabilidade de ocorrer **o evento A OU o evento B**. Se os eventos forem **mutuamente exclusivos** (não podem ocorrer ao mesmo tempo), a interseção $P(A \cap B)$ é zero.
    """)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### Simulação com Dados (Sair Soma ou Número Específico)")
        lancar_dois_dados = st.checkbox("Analisar Lançamento de 2 Dados (Soma)")
        
        if lancar_dois_dados:
            alvo_soma = st.slider("Qual soma deseja analisar?", 2, 12, 7)
            # Total de combinacoes de 2 dados = 36
            combinacoes = sum(1 for d1 in range(1, 7) for d2 in range(1, 7) if d1 + d2 == alvo_soma)
            prob_soma = combinacoes / 36
            st.metric(f"Probabilidade de a soma ser {alvo_soma}", f"{prob_soma*100:.1f}% ({combinacoes}/36)")
        else:
            st.markdown("#### Exemplo com Baralho (OU)")
            st.markdown("Qual a probabilidade de tirar uma carta que seja **Ás OU de Copas**?")
            p_as = 4 / 52
            p_copas = 13 / 52
            p_intersecao = 1 / 52 # Ás de Copas é contado duas vezes
            p_total = p_as + p_copas - p_intersecao
            st.markdown(f"""
            * $P(\\text{{Ás}}) = 4/52$
            * $P(\\text{{Copas}}) = 13/52$
            * $P(\\text{{Ás e Copas}}) = 1/52$
            * **Resultado:** $\\frac{{4 + 13 - 1}}{{52}} = \\frac{{16}}{{52}} \\approx {p_total*100:.1f}\\%$
            """)

    with col_s2:
        st.markdown("#### Diagrama Lógico de Conjuntos (União)")
        # Gráfico simples para ilustrar a união
        df_venn = pd.DataFrame({
            "Evento": ["A (Apenas)", "B (Apenas)", "Intersecção (A e B)"],
            "Qtde": [3, 12, 1]
        })
        st.bar_chart(df_venn.set_index("Evento"))

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 4: PROBABILIDADE CONDICIONAL
# ============================================
with tab4:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🔗 Probabilidade Condicional: $P(A | B) = \\frac{P(A \cap B)}{P(B)}$</div>', unsafe_allow_html=True)
    
    st.markdown("""
    A probabilidade condicional calcula a chance de um evento **A** ocorrer, **sabendo que** o evento **B** já ocorreu (reduzindo o espaço amostral original).
    """)
    
    col_p1, col_p2 = st.columns([1, 1], gap="large")
    
    with col_p1:
        st.markdown("### Exemplo Prático: Retirada de Cartas sem Reposição")
        st.markdown("1. Retiramos uma carta de um baralho de 52 cartas e sabemos que ela **é uma figura** (Evento B).")
        st.markdown("2. Qual é a probabilidade de ela ser um **Rei** (Evento A)?")
        
        p_b = 12 / 52 # Total de figuras
        p_a_inter_b = 4 / 52 # Total de Reis que também são figuras (todos os 4 reis)
        p_condicional = p_a_inter_b / p_b
        
        st.markdown(f"""
        * **Espaço Amostral Reduzido ($B$):** Apenas as 12 figuras do baralho.
        * **Casos Favoráveis ($A \\cap B$):** 4 Reis.
        * **Cálculo:** $\\frac{{4/52}}{{12/52}} = \\frac{{4}}{{12}} = \\frac{{1}}{{3}} \\approx {p_condicional*100:.1f}\\%$.
        """)

    with col_p2:
        st.markdown("### Simulador Rápido de Condicional")
        dado_cond = st.selectbox("Dado lançado. Condição prévia (B):", ["O número obtido é par", "O número obtido é maior que 3"])
        pergunta_cond = st.selectbox("Qual a probabilidade de (A):", ["Ser o número 6", "Ser um número primo"])
        
        if dado_cond == "O número obtido é par" and pergunta_cond == "Ser o número 6":
            # Pares: {2, 4, 6} (3 casos). O 6 ocorre 1 vez.
            st.success("Resultado: **1/3 (~33.3%)** — Pois dos 3 números pares posibles ({2, 4, 6}), apenas um é o 6.")
        elif dado_cond == "O número maior que 3" and pergunta_cond == "Ser um número primo":
            # Maiores que 3: {4, 5, 6} (3 casos). Primos entre eles: {5} (1 caso).
            st.success("Resultado: **1/3 (~33.3%)** — Pois o único número primo no subconjunto {4, 5, 6} é o 5.")
        else:
            st.info("Selecione uma combinação compatível para visualizar o cálculo passo a passo.")

    st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem;">
    🎲 <b>Laboratório de Probabilidades SaaS</b> — Ferramenta Educacional Interativa
</div>
""", unsafe_allow_html=True)