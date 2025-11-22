import time
import os
import pymysql
from deep_translator import GoogleTranslator

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": ",
    "charset": "utf8mb4"
}

IDIOMA_DESTINO = "pt"
CHECKPOINT_FILE = "checkpoint.txt"


# --------------------------------------------------------------------
# Carregar checkpoint
# --------------------------------------------------------------------
def carregar_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return 0
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0


# Salvar checkpoint
def salvar_checkpoint(last_id):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(last_id))


# --------------------------------------------------------------------
# Tradução segura individual
# --------------------------------------------------------------------
def traduzir_texto(texto):
    if not texto or texto.strip() == "":
        return texto
    try:
        return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
    except Exception:
        time.sleep(1)
        try:
            return GoogleTranslator(source="auto", target=IDIOMA_DESTINO).translate(str(texto))
        except Exception:
            return texto


# --------------------------------------------------------------------
# Tradução segura para textos longos (MEMO/LONGTEXT)
# --------------------------------------------------------------------
def traduzir_texto_longo(texto, max_chars=4500):
    if not texto or texto.strip() == "":
        return texto

    if len(texto) <= max_chars:
        return traduzir_texto(texto)

    partes = []
    inicio = 0
    while inicio < len(texto):
        partes.append(texto[inicio:inicio + max_chars])
        inicio += max_chars

    partes_traduzidas = []
    for parte in partes:
        partes_traduzidas.append(traduzir_texto(parte))
        time.sleep(0.3)

    return "".join(partes_traduzidas)


# --------------------------------------------------------------------
# Tradução em lista (batch) — exceto campos longos
# --------------------------------------------------------------------
def traduzir_lista(lista_textos):
    textos_validos = [t if t else "" for t in lista_textos]

    try:
        tradutor = GoogleTranslator(source="auto", target=IDIOMA_DESTINO)
        return tradutor.translate_batch(textos_validos)
    except Exception:
        # fallback 1 a 1
        return [traduzir_texto(t) for t in textos_validos]


# --------------------------------------------------------------------
# Processar catálogo com checkpoint
# --------------------------------------------------------------------
def traduzir_catalogo():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id, caption, page_text1, page_text_details FROM catalog_pages ORDER BY id ASC")
    rows = cursor.fetchall()

    total = len(rows)
    print(f"🔍 {total} linhas encontradas")

    ultimo_processado = carregar_checkpoint()
    print(f"⏩ Continuando a partir do ID > {ultimo_processado}")

    bloco_tamanho = 20

    # Filtrar linhas já processadas
    rows = [r for r in rows if r["id"] > ultimo_processado]

    if not rows:
        print("✅ Nada para traduzir. Tudo já está concluído.")
        return

    for inicio in range(0, len(rows), bloco_tamanho):
        bloco = rows[inicio:inicio + bloco_tamanho]

        ids = [r["id"] for r in bloco]
        captions = [r["caption"] for r in bloco]
        page_text1 = [r["page_text1"] for r in bloco]
        page_text_details = [r["page_text_details"] for r in bloco]

        print(f"▶ Traduzindo bloco: IDs {ids[0]} até {ids[-1]}")

        # Tradução dos captions e text1 usando batch
        captions_trad = traduzir_lista(captions)

        # Campos longos (MEMO) traduzir sempre individual
        page_text1_trad = [traduzir_texto_longo(t) for t in page_text1]
        page_text_details_trad = [traduzir_texto_longo(t) for t in page_text_details]

        # Atualizar banco
        for i, id_page in enumerate(ids):
            cursor.execute("""
                UPDATE catalog_pages
                SET caption = %s,
                    page_text1 = %s,
                    page_text_details = %s
                WHERE id = %s
            """, (
                captions_trad[i],
                page_text1_trad[i],
                page_text_details_trad[i],
                id_page
            ))

        conn.commit()

        # salvar checkpoint do último ID do bloco
        salvar_checkpoint(ids[-1])
        print(f"💾 Checkpoint salvo: {ids[-1]}")
        print(f"✅ Bloco concluído.\n")

        time.sleep(1)

    cursor.close()
    conn.close()
    print("🎉 Tradução concluída com sucesso!")


if __name__ == "__main__":
    traduzir_catalogo()
