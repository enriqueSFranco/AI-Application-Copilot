Base de datos

## Entidades
Users
- user_id (PK)
- name
- email (UQ)
- password

Vacancies
- vacancy_id (PK)
- title
- company
- location
- salary
- description
- url
- skills String[]
- seniority
- createdAt

Applications
- application_id (PK)
- user_id (FK)
- vacancy_id (FK)
- messages json (application, follow, reply)
- status Enum | Catalogo
- created_date
- updated_at

Notes
- note_id (PK)
- content
- application_id (FK)
- created_at

Companies
- company_id (PK)
- name

Classifications
- classification_id (PK)
- classification_name

## Catalogos
Application_Status
- CV sent
- viewed
- interview
- hired
- rejected