# Argon Vault

## O Argon Vault é um gerenciador de credenciais seguro projetado para oferecer uma interface intuitiva sem comprometer a integridade dos dados. O projeto utiliza uma arquitetura Zero-Knowledge, onde o servidor nunca tem acesso à senha mestre do usuário em texto puro, garantindo privacidade total.

* Segurança Avançada: Implementação de hashing com Argon2 (vencedor do Password Hashing Competition) para proteção contra ataques de força bruta.

* Comunicação Assíncrona: Interface dinâmica utilizando JavaScript Fetch API para criação e exclusão de registros sem recarregamento de página (SPA feeling).

* Arquitetura Robusta: Backend em Python/Flask com integração ao banco de dados SQLite via SQLAlchemy.

* Proteção de Sessão: Implementação de tokens CSRF e gerenciamento de sessões seguras para prevenir ataques comuns da web.