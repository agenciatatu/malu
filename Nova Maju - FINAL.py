
# coding: utf-8

# In[1]:


def robo_tempo(): 
    import requests     
    from bs4 import BeautifulSoup
    import os
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv())

    token = os.environ.get('TOKEN_CLIMATEMPO')
    login = os.environ.get('LOGIN_AT')                            
    senha = os.environ.get('SENHA_AT')
                            
    dados_maceio = requests.get(f'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/6809/days/15?token={token}').json()
    dados_tempo = dados_maceio["data"]

    proximo_dia = dados_tempo[1]

    texto = proximo_dia['text_icon']

    texto_longo = texto['text']

    texto_longo2 = texto_longo['phrase']

    texto_resumido = texto_longo2['afternoon']

    texto_detalhado = texto_longo2['reduced']

    texto_detalhado1, texto_detalhado2, texto_detalhado3 = texto_detalhado.split('.')

    if texto_detalhado3.isalpha() == False:
        textinho = (f'{texto_detalhado1} e{texto_detalhado2}')
    else:
        textinho = (f'{texto_detalhado1},{texto_detalhado2} e{texto_detalhado3}')

    data_completa = proximo_dia['date_br']

    dia, mes, ano = data_completa.split('/')
    
    # datas atuais
    
    data_atual = dados_tempo[0]

    data_atual = data_atual['date']

    ano_atual, mes_atual, dia_atual = data_atual.split('-')

    if mes_atual == '01':
        mes_atual = 'January'
    if mes_atual == '02':
        mes_atual = 'February'
    if mes_atual == '03':
        mes_atual = 'March'
    if mes_atual == '04':
        mes_atual = 'April'
    if mes_atual == '05':
        mes_atual = 'May'
    if mes_atual == '06':
        mes_atual = 'June'
    if mes_atual == '07':
        mes_atual = 'July'
    if mes_atual == '08':
        mes_atual = 'August'
    if mes_atual == '09':
        mes_atual = 'September'
    if mes_atual == '10':
        mes_atual = 'October'
    if mes_atual == '11':
        mes_atual = 'November'
    if mes_atual == '12':
        mes_atual = 'December'

    temperatura = proximo_dia['temperature']

    maxima = temperatura['max']
    minima = temperatura['min']

    chuva = proximo_dia['rain']

    pro_chuva = chuva['probability']

    from datetime import date
    from datetime import datetime

    hj = date.today()
    dias = ('terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo', 'segunda-feira')
    dia_semana = (dias[hj.weekday()])

    if dia_semana == "sábado" or dia_semana == "domingo":
        pronome = 'este'
    else:
        pronome = 'esta'


    # Imprimindo matéria final

    titulo = (f"'{texto_resumido.capitalize()}', indica previsão do tempo para amanhã em Maceió")

    lide = (f"A previsão do tempo para a cidade de Maceió para {pronome} {dia_semana}, dia {dia}, indica {textinho.lower()}. A máxima registrada será de {maxima}ºC e a mínima de {minima}ºC. A probabilidade de chuva para amanhã é de {pro_chuva}%.")
    sublide = ("As informações desta matéria foram coletadas pela nossa robô do tempo <strong>Maju</strong>, de modo automatizado, no Portal Climatempo. Para saber mais sobre a Maju <strong><a href='http://www.agenciatatu.com.br/maju-robo-do-tempo/'>clique aqui</a></strong>.")
    corpo = (lide + '\n' + '\n' + sublide)        
    print(titulo)
    print(lide)
    print(sublide)
    
    # Atualizar post

    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
    
    wp = Client('http://www.agenciatatu.com.br/xmlrpc.php', f'{login}', f'{senha}')


    def atualizar_post():
        def find_id(title):
            offset = 0
            increment = 10
            while True:
                filter = { 'offset' : offset }
                p = wp.call(GetPosts(filter))
                if len(p) == 0:
                        break  # no more posts returned
                for post in p:
                    if post.title == title:
                        return(post.id)
                offset = offset + increment
            return(False)

        #newish post
    post = WordPressPost()
    post.id = 942
    post.title = titulo
    post.content = corpo
    post.date = datetime.strptime(f'{dia_atual} {mes_atual} {ano_atual}','%d %B %Y')
    post.post_status = 'publish'
    post.terms_names = {
        'post_tag': ['Previsão do Tempo', 'Maceió'],
        'category': ['Previsão do Tempo']
    }

    if post.id:
        wp.call(EditPost(post.id, post))
    else:
        post_id=find_id(post.title)
        if post_id:
            print("Sorry, we already have such a post(-title):", post_id)
        else:
            wp.call(NewPost(post))
robo_tempo()

