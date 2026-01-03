#--------------------------------------------------------------#
# BIBLIOTECAS
#--------------------------------------------------------------#

import streamlit as st
from PIL import Image

#--------------------------------------------------------------#
# CONFIG STREAMLIT
#--------------------------------------------------------------#

st.set_page_config(page_title="Track Survey", page_icon="⚓", layout="centered")

#--------------------------------------------------------------#
# SIDEBAR
#--------------------------------------------------------------#

st.sidebar.markdown("# Survey Info")
st.sidebar.markdown("### ")

imagem = Image.open("lh2_foto.jpg")
st.sidebar.image(imagem, width=250)

st.sidebar.markdown("---")

st.sidebar.markdown("""<style>
    .sidebar-text {
        text-align: center;
        font-size: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p class="sidebar-text">Powered by Pedro Garcia.</p>', unsafe_allow_html=True)

#--------------------------------------------------------------#
# PROCESSAMENTO
#--------------------------------------------------------------#

# Inicializa session_state
if "conteudo_xyz" not in st.session_state:
    st.session_state.conteudo_xyz = None

with st.container():

    st.title("TRACK ROV - OCEANICASUB X 🚢")
    st.markdown("### 1. Selecione o arquivo LOG_Metadados_BR:")

    uploaded_file = st.file_uploader("", type=["npd"], help="Insira o arquivo LOG_Metadados_BR (.NPD) gerado pelo Navipac.")

    if uploaded_file is not None:
        st.success("Arquivo enviado com sucesso!")

with st.container():

    st.markdown("---")
    st.markdown("### 2. Extrair Track ROV - Formato MicroStation:")

    if st.button("Extrair Dados"):

        if uploaded_file is None:
            st.error("Selecione um arquivo antes de extrair os dados.")
        else:
            linhas_xyz = []

            conteudo = uploaded_file.getvalue().decode("utf-8", errors="ignore")

            # lógica do SPLIT das informações do arquivo navipac
            for linha in conteudo.splitlines():
                partes = linha.strip().split(",")

                try:
                    easting = partes[partes.index("Easting") + 1]
                    northing = partes[partes.index("Northing") + 1]
                    depth = partes[partes.index("Depth") + 1]

                    linhas_xyz.append(f"xy={easting},{northing},{depth}")

                except (ValueError, IndexError):
                    continue

            if linhas_xyz:
                st.session_state.conteudo_xyz = "\n".join(linhas_xyz)

                st.success(f"Dados extraídos com sucesso! Total de pontos: {len(linhas_xyz)}")
            else:
                st.error("Nenhum ponto válido encontrado no arquivo.")

with st.container():

    st.markdown("---")
    st.markdown("### 3. Download - Formato MicroStation:")
    if st.session_state.conteudo_xyz is not None:
        st.download_button("📥 Baixar", data=st.session_state.conteudo_xyz, file_name="track_rov.xyz", mime="text/plain")
    else:
        st.error("Nenhum ponto válido encontrado no arquivo.")

