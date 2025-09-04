Habbo Catalog Translator

Este projeto é um conjunto de scripts em Python para traduzir automaticamente os itens e páginas do catálogo do Habbo Hotel. Ele suporta a tradução de nomes, descrições e textos de páginas usando a API do Google Translator.

Os scripts foram feitos para lidar com grandes quantidades de dados, salvando o progresso automaticamente e permitindo retomar a tradução caso o processo seja interrompido.

Funcionalidades

Tradução de nomes e descrições do arquivo Furnituredata.json.

Tradução de páginas do catálogo (catalog_pages) no banco de dados MySQL.

Tradução de itens do catálogo (catalog_items) no banco de dados MySQL.

Retomada automática da tradução em caso de falha.

Tratamento seguro de erros e tentativas de nova tradução.

Registro do progresso no console.

No caso do Furnituredata.json, o script procura o arquivo na mesma pasta onde ele está sendo executado. Então basta:

Colocar o arquivo Furnituredata.json dentro da pasta do projeto (onde está o script translactor_name.py).

Executar o script normalmente.

O script vai criar automaticamente um backup do arquivo original e gerar um novo arquivo traduzido (Furnituredata_traduzido.json).


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                              English Version
Habbo Catalog Translator

This project is a set of Python scripts to automatically translate Habbo Hotel catalog items and pages. It supports translating names, descriptions, and page texts using the Google Translator API.

The scripts are designed to handle large amounts of data, automatically saving progress and allowing translation to resume if the process is interrupted.

Features

Translation of names and descriptions in the Furnituredata.json file.

Translation of catalog pages (catalog_pages) in the MySQL database.

Translation of catalog items (catalog_items) in the MySQL database.

Automatic resumption of translation in case of failure.

Safe error handling with retries for failed translations.

Progress logging in the console.

For the Furnituredata.json file, the script looks for the file in the same folder where it is executed. So you just need to:

Place the Furnituredata.json file inside the project folder (where the translactor_name.py script is located).

Run the script normally.

The script will automatically create a backup of the original file and generate a new translated file (Furnituredata_traduzido.json).
