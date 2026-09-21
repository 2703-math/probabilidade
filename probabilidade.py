import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
# CSS PROFISSIONAL 
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f8fafc;}
    .dashboard-card {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); margin-bottom: 1.5rem;}
    .concept-box {background: #f1f5f9; border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 4px; margin-bottom: 1rem;}
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.markdown("<h1 style='text-align: center; color: #0f172a;'>🎲 Laboratório Visual de Probabilidades</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;'>Explorando a matemática do acaso com recursos gráficos iterativos</p>", unsafe_allow_html=True)

# ============================================
# FUNÇÃO GERADORA DA ÁRVORE (RECURSIVA)
# ============================================
def build_tree_plotly(depth):
    nodes = []
    edges = []
    
    def traverse(x, y, current_depth, label, y_spacing):
        # Evitar rótulo vazio no início
        display_label = "Início" if label == "" else label
        nodes.append({'x': x, 'y': y, 'label': display_label})
        
        if current_depth < depth:
            # Ramo CARA (C) - Sobe
            y1 = y + y_spacing
            edges.append({'x0': x, 'y0': y, 'x1': x + 1, 'y1': y1})
            traverse(x + 1, y1, current_depth + 1, label + "C", y_spacing / 2)
            
            # Ramo COROA (K) - Desce
            y2 = y - y_spacing
            edges.append({'x0': x, 'y0': y, 'x1': x + 1, 'y1': y2})
            traverse(x + 1, y2, current_depth + 1, label + "K", y_spacing / 2)

    # Inicia a recursão: Y spacing inicial depende da profundidade
    traverse(0, 0, 0, "", 2**(depth-1))
    
    fig = go.Figure()
    
    # Desenhar as linhas primeiro (para ficarem atrás)
    for edge in edges:
        fig.add_shape(type="line", x0=edge['x0'], y0=edge['y0'], x1=edge['x1'], y1=edge['y1'], 
                      line=dict(color="#cbd5e1", width=2))
        
    # Extrair coordenadas dos nós
    nx = [n['x'] for n in nodes]
    ny = [n['y'] for n in nodes]
    ntext = [n['label'] for n in nodes]
    ncolors = ["#3b82f6" if l == "Início" else ("#10b981" if l.endswith("C") else "#ef4444") for l in ntext]
    
    # Desenhar os nós
    fig.add_trace(go.Scatter(
        x=nx, y=ny, mode="markers+text",
        text=ntext, textposition="middle right" if depth < 4 else "top center",
        marker=dict(size=12, color=ncolors, line=dict(width=2, color="white")),
        hoverinfo="skip"
    ))
    
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-0.5, depth + 1.5]),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', paper_bgcolor='white', height=400, margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False
    )
    return fig

# ============================================
# ABAS DE NAVEGAÇÃO
# ============================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🌲 Eventos Sucessivos", 
    "⚖️ Eventos Complementares", 
    "➕ Regra da Soma", 
    "🔗 Condicional"
])

# ============================================
# ABA 1: EVENTOS SUCESSIVOS (ÁRVORE VISUAL)
# ============================================
with tab1:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(r"Eventos Sucessivos e Independentes")
    
    st.markdown("""
    <div class="concept-box">
    Quando eventos ocorrem em sequência e um não afeta o outro (como jogar a mesma moeda várias vezes), multiplicamos as probabilidades de cada ramo.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown("#### Configuração (Moedas)")
        moedas = st.slider("Quantos lançamentos consecutivos?", 1, 4, 3)
        total_resultados = 2**moedas
        
        st.markdown(f"**Cálculo do Espaço Amostral:**")
        st.latex(rf"\Omega = 2^{moedas} = {total_resultados} \text{{ resultados possíveis}}")
        
        st.markdown("**Probabilidade de cada ramo final:**")
        st.latex(rf"P = \left(\frac{{1}}{{2}}\right)^{moedas} = \frac{{1}}{{{total_resultados}}}")
        
    with col2:
        st.markdown("#### Diagrama de Árvore Dinâmico")
        # Mostrando a arvore perfeitamente calculada
        st.plotly_chart(build_tree_plotly(moedas), use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 2: EVENTOS COMPLEMENTARES (GRÁFICO ROSCA)
# ============================================
with tab2:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(r"Eventos Complementares: $P(A') = 1 - P(A)$")
    
    st.markdown("""
    <div class="concept-box">
    O evento complementar (não ocorrer A) é o resto do espaço amostral. Juntos, o evento e seu complemento sempre somam 100%.
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 1], gap="large")
    
    with col_c1:
        exemplo_comp = st.selectbox("Escolha um cenário:", ["Baralho de 52 Cartas", "Dado de 6 Faces"])
        
        if exemplo_comp == "Baralho de 52 Cartas":
            alvo = st.selectbox("Evento A (Quero extrair):", ["Sair Carta de Copas (♥)", "Sair uma Figura (J, Q, K)"])
            if alvo == "Sair Carta de Copas (♥)":
                p_a = 13 / 52
                label_a, label_ac = "Copas (13)", "Outros Naipes (39)"
            else:
                p_a = 12 / 52
                label_a, label_ac = "Figuras (12)", "Números/Ás (40)"
        else:
            alvo = st.selectbox("Evento A (Lançamento de Dado):", ["Sair Número Primo {2, 3, 5}", "Sair o Número 6"])
            if alvo == "Sair Número Primo {2, 3, 5}":
                p_a = 3 / 6
                label_a, label_ac = "Primos (3)", "Não Primos (3)"
            else:
                p_a = 1 / 6
                label_a, label_ac = "Sair 6 (1)", "Sair 1 a 5 (5)"
                
        p_comp = 1 - p_a
        
        st.latex(rf"P(A) = {p_a*100:.1f}\%")
        st.latex(rf"P(A') = 100\% - {p_a*100:.1f}\% = {p_comp*100:.1f}\%")

    with col_c2:
        # Gráfico Donut para ilustrar o complemento preenchendo o todo (100%)
        fig_pie = go.Figure(data=[go.Pie(
            labels=[label_a, label_ac], 
            values=[p_a, p_comp], 
            hole=.5,
            marker=dict(colors=['#3b82f6', '#cbd5e1']),
            textinfo='percent+label'
        )])
        fig_pie.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 3: SOMA DE PROBABILIDADES (HEATMAP)
