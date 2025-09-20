CREATE TABLE Dim_Tempo (
    sk_tempo INT AUTO_INCREMENT PRIMARY KEY,
    data_completa DATETIME NOT NULL UNIQUE,
    dia INT NOT NULL,
    mes INT NOT NULL,
    ano INT NOT NULL,
    semana INT NOT NULL,
    dia_da_semana VARCHAR(20) NOT NULL,
    hora INT NOT NULL,
    minuto INT NOT NULL
);

CREATE TABLE Dim_Autor (
    sk_autor INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(255) NOT NULL UNIQUE,
    seguidores INT
);

CREATE TABLE Dim_Tema (
    sk_tema INT AUTO_INCREMENT PRIMARY KEY,
    hashtag VARCHAR(255) NOT NULL UNIQUE,
    categoria_geral VARCHAR(100)
);

CREATE TABLE Fato_EngajamentoPosts (
    id_fato INT AUTO_INCREMENT PRIMARY KEY,
    fk_tempo INT NOT NULL,
    fk_autor INT NOT NULL,
    fk_tema INT NOT NULL,
    curtidas INT,
    comentarios INT,
    compartilhamentos INT,
    url_post VARCHAR(500) UNIQUE,
    FOREIGN KEY (fk_tempo) REFERENCES Dim_Tempo(sk_tempo),
    FOREIGN KEY (fk_autor) REFERENCES Dim_Autor(sk_autor),
    FOREIGN KEY (fk_tema) REFERENCES Dim_Tema(sk_tema)
);