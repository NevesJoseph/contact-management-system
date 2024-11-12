SELECT C.id_contato, C.nome, C.data_aniversario, C.sexo, C.profissao,
       GROUP_CONCAT(T.numero) AS telefones,
       E.logradouro || ', ' || E.numero || ', ' || E.bairro || ', ' || E.cidade || ', ' || E.estado || ', ' || E.cep AS endereco
FROM Contato C
LEFT JOIN Telefone T ON C.id_contato = T.id_contato
LEFT JOIN Endereco E ON C.id_contato = E.id_contato
GROUP BY C.id_contato;
