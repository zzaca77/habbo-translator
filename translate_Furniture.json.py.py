import json
import time
import os
from deep_translator import GoogleTranslator

# idioma de destino (exemplo: "fr" para francês, "es" para espanhol, "pt" para português)
IDIOMA_DESTINO = "fr"

ARQUIVO_ORIGINAL = "Furnituredata.json"
ARQUIVO_TRADUZIDO = "Furnituredata_traduzido.json"
ARQUIVO_CHECKPOINT = "checkpoint.txt"

# Função segura para traduzir
def traduzir_texto(texto):
    try:
        return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
    except Exception as e:
        print(f"⚠ Erro ao traduzir: {e}, tentando novamente...")
        time.sleep(2)
        try:
            return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
        except Exception as e2:
            print(f"❌ Falha final: {e2}. Mantendo texto original.")
            return texto  # se falhar de novo, retorna o original

# Função para traduzir nomes e descrições
def traduzir_names_e_descricoes(lista, start_index=0):
    for i in range(start_index, len(lista)):
        item = lista[i]

        # Traduzir NAME
        if "name" in item and item["name"]:
            name_str = str(item["name"])
            traduzido = traduzir_texto(name_str)
            lista[i]["name"] = traduzido
            print(f"[{i+1}/{len(lista)}] NAME: {name_str} -> {traduzido}")
            time.sleep(0.5)

        # Traduzir DESCRIPTION
        if "description" in item and item["description"]:
            desc_str = str(item["description"])
            traduzido = traduzir_texto(desc_str)
            lista[i]["description"] = traduzido
            print(f"[{i+1}/{len(lista)}] DESC: {desc_str} -> {traduzido}")
            time.sleep(0.5)

        # Salvar checkpoint e progresso a cada 100 itens
        if i % 100 == 0:
            salvar_progresso(local_data, i)

    return lista

# Função para salvar progresso
def salvar_progresso(dados, indice):
    with open(ARQUIVO_TRADUZIDO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_CHECKPOINT, "w") as f:
        f.write(str(indice))
    print(f"💾 Progresso salvo até o item {indice}")

# Função para carregar checkpoint
def carregar_checkpoint():
    if os.path.exists(ARQUIVO_CHECKPOINT):
        with open(ARQUIVO_CHECKPOINT, "r") as f:
            return int(f.read().strip())
    return 0

# Programa principal
if __name__ == "__main__":
    try:
        # Carregar JSON original ou traduzido (se já existir)
        if os.path.exists(ARQUIVO_TRADUZIDO):
            with open(ARQUIVO_TRADUZIDO, "r", encoding="utf-8") as f:
                local_data = json.load(f)
            print("🔄 Continuando do arquivo já traduzido...")
        else:
            with open(ARQUIVO_ORIGINAL, "r", encoding="utf-8") as f:
                local_data = json.load(f)
            print("📂 Arquivo original carregado...")

        # Descobrir onde parou
        start_index = carregar_checkpoint()
        print(f"▶ Retomando a partir do item {start_index}")

        # Traduzir
        if "roomitemtypes" in local_data and "furnitype" in local_data["roomitemtypes"]:
            local_data["roomitemtypes"]["furnitype"] = traduzir_names_e_descricoes(
                local_data["roomitemtypes"]["furnitype"], start_index
            )

        # Salvar final
        salvar_progresso(local_data, len(local_data["roomitemtypes"]["furnitype"]))
        print("\n✅ Tradução concluída! Arquivo salvo como 'Furnituredata_traduzido.json'.")

    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{ARQUIVO_ORIGINAL}' não foi encontrado na pasta atual.")
    except json.JSONDecodeError:
        print("❌ Erro: O arquivo JSON está corrompido ou mal formatado.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
