import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Desempenho Escolar no Brasil",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .kpi-box {
        background-color: #f0f5fb;
        border-left: 5px solid #2e6da4;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 8px;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1a3a5c; }
    .kpi-label { font-size: 13px; color: #5a6a7a; margin-top: 2px; }
    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #1a3a5c;
        border-bottom: 2px solid #dce4ed; padding-bottom: 6px; margin-bottom: 16px;
    }
    .interpretacao {
        background-color: #f8f9fa;
        border-left: 4px solid #27ae60;
        border-radius: 6px;
        padding: 14px 18px;
        font-size: 14px;
        color: #2d2d2d;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados/simulacao_desempenho_escolar_brasil.csv")
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['periodo'] = df['ano'].astype(str) + '/S' + df['semestre'].astype(str)
    df['faixa_renda'] = pd.cut(
        df['renda_media_familiar'],
        bins=[0, 2000, 3000, 4500, 10000],
        labels=['Baixa', 'Média-baixa', 'Média-alta', 'Alta']
    )
    return df

df = carregar_dados()


# ─────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=64)
    st.title("Filtros")
    st.markdown("---")

    anos = sorted(df['ano'].unique())
    ano_range = st.slider(
        "Período (Ano)",
        min_value=int(min(anos)),
        max_value=int(max(anos)),
        value=(int(min(anos)), int(max(anos)))
    )

    semestres = st.multiselect(
        "Semestre",
        options=sorted(df['semestre'].unique()),
        default=sorted(df['semestre'].unique()),
        format_func=lambda x: f"{x}º Semestre"
    )

    regioes = st.multiselect(
        "Região",
        options=sorted(df['regiao'].unique()),
        default=sorted(df['regiao'].unique())
    )

    ufs_disponiveis = sorted(df[df['regiao'].isin(regioes)]['uf'].unique())
    ufs = st.multiselect(
        "Estado (UF)",
        options=ufs_disponiveis,
        default=ufs_disponiveis
    )

    redes = st.multiselect(
        "Rede de Ensino",
        options=sorted(df['rede_ensino'].unique()),
        default=sorted(df['rede_ensino'].unique())
    )

    disciplinas = st.multiselect(
        "Disciplina",
        options=sorted(df['disciplina'].unique()),
        default=sorted(df['disciplina'].unique())
    )

    niveis = st.multiselect(
        "Nível de Desempenho",
        options=['Baixo', 'Médio', 'Alto', 'Excelente'],
        default=['Baixo', 'Médio', 'Alto', 'Excelente']
    )

    st.markdown("---")
    st.caption("Projeto G2 · Tema 24\nDesempenho Escolar no Brasil")


# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df_f = df[
    (df['ano'] >= ano_range[0]) &
    (df['ano'] <= ano_range[1]) &
    (df['semestre'].isin(semestres)) &
    (df['regiao'].isin(regioes)) &
    (df['uf'].isin(ufs)) &
    (df['rede_ensino'].isin(redes)) &
    (df['disciplina'].isin(disciplinas)) &
    (df['nivel_desempenho'].isin(niveis))
].copy()

if df_f.empty:
    st.error("⚠️ Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros.")
    st.stop()


# ─────────────────────────────────────────────
# NAVEGAÇÃO POR PÁGINAS
# ─────────────────────────────────────────────
paginas = [
    "🏠 Visão Geral",
    "📈 Evolução Temporal",
    "🗺️ Análise Regional",
    "📚 Por Disciplina",
    "🔬 Correlações",
    "📋 Dados"
]
pagina = st.sidebar.radio("Página", paginas)


