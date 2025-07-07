PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- Tabla de disponibilidad de servicios
CREATE TABLE IF NOT EXISTS disponibilidad_servicio (
    id_disponibilidad_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL
);

-- Tabla de estados de pago
CREATE TABLE IF NOT EXISTS estados_pago (
    id_estados_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL
);

-- Tabla de estados de reserva
CREATE TABLE IF NOT EXISTS estados_reserva (
    id_estados_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL
);

-- Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id_roles INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL UNIQUE
);

-- Tabla de tipos de servicio
CREATE TABLE IF NOT EXISTS tipos_servicio (
    id_tipos_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL
);

-- Tabla de tipos de usuario
CREATE TABLE IF NOT EXISTS tipos_usuario (
    id_tipos_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuarios INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    contrasena TEXT,
    telefono TEXT NOT NULL UNIQUE,
    tipos_usuario_id INTEGER NOT NULL,
    imagen TEXT(255),
    FOREIGN KEY (tipos_usuario_id) REFERENCES tipos_usuario(id_tipos_usuario)
);

-- Tabla de servicios
CREATE TABLE IF NOT EXISTS servicios (
    id_servicios INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    precio REAL NOT NULL,
    ubicacion TEXT NOT NULL,
    tipos_servicio_id INTEGER NOT NULL,
    usuarios_proveedores_id INTEGER NOT NULL,
    disponibilidad_servicio_id INTEGER NOT NULL,
    imagen TEXT,
    FOREIGN KEY (tipos_servicio_id) REFERENCES tipos_servicio(id_tipos_servicio),
    FOREIGN KEY (usuarios_proveedores_id) REFERENCES usuarios(id_usuarios),
    FOREIGN KEY (disponibilidad_servicio_id) REFERENCES disponibilidad_servicio(id_disponibilidad_servicio)
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id_reservas INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_creacion_reserva TEXT NOT NULL,
    fecha_inicio_reserva TEXT NOT NULL,
    fecha_fin_reserva TEXT NOT NULL,
    servicios_id INTEGER NOT NULL,
    estados_reserva_id INTEGER NOT NULL,
    
    CONSTRAINT reservas_servicios_id_servicios_id_servicios_fk
        FOREIGN KEY (servicios_id)
        REFERENCES servicios(id_servicios),
    
    CONSTRAINT reservas_estados_reserva_id_estados_reserva_id_estados_reserva_fk
        FOREIGN KEY (estados_reserva_id)
        REFERENCES estados_reserva(id_estados_reserva)
);

-- Tabla de pagos
CREATE TABLE IF NOT EXISTS pagos (
    id_pagos INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_pago TEXT NOT NULL,
    monto REAL NOT NULL,
    reservas_id INTEGER NOT NULL,
    estados_pago_id INTEGER NOT NULL,
    usuarios_id INTEGER NOT NULL,
    FOREIGN KEY (reservas_id) REFERENCES reservas(id_reservas),
    FOREIGN KEY (estados_pago_id) REFERENCES estados_pago(id_estados_pago),
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id_usuarios)
);

-- Tabla de relación usuarios-roles
CREATE TABLE IF NOT EXISTS usuarios_tiene_roles (
    id_usuarios_tiene_roles INTEGER PRIMARY KEY AUTOINCREMENT,
    usuarios_id INTEGER NOT NULL,
    roles_id INTEGER NOT NULL,
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id_usuarios),
    FOREIGN KEY (roles_id) REFERENCES roles(id_roles)
);

-- Tabla de valoraciones
CREATE TABLE IF NOT EXISTS valoraciones (
    id_valoraciones INTEGER PRIMARY KEY AUTOINCREMENT,
    puntuacion INTEGER NOT NULL,
    comentario TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL,
    servicios_id INTEGER NOT NULL,
    usuarios_id INTEGER NOT NULL,
    FOREIGN KEY (servicios_id) REFERENCES servicios(id_servicios),
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id_usuarios)
);

-- Tabla de preguntas
CREATE TABLE IF NOT EXISTS preguntas (
    id_preguntas INTEGER PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta TEXT,
    fecha_pregunta NUMERIC NOT NULL,
    fecha_respuesta NUMERIC,
    servicios_id INTEGER NOT NULL,
    usuarios_pregunta_id INTEGER NOT NULL,
    usuarios_respuesta_id INTEGER,

    CONSTRAINT preguntas_servicios_id_servicios_id_servicios_fk
        FOREIGN KEY (servicios_id)
        REFERENCES servicios(id_servicios),

    CONSTRAINT preguntas_usuarios_pregunta_id_usuarios_id_usuarios_fk
        FOREIGN KEY (usuarios_pregunta_id)
        REFERENCES usuarios(id_usuarios),

    CONSTRAINT preguntas_usuarios_respuesta_id_usuarios_id_usuarios_fk
        FOREIGN KEY (usuarios_respuesta_id)
        REFERENCES usuarios(id_usuarios)
);

COMMIT;