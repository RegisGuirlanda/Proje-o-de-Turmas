import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Projeção de Turmas", layout="wide")
st.title("📈 Projeção de Turmas por Turno e Ano Letivo")

anos_letivos = [2025, 2026]
turnos = ["Integral", "Manhã", "Tarde", "Noite"]
series = ["1º EF", "2º EF", "3º EF", "4º EF", "5º EF",
           "6º EF", "7º EF", "8º EF", "9º EF",
           "1º EM", "2º EM", "3º EM"]

# Entrada de filtros
st.sidebar.header("Filtros")
sre = st.sidebar.text_input("SRE")
municipio = st.sidebar.text_input("Município")
escola = st.sidebar.text_input("Escola")

st.write("Preencha a quantidade de turmas por série e turno para cada ano letivo.")

data = []

for ano in anos_letivos:
    st.subheader(f"Ano Letivo: {ano}")
    for serie in series:
        with st.expander(serie):
            linha = {
                "Ano Letivo": ano,
                "Série": serie,
                "SRE": sre,
                "Município": municipio,
                "Escola": escola
            }
            total = 0
            for turno in turnos:
                valor = st.number_input(
                    f"{turno} - {serie} ({ano})",
                    min_value=0,
                    max_value=40,
                    step=1,
                    key=f"{ano}_{serie}_{turno}"
                )
                linha[turno] = valor
                total += valor
            linha["Total"] = total
            if total == 0:
                st.warning(f"Atenção: Nenhuma turma inserida para {serie} ({ano})")
            data.append(linha)

# Mostrar dataframe com resultado
resultado_df = pd.DataFrame(data)

st.markdown("---")
st.subheader(":bar_chart: Resultado da Projeção")
st.dataframe(resultado_df, use_container_width=True)

# Gráficos
st.subheader(":chart_with_upwards_trend: Visualização Gráfica")

# Gráfico de barras
grafico_barras = resultado_df.melt(
    id_vars=["Ano Letivo", "Série"],
    value_vars=turnos,
    var_name="Turno",
    value_name="Turmas"
)
grafico1 = px.bar(grafico_barras, x="Série", y="Turmas", color="Turno", barmode="group", facet_col="Ano Letivo")
st.plotly_chart(grafico1, use_container_width=True)

# Gráfico de pizza por turno
total_por_turno = grafico_barras.groupby("Turno")["Turmas"].sum().reset_index()
grafico2 = px.pie(total_por_turno, names="Turno", values="Turmas", title="Distribuição Total por Turno")
st.plotly_chart(grafico2, use_container_width=True)

# Exportar para Excel
st.markdown("### 🗎 Exportar")

@st.cache_data
def gerar_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Projecao')
        writer.save()
    output.seek(0)
    return output

excel_data = gerar_excel(resultado_df)
st.download_button(
    label="📄 Baixar como Excel",
    data=excel_data,
    file_name="projecao_turmas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Upload de dados existentes
st.markdown("### 📂 Importar dados existentes")
arquivo = st.file_uploader("Carregar planilha Excel com dados de projeção")
if arquivo:
    df_importado = pd.read_excel(arquivo)
    st.dataframe(df_importado, use_container_width=True)
