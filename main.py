# Importa bibliotecas principais
import gradio as gr  # Criação da interface web
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageStat  # Manipulação de imagens
import torch  # GPU/CPU
from transformers import BlipProcessor, BlipForConditionalGeneration, MarianMTModel, MarianTokenizer  # Modelos da HuggingFace
import transformers

# Mostra versão da biblioteca Transformers
print(transformers.__version__)

# ============================
# Carregamento dos modelos
# ============================

# Modelo BLIP para geração de legendas a partir de imagens
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Define o dispositivo de execução (GPU se disponível, senão CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Modelo MarianMT para tradução de inglês para português
modelo_traducao = "Helsinki-NLP/opus-mt-en-ROMANCE"
tokenizer_pt = MarianTokenizer.from_pretrained(modelo_traducao)
model_pt = MarianMTModel.from_pretrained(modelo_traducao)

# ============================
# Funções auxiliares
# ============================

# Traduz um texto em inglês para o português
def traduzir_para_portugues(texto):
    tokens = tokenizer_pt(texto, return_tensors="pt", padding=True)
    traducao = model_pt.generate(**tokens)
    return tokenizer_pt.decode(traducao[0], skip_special_tokens=True)

# Redimensiona a imagem para uma largura padrão sem distorcer
def redimensionar_imagem(imagem, largura_max=600):
    if imagem.width > largura_max:
        proporcao = largura_max / imagem.width
        nova_altura = int(imagem.height * proporcao)
        return imagem.resize((largura_max, nova_altura))
    return imagem

# Gera uma legenda em português para a imagem enviada
def gerar_legenda(imagem):
    imagem = imagem.convert('RGB')
    imagem = redimensionar_imagem(imagem)
    inputs = processor(images=imagem, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    legenda_en = processor.decode(out[0], skip_special_tokens=True)
    return traduzir_para_portugues(legenda_en)

# Analisa a imagem e gera sugestões de edição com base em brilho e contraste
def sugerir_melhorias(imagem):
    imagem_gray = imagem.convert("L")  # Converte para escala de cinza
    stat = ImageStat.Stat(imagem_gray)
    brilho = stat.mean[0]
    contraste = stat.stddev[0]

    sugestoes = []

    if brilho < 60:
        sugestoes.append("A imagem parece escura. Tente aumentar o brilho.")
    elif brilho > 200:
        sugestoes.append("A imagem está muito clara. Reduza o brilho.")

    if contraste < 40:
        sugestoes.append("A imagem tem pouco contraste. Experimente aumentá-lo.")

    if not sugestoes:
        sugestoes.append("A imagem parece boa. Você pode aplicar um estilo artístico se desejar.")

    return " ".join(sugestoes)

# Ajusta brilho e contraste da imagem automaticamente
def ajustar_imagem(imagem):
    imagem_corrigida = ImageEnhance.Brightness(imagem).enhance(1.3)
    imagem_corrigida = ImageEnhance.Contrast(imagem_corrigida).enhance(1.2)
    return imagem_corrigida

# Aplica um estilo artístico selecionado sobre a imagem
def aplicar_estilo(imagem, estilo):
    if estilo == "Nenhum":
        return imagem
    elif estilo == "Sépia":
        sepia = ImageOps.colorize(imagem.convert("L"), "#704214", "#C0A080")
        return sepia
    elif estilo == "Preto e Branco":
        return imagem.convert("L").convert("RGB")
    elif estilo == "Posterização":
        return ImageOps.posterize(imagem, bits=3)
    elif estilo == "Sketch":
        return imagem.filter(ImageFilter.CONTOUR)
    else:
        return imagem

# ============================
# Função principal de processamento
# ============================

# Processa a imagem: legenda, sugestão, correção e aplicação de estilo
def interface(imagem, estilo_artistico):
    if imagem is None:
        return "Nenhuma imagem enviada.", "", None

    imagem_original = imagem.copy()  # Mantém imagem original para não perder qualidade
    imagem_exibicao = redimensionar_imagem(imagem)  # Reduzida só para visualização

    legenda = gerar_legenda(imagem_exibicao)
    sugestao = sugerir_melhorias(imagem_exibicao)

    try:
        imagem_corrigida = ajustar_imagem(imagem_original)
        imagem_final = aplicar_estilo(imagem_corrigida, estilo_artistico)
    except Exception as e:
        print(f"Erro ao corrigir/aplicar estilo: {e}")
        imagem_final = None

    return legenda, sugestao, imagem_final

# ============================
# Interface Gradio
# ============================

with gr.Blocks() as demo:
    gr.Markdown("## Manna artIA - Protótipo de Edição Inteligente de Imagens")

    # Entrada da imagem + seleção de estilo artístico
    with gr.Row():
        imagem_input = gr.Image(type="pil", label="Envie uma imagem")
        estilo_dropdown = gr.Dropdown(
            ["Nenhum", "Sépia", "Preto e Branco", "Posterização", "Sketch"],
            value="Nenhum",
            label="Estilo Artístico"
        )

    # Saídas: legenda, sugestões e imagem final com estilo aplicado
    legenda_output = gr.Textbox(label="Legenda em Português")
    sugestao_output = gr.Textbox(label="Sugestões de Edição")
    imagem_corrigida = gr.Image(label="Imagem Final com Estilo")

    # Botão de execução
    botao = gr.Button("Gerar Legenda e Sugestão")

    # Ação ao clicar no botão
    botao.click(
        fn=interface,
        inputs=[imagem_input, estilo_dropdown],
        outputs=[legenda_output, sugestao_output, imagem_corrigida]
    )

# Executa localmente a interface
if __name__ == "__main__":
    demo.launch()
