import urllib.parse

class ServicoPosVenda:
    def __init__(self, vendedora, cliente, ddd, telefone):
        # Aqui pegamos o nome real da vendedora da planilha
        # O .split()[0] garante que pegamos apenas o primeiro nome dela
        self.vendedora_real = str(vendedora).split()[0].title()
        
        # Nome do cliente tratado
        self.cliente_nome = str(cliente).split()[0].title()
        
        # Formata o telefone (55 + DDD + Numero)
        tel_limpo = str(telefone).replace("-", "").replace(" ", "")
        self.telefone_formatado = f"55{str(ddd).strip()}{tel_limpo}"
        
        # CORREÇÃO: O nome que aparece na lista agora usa a vendedora real da planilha
        # Exemplo: Adylene (Kawany)
        self.nome_contato = f"{self.cliente_nome} ({self.vendedora_real})"

    def gerar_link_whatsapp(self):
        # MENSAGEM: Aqui permanece fixo com o meu nome
        texto = (
            f"Olá, {self.cliente_nome}! Tudo bem?\n\n"
            f"Sou Viviane da My Acessórios do Shopping Tambiá 😄 "
            f"Estou entrando em contato para saber o que achou das peças e do nosso atendimento. 💓\n\n"
            f"Ahhhh, também temos atendimento online por WhatsApp com envio por delivery e também no nosso site: "
            f"https://www.myacessorios.com.br 📲💻\n\n"
            f"E com o meu cupom (VIVI15) você ainda tem desconto de 15% no nosso site 🥰"
        )
        
        texto_url = urllib.parse.quote(texto)
        return f"https://api.whatsapp.com/send?phone={self.telefone_formatado}&text={texto_url}"