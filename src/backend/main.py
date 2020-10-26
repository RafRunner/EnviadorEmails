from typing import *
from backend.planilha import Planilha
from backend.info_adicional import InformacaoAdicionalASerObtida
from backend.pessoa import Pessoa
from backend.enviador_emails import enviar_emails_com_informacoes_planilha

import os

email_origem = os.environ.get('EMAIL_USER')
senha_origem = os.environ.get('EMAIL_PASS')

nome_planilha: str = 'Testes'
numero_sheet: int = 0
linha_inicial: int = 3
linha_final: int = 5
coluna_nome: str = 'B'
coluna_email: str = 'C'
coluna_check: str = 'D'

infos_adicionais: List[InformacaoAdicionalASerObtida] = \
    []


def funcao_deve_enviar(_: Pessoa) -> bool:
    return True


nome_arquivo_resultado: str = 'teste bot'

partes_email: List[str] = ['Agora seu nome está aqui: %primeiro_nome', 'Se o seu primeiro nome, %nome, apareceu no assunto é porque deu bom\n',
                           'Atensionamente (espero que mais),\n', 'Rafael Nunes Santana']

planilha: Planilha = Planilha(nome_planilha, numero_sheet, linha_inicial, linha_final, coluna_nome, coluna_email, coluna_check,
                              infos_adicionais, funcao_deve_enviar)

enviar_emails_com_informacoes_planilha(email_origem, senha_origem, planilha, partes_email, nome_arquivo_resultado)
