# IUTMtpEdt
[fr] Emploi du temps pour l'IUT Info de Montpellier

## Stack

La stack se base sur 3 containers et un 4ème optionnel

- mariadb, pour stocker toutes nos données
- php-nginx, pour le site
- un container custom pour le scrapper
- adminer, un outil pour manager la base de donnée (comme phpmyadmin)

### Comment la déployer

1. Déployez la stack comme vous le feriez normalement (`docker compose up -d` par ex)
2. Connectez vous sur la base de donnée (adminer ou client quelconque) et executez le contenu de `./php/config/default.sql`
3. Amusez-vous !