from typing import *
from backend.planilha import Planilha
from backend.info_adicional import InformacaoAdicionalASerObtida
from backend.pessoa import Pessoa
from backend.enviador_emails import enviar_emails_com_informacoes_planilha
from formatador import parse_verdadeiro_falso

import os

email_origem = os.environ.get('EMAIL_USER')
senha_origem = os.environ.get('EMAIL_PASS')

nome_planilha: str = 'Testes'
numero_sheet: int = 0
linha_inicial: int = 3
linha_final: int = 5
coluna_nome: str = 'B'
coluna_email: str = 'C'
coluna_check: str = 'F'

infos_adicionais: List[InformacaoAdicionalASerObtida] = \
    [InformacaoAdicionalASerObtida('D', 'gasto', lambda info, pessoa: f"R${info.valor},00"),
     InformacaoAdicionalASerObtida('E', 'ja_pagou', lambda _, __: "")]


def funcao_deve_enviar(pessoa: Pessoa) -> bool:
    return not parse_verdadeiro_falso(pessoa.get_informacao_adicional('ja_pagou').valor)


nome_arquivo_resultado: str = 'capturando informações extras'

mensagem_html: Optional[str] = None

partes_email: List[str] = ['Boa noite! Estou fazendo a cobrança de uns produtos, %primeiro_nome', 'Seu gasto na nossa loja foi: %gasto',
                           '\nPor favor, tente pagar até a próxima quinta %nome\n Estamos enviado os boletos em anexo',
                           '\nAtenciosamente,', 'Rafael Nunes Santana']

anexos: List[str] = ['/home/rafaelsantana/Downloads/LR corrigido.pdf', '/home/rafaelsantana/Pictures/wallpapers/midnight forest.jpg']

planilha: Planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_email, coluna_check,
                              infos_adicionais, funcao_deve_enviar)

enviar_emails_com_informacoes_planilha(email_origem, senha_origem, planilha, mensagem_html, partes_email, anexos, nome_arquivo_resultado)