# ══════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ══════════════════════════════════════════════
if pagina == "🏠 Visão Geral":

    st.title("📚 Desempenho Escolar no Brasil")
    st.markdown(
        "Análise de indicadores educacionais de **2015 a 2024** com base em dados de regiões, "
        "estados, redes de ensino e disciplinas do Brasil."
    )
    st.markdown("---")

    # KPIs
    st.markdown('<p class="section-title">📊 Indicadores-Chave (KPIs)</p>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    media_notas   = df_f['media_notas'].mean()
    taxa_aprov    = df_f['taxa_aprovacao'].mean()
    taxa_reprov   = df_f['taxa_reprovacao'].mean()
    idx_desemp    = df_f['indice_desempenho'].mean()
    melhor_uf     = df_f.groupby('uf')['media_notas'].mean().idxmax()
    pior_disc     = df_f.groupby('disciplina')['media_notas'].mean().idxmin()

    with c1:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{media_notas:.1f}</div>
            <div class="kpi-label">Média Geral das Notas</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{taxa_aprov:.1f}%</div>
            <div class="kpi-label">Taxa Média de Aprovação</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{taxa_reprov:.1f}%</div>
            <div class="kpi-label">Taxa Média de Reprovação</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{idx_desemp:.1f}</div>
            <div class="kpi-label">Índice Médio de Desempenho</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{melhor_uf}</div>
            <div class="kpi-label">Estado com Melhor Desempenho</div></div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-value">{pior_disc}</div>
            <div class="kpi-label">Disciplina Mais Crítica</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Gráficos resumo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Desempenho por Rede de Ensino</p>', unsafe_allow_html=True)
        por_rede = df_f.groupby('rede_ensino')[['media_notas', 'taxa_aprovacao', 'indice_desempenho']].mean().reset_index()
        fig_rede = px.bar(
            por_rede.melt(id_vars='rede_ensino', var_name='Indicador', value_name='Valor'),
            x='Indicador', y='Valor', color='rede_ensino', barmode='group',
            color_discrete_map={'Pública': '#2e6da4', 'Privada': '#e67e22'},
            labels={'rede_ensino': 'Rede', 'Valor': 'Valor', 'Indicador': 'Indicador'},
            text_auto='.1f'
        )
        fig_rede.update_layout(height=350, legend_title='Rede', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rede, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Distribuição dos Níveis de Desempenho</p>', unsafe_allow_html=True)
        nivel_counts = df_f['nivel_desempenho'].value_counts().reset_index()
        nivel_counts.columns = ['nivel', 'contagem']
        cores_nivel = {'Baixo': '#e74c3c', 'Médio': '#f39c12', 'Alto': '#3498db', 'Excelente': '#2ecc71'}
        fig_nivel = px.pie(
            nivel_counts, names='nivel', values='contagem',
            color='nivel', color_discrete_map=cores_nivel,
            hole=0.4
        )
        fig_nivel.update_layout(height=350)
        st.plotly_chart(fig_nivel, use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Desempenho por Região</p>', unsafe_allow_html=True)
    por_regiao = df_f.groupby('regiao')['media_notas'].mean().reset_index().sort_values('media_notas', ascending=False)
    fig_reg = px.bar(
        por_regiao, x='regiao', y='media_notas',
        color='media_notas', color_continuous_scale='Blues',
        labels={'regiao': 'Região', 'media_notas': 'Média das Notas'},
        text_auto='.1f'
    )
    fig_reg.update_layout(height=350, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_reg, use_container_width=True)

    st.markdown('<div class="interpretacao">💡 <strong>Interpretação:</strong> '
        'A análise da visão geral revela que o desempenho escolar nacional é moderado, '
        'com média de notas próxima a 65. A distribuição dos níveis de desempenho mostra '
        'uma presença significativa de estudantes nos níveis Baixo e Médio, sinalizando '
        'oportunidades de melhoria no sistema educacional brasileiro.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 2 — EVOLUÇÃO TEMPORAL
# ══════════════════════════════════════════════
elif pagina == "📈 Evolução Temporal":

    st.title("📈 Evolução Temporal do Desempenho")
    st.markdown("Acompanhe como os indicadores educacionais evoluíram ao longo dos anos e semestres.")
    st.markdown("---")

    evolucao = df_f.groupby('ano')[['media_notas', 'taxa_aprovacao', 'taxa_reprovacao', 'indice_desempenho']].mean().reset_index()

    # Linha temporal principal
    st.markdown('<p class="section-title">Evolução da Média das Notas (2015–2024)</p>', unsafe_allow_html=True)
    fig_linha = px.line(
        evolucao, x='ano', y='media_notas',
        markers=True, line_shape='spline',
        labels={'ano': 'Ano', 'media_notas': 'Média das Notas'},
        color_discrete_sequence=['#2e6da4']
    )
    fig_linha.update_traces(line_width=3, marker_size=8)
    fig_linha.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)')
    fig_linha.update_xaxes(tickmode='linear', dtick=1)
    st.plotly_chart(fig_linha, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Aprovação e Reprovação ao Longo do Tempo</p>', unsafe_allow_html=True)
        fig_aprov = go.Figure()
        fig_aprov.add_trace(go.Scatter(
            x=evolucao['ano'], y=evolucao['taxa_aprovacao'],
            name='Aprovação', mode='lines+markers',
            line=dict(color='#27ae60', width=2.5),
            fill='tozeroy', fillcolor='rgba(39,174,96,0.1)'
        ))
        fig_aprov.add_trace(go.Scatter(
            x=evolucao['ano'], y=evolucao['taxa_reprovacao'],
            name='Reprovação', mode='lines+markers',
            line=dict(color='#e74c3c', width=2.5),
            fill='tozeroy', fillcolor='rgba(231,76,60,0.1)'
        ))
        fig_aprov.update_layout(
            height=320, plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', dtick=1),
            yaxis_title='Percentual (%)'
        )
        st.plotly_chart(fig_aprov, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Evolução por Rede de Ensino</p>', unsafe_allow_html=True)
        evo_rede = df_f.groupby(['ano', 'rede_ensino'])['media_notas'].mean().reset_index()
        fig_rede_t = px.line(
            evo_rede, x='ano', y='media_notas', color='rede_ensino',
            markers=True, line_shape='spline',
            color_discrete_map={'Pública': '#2e6da4', 'Privada': '#e67e22'},
            labels={'ano': 'Ano', 'media_notas': 'Média das Notas', 'rede_ensino': 'Rede'}
        )
        fig_rede_t.update_traces(line_width=2.5, marker_size=7)
        fig_rede_t.update_layout(
            height=320, plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', dtick=1)
        )
        st.plotly_chart(fig_rede_t, use_container_width=True)

    # Heatmap semestral
    st.markdown('<p class="section-title">Heatmap — Média das Notas por Região e Período</p>', unsafe_allow_html=True)
    pivot = df_f.pivot_table(index='regiao', columns='periodo', values='media_notas', aggfunc='mean')
    cols_ord = sorted(pivot.columns, key=lambda x: (int(x.split('/S')[0]), int(x.split('/S')[1])))
    pivot = pivot[cols_ord]

    fig_heat = px.imshow(
        pivot.round(1), text_auto=True,
        color_continuous_scale='YlOrRd',
        labels=dict(x='Período', y='Região', color='Média'),
        aspect='auto'
    )
    fig_heat.update_layout(height=350)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="interpretacao">💡 <strong>Interpretação:</strong> '
        'A análise temporal mostra a trajetória do desempenho escolar ao longo de uma década. '
        'O heatmap permite identificar períodos e regiões com desempenho mais alto (tons escuros) '
        'ou mais baixo (tons claros), facilitando a detecção de padrões sazonais e tendências '
        'regionais.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 3 — ANÁLISE REGIONAL
# ══════════════════════════════════════════════
elif pagina == "🗺️ Análise Regional":

    st.title("🗺️ Análise Regional e por Estado")
    st.markdown("Compare o desempenho entre as diferentes regiões e estados brasileiros.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Média das Notas por Região</p>', unsafe_allow_html=True)
        por_reg = df_f.groupby('regiao')[['media_notas', 'taxa_aprovacao', 'indice_desempenho']].mean().reset_index()
        por_reg = por_reg.sort_values('media_notas', ascending=True)
        fig_reg = px.bar(
            por_reg, x='media_notas', y='regiao', orientation='h',
            color='media_notas', color_continuous_scale='Blues',
            labels={'media_notas': 'Média das Notas', 'regiao': 'Região'},
            text_auto='.1f'
        )
        fig_reg.update_layout(height=320, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_reg, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Taxa de Aprovação por Região</p>', unsafe_allow_html=True)
        fig_aprov_reg = px.bar(
            por_reg.sort_values('taxa_aprovacao', ascending=True),
            x='taxa_aprovacao', y='regiao', orientation='h',
            color='taxa_aprovacao', color_continuous_scale='Greens',
            labels={'taxa_aprovacao': 'Taxa de Aprovação (%)', 'regiao': 'Região'},
            text_auto='.1f'
        )
        fig_aprov_reg.update_layout(height=320, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_aprov_reg, use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Ranking de Estados por Média das Notas</p>', unsafe_allow_html=True)
    por_uf = df_f.groupby(['uf', 'regiao'])['media_notas'].mean().reset_index().sort_values('media_notas', ascending=True)
    media_nac = por_uf['media_notas'].mean()
    por_uf['acima_media'] = por_uf['media_notas'] >= media_nac

    fig_uf = px.bar(
        por_uf, x='media_notas', y='uf', orientation='h',
        color='acima_media',
        color_discrete_map={True: '#2e6da4', False: '#e74c3c'},
        labels={'media_notas': 'Média das Notas', 'uf': 'Estado', 'acima_media': 'Acima da média'},
        text_auto='.1f',
        hover_data=['regiao']
    )
    fig_uf.add_vline(x=media_nac, line_dash='dash', line_color='gray',
                     annotation_text=f'Média nacional: {media_nac:.1f}')
    fig_uf.update_layout(height=700, plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig_uf, use_container_width=True)

    st.markdown('<div class="interpretacao">💡 <strong>Interpretação:</strong> '
        'O mapa regional evidencia as desigualdades educacionais entre os estados brasileiros. '
        'Barras em <strong style="color:#2e6da4">azul</strong> indicam estados acima da média nacional, '
        'enquanto barras em <strong style="color:#e74c3c">vermelho</strong> indicam estados abaixo. '
        'Políticas públicas focadas nos estados com menor desempenho podem contribuir para reduzir '
        'essas disparidades.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 4 — POR DISCIPLINA
# ══════════════════════════════════════════════
elif pagina == "📚 Por Disciplina":

    st.title("📚 Análise por Disciplina")
    st.markdown("Explore o desempenho por área do conhecimento e identifique as disciplinas mais críticas.")
    st.markdown("---")

    por_disc = df_f.groupby('disciplina')[['media_notas', 'taxa_aprovacao', 'taxa_reprovacao']].mean().reset_index()
    por_disc = por_disc.sort_values('media_notas', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Média das Notas por Disciplina</p>', unsafe_allow_html=True)
        fig_disc = px.bar(
            por_disc, x='disciplina', y='media_notas',
            color='media_notas', color_continuous_scale='Blues',
            labels={'disciplina': 'Disciplina', 'media_notas': 'Média das Notas'},
            text_auto='.1f'
        )
        fig_disc.update_layout(height=350, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_disc, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Taxa de Aprovação e Reprovação</p>', unsafe_allow_html=True)
        disc_melt = por_disc.melt(id_vars='disciplina',
                                   value_vars=['taxa_aprovacao', 'taxa_reprovacao'],
                                   var_name='Indicador', value_name='Percentual')
        disc_melt['Indicador'] = disc_melt['Indicador'].map({
            'taxa_aprovacao': 'Aprovação', 'taxa_reprovacao': 'Reprovação'
        })
        fig_apr = px.bar(
            disc_melt, x='disciplina', y='Percentual', color='Indicador', barmode='group',
            color_discrete_map={'Aprovação': '#27ae60', 'Reprovação': '#e74c3c'},
            labels={'disciplina': 'Disciplina', 'Percentual': 'Percentual (%)'},
            text_auto='.1f'
        )
        fig_apr.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_apr, use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Evolução das Notas por Disciplina ao Longo do Tempo</p>', unsafe_allow_html=True)
    disc_tempo = df_f.groupby(['ano', 'disciplina'])['media_notas'].mean().reset_index()
    fig_disc_t = px.line(
        disc_tempo, x='ano', y='media_notas', color='disciplina',
        markers=True, line_shape='spline',
        labels={'ano': 'Ano', 'media_notas': 'Média das Notas', 'disciplina': 'Disciplina'}
    )
    fig_disc_t.update_traces(line_width=2, marker_size=6)
    fig_disc_t.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(tickmode='linear', dtick=1))
    st.plotly_chart(fig_disc_t, use_container_width=True)

    st.markdown('<p class="section-title">Desempenho por Disciplina e Rede de Ensino</p>', unsafe_allow_html=True)
    disc_rede = df_f.groupby(['disciplina', 'rede_ensino'])['media_notas'].mean().reset_index()
    fig_dr = px.bar(
        disc_rede, x='disciplina', y='media_notas', color='rede_ensino',
        barmode='group',
        color_discrete_map={'Pública': '#2e6da4', 'Privada': '#e67e22'},
        labels={'disciplina': 'Disciplina', 'media_notas': 'Média das Notas', 'rede_ensino': 'Rede'},
        text_auto='.1f'
    )
    fig_dr.update_layout(height=350, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dr, use_container_width=True)

    st.markdown('<div class="interpretacao">💡 <strong>Interpretação:</strong> '
        'Português apresenta o menor rendimento médio entre todas as disciplinas, '
        'o que sugere a necessidade de atenção especial ao ensino de Língua Portuguesa. '
        'A análise por rede de ensino permite verificar se essa dificuldade é generalizada '
        'ou concentrada em algum tipo de escola.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 5 — CORRELAÇÕES
# ══════════════════════════════════════════════
elif pagina == "🔬 Correlações":

    st.title("🔬 Análise de Correlações e Fatores")
    st.markdown("Investigue a relação entre fatores socioeconômicos e o desempenho escolar.")
    st.markdown("---")

    # Correlações estatísticas
    corr_renda = df_f[['renda_media_familiar', 'media_notas']].corr().iloc[0, 1]
    corr_inet  = df_f[['acesso_internet', 'media_notas']].corr().iloc[0, 1]
    corr_idxr  = df_f[['renda_media_familiar', 'indice_desempenho']].corr().iloc[0, 1]
    corr_idxi  = df_f[['acesso_internet', 'indice_desempenho']].corr().iloc[0, 1]

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val in [
        (c1, "Corr. Renda x Notas", corr_renda),
        (c2, "Corr. Internet x Notas", corr_inet),
        (c3, "Corr. Renda x Índice", corr_idxr),
        (c4, "Corr. Internet x Índice", corr_idxi),
    ]:
        cor_val = "#27ae60" if abs(val) > 0.3 else "#e67e22" if abs(val) > 0.1 else "#95a5a6"
        with col:
            st.markdown(f"""<div class="kpi-box">
                <div class="kpi-value" style="color:{cor_val};font-size:1.6rem">{val:.4f}</div>
                <div class="kpi-label">{label}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Renda Familiar × Média das Notas</p>', unsafe_allow_html=True)
        fig_renda = px.scatter(
            df_f, x='renda_media_familiar', y='media_notas',
            color='regiao', opacity=0.5,
            trendline='ols', trendline_scope='overall',
            labels={'renda_media_familiar': 'Renda Familiar (R$)', 'media_notas': 'Média das Notas', 'regiao': 'Região'},
        )
        fig_renda.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_renda, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Acesso à Internet × Média das Notas</p>', unsafe_allow_html=True)
        fig_inet = px.scatter(
            df_f, x='acesso_internet', y='media_notas',
            color='regiao', opacity=0.5,
            trendline='ols', trendline_scope='overall',
            labels={'acesso_internet': 'Acesso à Internet (%)', 'media_notas': 'Média das Notas', 'regiao': 'Região'},
        )
        fig_inet.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_inet, use_container_width=True)

    # Matriz de correlação
    st.markdown("---")
    st.markdown('<p class="section-title">Matriz de Correlação — Variáveis Numéricas</p>', unsafe_allow_html=True)
    num_cols = ['media_notas', 'taxa_aprovacao', 'taxa_reprovacao',
                'acesso_internet', 'renda_media_familiar', 'indice_desempenho']
    corr_matrix = df_f[num_cols].corr().round(3)

    fig_corr = px.imshow(
        corr_matrix, text_auto=True,
        color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
        labels=dict(color='Correlação')
    )
    fig_corr.update_layout(height=450)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown('<div class="interpretacao">💡 <strong>Interpretação:</strong> '
        'As correlações entre renda familiar, acesso à internet e desempenho são próximas de zero '
        'neste dataset, indicando ausência de relação linear direta. Isso não significa que esses '
        'fatores não importam, mas que seu efeito pode ser não-linear ou mediado por outras variáveis '
        'não capturadas aqui. A matriz completa permite identificar quais pares de variáveis apresentam '
        'associações mais fortes.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 6 — DADOS
# ══════════════════════════════════════════════
elif pagina == "📋 Dados":

    st.title("📋 Tabela de Dados")
    st.markdown("Explore os dados brutos com os filtros selecionados.")
    st.markdown("---")

    # Resumo
    c1, c2, c3 = st.columns(3)
    c1.metric("Registros filtrados", f"{len(df_f):,}")
    c2.metric("Total de registros", f"{len(df):,}")
    c3.metric("% dos dados", f"{len(df_f)/len(df)*100:.1f}%")

    st.markdown("---")

    # Tabela dinâmica
    st.markdown('<p class="section-title">Tabela Dinâmica — Média por Grupo</p>', unsafe_allow_html=True)
    grupo = st.selectbox("Agrupar por", ['regiao', 'uf', 'rede_ensino', 'disciplina', 'nivel_desempenho', 'ano'])
    tabela = df_f.groupby(grupo).agg(
        Registros=('media_notas', 'count'),
        Média_Notas=('media_notas', 'mean'),
        Taxa_Aprovação=('taxa_aprovacao', 'mean'),
        Taxa_Reprovação=('taxa_reprovacao', 'mean'),
        Índice_Desempenho=('indice_desempenho', 'mean'),
        Renda_Média=('renda_media_familiar', 'mean'),
    ).round(2).reset_index()
    st.dataframe(tabela, use_container_width=True)

    st.markdown("---")
    st.markdown('<p class="section-title">Dados Brutos</p>', unsafe_allow_html=True)
    st.dataframe(df_f.reset_index(drop=True), use_container_width=True, height=400)

    # Download
    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Baixar dados filtrados (CSV)",
        data=csv,
        file_name="desempenho_escolar_filtrado.csv",
        mime='text/csv'
    )

    st.markdown("---")
    st.markdown("### 📌 Conclusão Executiva")
    st.markdown("""
    Com base na análise completa dos dados educacionais brasileiros de 2015 a 2024:

    - 📊 A **média nacional de notas** é de **64,97**, indicando desempenho moderado.
    - ✅ A **taxa de aprovação média** é **77,42%**, mas ainda há 1 em cada 4 alunos com dificuldade de aprovação.
    - 🏆 O estado de **Mato Grosso (MT)** lidera o ranking de desempenho.
    - 📖 **Português** é a disciplina com menor rendimento e merece atenção especial.
    - 🌍 Há **desigualdades regionais relevantes** que exigem políticas públicas diferenciadas.
    - 💡 O impacto da **renda e do acesso à internet** sobre o desempenho não é linear, mas continua sendo um fator estrutural importante a ser monitorado.
    """)