# ============================================
with tab3:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(r"Regra da Soma: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$")
    
    st.markdown("""
    <div class="concept-box">
    Usada para calcular a chance de ocorrer o evento A <b>OU</b> o evento B. Descontamos a interseção (quando ocorrem juntos) para não contar o mesmo evento duas vezes.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🎲 Estudo de Caso Visual: Lançamento de 2 Dados")
    
    col_s1, col_s2 = st.columns([1, 1.5], gap="large")
    
    with col_s1:
        soma_alvo = st.slider("Selecione a SOMA que deseja obter nos 2 dados:", 2, 12, 7)
        
        # Lógica matemática
        matriz_somas = [[i+j for j in range(1,7)] for i in range(1,7)]
        casos_favoraveis = sum(1 for linha in matriz_somas for val in linha if val == soma_alvo)
        
        st.latex(rf"\text{{Espaço Amostral Total }} (\Omega) = 6 \times 6 = 36")
        st.latex(rf"\text{{Casos Favoráveis }} (Soma = {soma_alvo}) = {casos_favoraveis}")
        st.latex(rf"P(\text{{Soma }} {soma_alvo}) = \frac{{{casos_favoraveis}}}{{36}} \approx {(casos_favoraveis/36)*100:.1f}\%")
        
    with col_s2:
        # Gráfico Heatmap Interativo destacando os resultados!
        z_colors = [[1 if val == soma_alvo else 0 for val in linha] for linha in matriz_somas]
        text_vals = [[str(val) for val in linha] for linha in matriz_somas]
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=z_colors,
            x=["D2: 1", "D2: 2", "D2: 3", "D2: 4", "D2: 5", "D2: 6"],
            y=["D1: 1", "D1: 2", "D1: 3", "D1: 4", "D1: 5", "D1: 6"],
            text=text_vals,
            texttemplate="%{text}",
            colorscale=[[0, "#f1f5f9"], [1, "#3b82f6"]], # Fundo cinza, Destaque Azul
            showscale=False,
            hoverinfo="skip"
        ))
        
        fig_heat.update_layout(
            title=f"Mapa de todas as somas possíveis (Destaque em {soma_alvo})",
            height=350, margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ABA 4: PROBABILIDADE CONDICIONAL (GAUGE)
# ============================================
with tab4:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(r"Probabilidade Condicional: $P(A | B) = \frac{P(A \cap B)}{P(B)}$")
    
    st.markdown("""
    <div class="concept-box">
    A probabilidade condicional calcula a chance de A ocorrer <b>sabendo que</b> a condição B já aconteceu. Isso significa que nosso <b>espaço amostral encolheu</b>!
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([1.5, 1], gap="large")
    
    with col_p1:
        st.markdown("#### 🃏 Exemplo do Baralho: Atualizando a Informação")
        st.markdown("Imagine que você puxe uma carta às cegas e pergunte qual a chance de ser um **Rei (K)**.")
        
        prior = 4 / 52
        st.latex(rf"\text{{Cenário Inicial: }} P(\text{{Rei}}) = \frac{{4}}{{52}} = {prior*100:.1f}\%")
        
        st.markdown("Agora, alguém olha a carta e te dá uma dica: **\"A carta é uma FIGURA (J, Q, K)\"**.")
        st.markdown("Como isso altera a matemática?")
        
        st.latex(r"P(\text{Figura}) = \frac{12}{52} \text{ (Novo Espaço Amostral)}")
        st.latex(r"P(\text{Rei} \cap \text{Figura}) = \frac{4}{52} \text{ (Reis que são figuras)}")
        
        posterior = (4/52) / (12/52)
        st.latex(rf"\text{{Nova Probabilidade: }} P(\text{{Rei}} | \text{{Figura}}) = \frac{{4}}{{12}} = {posterior*100:.1f}\%")
        
    with col_p2:
        # Gráfico Gauge (Velocímetro) para mostrar o salto na probabilidade
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = posterior * 100,
            number = {'suffix': "%", 'font': {'size': 40}},
            title = {'text': "P(Rei | Figura)", 'font': {'size': 20}},
            delta = {'reference': prior * 100, 'position': "top", 'valueformat': ".1f", 'prefix': "Ganho de +"},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#10b981"},
                'bgcolor': "#f1f5f9",
                'borderwidth': 2,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, prior*100], 'color': '#3b82f6'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': posterior * 100
                }
            }
        ))
        
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.info("O gráfico acima mostra o 'salto' na probabilidade. Saber que é uma figura fez sua chance subir de ~7.7% para ~33.3%!")

    st.markdown('</div>', unsafe_allow_html=True)
