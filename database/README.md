# Database

- `migrations/001_init.sql`: esquema inicial com entidades de governança, IA, auditoria e RBAC.
- `seeds/001_seed.sql`: dados fictícios para ambiente de demonstração.

## Apply local
```bash
psql -h localhost -U board_user -d board_os -f database/migrations/001_init.sql
psql -h localhost -U board_user -d board_os -f database/seeds/001_seed.sql
```

