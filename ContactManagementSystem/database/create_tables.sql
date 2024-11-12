CREATE TABLE Contato (
    id_contato INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data_aniversario DATE NOT NULL,
    sexo TEXT NOT NULL,
    profissao TEXT
);

CREATE TABLE Telefone (
    id_telefone INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    tipo TEXT NOT NULL,
    id_contato INTEGER,
    FOREIGN KEY (id_contato) REFERENCES Contato(id_contato)
);

CREATE TABLE Endereco (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    logradouro TEXT NOT NULL,
    numero TEXT NOT NULL,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    cep TEXT NOT NULL,
    id_contato INTEGER,
    FOREIGN KEY (id_contato) REFERENCES Contato(id_contato)
);
