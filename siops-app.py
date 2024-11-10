from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configurações do WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Lista de municípios
municipios = {'110012': "Ji-Paraná"}
# municipios = {
#     '110001': "Alta Floresta D'Oeste",
#     '110002': "Ariquemes",
#     '110003': "Cabixi",
#     '110004': "Cacoal",
#     '110005': "Cerejeiras",
#     '110006': "Colorado do Oeste",
#     '110007': "Corumbiara",
#     '110008': "Costa Marques",
#     '110009': "Espigão D'Oeste",
#     '110010': "Guajará-Mirim",
#     '110011': "Jaru",
#     '110012': "Ji-Paraná",
#     '110013': "Machadinho D'Oeste",
#     '110014': "Nova Brasilândia D'Oeste",
#     '110015': "Ouro Preto do Oeste",
#     '110016': "Parecis",
#     '110017': "Pimenta Bueno",
#     '110018': "Rolim de Moura",
#     '110019': "Santa Luzia D'Oeste",
#     '110020': "Porto Velho",
#     '110021': "Presidente Médici",
#     '110022': "Primavera de Rondônia",
#     '110023': "Rio Crespo",
#     '110024': "São Felipe D'Oeste",
#     '110025': "São Francisco do Guaporé",
#     '110026': "São Miguel do Guaporé",
#     '110027': "Seringueiras",
#     '110028': "Teixeirópolis",
#     '110029': "Theobroma",
#     '110030': "Urupá",
#     '110031': "Vale do Anari",
#     '110032': "Vale do Paraíso",
#     '110033': "Nova Mamoré",
#     '110034': "Alvorada D'Oeste",
#     '110035': "Alto Alegre dos Parecis",
#     '110036': "Alto Paraíso",
#     '110037': "Buritis",
#     '110038': "Candeias do Jamari",
#     '110039': "Castanheiras",
#     '110040': "Chupinguaia",
#     '110041': "Ministro Andreazza",
#     '110042': "Monte Negro",
#     '110043': "Mirante da Serra",
#     '110044': "Nova União",
#     '110045': "Novo Horizonte do Oeste"
# }

