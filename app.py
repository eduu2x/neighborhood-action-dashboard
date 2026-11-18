from html import escape

import streamlit as st

from dados_simulados import ocorrencias_simuladas
from modulo_logico import avaliar_ocorrencia

COR_CRITICA = "#D32F2F"
COR_ALERTA = "#FBC02D"
COR_COMUM = "#9E9E9E"

ESTILO_ETIQUETA = (
    "padding:4px 10px;border-radius:12px;font-size:0.72rem;"
    "font-weight:700;letter-spacing:0.3px;white-space:nowrap;"
)

ESTILO_PINO = (
    "display:inline-block;background:white;border:1px solid rgb(207,207,207);"
    "border-radius:6px;padding:4px 9px;font-size:0.82rem;color:rgb(51,51,51);"
    "margin:3px 6px 3px 0;"
)

st.set_page_config(page_title="Painel de Acao no Bairro", layout="wide")


def avaliar_lista(lista):
    # avaliar lista
    avaliadas = []
    for ocorrencia in lista:
        resultado = avaliar_ocorrencia(
            ocorrencia["risco_imediato"],
            ocorrencia["prazo_excedido"],
            ocorrencia["reincidencia_registrada"],
        )
        item = dict(ocorrencia)
        item["alerta_prioridade"] = resultado["alerta_prioridade"]
        item["pendencia_critica"] = resultado["pendencia_critica"]
        item["status_visual_dashboard"] = resultado["status_visual_dashboard"]
        avaliadas.append(item)
    return avaliadas


def ordem_visual(ocorrencia):
    # ordenar fila
    if ocorrencia["pendencia_critica"] == 1:
        return 0
    if ocorrencia["alerta_prioridade"] == 1:
        return 1
    return 2


def criar_cartao(ocorrencia):
    # monta cartao
    etiqueta_s2 = (
        f'<span style="background:{COR_CRITICA};color:white;{ESTILO_ETIQUETA}">'
        "PENDENCIA CRITICA</span>"
    )
    etiqueta_s1 = (
        f'<span style="background:{COR_ALERTA};color:rgb(33,33,33);{ESTILO_ETIQUETA}">'
        "ALERTA DE PRIORIDADE</span>"
    )
    etiqueta_comum = (
        f'<span style="background:rgb(224,224,224);color:rgb(66,66,66);{ESTILO_ETIQUETA}">'
        "FILA COMUM</span>"
    )

    if ocorrencia["pendencia_critica"] == 1:
        cor = COR_CRITICA
        fundo = "rgb(253,236,234)"
        etiquetas = etiqueta_s2 + etiqueta_s1
    elif ocorrencia["alerta_prioridade"] == 1:
        cor = COR_ALERTA
        fundo = "rgb(255,248,225)"
        etiquetas = etiqueta_s1
    else:
        cor = COR_COMUM
        fundo = "rgb(245,245,245)"
        etiquetas = etiqueta_comum

    identificador = escape(ocorrencia["id"])
    titulo = escape(ocorrencia["titulo"])
    local = escape(ocorrencia["local"])
    pino_a = ocorrencia["risco_imediato"]
    pino_b = ocorrencia["prazo_excedido"]
    pino_c = ocorrencia["reincidencia_registrada"]
    valor_pino_a = "Sim" if pino_a == 1 else "Nao"
    valor_pino_b = "Sim" if pino_b == 1 else "Nao"
    valor_pino_c = "Sim" if pino_c == 1 else "Nao"

    cartao = (
        f'<div style="background:{fundo};border-left:8px solid {cor};'
        "border-radius:10px;padding:16px 20px;margin-bottom:14px;"
        'box-shadow:0 2px 6px rgba(0,0,0,0.10);">'
        '<div style="display:flex;justify-content:space-between;'
        'align-items:flex-start;gap:16px;flex-wrap:wrap;">'
        "<div>"
        f'<div style="font-size:0.75rem;color:rgb(102,102,102);font-weight:700;">{identificador}</div>'
        f'<div style="font-size:1.12rem;color:rgb(31,31,31);font-weight:700;margin-top:2px;">{titulo}</div>'
        f'<div style="font-size:0.88rem;color:rgb(95,95,95);margin-top:3px;">{local}</div>'
        "</div>"
        '<div style="display:flex;flex-direction:column;gap:6px;align-items:flex-end;">'
        f"{etiquetas}"
        "</div>"
        "</div>"
        '<div style="margin-top:12px;">'
        f'<span style="{ESTILO_PINO}"><strong>Risco Imediato:</strong> {valor_pino_a}</span>'
        f'<span style="{ESTILO_PINO}"><strong>Prazo Excedido:</strong> {valor_pino_b}</span>'
        f'<span style="{ESTILO_PINO}"><strong>Reincidencia Registrada:</strong> {valor_pino_c}</span>'
        "</div>"
        "</div>"
    )
    return cartao


