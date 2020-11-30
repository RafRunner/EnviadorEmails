from typing import *
from backend.formatador import formatar_partes_email
from backend.formatador import personalisa
from backend.pessoa import Pessoa
from backend.planilha import Planilha
from email.message import EmailMessage

import smtplib
import os
import errno
import imghdr


def enviar_emails_com_informacoes_planilha(
        email_origim: str,
        senha_origem: str,
        planilha: Planilha,
        mensagem_html: Optional[str],
        partes_email: List[str],
        anexos: List[str],
        nome_arquivo_resultado: str) -> None:

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
                registra_resultado_pessoa(pessoa, 'FALHA! Email não enviado para a pessoa acima por ela estar com o endereço de email inválido', resultado)
                continue

            if not pessoa.deve_enviar:
                registra_resultado_pessoa(pessoa, 'Email não enviado para a pessoa acima pois não era necessário', resultado)
                continue

            # Enviando o email de fato
            try:
                smtp.send_message(monta_mensagem_email(email_origim, pessoa, mensagem_html, partes_email, anexos, resultado))

                planilha.marca_como_enviado(pessoa)
                registra_resultado_pessoa(pessoa, 'SUCESSO! Email enviado para a pessoa acima com sucesso', resultado)

            except Exception as e:
                registra_resultado_pessoa(pessoa, f'Ocorreu um erro ao enviar o email para a pessoa acima: {e}', resultado)

    except Exception as err:
        resultado.write('\nERRO CRÍTICO! A execução teve que ser interrompida por uma exception: ' + str(err) + '\n\n')
    finally:
        resultado.close()
        smtp.close()


def registra_resultado_pessoa(pessoa: Pessoa, mensgem: str, resultado):
    resultado.write(str(pessoa) + '\n')
    resultado.write(mensgem + '\n\n')


def monta_mensagem_email(
        email_origim: str,
        pessoa: Pessoa,
        mensagem_html: Optional[str],
        partes_email: List[str],
        anexos: List[str],
        resultado) -> EmailMessage:

    msg: EmailMessage = EmailMessage()
    partes_formatadas: List[str] = formatar_partes_email(partes_email, pessoa)

    msg['Subject'] = partes_formatadas[0]
    msg['From'] = email_origim
    msg['To'] = pessoa.email
    msg.set_content(partes_formatadas[1])

    if mensagem_html:
        html_formatado: str = personalisa(mensagem_html, pessoa)
        msg.add_alternative(html_formatado, subtype='html')

    for arquivo in anexos:
        arquivo = personalisa(arquivo, pessoa)

        if os.path.exists(arquivo):
            with open(arquivo, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(f.name)
                file_type: str
                subtype: str

                image_type: str = imghdr.what(arquivo)

                if image_type is not None:
                    file_type = 'image'
                    subtype = image_type
                else:
                    file_type = 'application'
                    subtype = 'octet-stream'

                msg.add_attachment(file_data, maintype=file_type, subtype=subtype, filename=file_name)
        else:
            resultado.write(f"Arquivo {arquivo} não anexado pois não existe\n")

    return msg
