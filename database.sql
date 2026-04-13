-- ============================================
-- PETSHOP - Script de criação do banco de dados
-- ============================================

CREATE DATABASE IF NOT EXISTS petshop_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE petshop_db;

-- ----------------------------
-- Tabela: funcionarios
-- ----------------------------
CREATE TABLE IF NOT EXISTS funcionarios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    cargo       VARCHAR(50)  NOT NULL,
    telefone    VARCHAR(20),
    email       VARCHAR(100) UNIQUE,
    ativo       TINYINT(1)   NOT NULL DEFAULT 1,
    criado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Tabela: clientes
-- ----------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    cpf         VARCHAR(14)  UNIQUE,
    telefone    VARCHAR(20)  NOT NULL,
    email       VARCHAR(100),
    endereco    VARCHAR(200),
    criado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------
-- Tabela: pets
-- ----------------------------
CREATE TABLE IF NOT EXISTS pets (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    especie     VARCHAR(50)  NOT NULL,
    raca        VARCHAR(100),
    idade       INT,
    peso        DECIMAL(5,2),
    cliente_id  INT          NOT NULL,
    criado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- ----------------------------
-- Tabela: servicos
-- ----------------------------
CREATE TABLE IF NOT EXISTS servicos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    descricao   TEXT,
    preco       DECIMAL(10,2) NOT NULL,
    duracao_min INT          NOT NULL DEFAULT 60,
    ativo       TINYINT(1)   NOT NULL DEFAULT 1
);

-- ----------------------------
-- Tabela: agendamentos
-- ----------------------------
CREATE TABLE IF NOT EXISTS agendamentos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    pet_id          INT          NOT NULL,
    servico_id      INT          NOT NULL,
    funcionario_id  INT,
    data_hora       DATETIME     NOT NULL,
    status          ENUM('agendado','concluido','cancelado') NOT NULL DEFAULT 'agendado',
    observacoes     TEXT,
    criado_em       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pet_id)         REFERENCES pets(id)         ON DELETE CASCADE,
    FOREIGN KEY (servico_id)     REFERENCES servicos(id)     ON DELETE RESTRICT,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE SET NULL
);

-- ----------------------------
-- Dados iniciais de exemplo
-- ----------------------------
INSERT INTO funcionarios (nome, cargo, telefone, email) VALUES
    ('Ana Costa',   'Tosadora',     '(11) 91111-1111', 'ana@petshop.com'),
    ('Bruno Lima',  'Banhista',     '(11) 92222-2222', 'bruno@petshop.com'),
    ('Carla Souza', 'Veterinária',  '(11) 93333-3333', 'carla@petshop.com');

INSERT INTO servicos (nome, descricao, preco, duracao_min) VALUES
    ('Banho Simples',       'Banho completo com secagem',                  45.00,  60),
    ('Banho + Tosa',        'Banho completo e tosa higiênica ou na tesoura', 80.00, 90),
    ('Tosa Higiênica',      'Limpeza de patas, barriga e região íntima',   35.00,  30),
    ('Consulta Veterinária','Consulta clínica geral',                     120.00,  30),
    ('Hidratação',          'Hidratação profunda dos pelos',               60.00,  45);

INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES
    ('João Silva',   '111.222.333-44', '(11) 98888-0001', 'joao@email.com',  'Rua das Flores, 10'),
    ('Maria Oliveira','222.333.444-55','(11) 98888-0002', 'maria@email.com', 'Av. Central, 200');

INSERT INTO pets (nome, especie, raca, idade, peso, cliente_id) VALUES
    ('Rex',    'Cachorro', 'Labrador',   3, 28.5, 1),
    ('Mia',    'Gato',     'Siamês',     2,  4.2, 2),
    ('Bolinha', 'Cachorro', 'Poodle',    5,  6.0, 1);