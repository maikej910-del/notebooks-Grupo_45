import streamlit as st
import joblib
import pandas as pd
import io
import altair as alt

st.set_page_config(page_title="Diagnóstico de Peso Corporal", layout="wide")

# Inserção do Logo ao lado do Título
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    st.image("https://raw.githubusercontent.com/maikej910-del/notebooks-Grupo_45/main/logo.jpeg", width=120)
with col_titulo:
    st.title("🔬 Sistema Clínico para Diagnóstico de Peso Corporal")

model = joblib.load('modelo_obesidade_rf.pkl')

nome_paciente = st.text_input("Nome Completo do Paciente", placeholder="Digite aqui...")

col1, col2, col3 = st.columns(3)

with col1:
    genero = st.selectbox("Gênero", ["", "Masculino", "Feminino"], index=0)
    idade = st.number_input("Idade", min_value=0, max_value=120, value=None, placeholder="Ex: 25")
    altura = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, value=None, step=0.01, placeholder="Ex: 1.75")
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=300.0, value=None, step=0.1, placeholder="Ex: 70.5")
    familia = st.selectbox("Histórico Familiar de Obesidade?", ["", "Sim", "Nao"], index=0)
    transporte = st.selectbox("Meio de transporte habitual", ["", "Carro", "Moto", "Bicicleta", "Transporte Publico", "A pe"], index=0)

with col2:
    calorico = st.selectbox("Consumo frequente de alimentos calóricos?", ["", "Sim", "Nao"], index=0)
    vegetais = st.selectbox("Frequência de consumo de vegetais", ["", "Raramente", "As vezes", "Sempre"], index=0)
    refeicoes = st.selectbox("Quantidade de refeições por dia", ["", "1 refeicao", "2 refeicoes", "3 refeicoes", "4 ou mais"], index=0)
    lanches = st.selectbox("Consumo de alimentos entre as refeições", ["", "Nao", "As vezes", "Frequentemente", "Sempre"], index=0)
    agua = st.selectbox("Consumo diário de água", ["", "< 1 L/dia", "1-2 L/dia", "> 2 L/dia"], index=0)

with col3:
    fumante = st.selectbox("Possui hábito de fumar?", ["", "Sim", "Nao"], index=0)
    monitora_cal = st.selectbox("Monitora a ingestão de calorias?", ["", "Sim", "Nao"], index=0)
    ativ_fisica = st.selectbox("Frequência de atividade física", ["", "Nenhuma", "1-2 dias/sem", "3-4 dias/sem", "5+ dias/sem"], index=0)
    telas = st.selectbox("Tempo diário em dispositivos com tela", ["", "0-2 h/dia", "3-5 h/dia", "> 5 h/dia"], index=0)
    alcool = st.selectbox("Consumo de bebidas alcoólicas", ["", "Nao", "As vezes", "Frequentemente", "Sempre"], index=0)

st.markdown("---")

if st.button("Gerar Diagnóstico"):
    if not nome_paciente or not genero or not idade or not altura or not peso or not familia or not transporte:
        st.warning("Aviso: Por favor, preencha todos os campos obrigatórios do formulário.")
    else:
        imc = round(peso / (altura ** 2), 2)

        veg_map = {"Raramente": 1, "As vezes": 2, "Sempre": 3}
        ref_map = {"1 refeicao": 1, "2 refeicoes": 2, "3 refeicoes": 3, "4 ou mais": 4}
        h2o_map = {"< 1 L/dia": 1, "1-2 L/dia": 2, "> 2 L/dia": 3}
        atv_map = {"Nenhuma": 0, "1-2 dias/sem": 1, "3-4 dias/sem": 2, "5+ dias/sem": 3}
        tel_map = {"0-2 h/dia": 0, "3-5 h/dia": 1, "> 5 h/dia": 2}

        score_atv = float(atv_map.get(ativ_fisica, 0) * tel_map.get(telas, 0))

        # Envio dos dados SEM Peso, Altura e IMC para o modelo, focando apenas nos hábitos
        dados = pd.DataFrame([{
            'Genero': genero, 'Idade': float(idade), 'Altura': float(altura), 'Historico_Familiar': familia,
            'Consumo_Alta_Caloria': calorico, 'Consumo_Vegetais': veg_map.get(vegetais, 2),
            'Refeicoes_Dia': ref_map.get(refeicoes, 3), 'Consumo_Entre_Refeicoes': lanches,
            'Fumante': fumante, 'Consumo_Agua': h2o_map.get(agua, 2),
            'Monitora_Calorias': monitora_cal, 'Frequencia_Ativ_Fisica': atv_map.get(ativ_fisica, 0),
            'Tempo_Telas': tel_map.get(telas, 0), 'Consumo_Alcool': alcool,
            'Meio_Transporte': transporte, 'Score_Atividade': score_atv
        }])

        # Obter classe final e as probabilidades
        resultado = model.predict(dados)[0]
        probabilidades = model.predict_proba(dados)[0]
        classes = model.classes_
        confianca = max(probabilidades) * 100

        st.markdown("### 📋 Resultado do Diagnóstico")

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.success(f"**Paciente:** {nome_paciente}  |  **Diagnóstico:** {resultado}")
            st.info(f"**Grau de Confiança do Modelo:** {confianca:.2f}%")

        with col_res2:
            st.markdown("**Indicadores Corporais Base:**")
            st.write(f"- **Peso Registrado:** {peso} kg")
            st.write(f"- **Altura Registrada:** {altura} m")
            st.write(f"- **IMC Calculado:** {imc}")

        st.markdown("#### 📊 Distribuição das Probabilidades por Classe")

        # Criação de DataFrame para o gráfico interativo
        df_probs = pd.DataFrame({'Classe': classes, 'Probabilidade (%)': probabilidades * 100})
        ordem = ['Abaixo do peso', 'Peso normal', 'Sobrepeso I', 'Sobrepeso II', 'Obesidade I', 'Obesidade II', 'Obesidade III']
        df_probs['Classe'] = pd.Categorical(df_probs['Classe'], categories=ordem, ordered=True)
        df_probs = df_probs.sort_values('Classe')

        chart = alt.Chart(df_probs).mark_bar(color='#1D5E4D', cornerRadiusEnd=4).encode(
            x=alt.X('Probabilidade (%):Q', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('Classe:N', sort=ordem, axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip('Classe', title='Diagnóstico'), alt.Tooltip('Probabilidade (%)', format='.1f')]
        ).properties(height=250)

        st.altair_chart(chart, use_container_width=True)

        # Preparação do Export (Retornando o peso, altura e imc visuais para o relatório do médico)
        df_export = dados.copy()
        df_export.insert(0, 'Nome_Paciente', nome_paciente)
        df_export.insert(3, 'Altura', altura)
        df_export.insert(4, 'Peso', peso)
        df_export.insert(5, 'IMC', imc)
        df_export['Resultado_Diagnostico'] = resultado
        df_export['Confianca_Modelo_%'] = round(confianca, 2)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Diagnostico')

        st.download_button(
            label="📥 Exportar Relatório da Avaliação (Excel)",
            data=output.getvalue(),
            file_name=f"diagnostico_{nome_paciente.lower().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
