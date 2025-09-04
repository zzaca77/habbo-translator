import time
import pymysql
from deep_translator import GoogleTranslator

# Configurações do banco
DB_CONFIG = {
    "host": "localhost",      # ou IP do seu servidor MySQL
    "user": "root",           # seu usuário
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

def traduzir_catalogo():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id, caption, page_text1, page_text_details FROM catalog_pages")
    rows = cursor.fetchall()

    print(f"🔍 {len(rows)} linhas encontradas na tabela catalog_pages")

    for i, row in enumerate(rows, start=1):
        id_page = row["id"]
        caption = traduzir_texto(row["caption"])
        page_text1 = traduzir_texto(row["page_text1"])
        page_text_details = traduzir_texto(row["page_text_details"])

        cursor.execute("""
            UPDATE catalog_pages
            SET caption = %s, page_text1 = %s, page_text_details = %s
            WHERE id = %s
        """, (caption, page_text1, page_text_details, id_page))

        print(f"[{i}/{len(rows)}] ID {id_page} traduzido ✅")

        # Salva no banco a cada linha (para evitar perder progresso se travar)
        conn.commit()
        time.sleep(0.5)

    cursor.close()
    conn.close()
    print("🎉 Tradução concluída com sucesso!")

if __name__ == "__main__":
    traduzir_catalogo()
