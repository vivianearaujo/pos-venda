from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd
import io
from datetime import datetime
from models import ServicoPosVenda

app = FastAPI()

ESTILO_CSS = """
<style>
    :root { --primaria: #800080; --secundaria: #ff69b4; --fundo: #f8f9fa; --whatsapp: #25D366; --clicado: #6c757d; }
    body { font-family: 'Segoe UI', sans-serif; background-color: var(--fundo); margin: 0; padding: 0; }
    .header { background: linear-gradient(135deg, var(--primaria), var(--secundaria)); color: white; padding: 40px 20px; text-align: center; }
    .container { max-width: 900px; margin: -30px auto 50px; padding: 20px; }
    
    table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    th { background-color: var(--primaria); color: white; padding: 15px; text-align: left; }
    td { padding: 15px; border-bottom: 1px solid #eee; vertical-align: middle; }
    
    .linha-cliente { transition: all 0.3s; }
    
    /* Efeito para quando a linha for clicada */
    .processado { background-color: #f1f1f1 !important; opacity: 0.6; }
    .processado td { color: var(--clicado); }
    
    .btn-whats { 
        background-color: var(--whatsapp); color: white; padding: 10px 20px; 
        text-decoration: none; border-radius: 20px; font-weight: bold; font-size: 0.9em;
        display: inline-block; transition: background 0.3s;
    }

    .processado .btn-whats { background-color: var(--clicado) !important; pointer-events: none; }
    
    .info-secundaria { font-size: 0.85em; color: #888; }
    .btn-voltar { display: inline-block; margin-top: 20px; color: var(--primaria); text-decoration: none; font-weight: bold; }
</style>

<script>
    function marcarComoEnviado(elemento) {
        // Acha a linha da tabela (tr) e marca como processada
        const linha = elemento.closest('tr');
        linha.classList.add('processado');
        elemento.innerHTML = "✅ ENVIADO";
    }
</script>
"""

@app.get("/", response_class=HTMLResponse)
async def principal():
    return f"""
    <html>
        <head><title>My Acessórios - Pós-Venda</title>{ESTILO_CSS}</head>
        <body>
            <div class="header"><h1>My Acessórios 🌸</h1><p>Sistema de Pós-Venda</p></div>
            <div class="container" style="text-align:center; background:white; padding:30px; border-radius:15px;">
                <p>Selecione a planilha de vendas para gerar a lista de contatos:</p>
                <form action="/gerar-links" enctype="multipart/form-data" method="post">
                    <input name="file" type="file" accept=".xlsx" required><br><br>
                    <button type="submit" style="background:var(--primaria); color:white; padding:10px 30px; border:none; border-radius:20px; cursor:pointer; font-weight:bold;">GERAR LISTA DE ENVIO</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/gerar-links", response_class=HTMLResponse)
async def gerar_links(file: UploadFile = File(...)):
    conteudo = await file.read()
    df = pd.read_excel(io.BytesIO(conteudo))
    
    html_links = f"""
    <html>
        <head><title>Lista de Envios - My Acessórios</title>{ESTILO_CSS}</head>
        <body>
            <div class="header"><h1>Lista de Envios 📲</h1></div>
            <div class="container">
                <table>
                    <thead>
                        <tr>
                            <th>Cliente</th>
                            <th>Info Compra</th>
                            <th>Ação</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for index, linha in df.iterrows():
        try:
            # Posições: 0:Vend, 1:Cli, 2:DDD, 3:Tel, 4:Data, 5:Cidade
            vendedora = str(linha.iloc[0]).strip() if not pd.isna(linha.iloc[0]) else ""
            cliente = str(linha.iloc[1]).strip() if not pd.isna(linha.iloc[1]) else ""
            ddd = str(linha.iloc[2]).replace(".0", "").strip() if not pd.isna(linha.iloc[2]) else "83"
            telefone = str(linha.iloc[3]).replace(".0", "").strip() if not pd.isna(linha.iloc[3]) else ""
            data_venda = linha.iloc[4]
            cidade = str(linha.iloc[5]).strip() if not pd.isna(linha.iloc[5]) else ""

            if not cliente or cliente.lower() == 'nan': continue

            # Formata data
            if isinstance(data_venda, datetime):
                data_str = data_venda.strftime('%d/%m/%Y')
            else:
                data_str = str(data_venda) if str(data_venda).lower() != 'nan' else "--/--"

            servico = ServicoPosVenda(vendedora, cliente, ddd, telefone, data_venda, cidade)
            link = servico.gerar_link_whatsapp()
            
            html_links += f"""
                <tr class="linha-cliente">
                    <td>
                        <strong>{cliente.title()}</strong><br>
                        <span class="info-secundaria">Atendida por: {vendedora.title()}</span>
                    </td>
                    <td>
                        📍 {cidade.title()}<br>
                        📅 {data_str}
                    </td>
                    <td>
                        <a href="{link}" 
                           target="zap_janela" 
                           class="btn-whats" 
                           onclick="marcarComoEnviado(this)">ENVIAR WHATSAPP</a>
                    </td>
                </tr>
            """
        except Exception as e:
            print(f"Erro na linha {index}: {e}")

    html_links += """
                    </tbody>
                </table>
                <div style='text-align:center'><a href='/' class='btn-voltar'>⬅ Voltar e subir outra lista</a></div>
            </div>
        </body>
    </html>
    """
    return html_links