st.title("Neighborhood Action Dashboard")
st.caption("Acompanhe as ocorrencias do bairro e veja o que precisa de atencao primeiro.")

if "ocorrencias" not in st.session_state:
    # lista inicial
    st.session_state.ocorrencias = [dict(ocorrencia) for ocorrencia in ocorrencias_simuladas]

st.sidebar.header("Nova ocorrencia")
titulo_novo = st.sidebar.text_input("Titulo", placeholder="Ex: Buraco na calcada")
local_novo = st.sidebar.text_input("Local", placeholder="Ex: Rua das Flores, 120")
risco_novo = st.sidebar.checkbox("Risco Imediato")
prazo_novo = st.sidebar.checkbox("Prazo Excedido")
reincidencia_novo = st.sidebar.checkbox("Reincidencia Registrada")

# previa
previa = avaliar_ocorrencia(int(risco_novo), int(prazo_novo), int(reincidencia_novo))
valor_previa_alerta = "Sim" if previa["alerta_prioridade"] == 1 else "Nao"
valor_previa_pendencia = "Sim" if previa["pendencia_critica"] == 1 else "Nao"
st.sidebar.markdown("**Previa do resultado**")
st.sidebar.metric("Alerta de Prioridade", valor_previa_alerta)
st.sidebar.metric("Pendencia Critica", valor_previa_pendencia)
st.sidebar.caption("Resultado no painel: " + previa["status_visual_dashboard"])

if st.sidebar.button("Adicionar ocorrencia"):
    # novo cartao
    if titulo_novo.strip() == "" or local_novo.strip() == "":
        st.sidebar.warning("Informe titulo e local.")
    else:
        numero = len(st.session_state.ocorrencias) + 1
        nova_ocorrencia = {
            "id": f"OC-{numero:03d}",
            "titulo": titulo_novo.strip(),
            "local": local_novo.strip(),
            "risco_imediato": int(risco_novo),
            "prazo_excedido": int(prazo_novo),
            "reincidencia_registrada": int(reincidencia_novo),
        }
        st.session_state.ocorrencias.append(nova_ocorrencia)
        st.sidebar.success("Ocorrencia adicionada.")

avaliadas = avaliar_lista(st.session_state.ocorrencias)
avaliadas.sort(key=ordem_visual)

# metricas
total = len(avaliadas)
criticas = 0
alertas = 0
comuns = 0

for ocorrencia in avaliadas:
    if ocorrencia["pendencia_critica"] == 1:
        criticas += 1
    if ocorrencia["alerta_prioridade"] == 1:
        alertas += 1
    if ocorrencia["alerta_prioridade"] == 0 and ocorrencia["pendencia_critica"] == 0:
        comuns += 1

coluna_1, coluna_2, coluna_3, coluna_4 = st.columns(4)
coluna_1.metric("Total de Ocorrencias", total)
coluna_2.metric("Pendencias Criticas", criticas)
coluna_3.metric("Alertas de Prioridade", alertas)
coluna_4.metric("Fila Comum", comuns)

st.markdown("---")
st.subheader("Fila de atendimento")
st.caption("As ocorrencias mais urgentes aparecem primeiro.")

# cartoes
for ocorrencia in avaliadas:
    st.markdown(criar_cartao(ocorrencia), unsafe_allow_html=True)
