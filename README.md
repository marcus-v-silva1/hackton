# Mapeamento e Análise de Eventos Climáticos
Este projeto fornece uma solução interativa para o mapeamento e análise de eventos climáticos usando Streamlit, Folium e LangChain. A aplicação permite visualizar eventos climáticos em um mapa dinâmico, adicionar novos eventos, realizar análises avançadas e interagir com um chatbot para obter informações detalhadas sobre os eventos registrados.

## Funcionalidades
- Visualização de Eventos Climáticos: Exibe eventos climáticos em um mapa interativo com agrupamento usando MarkerCluster.
- Adição de Eventos: Permite adicionar novos eventos através de um formulário, incluindo informações como tipo de evento e descrição.
- Geocodificação Reversa: Converte coordenadas geográficas em cidade e bairro para uma melhor compreensão da localização.
- Análise de Dados com IA: Inclui um chatbot que responde a perguntas sobre eventos climáticos, utilizando LangChain para análise avançada.
- Exibição de Eventos: Tabela que mostra todos os eventos registrados para fácil revisão.

## Tecnologias Utilizadas
- Python
- Streamlit: Para criar a interface web interativa.
- Folium: Para visualização de mapas interativos.
- LangChain: Para análise de dados e integração com modelos de linguagem.
- Pandas: Para manipulação e análise de dados.
- Requests: Para realizar requisições HTTP

## Instalação
```python
  python -m venv venv
  source venv/bin/activate  # Para Linux/Mac
  venv\Scripts\activate
```
Crie um arquivo requirements.txt com as seguintes dependências:
- streamlit
- folium
- streamlit_folium
- pandas
- langchain
- python-dotenv
- requests
- FAISS
- pandas
- openai
- langchain
- faiss-cpu
- langchain-community

Instale as dependências com:
```terminal
  pip install -r requirements.txt
```
Certifique-se de criar um arquivo .env na raiz do projeto para carregar suas variáveis de ambiente. O conteúdo do arquivo pode incluir:
```python
  OPENAI_API_KEY=suachaveapi
```
Para iniciar a aplicação, execute o seguinte comando:
```terminal
  streamlit run hackton.py
```
### Como Funciona
- Interface do Usuário: O formulário na barra lateral permite que os usuários adicionem novos eventos e visualizem eventos existentes.
- Mapa Interativo: O mapa mostra a localização dos eventos com a possibilidade de adicionar novos eventos ao clicar no mapa.
- Chatbot: O chatbot responde a perguntas sobre eventos climáticos registrados com base nos dados fornecidos.

### Imagens
![image](https://github.com/user-attachments/assets/8f8a950e-9487-4585-be70-bed8d80e4af8)
![image](https://github.com/user-attachments/assets/1ca7266d-6e9d-4952-b437-1de27dc7cb3b)

