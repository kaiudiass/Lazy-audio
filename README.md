# Lazy Audio

O Lazy Audio é uma aplicação desktop desenvolvida em Python para transcrição de áudio de forma ágil. Utilizando CustomTkinter para uma interface gráfica moderna e o Faster Whisper para transcrição, o aplicativo permite gravar a sua voz e transcrevê-la automaticamente, copiando o texto final direto para a sua área de transferência ou realizando ações automatizadas.

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Recomenda-se a versão 3.8 ou superior.

## Como instalar as dependências

Para rodar o projeto, é necessário instalar as bibliotecas listadas no arquivo de requisitos. Abra o terminal na pasta raiz do projeto e execute o comando abaixo:

```bash
pip install -r requirements.txt
```

## Como executar

Após instalar todas as dependências, você pode iniciar o aplicativo executando o arquivo principal a partir da raiz do projeto:

```bash
python main.py
```

## Estrutura de Pastas

Abaixo está a organização dos arquivos e diretórios do projeto e suas respectivas responsabilidades:

- `core/`: Contém a lógica principal de negócios da aplicação, dividida em módulos de gravação de áudio (`audio_recorder`) e o modelo de transcrição (`transcriber`).
- `image/`: Diretório destinado ao armazenamento de imagens, ícones e outros assets visuais utilizados na interface.
- `temp/`: Pasta utilizada para armazenar arquivos temporários durante a execução, como o arquivo de áudio gravado antes de ser processado pela transcrição.
- `tools/`: Scripts utilitários e ferramentas auxiliares (como o script para listar os microfones disponíveis no sistema).
- `ui/`: Componentes da interface de usuário, incluindo a janela principal (`app`), canvas do microfone e as configurações de layout baseadas em CustomTkinter.
- `config.py`: Arquivo de configuração global contendo definições de caminhos de diretórios, paleta de cores e tema da interface.
- `main.py`: Ponto de entrada da aplicação. É o arquivo que deve ser executado para abrir o programa.
- `requirements.txt`: Lista de todas as dependências e bibliotecas Python necessárias para o funcionamento do projeto.
