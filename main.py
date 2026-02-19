from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import io
from models import ServicoPosVenda

app = FastAPI()
ARQUIVO_RETORNO = "planilha_confirmada.xlsx"

@app.get("/", response_class=HTMLResponse)
async def principal():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h2>Bot de Pós-Venda My Acessórios 🌸</h2>
            <form action="/gerar-links" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept=".xlsx" required><br><br>
                <button type="submit" style="background: #800080; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    GERAR LISTA DE ENVIOS
                </button>
            </form>
        </body>
    </html>
    """

@app.post("/gerar-links", response_class=HTMLResponse)
async def gerar_links(file: UploadFile = File(...)):
    conteudo = await file.read()
    df = pd.read_excel(io.BytesIO(conteudo))
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    wb = load_workbook(io.BytesIO(conteudo))
    ws = wb.active
    roxo_fill = PatternFill(start_color="800080", end_color="800080", fill_type="solid")

    # CSS Adicionado para marcar os clicados
    html_links = """
    <html>
        <head>
            <style>
                .btn-whats {
                    display: inline-block; 
                    margin-top: 5px; 
                    color: white; 
                    background: #25D366; 
                    padding: 8px 15px; 
                    text-decoration: none; 
                    border-radius: 4px; 
                    font-weight: bold;
                }
                /* QUANDO O LINK FOR CLICADO, MUDA A COR */
                .btn-whats:visited {
                    background: #555 !important;
                    color: #ccc !important;
                }
                .btn-whats:visited::after {
                    content: " (ENVIADO ✅)";
                    font-size: 0.8em;
                }
            </style>
        </head>
        <body style="font-family: sans-serif; padding: 20px;">
            <div style="background: #eee; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <strong>Dica:</strong> O botão ficará <b>cinza</b> após você clicar, para você saber quem já chamou.
            </div>
            <h2>Próximos Envios:</h2>
            <ul style="list-style: none; padding: 0;">
    """

    for index, linha in df.iterrows():
        try:
            servico = ServicoPosVenda(
                vendedora=linha['vendedora'],
                cliente=linha['cliente'],
                ddd=linha['ddd'],
                telefone=linha['telefone']
            )
            link = servico.gerar_link_whatsapp()
            
            html_links += f"""
                <li style="margin-bottom: 15px; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                    <span style="font-size: 1.1em;">👤 {servico.nome_contato}</span><br>
                    <a href="{link}" target="_self" class="btn-whats">
                        ENVIAR WHATSAPP
                    </a>
                </li>
            """
            ws.cell(row=index + 2, column=7).fill = roxo_fill
        except Exception as e:
            print(f"Erro na linha {index}: {e}")

    wb.save(ARQUIVO_RETORNO)
    html_links += """
            </ul>
            <br><hr>
            <a href="/baixar-planilha" style="color: #800080; font-weight: bold;">📥 Baixar Planilha Marcada</a>
            <br><br>
            <a href="/">⬅ Voltar para Início</a>
        </body>
    </html>
    """
    return html_links

@app.get("/baixar-planilha")
async def baixar_planilha():
    return FileResponse(ARQUIVO_RETORNO, filename="pos_venda_concluido.xlsx")