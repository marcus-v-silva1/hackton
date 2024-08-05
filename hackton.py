import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import requests



# Carregar variáveis de ambiente
load_dotenv()

# Título do app
st.title("Mapeamento de Eventos Climáticos")

# Função para obter cidade e bairro a partir de coordenadas
def reverse_geocode(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}'
    response = requests.get(url)
    data = response.json()
    address = data.get('address', {})
    city = address.get('city', 'Desconhecido')
    suburb = address.get('suburb', 'Desconhecido')
    return city, suburb

# DataFrame para armazenar eventos
if 'events' not in st.session_state:
    st.session_state.events = pd.DataFrame(columns=['Tipo', 'Descrição', 'Cidade', 'Bairro', 'Latitude', 'Longitude'])

# Função para adicionar evento ao DataFrame
def add_event(event_type, event_description, lat, lon):
    city, suburb = reverse_geocode(lat, lon)
    new_event = pd.DataFrame({
        'Tipo': [event_type],
        'Descrição': [event_description],
        'Cidade': [city],
        'Bairro': [suburb],
        'Latitude': [lat],
        'Longitude': [lon]
    })
    st.session_state.events = pd.concat([st.session_state.events, new_event], ignore_index=True)

# Formulário para adicionar novos eventos
st.sidebar.header("Adicionar Novo Evento")
event_type = st.sidebar.selectbox("Tipo de Evento", ["Doação de Comida", "Tempestade", "Outros"])
event_description = st.sidebar.text_area("Descrição do Evento")
add_event_button = st.sidebar.button("Adicionar Evento")

# Criar mapa
mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
marker_cluster = MarkerCluster().add_to(mapa)

# Adicionar marcadores ao mapa
for idx, row in st.session_state.events.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Tipo']}: {row['Descrição']} ({row['Cidade']}, {row['Bairro']})",
        icon=folium.Icon(color="blue" if row['Tipo'] == "Doação de Comida" else "red")
    ).add_to(marker_cluster)

# Função para obter a localização clicada no mapa
map_data = st_folium(mapa, width=700, height=500)
if map_data and map_data['last_clicked']:
    lat, lon = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
    st.session_state['last_clicked_location'] = (lat, lon)
else:
    lat, lon = None, None

# Mostrar coordenadas clicadas
if lat and lon:
    city, suburb = reverse_geocode(lat, lon)
    st.sidebar.write(f"Localização selecionada: {city}, {suburb}")

# Adicionar evento se coordenadas estiverem disponíveis
if add_event_button and lat and lon:
    add_event(event_type, event_description, lat, lon)

# Exibir eventos na tabela
st.header("Eventos Registrados")
st.dataframe(st.session_state.events)

# Campo de texto para perguntas do usuário
st.header("Chatbot de Eventos Climáticos")
user_question = st.text_input("Faça sua pergunta sobre eventos climáticos:")
send_button = st.button("Enviar Pergunta")

# Carregar dados dos eventos para o chatbot
def load_events_data():
    events_data = st.session_state.events.to_dict('records')
    return events_data

# Implementar função de resposta do chatbot
def get_chatbot_response(question, events_data):
    if not events_data:
        return "Não há eventos registrados no momento."

    # Estrutura de dados para FAISS
    documents = [f"Tipo: {event['Tipo']}, Descrição: {event['Descrição']}, Cidade: {event['Cidade']}, Bairro: {event['Bairro']}" for event in events_data]
    
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(documents, embeddings)

    # Prompt Template
    template = """ 
    Você é um assistente virtual especializado em eventos climáticos.
    Seu objetivo é fornecer informações claras e detalhadas sobre os eventos climáticos registrados.
    Siga as regras abaixo:
    1/ Responda com base nos eventos fornecidos.
    2/ Forneça informações relevantes e precisas.

    Lista de eventos:
    {events}

    Pergunta: {question}

    Resposta:
    """
    prompt = PromptTemplate(input_variables=["events", "question"], template=template)
    chain = LLMChain(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"), prompt=prompt)

    # Obter resposta
    response = chain.run(events="\n".join(documents), question=question)
    return response

# Carregar dados dos eventos
events_data = load_events_data()

# Gerar resposta do chatbot
if send_button and user_question:
    chatbot_response = get_chatbot_response(user_question, events_data)
    st.info(chatbot_response)
