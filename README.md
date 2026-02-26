📸 Demonstração do Sistema (Pós-Venda)
<p align="center">
<img src="pos-venda1.PNG" height="350px" alt="Sistema de Pós-Venda" />
<img src="lista.PNG" height="350px" alt="Lista de Clientes" />
</p>

🌸 My Acessórios - Sistema de Pós-Venda
Sistema desenvolvido para automatizar e organizar o contato de pós-venda com clientes da loja My Acessórios. O sistema lê uma planilha de vendas, gera links personalizados de WhatsApp e organiza o fluxo de atendimento.

🚀 Funcionalidades
Leitura de Planilha: Processa arquivos .xlsx capturando dados de clientes, vendedoras e compras.

Mensagens Personalizadas: Gera automaticamente saudações usando apenas o primeiro nome da cliente e assinatura fixa da Viviane.

Gestão de Cliques: Marcador visual que esmaece a linha da tabela após o clique, evitando envios duplicados.

Interface Limpa: Abertura do WhatsApp sempre na mesma aba para evitar poluição no navegador.

Identidade Visual (Desktop): Ícone personalizado com fundo preto e logo rosa, proporcionando um contraste sofisticado e alta visibilidade na área de trabalho.

🛠️ Tecnologias Utilizadas
Python 3.12

FastAPI: Framework web de alta performance.

Pandas & OpenPyXL: Manipulação e leitura de dados de planilhas.

PyInstaller: Utilizado para converter o script num executável (.exe) de arquivo único.

📋 Como gerar o Executável (.exe)

Para gerar a versão final do sistema com o ícone de fundo preto da My Acessórios, utilize o seguinte comando no terminal:

pyinstaller --onefile --noconsole --clean --icon="Logo_Preto.ico" --name "My_PosVenda_Oficial" main.py
