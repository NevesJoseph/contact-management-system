# Gerenciamento de Contatos

Este projeto implementa um sistema de gerenciamento de contatos utilizando SQLite e Python.

## Estrutura do Projeto

- `database/` - Contém o banco de dados SQLite e os scripts de criação.
- `src/` - Contém os scripts Python para manipulação do banco.
- `sql/` - Scripts SQL de inserção de dados e consultas.

## Configuração

1. Crie o banco de dados e as tabelas:
   ```bash
   sqlite3 database/gerenciamento_contatos.db < database/create_tables.sql
