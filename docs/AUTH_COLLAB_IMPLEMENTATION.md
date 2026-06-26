# Implémentation : Authentification et Collaboration (Parties 3 & 4)

## Plan d'implémentation (Étape par étape)

### Phase 1 : Backend (FastAPI)
1. **Modèles & Base de données** :
   - Ajout du champ `assignee_id` à la table `todos` (clé étrangère vers `users.id`).
   - Mise à jour de la relation SQLAlchemy `assignee`.
2. **Endpoints & Sécurité** :
   - Création des endpoints `/login` et `/register`.
   - Ajout du décorateur `Depends(get_current_active_user)` pour protéger les routes `/todos`.
3. **Logique Métier (CRUD)** :
   - Mise à jour de la fonction `create_todo` pour associer l'ID du créateur connecté (`owner_id`).
   - Modification de `get_todos` pour ne retourner que les tâches dont l'utilisateur est le propriétaire ou l'assigné.
4. **Schémas Pydantic** :
   - Intégration de `assignee_id` dans `TodoBase`.
   - Intégration des objets complets `owner` et `assignee` dans `TodoResponse`.

### Phase 2 : Frontend (SvelteKit)
1. **Gestion de l'état global** :
   - Mise en place d'un store global Svelte (`auth.ts`) pour persister le JWT et les infos de l'utilisateur.
2. **Interface d'Authentification** :
   - Création de pages `/login` et `/register` avec des formulaires liés à l'API.
3. **Intégration API** :
   - Injection automatique du header `Authorization: Bearer <token>` dans les appels réseau (`api.ts`).
4. **Interface Todo** :
   - Ajout de l'affichage de l'utilisateur assigné et d'un menu déroulant sur `TodoItem.svelte` pour réassigner une tâche.
   - Ajout d'avatars et d'un bouton de déconnexion dans le layout global.

### Phase 3 : Tests BDD (Spec Driven Development)
1. **Écriture des Spécifications (Gherkin)** :
   - Création de `auth_collaboration.feature` pour couvrir l'inscription, la connexion et l'assignation de tâches.
2. **Implémentation Pytest-BDD** :
   - Création de fixtures robustes via `test_auth_bdd.py` pour valider que le système bloque les requêtes non-autorisées et filtre bien les accès concurrents.

---

## Problèmes rencontrés et solutions

1. **Bug avec `passlib` et `bcrypt` (ValueError 72 bytes limit)** :
   - **Problème** : Lors de l'exécution des tests BDD, la création d'utilisateurs déclenchait une erreur interne dans `passlib` (`ValueError: password cannot be longer than 72 bytes`). Cela était dû à un bug de compatibilité entre `passlib` (qui n'est plus maintenu activement) et les versions récentes de `bcrypt` (>4.0) qui suppriment le comportement silencieux face au "wrap bug".
   - **Solution** : Downgrade de `bcrypt` vers la version `4.0.1` via `uv add "bcrypt==4.0.1"`, ce qui résout l'incompatibilité.

2. **Conflit d'argument `owner_id` (TypeError)** :
   - **Problème** : L'API crashait lors de la création d'une tâche avec `models.Todo() got multiple values for keyword argument 'owner_id'`, car le dictionnaire retourné par `model_dump()` contenait déjà une valeur pour `owner_id` (à `None`) venant de Pydantic.
   - **Solution** : Exclusion ou remplacement manuel de la clé `owner_id` dans le dictionnaire avant l'instanciation du modèle SQLAlchemy.

3. **Perte de relation `assignee` lors du retour API** :
   - **Problème** : L'API retournait l'objet `assignee` à `None` après une création, car le schéma de requête initial (`TodoCreate`) ne prenait pas en compte `assignee_id`.
   - **Solution** : Déplacement de `assignee_id` vers `TodoBase` dans `schemas.py` pour assurer sa sérialisation dès la création.

4. **Gestion de l'état dans les scénarios BDD** :
   - **Problème** : Des états partagés entre scénarios créaient de fausses erreurs 401.
   - **Solution** : Groupement cohérent des scénarios dans `.feature` pour garantir un ordre robuste, et la conservation du jeton JWT entre la création et la vérification.

---

## Ce qu'il reste à faire selon le brief

D'après les discussions passées sur le découpage du brief (Partie 1 à Partie 4) :

1. **Les 4 piliers sur 8 (Partie 3 - Outillage du Projet)** :
   - Sans le contenu exact du Google Drive, je ne peux pas identifier avec certitude les 4 autres piliers "outillage / craftmanship" de TechSolve. Cependant, cela implique potentiellement :
     - Le CI/CD (GitHub Actions / GitLab CI)
     - L'analyse statique avancée (SonarQube)
     - Le monitoring et la télémétrie (Sentry / Prometheus)
     - La conteneurisation avancée et l'orchestration (Kubernetes)
     - (Note: Nous avons déjà couvert les bases du linter (Biome/Bun) et Docker).

2. **Extensions Skills & MCP (Partie 2)** :
   - Nous avons défini qu'il fallait créer des branches pour l'implémentation des MCPs (`github`, `context7`) et des Hooks de sécurité.
   - La branche `feature/mcp-setup` a été créée mais il reste à configurer formellement le serveur MCP ou les scripts de skills/hooks.

3. **Documentations à parfaire** :
   - Valider la complétion de tous les `docs/*.md` pour le contexte statique.
   - S'assurer que le README root pointe bien sur ces nouveaux ajouts architecturaux.
   - Fusionner ces branches (`feature/auth-collaboration`, etc.) dans `develop` via des Pull Requests (si applicable).
