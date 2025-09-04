import json
import time
from deep_translator import GoogleTranslator

# idioma de destino (mude se quiser outro)
IDIOMA_DESTINO = "fr"

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

# Função para traduzir descriptions
def traduzir_descriptions_bloco(lista):
    for i, item in enumerate(lista):
        if "description" in item and item["description"]:
            desc_str = str(item["description"])
            traduzido = traduzir_texto(desc_str)
            lista[i]["description"] = traduzido
            print(f"[{i+1}/{len(lista)}] Traduzido: {desc_str} -> {traduzido}")
            time.sleep(0.5)  # meio segundo de pausa entre traduções
    return lista

# Programa principal
if __name__ == "__main__":
    try:
        # Carregar JSON original
        with open("Furnituredata.json", "r", encoding="utf-8") as f:
            local_data = json.load(f)

        # Traduzir as descrições
        if "roomitemtypes" in local_data and "furnitype" in local_data["roomitemtypes"]:
            local_data["roomitemtypes"]["furnitype"] = traduzir_descriptions_bloco(
                local_data["roomitemtypes"]["furnitype"]
            )

        # Salvar em novo arquivo
        with open("Furnituredata_traduzido.json", "w", encoding="utf-8") as f:
            json.dump(local_data, f, ensure_ascii=False, indent=4)

        print("\n✅ Tradução concluída! Arquivo salvo como 'Furnituredata_traduzido.json'.")

    except FileNotFoundError:
        print("❌ Erro: O arquivo 'Furnituredata.json' não foi encontrado na pasta atual.")
    except json.JSONDecodeError:
        print("❌ Erro: O arquivo JSON está corrompido ou mal formatado.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
