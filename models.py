import urllib.parse

class ServicoPosVenda:
    def __init__(self, vendedora, cliente, ddd, telefone, data=None, cidade=None):
        self.vendedora = vendedora
        self.cliente = cliente
        self.ddd = ddd
        self.telefone = telefone
        
    def gerar_link_whatsapp(self):
        # Pega so o primeiro nome da cliente (Ex: Andrea)
        nome_cliente = self.cliente.strip().split()[0].title() if self.cliente else "Cliente"
        
        tel_limpo = str(self.telefone).replace("-", "").replace(" ", "").replace(".0", "").strip()
        numero_completo = f"55{self.ddd}{tel_limpo}"
        
        # MENSAGEM FIXA COM SEU NOME: VIVIANE
        mensagem = (
            f"Olá, {nome_cliente}! Tudo bem?\n\n"
            f"Sou Viviane da My Acessórios do Shopping Tambiá 😄 "
            f"Estou entrando em contato para saber o que achou das peças e do nosso atendimento. 💓\n\n"
            f"Ahhhh, também temos atendimento online por WhatsApp com envio por delivery e também no nosso site: "
            f"https://www.myacessorios.com.br 📲💻\n\n"
            f"E com o meu cupom (VIVI15) você ainda tem desconto de 15% no nosso site 🥰"
        )
        
        msg_codificada = urllib.parse.quote(mensagem)
        return f"https://api.whatsapp.com/send?phone={numero_completo}&text={msg_codificada}"