periodos = {'12':'1', '14':'2'}
# Função para extrair dados de cada município
def extrair_dados_municipio(cod_municipio, p):
   
    # Acessando a URL desejada
    driver.get(f'http://siops.datasus.gov.br/consleirespfiscal.php?S=1&UF=11;&Municipio={cod_municipio};&Ano=2024&Periodo={p}')

    # Clicando no botão de consulta com espera explícita
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "BtConsultar"))
    ).click()

    # Esperando o carregamento das tabelas
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[1]'))
    )

    # Inicializando listas para armazenar dados
    dados_receita = []
    dados_despesas = []
    dados_apuracao = []
    empenho_exercicio = []
    receita_adcional = []
    despesas_saude_fuc = []
    despesas_saude_total = []

    # Localizando as tabelas
    tabela_receita = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[1]')
    tabela_despesas = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[2]')
    tabela_apuracao = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[3]')
    tabela_empenho_exercicio = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[5]')
    tabela_receita_adcional = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[10]')
    tabela_receita_despesas_saude_fuc = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[11]')
    tabela_despesas_saude_total = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div/table[12]')


    # Extraindo dados da tabela de receitas
    for linha in tabela_receita.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        dados_receita.append(linha_dados)

    # Extraindo dados da tabela de despesas
    for linha in tabela_despesas.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        dados_despesas.append(linha_dados)

    # Extraindo dados da tabela de apuração
    for linha in tabela_apuracao.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        dados_apuracao.append(linha_dados)

    for linha in tabela_empenho_exercicio.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        empenho_exercicio.append(linha_dados)

    for linha in tabela_receita_adcional.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        receita_adcional.append(linha_dados)

    for linha in tabela_receita_despesas_saude_fuc.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        despesas_saude_fuc.append(linha_dados)

    for linha in tabela_despesas_saude_total.find_elements(By.TAG_NAME, 'tr'):
        linha_dados = [coluna.text for coluna in linha.find_elements(By.TAG_NAME, 'td')]
        despesas_saude_total.append(linha_dados)
   
    

    # Definindo os nomes das colunas
    colunaReceita = ['RECEITAS RESULTANTES DE IMPOSTOS E TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS',
                     'PREVISÃO INICIAL', 'RECEITAS REALIZADAS - PREVISÃO ATUALIZADA (a)',
                     'RECEITAS REALIZADAS Até o mes', '% (b/a) x 100']

    colunaDespesas = ['DESPESAS COM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (ASPS) - POR SUBFUNÇÃO E CATEGORIA ECONÔMICA',
                      'DOTAÇÃO INICIAL', 'DOTAÇÃO ATUALIZADA (c)', 'DESPESAS EMPENHADAS - DESPESAS EMPENHADAS',
                      'DESPESAS EMPENHADAS - % (d/c) x 100', 'DESPESAS LIQUIDADAS Até o mes',
                      'DESPESAS LIQUIDADAS - % (e/c) x 100', 'DESPESAS PAGAS Até o mes',
                      'DESPESAS PAGAS - % (f/c) x 100', 'Inscritas em Restos a Pagar não Processados']
    
    colunaApuração = ['APURAÇÃO DO CUMPRIMENTO DO LIMITE MÍNIMO PARA APLICAÇÃO EM ASPS','DESPESAS EMPENHADAS (d)','DESPESAS LIQUIDADAS Até o mes','DESPESAS PAGAS (f)']

    coluna_receita_adcional = ['RECEITAS ADICIONAIS PARA O FINANCIAMENTO DA SAÚDE NÃO COMPUTADAS NO CÁLCULO DO MÍNIMO','PREVISÃO INICIAL','RECEITAS REALIZADAS -  ATUALIZADA (a)','DESPESAS LIQUIDADAS Até o mes','RECEITAS REALIZADAS - % (b/a) x 100']

    coluna_tabela_receita_despesas_saude_fuc = ['DESPESAS COM SAUDE POR SUBFUNÇÕES E CATEGORIA ECONÔMICA NÃO COMPUTADAS NO CÁLCULO DO MÍNIMO', 'DOTAÇÃO INICIAL', 'DOTAÇÃO ATUALIZADA', 'DESPESAS EMPENHADAS - Até o bimestre (d)','DESPESAS EMPENHADAS - % (d/c) x 100', 'DESPESAS LIQUIDADAS Até o mes',  'DESPESAS LIQUIDADAS - % (e/c) x 100', 'RECEITAS REALIZADAS Até o mes','DESPESAS PAGAS Até o bimestre (f)', 'Inscritas em Restos a Pagar não Processados']

    coluna_despesas_saude_total = ['DESPESAS TOTAIS COM SAÚDE EXECUTADAS COM COM RECURSOS PRÓPRIOS E COM RECURSOS TRANSFERIDOS DE OUTROS ENTES', 'DOTAÇÃO INICIAL', 'DOTAÇÃO ATUALIZADA','DESPESAS EMPENHADAS - Até o bimestre (d)','DESPESAS EMPENHADAS - % (d/c) x 100', 'DESPESAS LIQUIDADAS Até o mes',  'DESPESAS LIQUIDADAS - % (e/c) x 100', 'DESPESAS PAGAS Até o bimestre (f)','DESPESAS PAGAS - % (f/c) x 100','Inscritas em Restos a Pagar não Processados']

    # Criando DataFrames
    df_receita = pd.DataFrame(data=dados_receita, columns=colunaReceita)
    df_despesas = pd.DataFrame(data=dados_despesas, columns=colunaDespesas)
    df_apuracao = pd.DataFrame(data=dados_apuracao, columns=colunaApuração)
    df_receita_adcional = pd.DataFrame(data=receita_adcional, columns=coluna_receita_adcional)
    df_despesas_saude_fuc = pd.DataFrame(data=despesas_saude_fuc, columns=coluna_tabela_receita_despesas_saude_fuc)
    df_despesas_saude_total = pd.DataFrame(data=despesas_saude_total, columns=coluna_despesas_saude_total)
    

    return df_receita, df_despesas, df_apuracao, df_receita_adcional, df_despesas_saude_fuc, df_despesas_saude_total

# Função para formatar os DataFrames
def formatar_dataframe(df, descricao_coluna, valor_coluna, cod_municipio, p):
    # Renomeando e selecionando as colunas necessárias
    df_formatado = df[[descricao_coluna, valor_coluna]].copy()
    df_formatado.columns = ['CONTA', 'VALOR']
    
    # Adicionando a coluna "COLUNA" e "COD"
    df_formatado['COLUNA'] = valor_coluna
    df_formatado['COD'] = cod_municipio
    df_formatado['BIMESTRE'] = p
    
    return df_formatado

# Função para concatenar as duas linhas subsequentes com a referência
def concatenar_blocos(df):
    referencia = ""  # Armazena a linha de referência atual

    # Iterando por todas as linhas do DataFrame
    for i in range(len(df)):
        # Se a linha contém '(' -> Atualiza a referência
        if "(" in df.at[i, df.columns[0]]:
            referencia = df.at[i, df.columns[0]]
        else:
            # Concatena a linha atual com a referência
            df.at[i, df.columns[0]] = f"{df.at[i, df.columns[0]]} {referencia}"
    
    return df

# Lista para armazenar os DataFrames
dfs_unificados = []

