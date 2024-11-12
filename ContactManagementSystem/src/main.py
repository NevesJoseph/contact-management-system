import sqlite3
import pandas as pd
import unicodedata
from db_utils import execute_query, get_connection

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def inserir_contato(nome, data_aniversario, sexo, profissao, telefones, logradouro, numero, bairro, cidade, estado, cep):
    nome = normalize_text(nome)
    profissao = normalize_text(profissao)
    logradouro = normalize_text(logradouro)
    bairro = normalize_text(bairro)
    cidade = normalize_text(cidade)
    estado = normalize_text(estado)
    cep = normalize_text(cep)

    # Verificar se o contato já existe para evitar duplicidades
    query_check = '''
    SELECT COUNT(*) FROM Contato
    WHERE nome = ? AND data_aniversario = ? AND sexo = ? AND profissao = ?
    '''
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query_check, (nome, data_aniversario, sexo, profissao))
        count = cursor.fetchone()[0]
    
    if count == 0:
        query_insert_contato = '''
        INSERT INTO Contato (nome, data_aniversario, sexo, profissao)
        VALUES (?, ?, ?, ?)
        '''
        execute_query(query_insert_contato, (nome, data_aniversario, sexo, profissao))
        
        # Obter o id do contato recém-inserido
        cursor.execute('SELECT last_insert_rowid()')
        id_contato = cursor.fetchone()[0]
        
        # Inserir telefones
        for telefone in telefones:
            query_insert_telefone = '''
            INSERT INTO Telefone (numero, tipo, id_contato)
            VALUES (?, 'celular', ?)
            '''
            execute_query(query_insert_telefone, (telefone, id_contato))
        
        # Inserir endereço
        query_insert_endereco = '''
        INSERT INTO Endereco (logradouro, numero, bairro, cidade, estado, cep, id_contato)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        execute_query(query_insert_endereco, (logradouro, numero, bairro, cidade, estado, cep, id_contato))
        
        print(f"Contato '{nome}' inserido com sucesso.")
    else:
        print(f"Contato '{nome}' já existe e não foi inserido novamente.")

def consultar_contatos():
    query = '''
    SELECT C.id_contato, C.nome, C.data_aniversario, C.sexo, C.profissao,
           GROUP_CONCAT(T.numero) AS telefones,
           E.logradouro || ', ' || E.numero || ', ' || E.bairro || ', ' || E.cidade || ', ' || E.estado || ', ' || E.cep AS endereco
    FROM Contato C
    LEFT JOIN Telefone T ON C.id_contato = T.id_contato
    LEFT JOIN Endereco E ON C.id_contato = E.id_contato
    GROUP BY C.id_contato
    '''
    with get_connection() as conn:
        # Usando pandas para carregar dados diretamente em um DataFrame
        df = pd.read_sql_query(query, conn)
        return df

def remover_contato(id_contato):
    query_delete_telefone = 'DELETE FROM Telefone WHERE id_contato = ?'
    execute_query(query_delete_telefone, (id_contato,))
    
    query_delete_endereco = 'DELETE FROM Endereco WHERE id_contato = ?'
    execute_query(query_delete_endereco, (id_contato,))
    
    query_delete_contato = 'DELETE FROM Contato WHERE id_contato = ?'
    execute_query(query_delete_contato, (id_contato,))
    
def atualizar_contato(id_contato, nome=None, data_aniversario=None, sexo=None, profissao=None,
                      telefones=None, logradouro=None, numero=None,
                      bairro=None, cidade=None, estado=None, cep=None):
    
    if nome:
        nome = normalize_text(nome)
        query_update_nome = 'UPDATE Contato SET nome = ? WHERE id_contato = ?'
        execute_query(query_update_nome, (nome, id_contato))
    
    if data_aniversario:
        query_update_data_aniversario = 'UPDATE Contato SET data_aniversario = ? WHERE id_contato = ?'
        execute_query(query_update_data_aniversario, (data_aniversario, id_contato))
    
    if sexo:
        query_update_sexo = 'UPDATE Contato SET sexo = ? WHERE id_contato = ?'
        execute_query(query_update_sexo, (sexo, id_contato))
    
    if profissao:
        profissao = normalize_text(profissao)
        query_update_profissao = 'UPDATE Contato SET profissao = ? WHERE id_contato = ?'
        execute_query(query_update_profissao, (profissao, id_contato))
    
    if telefones:
        query_delete_telefones = 'DELETE FROM Telefone WHERE id_contato = ?'
        execute_query(query_delete_telefones, (id_contato,))
        
        for telefone in telefones:
            query_insert_telefone = '''
            INSERT INTO Telefone (numero, tipo, id_contato)
            VALUES (?, 'celular', ?)
            '''
            execute_query(query_insert_telefone, (telefone, id_contato))
    
    if logradouro or numero or bairro or cidade or estado or cep:
        if logradouro:
            logradouro = normalize_text(logradouro)
            query_update_logradouro = 'UPDATE Endereco SET logradouro = ? WHERE id_contato = ?'
            execute_query(query_update_logradouro, (logradouro, id_contato))
        
        if numero:
            query_update_numero = 'UPDATE Endereco SET numero = ? WHERE id_contato = ?'
            execute_query(query_update_numero, (numero, id_contato))
        
        if bairro:
            bairro = normalize_text(bairro)
            query_update_bairro = 'UPDATE Endereco SET bairro = ? WHERE id_contato = ?'
            execute_query(query_update_bairro, (bairro, id_contato))
        
        if cidade:
            cidade = normalize_text(cidade)
            query_update_cidade = 'UPDATE Endereco SET cidade = ? WHERE id_contato = ?'
            execute_query(query_update_cidade, (cidade, id_contato))
        
        if estado:
            estado = normalize_text(estado)
            query_update_estado = 'UPDATE Endereco SET estado = ? WHERE id_contato = ?'
            execute_query(query_update_estado, (estado, id_contato))
        
        if cep:
            cep = normalize_text(cep)
            query_update_cep = 'UPDATE Endereco SET cep = ? WHERE id_contato = ?'
            execute_query(query_update_cep, (cep, id_contato))

def lembretes_aniversarios():
    query = '''
    SELECT nome, data_aniversario
    FROM Contato
    WHERE strftime('%m-%d', data_aniversario) = strftime('%m-%d', 'now')
    '''
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn)
        return df

if __name__ == "__main__":
    # Exemplo de inserção e consulta
    inserir_contato('José Andrade', '1999-12-07', 'masculino', 'Estudante', ['1234-5678', '9876-5432'], 'Rua das Flores', '100', 'Centro', 'São Paulo', 'SP', '01000-000')
    
    contatos = consultar_contatos()
    # Exibindo os contatos em formato tabular
    print("Contatos:")
    print(contatos)
    
    # Exemplo de lembretes de aniversários
    aniversariantes = lembretes_aniversarios()
    print("\nAniversariantes de hoje:")
    print(aniversariantes)

    # Remoção de contato opcional
    remover_id = input("\nDigite o ID do contato que deseja remover (ou pressione Enter para pular): ")
    if remover_id:
        remover_contato(int(remover_id))
        
        contatos = consultar_contatos()
        print("\nContatos após a remoção:")
        print(contatos)

    # Atualização de contato opcional
    atualizar_id = input("\nDigite o ID do contato que deseja atualizar (ou pressione Enter para pular): ")
    if atualizar_id:
        atualizar_contato(int(atualizar_id), nome='José Silva', telefones=['1111-2222', '3333-4444'], cidade='Rio de Janeiro')
        
        contatos = consultar_contatos()
        print("\nContatos após a atualização:")
        print(contatos)
