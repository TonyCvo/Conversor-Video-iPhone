# 🚀 Instruções Rápidas - Conversor de Vídeo

## ⚡ Instalação Rápida

### Windows:
1. **Duplo clique** no arquivo `install.bat`
2. Aguarde a instalação das dependências
3. Execute: `python "Converter MPG em MOV.py"`

### Linux/macOS:
1. **Terminal**: `chmod +x install.sh && ./install.sh`
2. Execute: `python3 "Converter MPG em MOV.py"`

## 🎬 FFmpeg (Obrigatório)

### Windows:
1. Baixe: https://ffmpeg.org/download.html
2. Extraia para `C:\ffmpeg`
3. Adicione `C:\ffmpeg\bin` ao PATH do sistema

### Linux:
```bash
sudo apt update && sudo apt install ffmpeg
```

### macOS:
```bash
brew install ffmpeg
```

## 🎯 Como Usar

1. **Abra o conversor**
2. **Arraste um vídeo** ou clique em "Procurar"
3. **Escolha a qualidade** (High/Medium/Low)
4. **Clique em "Converter Vídeo"**
5. **Aguarde a conclusão**

## ⌨️ Atalhos Úteis

- `Ctrl+O`: Abrir arquivo
- `Ctrl+D`: Alternar tema
- `F1`: Ajuda
- `Esc`: Cancelar conversão

## ❓ Problemas Comuns

### "FFmpeg não encontrado"
- Instale o FFmpeg (ver seção acima)
- Reinicie o conversor

### "Módulo não encontrado"
- Execute o script de instalação
- Ou: `pip install -r requirements.txt`

### Erro de conversão
- Verifique se o arquivo não está corrompido
- Tente com qualidade menor

---

**🎉 Pronto! Seu conversor está funcionando!**
