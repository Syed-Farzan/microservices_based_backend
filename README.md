# Microservices Backend Assignment

A microservices-based system consisting of an API Gateway, User Service, and Notification Service, using NATS JetStream for secure, reliable, and asynchronous event-driven communication.

## Architecture Diagram

```mermaid
graph TD
    Client(Client / Postman) -->|HTTP POST :8080/api/users| Gateway(API Gateway)
    Gateway -->|HTTP POST Internal| UserService(User Service)
    UserService -.->|Publish 'user.created' event| NATS(NATS JetStream Message Broker)
    NATS -.->|Push event to durable subscriber| NotificationService(Notification Service)
    NotificationService -->|Acknowledge Message| NATS
```
