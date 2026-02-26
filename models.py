import urllib.parse

import urllib.parse

class ServicoPosVenda:
    def __init__(self, vendedora_planilha, cliente, ddd, telefone, data=None, cidade=None):
        # Pega apenas o primeiro nome da vendedora da planilha
        self.vendedora_original = str(vendedora_planilha).strip().split()[0].title() if vendedora_planilha else "Equipe"
        self.cliente = cliente
        self.ddd = ddd
        self.telefone = telefone
        self.data = data
        self.cidade = cidade
        
    def gerar_link_whatsapp(self, modelo_texto, nome_remetente):
        nome_cliente = self.cliente.strip().split()[0].title() if self.cliente else "Cliente"
        
        tel_limpo = str(self.telefone).replace("-", "").replace(" ", "").replace(".0", "").strip()
        numero_completo = f"55{self.ddd}{tel_limpo}"
        
        # Substitui as variáveis: {nome_cliente} e {vendedora} (que é quem está enviando agora)
        mensagem_final = modelo_texto.replace("{nome_cliente}", nome_cliente)
        mensagem_final = mensagem_final.replace("{vendedora}", nome_remetente)
        
        msg_codificada = urllib.parse.quote(mensagem_final)
        return f"https://api.whatsapp.com/send?phone={numero_completo}&text={msg_codificada}"
