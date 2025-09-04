import time
import pymysql
from deep_translator import GoogleTranslator

# Configurações do banco
DB_CONFIG = {
    "host": "localhost",       # ou IP do seu servidor MySQL
    "user": "root",            # seu usuário
    "password": "", # sua senha
    "database": "",
    "charset": "utf8mb4"
}

# Idioma alvo da tradução
IDIOMA_DESTINO = "fr"  # mude para "es", "pt", etc.

# Função segura para traduzir texto
def traduzir_texto(texto):
    if not texto or texto.strip() == "":
        return texto
    try:
        return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
    except Exception as e:
        print(f"⚠ Erro ao traduzir: {e}, tentando novamente...")
        time.sleep(2)
        try:
            return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
        except Exception as e2:
            print(f"❌ Falha final: {e2}. Mantendo original.")
            return texto

def traduzir_catalog_items():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id, catalog_name FROM catalog_items")
    rows = cursor.fetchall()

    print(f"🔍 {len(rows)} linhas encontradas na tabela catalog_items")

    for i, row in enumerate(rows, start=1):
        id_item = row["id"]
        catalog_name_traduzido = traduzir_texto(row["catalog_name"])

        cursor.execute("""
            UPDATE catalog_items
            SET catalog_name = %s
            WHERE id = %s
        """, (catalog_name_traduzido, id_item))

        print(f"[{i}/{len(rows)}] ID {id_item} traduzido ✅")

        # Salva no banco a cada linha (para evitar perder progresso se travar)
        conn.commit()
        time.sleep(0.5)

    cursor.close()
    conn.close()
    print("🎉 Tradução concluída com sucesso!")

if __name__ == "__main__":
    traduzir_catalog_items()
