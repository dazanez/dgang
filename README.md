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

| Microservicio            | Funcionalidad                                    |
| ------------------------ | ------------------------------------------------ |
| **API Gateway**          | Entrada única para peticiones externas.          |
| **Auth Service**         | Registro, login y autenticación de usuarios.     |
| **User Group Service**   | Gestión de grupos privados y miembros.           |
| **Validation Service**   | Validación de respuestas para ingresar a grupos. |
| **Media Feed Service**   | Gestión de publicaciones de fotos.               |
| **Notification Service** | Programación de notificaciones diarias.          |

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
- [x] Implementación de Auth Service
- [x] Implementación de User Group Service
- [x] Implementación de Media Feed Service
- [ ] Simulación de notificaciones diarias
- [ ] Despliegue en un servidor de pruebas

---

## 🧠 ¿Por qué usamos microservicios?

Desde el inicio, sabíamos que nuestra app tenía varias funcionalidades diferentes que queríamos manejar con orden y que probablemente iban a crecer con el tiempo. Por eso, decidimos usar una arquitectura basada en microservicios. Acá explicamos por qué creemos que fue una buena decisión:

### 🧩 1. Separación de responsabilidades

Cada parte de la app hace cosas distintas: registrar usuarios, crear grupos, validar miembros con preguntas, subir fotos, mandar notificaciones… En lugar de tener todo mezclado, preferimos separar cada funcionalidad en su propio microservicio. Así es más fácil desarrollar, mantener y entender cada módulo.

### 🚀 2. Escalabilidad independiente

No todos los servicios van a tener la misma carga. Por ejemplo, cuando suena el “reto diario” y todos suben su foto, el microservicio de publicaciones puede necesitar más recursos, mientras que otros no. Con microservicios, podemos escalar solo esa parte sin afectar el resto.

### 🔧 3. Mantenimiento y cambios más simples

Si en el futuro queremos agregar nuevas formas de validación para entrar a un grupo, o cambiar cómo se guardan las imágenes, solo tendríamos que modificar un servicio, no toda la aplicación. Eso nos da más libertad y evita romper cosas sin querer.

### 🧪 4. Uso de diferentes tecnologías

Ya empezamos usando Flask para algunos servicios, pero también nos gustaría experimentar con Node.js o Spring Boot. Como cada servicio es independiente, podemos usar la tecnología que nos parezca mejor en cada caso, sin que eso genere problemas.

### ⚡ 5. Resistencia a fallos

Si por alguna razón el servicio de notificaciones se cae, igual se puede seguir usando la app: los usuarios pueden seguir entrando, creando grupos y subiendo fotos. Esto hace que la aplicación sea más robusta.

### 🔮 6. Pensando a futuro

Si algún día la app crece, podríamos agregar más funciones, como sugerencias de grupos, filtros de contenido, planes premium, etc. Con esta arquitectura, eso es mucho más fácil de manejar.

---

En resumen, decidimos trabajar con microservicios porque nos permite construir una app más organizada, escalable y preparada para crecer, tanto en usuarios como en funcionalidades. Creemos que fue una decisión clave para hacer realidad lo que nos imaginamos desde el principio.

## 🤝 Contribuciones

Este proyecto es parte de un trabajo académico, pero si tienes sugerencias o quieres aportar mejoras, ¡serán bien recibidas!
