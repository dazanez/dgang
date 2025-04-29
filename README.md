# Dgang! for Friends - Proyecto de Ingeniería de Software

Una aplicación de tipo **BeReal privado** que fortalece la conexión entre grupos de amigos, utilizando una arquitectura basada en **microservicios**.

---

## 📖 Descripción

**Dgang!** permite a los miembros de un grupo privado compartir un momento de su día a través de fotos, activado por una alerta diaria.  
Para ingresar a un grupo, los nuevos usuarios deben demostrar su cercanía respondiendo correctamente a preguntas secretas establecidas por los miembros existentes.

El enfoque principal del proyecto es demostrar el uso de **microservicios** como base de una aplicación moderna y escalable.

---

## 🎯 Funcionalidades del MVP

- Registro y autenticación de usuarios (JWT).
- Creación de grupos privados de amigos.
- Validación de nuevos miembros mediante preguntas personalizadas.
- Notificaciones diarias simuladas para capturar el momento.
- Subida y visualización de fotos diarias en el feed del grupo.

---

## 🛠️ Arquitectura

La aplicación está compuesta por varios microservicios independientes:

| Microservicio        | Funcionalidad                                     |
|----------------------|---------------------------------------------------|
| **API Gateway**       | Entrada única para peticiones externas.          |
| **Auth Service**      | Registro, login y autenticación de usuarios.     |
| **User Group Service**| Gestión de grupos privados y miembros.           |
| **Validation Service**| Validación de respuestas para ingresar a grupos. |
| **Media Feed Service**| Gestión de publicaciones de fotos.               |
| **Notification Service**| Programación de notificaciones diarias.       |

Cada microservicio tiene su propia base de datos y se comunica mediante **REST APIs**.

**Tecnologías utilizadas:**
- Backend: Node.js (Express) / Alternativamente Spring Boot (Java)
- Bases de datos: PostgreSQL o MongoDB
- Contenerización: Docker
- Comunicación: REST
- Orquestación local: Docker Compose

---

## 📦 Estructura del repositorio

```bash
be-real-for-friends/
│
├── gateway/                # API Gateway
├── auth-service/           # Servicio de autenticación
├── user-group-service/     # Servicio de grupos
├── validation-service/     # Servicio de validaciones
├── media-feed-service/     # Servicio de publicaciones
├── notification-service/   # Servicio de notificaciones
├── docker-compose.yml      # Orquestación de servicios
├── README.md               # Este archivo
└── docs/                   # Documentación adicional (diagramas, especificaciones)
```

---

## 🚀 Cómo levantar el proyecto (modo desarrollo)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/be-real-for-friends.git
   cd be-real-for-friends
   ```

2. Construir y levantar los contenedores:
   ```bash
   docker-compose up --build
   ```

3. Acceder a la aplicación a través del API Gateway (por ejemplo en `http://localhost:8080`).

---

## 📈 Estado del proyecto

- [x] Definición de la arquitectura
- [x] Configuración de microservicios base
- [ ] Implementación de Auth Service
- [ ] Implementación de User Group Service
- [ ] Implementación de Media Feed Service
- [ ] Simulación de notificaciones diarias
- [ ] Despliegue en un servidor de pruebas

---

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico, pero si tienes sugerencias o quieres aportar mejoras, ¡serán bien recibidas!
