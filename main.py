from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import io
from datetime import datetime
from models import ServicoPosVenda

app = FastAPI()

ESTILO_CSS = """
<style>
    :root { --primaria: #800080; --secundaria: #ff69b4; --fundo: #f8f9fa; --whatsapp: #25D366; --clicado: #6c757d; }
    body { font-family: 'Segoe UI', sans-serif; background-color: var(--fundo); margin: 0; padding: 0; display: flex; flex-direction: column; min-height: 100vh; }
    .header { background: linear-gradient(135deg, var(--primaria), var(--secundaria)); color: white; padding: 40px 20px; text-align: center; }
    .container { max-width: 900px; margin: -30px auto 50px; padding: 20px; flex: 1; }
    .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    
    input, textarea { width: 100%; padding: 12px; margin-top: 8px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-family: inherit; }
    
    table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; margin-top: 20px; }
    th { background-color: var(--primaria); color: white; padding: 15px; text-align: left; }
    td { padding: 15px; border-bottom: 1px solid #eee; }
    
    .btn-whats { 
        background-color: var(--whatsapp); color: white; padding: 10px 20px; 
        text-decoration: none; border-radius: 20px; font-weight: bold; display: inline-block;
    }
    .processado { opacity: 0.5; background-color: #f1f1f1 !important; }
    .processado .btn-whats { background-color: var(--clicado) !important; pointer-events: none; }
    
    .guia-planilha { background: #fff0f5; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #ffb6c1; }
    .guia-planilha table { font-size: 0.75em; margin-top: 5px; box-shadow: none; border: 1px solid #ddd; }
    .guia-planilha th { background: #800080; color: white; padding: 5px 10px; }
    
    .footer { text-align: center; padding: 20px; color: #888; font-size: 0.9em; }
</style>
<script>
    function marcarComoEnviado(elemento) {
        const linha = elemento.closest('tr');
        linha.classList.add('processado');
        elemento.innerHTML = "✅ ENVIADO";
    }
</script>
"""

CREDITOS = '<div class="footer">Desenvolvido por <strong>Viviane Santos</strong> - 2026 💎</div>'

@app.get("/", response_class=HTMLResponse)
async def principal():
    # Mensagem exatamente como você solicitou
    mensagem_padrao = """Olá, {nome_cliente}! Tudo bem? 
Sou {vendedora} da My Acessórios do Shopping Tambiá 😄 Estou entrando em contato para saber o que achou das peças e do nosso atendimento. 💓

Ahhhh, também temos atendimento online por WhatsApp com envio por delivery e também no nosso site https://www.myacessorios.com.br 📲💻

E com o meu cupom (VIVI15) você ainda tem desconto de 15% no nosso site🥰"""
    
    return f"""
    <html>
        <head><title>My Acessórios - Pós-Venda</title>{ESTILO_CSS}</head>
        <body>
            <div class="header"><h1>My Acessórios 🌸</h1><p>Sistema de Pós-Venda</p></div>
            <div class="container">
                <div class="card">
                    <div class="guia-planilha">
                        <h4 style="margin:0; color: #800080;">Atenção à ordem das colunas no Excel:</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>1. Vendedor</th><th>2. Cliente</th><th>3. DDD</th>
                                    <th>4. Telefone</th><th>5. Data</th><th>6. Cidade</th>
                                </tr>
                            </thead>
                        </table>
                    </div>

                    <form action="/gerar-links" enctype="multipart/form-data" method="post">
                        <label><strong>Quem está enviando as mensagens agora?</strong></label>
                        <input type="text" name="nome_remetente" value="Viviane" required>
                        
                        <br><br>
                        <label><strong>Modelo da Mensagem:</strong></label>
                        <textarea name="modelo_mensagem" rows="12" required>{mensagem_padrao}</textarea>
                        
                        <br><br>
                        <label><strong>Selecione a Planilha de Vendas (.xlsx):</strong></label>
                        <input name="file" type="file" accept=".xlsx" required>
                        
                        <br><br>
                        <button type="submit" style="background:var(--primaria); color:white; padding:15px; border:none; border-radius:25px; width:100%; cursor:pointer; font-weight:bold;">GERAR LISTA DE CONTATOS</button>
                    </form>
                </div>
                {CREDITOS}
            </div>
        </body>
    </html>
    """

@app.post("/gerar-links", response_class=HTMLResponse)
async def gerar_links(file: UploadFile = File(...), modelo_mensagem: str = Form(...), nome_remetente: str = Form(...)):
    conteudo = await file.read()
    df = pd.read_excel(io.BytesIO(conteudo))
    
    html_links = f"""
    <html>
        <head><title>Lista de Envios</title>{ESTILO_CSS}</head>
        <body>
            <div class="header"><h1>Lista de Envios 📲</h1><p>Enviando como: <b>{nome_remetente}</b></p></div>
            <div class="container">
                <table>
                    <thead><tr><th>Cliente / Vendedora</th><th>Cidade / Data</th><th>Ação</th></tr></thead>
                    <tbody>
    """

    for index, linha in df.iterrows():
        try:
            vendedora_plan = str(linha.iloc[0]).strip().split()[0].title() if not pd.isna(linha.iloc[0]) else "Equipe"
            cliente = str(linha.iloc[1]).strip()
            ddd = str(linha.iloc[2]).replace(".0", "").strip() if not pd.isna(linha.iloc[2]) else "83"
            telefone = str(linha.iloc[3]).replace(".0", "").strip()
            data_venda = linha.iloc[4]
            cidade = str(linha.iloc[5]).strip() if not pd.isna(linha.iloc[5]) else "Paraíba"

            if not cliente or cliente.lower() == 'nan': continue

            data_str = data_venda.strftime('%d/%m/%Y') if isinstance(data_venda, datetime) else str(data_venda)

            servico = ServicoPosVenda(vendedora_plan, cliente, ddd, telefone)
            link = servico.gerar_link_whatsapp(modelo_mensagem, nome_remetente)
            
            html_links += f"""
                <tr>
                    <td><strong>{cliente.title()}</strong><br><span style="font-size:0.8em; color:gray;">Atendida por: {vendedora_plan}</span></td>
                    <td>📍 {cidade.title()}<br>📅 {data_str}</td>
                    <td><a href="{link}" target="_blank" class="btn-whats" onclick="marcarComoEnviado(this)">ENVIAR</a></td>
                </tr>
            """
        except: continue

    html_links += f"""
                    </tbody>
                </table>
                <div style='text-align:center'><a href='/' style='display:inline-block; margin-top:20px; color:var(--primaria); font-weight:bold;'>⬅ Voltar</a></div>
                {CREDITOS}
            </div>
        </body>
    </html>
    """
    return html_links

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    from threading import Timer

    Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8050")).start()
    uvicorn.run(app, host="127.0.0.1", port=8050, log_config=None)
