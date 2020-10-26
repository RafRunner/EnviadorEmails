from typing import *
from backend.formatador import formatar_partes_em_email
from backend.pessoa import Pessoa
from backend.planilha import Planilha

import smtplib
import os
import errno


def enviar_emails_com_informacoes_planilha(email_origim: str, senha_origem: str, planilha: Planilha, partes_email: List[str], nome_arquivo_resultado: str):
    pasta_resultados: str = 'resultados'
    arquivo_resultado = os.path.join(pasta_resultados, nome_arquivo_resultado)

    try:
        os.makedirs(pasta_resultados)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e

    pessoas: List[Pessoa] = planilha.get_pessoas()

    resultado = open(arquivo_resultado + '.txt', 'a')
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    try:
        resultado.write(
            '\n\n///////////////////////////////////////////Inicio de uma nova execução de envio!!//////////////////////////////////////////////////////\n\n')

        resultado.write(f'Email de origem das mensagens: {email_origim}\n\n')

        resultado.write('Composição do email:\n')

        for parte in partes_email:
            resultado.write('\t' + parte + '\n')

        resultado.write('\n')

        smtp.login(email_origim, senha_origem)

        for pessoa in pessoas:
            if pessoa.invalido:
                resultado.write(str(pessoa))
                resultado.write('FALHA! Email não enviado para a pessoa acima por ela estar com o endereço de email inválido\n\n')
                continue

            if not pessoa.deve_enviar:
                resultado.write(str(pessoa))
                resultado.write('Email não enviado para a pessoa acima pois não era necessário\n\n')
                continue

            try:
                email_formatado: str = formatar_partes_em_email(email_origim, partes_email, pessoa)
                smtp.sendmail(email_origim, pessoa.email, email_formatado.encode('utf-8'))
                planilha.marca_como_enviado(pessoa)
                resultado.write(str(pessoa))
                resultado.write('SUCESSO! Email enviado para a pessoa acima com sucesso\n\n')

            except Exception as e:
                print(str(pessoa))
                print(e)
                resultado.write(str(pessoa))
                resultado.write(f"Ocorreu um erro ao enviar o email para a pessoa acima:\n{e}\n\n")

    except Exception as err:
        resultado.write('\nERRO CRÍTICO! A execução teve que ser interrompida por uma exception:' + str(err))
    finally:
        resultado.close()
        smtp.close()
