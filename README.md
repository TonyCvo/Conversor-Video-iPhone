# 🎬 Conversor de Vídeo Avançado v3.0

Um conversor de vídeo moderno e intuitivo para converter vídeos para formato MOV compatível com iPhone, com interface gráfica avançada e recursos profissionais.

## ✨ Características

### 🎯 **Funcionalidades Principais**
- **Conversão para MOV**: Formato otimizado para iPhone
- **Interface Moderna**: Tema escuro/claro com design intuitivo
- **Drag & Drop**: Arraste arquivos diretamente para a interface
- **Conversão em Lote**: Processe múltiplos arquivos de uma vez
- **Progresso em Tempo Real**: Acompanhe a conversão com barra de progresso
- **Prévia de Vídeo**: Visualize informações detalhadas do arquivo

### 🚀 **Recursos Avançados**
- **Atalhos de Teclado**: Navegação rápida e eficiente
- **Configurações Avançadas**: Controle total sobre parâmetros do FFmpeg
- **Validação de Arquivos**: Verificação automática de integridade
- **Verificação de Espaço**: Previne erros por falta de espaço em disco
- **Histórico de Conversões**: Registro completo de todas as conversões
- **Tooltips Informativos**: Dicas contextuais para melhor usabilidade

### 🎨 **Interface**
- **Tema Escuro/Claro**: Alternância automática (Ctrl+D)
- **Responsivo**: Adapta-se ao tamanho da janela
- **Ícones Intuitivos**: Navegação visual clara
- **Log Detalhado**: Acompanhamento completo do processo

## 📋 Requisitos

### 🔧 **Sistema**
- Windows 10/11, macOS 10.14+, ou Linux
- Python 3.7 ou superior
- FFmpeg instalado no sistema

### 📦 **Dependências Python**
```bash
pip install -r requirements.txt
```

### 🎬 **FFmpeg**
O FFmpeg é obrigatório para a conversão de vídeos.

**Windows:**
1. Baixe de: https://ffmpeg.org/download.html
2. Extraia para uma pasta (ex: `C:\ffmpeg`)
3. Adicione `C:\ffmpeg\bin` ao PATH do sistema

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🚀 Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Instale o FFmpeg** (ver seção acima)
4. **Execute o conversor:**
   ```bash
   python "Converter MPG em MOV.py"
   ```

## 🎯 Como Usar

### 📁 **Conversão Simples**
1. Abra o conversor
2. Clique em "Procurar" ou arraste um arquivo
3. Escolha a qualidade (High/Medium/Low)
4. Clique em "Converter Vídeo"
5. Aguarde a conclusão

### 📦 **Conversão em Lote**
1. Selecione "Conversão em Lote"
2. Adicione múltiplos arquivos ou selecione uma pasta
3. Defina a pasta de saída
4. Clique em "Converter Vídeo"
5. Acompanhe o progresso

### ⚙️ **Configurações Avançadas**
- Acesse a aba "Configurações"
- Ajuste parâmetros do FFmpeg
- Configure codecs de áudio
- Defina presets de codificação

## ⌨️ Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+O` | Abrir arquivo de vídeo |
| `Ctrl+S` | Salvar configurações |
| `Ctrl+D` | Alternar tema claro/escuro |
| `F1` | Mostrar ajuda |
| `Esc` | Cancelar conversão |

## 📁 Formatos Suportados

### 🎬 **Entrada**
- MPG/MPEG
- AVI
- MKV
- WMV
- FLV
- WEBM

### 💾 **Saída**
- MOV (compatível com iPhone)

## 🔧 Configurações

### 🎯 **Qualidade**
- **High**: Melhor qualidade, arquivo maior
- **Medium**: Equilíbrio entre qualidade e tamanho
- **Low**: Menor qualidade, arquivo menor

### 🔊 **Áudio**
- **Preservar Áudio**: Mantém o áudio original
- **Codec**: AAC (padrão), MP3, AC3
- **Taxa de Bits**: 128k (padrão)

### ⚙️ **Avançado**
- **Preset**: Velocidade de codificação
- **Profile H.264**: Compatibilidade
- **Level H.264**: Limitações de hardware

## 🐛 Solução de Problemas

### ❌ **FFmpeg não encontrado**
- Verifique se o FFmpeg está instalado
- Confirme se está no PATH do sistema
- Reinicie o conversor após instalar

### ❌ **Erro de conversão**
- Verifique se o arquivo não está corrompido
- Confirme se há espaço suficiente em disco
- Tente com qualidade menor

### ❌ **Arquivo não suportado**
- Verifique se o formato é suportado
- Tente converter para outro formato primeiro

## 📊 Histórico

O conversor mantém um histórico completo de todas as conversões:
- Data e hora
- Arquivo original
- Arquivo convertido
- Status da conversão
- Tamanho do arquivo

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- **FFmpeg**: Pelo poderoso framework de conversão
- **Tkinter**: Pela interface gráfica
- **Comunidade Python**: Pelo suporte e bibliotecas

---

**Desenvolvido com ❤️ para facilitar a conversão de vídeos**
