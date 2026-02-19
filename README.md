# 🌸 Bot de Pós-Venda - My Acessórios

Este projeto é uma ferramenta de automação para facilitar o contato de pós-venda com clientes. Ele lê uma planilha de vendas, gera links personalizados de WhatsApp e organiza o fluxo de atendimento de forma visual e rápida.

## 🚀 Funcionalidades

* **Leitura de Excel:** Processa automaticamente planilhas com dados de vendas.
* **Links Diretos:** Gera links de WhatsApp com mensagens pré-definidas e cupons de desconto.
* **Marcação Visual:** O sistema pinta a planilha original e muda a cor dos botões já clicados para evitar duplicidade.
* **Interface Web:** Interface simples e intuitiva desenvolvida com FastAPI.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework para a criação da API e interface web.
* **Pandas:** Para manipulação de dados da planilha.
* **Openpyxl:** Para edição e estilização do arquivo Excel.

## 📋 Como usar (Passo a Passo)

1. **Subir o servidor:**
   ```bash
   uvicorn main:app --reload
