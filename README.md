# 🧠 Manna ImagIA

Protótipo de sistema inteligente de edição de imagens com geração automática de legendas, sugestões de edição e aplicação de estilos artísticos, usando **modelos de linguagem e visão computacional** com **Transformers + Gradio**.

---

## ✨ Funcionalidades

- 🔍 Geração de legenda automática com base no conteúdo da imagem
- 🌍 Tradução automática da legenda para o português
- 🧠 Sugestões inteligentes de edição com base em brilho e contraste
- 🎨 Aplicação de filtros artísticos: Sépia, Preto e Branco, Posterização e Sketch
- 📷 Interface web interativa feita com [Gradio](https://gradio.app)

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- [Transformers (Hugging Face)](https://huggingface.co/docs/transformers/)
- [Gradio](https://gradio.app)
- [Pillow (PIL)](https://python-pillow.org/)
- [Torch (PyTorch)](https://pytorch.org)

---

## 🚀 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/ImagIA.git
cd ImagIA
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
# Ative no Windows:
.venv\Scripts\activate
# Ou no Linux/Mac:
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python main.py
```

Acesse no navegador: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 📁 Estrutura do Projeto

```
ImagIA/
├── main.py               # Código principal com a interface Gradio e lógica
├── requirements.txt      # Dependências do projeto
├── .gitignore            # Arquivos/pastas ignoradas pelo Git
└── README.md             # Este arquivo de documentação
```

---

## 📦 Dependências principais

Caso prefira instalar manualmente:

```bash
pip install torch transformers gradio pillow sentencepiece sacremoses
```

---

## 💡 Melhorias futuras

- [ ] Aplicação de filtros baseados em IA (ex: Van Gogh, Ghibli, Cyberpunk)
- [ ] Detecção de nitidez automática com OpenCV
- [ ] Upload de múltiplas imagens
- [ ] Opção para download da imagem final
- [ ] Modo mobile responsivo

---

## 🧑‍💻 Autor

**Tiago Madrigar**  
Coordenador Pedagógico | MannaBRAx  
[LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com/seu-usuario)

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
