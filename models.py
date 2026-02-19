import urllib.parse

class ServicoPosVenda:
    def __init__(self, vendedora: str, cliente: str, ddd, telefone):
        self.vendedora = vendedora
        self.cliente = cliente
        self.ddd = ddd
        self.telefone = telefone
        
    def gerar_link_whatsapp(self):
        # Limpeza do telefone
        tel_limpo = str(self.telefone).replace("-", "").replace(" ", "").replace(".0", "").strip()
        
        # Montagem do número (55 + DDD + Telefone)
        numero_completo = f"55{self.ddd}{tel_limpo}"
        
        # Mensagem personalizada My Acessórios
        mensagem = (
            f"Oi, {self.cliente.title()}! ✨\n\n"
            f"Aqui é a {self.vendedora.title()} da **My Acessórios** do Shopping Tambiá. "
            f"Passando para agradecer sua visita e dizer que amamos te atender! 🌸\n\n"
            f"Como forma de carinho, preparei um presente: na sua próxima compra, "
            f"use o cupom **VIVI15** para ganhar 15% de desconto! 🎁\n\n"
            f"Esperamos te ver em breve!"
        )
        
        mensagem_codificada = urllib.parse.quote(mensagem)
        return f"https://api.whatsapp.com/send?phone={numero_completo}&text={mensagem_codificada}"

    @property
    def nome_contato(self):
        return self.cliente.title()