# Iterando sobre os municípios e extraindo os dados
for municipio, nome_municipio in municipios.items():
    for periodo, bimestre in periodos.items():
        try:
            df_receita, df_despesas, df_apuracao, df_receita_adcional, df_despesas_saude_fuc, df_despesas_saude_total = extrair_dados_municipio(municipio,periodo)
       
            # Aplicando a função de concatenação
            df_despesas_ate_concat = concatenar_blocos(df_despesas)

            # Formatar os DataFrames de Receita e Despesas
            df_receita_formatado = formatar_dataframe(df_receita, 
                                                    'RECEITAS RESULTANTES DE IMPOSTOS E TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS', 
                                                    'RECEITAS REALIZADAS Até o mes', 
                                                    municipio, bimestre)

            df_despesas_ate_formatado = formatar_dataframe(df_despesas_ate_concat, 
                                                        'DESPESAS COM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (ASPS) - POR SUBFUNÇÃO E CATEGORIA ECONÔMICA', 
                                                        'DESPESAS LIQUIDADAS Até o mes', 
                                                        municipio, bimestre)
            
            df_despesas_IRPN_formatado = formatar_dataframe(df_despesas_ate_concat, 
                                                        'DESPESAS COM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (ASPS) - POR SUBFUNÇÃO E CATEGORIA ECONÔMICA', 
                                                        'Inscritas em Restos a Pagar não Processados', 
                                                        municipio, bimestre)
            df_apuracao_ate_formatado = formatar_dataframe(df_apuracao, 
                                                    'APURAÇÃO DO CUMPRIMENTO DO LIMITE MÍNIMO PARA APLICAÇÃO EM ASPS', 
                                                    'DESPESAS LIQUIDADAS Até o mes', 
                                                    municipio, bimestre)
            
            df_apuracao_irpn_formatado = formatar_dataframe(df_apuracao, 
                                                    'APURAÇÃO DO CUMPRIMENTO DO LIMITE MÍNIMO PARA APLICAÇÃO EM ASPS', 
                                                    'DESPESAS LIQUIDADAS Até o mes', 
                                                    municipio, bimestre)
            

            df_apuracao_receita_adc = formatar_dataframe(df_receita_adcional, 
                                                    'RECEITAS ADICIONAIS PARA O FINANCIAMENTO DA SAÚDE NÃO COMPUTADAS NO CÁLCULO DO MÍNIMO', 
                                                    'DESPESAS LIQUIDADAS Até o mes', 
                                                    municipio, bimestre)
            df_despesas_saude_fuc = concatenar_blocos(df_despesas_saude_fuc)
            df_apuracao_saude_ate = formatar_dataframe(df_despesas_saude_fuc, 
                                                    'DESPESAS COM SAUDE POR SUBFUNÇÕES E CATEGORIA ECONÔMICA NÃO COMPUTADAS NO CÁLCULO DO MÍNIMO', 
                                                    'DESPESAS LIQUIDADAS Até o mes', 
                                                    municipio, bimestre)
            
            
            df_apuracao_saude_irpn = formatar_dataframe(df_despesas_saude_fuc, 
                                                    'DESPESAS COM SAUDE POR SUBFUNÇÕES E CATEGORIA ECONÔMICA NÃO COMPUTADAS NO CÁLCULO DO MÍNIMO', 
                                                    'Inscritas em Restos a Pagar não Processados', 
                                                    municipio, bimestre)


            df_despesas_saude_total = concatenar_blocos(df_despesas_saude_total)
            df_despesas_saude_total_ate = formatar_dataframe(df_despesas_saude_total, 
                                                    'DESPESAS TOTAIS COM SAÚDE EXECUTADAS COM COM RECURSOS PRÓPRIOS E COM RECURSOS TRANSFERIDOS DE OUTROS ENTES', 
                                                    'DESPESAS LIQUIDADAS Até o mes', 
                                                    municipio, bimestre)
            
            
            df_apuracao_saude_total_irpn = formatar_dataframe(df_despesas_saude_total, 
                                                    'DESPESAS TOTAIS COM SAÚDE EXECUTADAS COM COM RECURSOS PRÓPRIOS E COM RECURSOS TRANSFERIDOS DE OUTROS ENTES', 
                                                    'Inscritas em Restos a Pagar não Processados', 
                                                    municipio, bimestre)

            # Concatenando os DataFrames em um único
            df_unico = pd.concat([df_receita_formatado, df_despesas_ate_formatado, df_despesas_IRPN_formatado,df_apuracao_ate_formatado,df_apuracao_irpn_formatado,df_apuracao_saude_ate, df_apuracao_saude_irpn, df_despesas_saude_total_ate, df_apuracao_saude_total_irpn ], ignore_index=True)
            
            # Adicionando o DataFrame processado à lista
            dfs_unificados.append(df_unico)
        except:
            print(f"ERRO {nome_municipio.upper()} Não encontrado para o {bimestre}° Bimestre")
# Concatenando todos os DataFrames de diferentes municípios
df_final = pd.concat(dfs_unificados, ignore_index=True)

# Exibindo os DataFrames resultantes
print(f'dados:\n{df_final}\n')

# Salvando em arquivo Excel (se necessário)
# df_final.to_excel("siops0511.xlsx", index=False)

from sqlalchemy import create_engine

# Corrige a conexão substituindo o '@' por '%40' ou usando aspas
engine = create_engine('mysql+pymysql://root:@Talis123@localhost:3306/siops')

# Insere os dados na tabela
df_final.to_sql('dados_siops', con=engine, if_exists='append', index=False)

# Fechando o navegador
driver.quit()


