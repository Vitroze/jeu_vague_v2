# Principe du jeu 
Le joueur doit combattre une vague de monstre.

# Fonctionnaltiés
## Notion de base de donnée
Utilisation de MongoDB avec comme tables :
- Score du joueur

| Nom de la valeur | Type de donnée | Description |
| :--- | :---: | :--- |
| player_name | string | Nom du joueur |
| score | uint | Score du joueur |
| date | DATETIME | Date + heure du score réalisé |

- Characters

| Nom de la valeur | Type de donnée | Description |
| :--- | :---: | :--- |
| name | string | Nom du personnage |
| health | uint | Vie du personnage
| power_attack | uint | Puissance d'attaque |
| power_defense | uint | Puissance de défénse |
| is_ennemy | bool | Est-ce un ennemi ? |

- Inventory

| Nom de la valeur | Type de donnée | Description |
| :--- | :---: | :--- |
| name | string | Nom du personnage |
| power_attack | uint | Puissance d'attaque |
| power_defense | uint | Puissance de défénse |
| durability | uint | Durabilité de l'arme (se casse au bout de combien tours ?)

## Algorithme DB
Au lancement du programme.

1. Vérifier si la base de donnée est connecté
    - Cela permet d'éviter d'avoir des données corrompus en faisant une double connexion.
Si elle n'est pas conencté alors on lance connect. Procédure de connexion (Etape 2)
Si elle est connecté alors on affiche un message et on continue le programme

2. On vérifie si les données du env sont valides.
- Si URL de connexion n'a pas de chaine de caractère ou est inférieur à 3 caractère alors on arrête le programme
- Si le nom de la base de donnée n'a pas de chaine de caractère ou est inférieur à 1 caractère alors on arrête le programme
- Sinon on continue a la prochaine étape

2. On connecte la base de donnée

3. On vérifie que la base de donnée est connecté en envoyant un ping
- Si le ping est reçu alors on continue a la prochaine étape
- Sinon on arrête le programme (TIMED-OUT de 20 secondes)

4. On crée les tables de la base de donnée
- Si les tables réussisent à se crée alors on passe au menu principale
- Sinon on envoie une erreur et on arrête le programme


## Choix Valide
### ID par personnage
- Si ID est un nombre
- Si ID existe dans la liste de tous les personnages (GLOBAL).

Si ``True`` alors on passe a la suite
Si ``False`` alors on redemande a l'utilisateur.

## Menu principal

### Configuration
Il aura toujours une option pour revenir au menu arrière.

1. Création d'un personnage
    - Son nom ? (Obligatoire)
    - Sa vie ? (Obligatoire)
    - Sa puissance d'attaque ? (Obligatoire)
    - Sa puissance de défense ? (Obligatoire)
    - Es-ce que c'est un ennemi ? (Par défaut : False)

2. Modification d'un personnage
    - Afficher la liste ID des personnages
    - L'utilisateur a choisi un choix valide.
    Si le choix n'est pas valide alors on redemande a l'utilisateur.

    A. Modification du personnage
    - Son nom ? (Laisser vide si pas de modification)
    - Sa vie ? (Laisser vide si pas de modification)
    - Sa puissance d'attaque ? (Laisser vide si pas de modification)
    - Sa puissance de défense ? (Laisser vide si pas de modification)
    - Es-ce que c'est un ennemi ? (Laisser vide si pas de modification)

3. Supprimer un personnage
    - Afficher la liste ID des personnages
    - L'utilisateur a choisi un choix valide
    Si le choix n'est pas valide alors on redemande a l'utilisateur.
    - Confirmer la suppression

4. Création d'un item
    - Son nom ? (Obligatoire)
    - Son bonus d'attaque ? (Obligatoire)
    - Son bonus de défense ? (Obligatoire)
    - Sa durabilité ? (Obligatoire)

5. Modifier un item
    - Afficher la liste ID des items
    - Choisir une option valide.
    Si le choix n'est pas valide alors on redemande a l'utilisateur.

    A. Modification de l'item
    - Son nom ? (Laisser vide si pas de modification)
    - Son bonus d'attaque ? (Laisser vide si pas de modification)
    - Son bonus de défense ? (Laisser vide si pas de modification)
    - Sa durabilité ? (Laisser vide si pas de modification)

6. Supprimer un item
    - Afficher la liste ID des items
    - Choisir un choix valide
    Si le choix n'est pas valide alors on redemande a l'utilisateur.

    - Confirmer la suppression (Ecrire 1 pour confirmer sinon il sort.)


7. Supprimer un score
    - Afficher la liste ID des scores
    - Choisir un choix valide
    Si le choix n'est pas valide alors on redemande a l'utilisateur.

    - Confirmer la suppression (Ecrire 1 pour confirmer sinon il sort)

### Jouer

1. Vérifié si les données sont valides
    - Si la liste des alliés **et** des monstres est supérieur à 0 et qu'ils contiennent les données obligatoires comme (``name``, ``health``, ``power_attack``, ``power_defense`` ) alors on passe la prochaine
2. Tant que l'équipe n'est pas complet.
    1. Afficher la liste ID des personnages non sélectionnés.
    2. Choisir ID
    Si le choix n'est pas valide, alors on repasse a l'étape 2
    Si le choix est valide alors on passe a l'étape 3

    2.a. Choix Valide
    - Si c'est un nombre
    - Si la clé existe bien dans la liste.
    - Si ce n'est pas un ennemi qui est choisi
3. On vérifie l'équipe complet
    - Si l'équipe est invalide alors on retourne dans le menu principale
    - Sinon on passe a la prochaine étape
4. On vérifie le monstre actuel
    - Si la liste des monstres de config est vide, alors on termine le jeu.
    - Sinon on passe a la prochaine étape
5. Système de tours

### Score
Afficher les scores sous forme de liste.

## Système de tours

A chaque tours, on fait (BOUCLE) :
1. Tant que l'équipe est encore vivant
    Boucle :
    - Si la vie de tous les équipiers est supérieur à 0 alors on continue le tours
    - Sinon on termine la partie (5.)

2. Gestion du personnage prinicipal
    - Si aucun personnage principale n'est choisie ou que le personnage est mort alors on choisie aléatoirement le personnage dans la liste **si** celui-ci contient encore des alliés en vie.
    - Si le personnage principale choisi est invalide, alors on termine la partie avec un message de notification.

3. Attaque Personnage principale

    1. Le personnage actuel frappe le méchant
        - Puissance d'attaque = ``Puissance d'attaque du personnage - Puissance de défense du méchant``

    2. Vérifier la vie du méchant actuel.
    Si le méchant actuel n'est pas en vie, on passe au prochain méchant aléatoire.

4. Gestion de l'ennemi
    - Si aucun ennemi n'est choisie ou qu'il est mort alors on choisie aléatoirement le personnage dans la liste.
    - Si l'ennemi choisi aléatoirement est invalide, alors on recommence jusqu'à 3 essaies. Si au bout de 3 essaies on ne trouve toujours pas de monstre, alors on termine la partie avec un message de notification.

4. Attaque du méchant
    1. Le personnage actuel frappe le méchant
        - Puissance d'attaque = ``Puissance d'attaque du personnage - Puissance de défense du méchant``

    2. Vérifier la vie du personnage actuel.
    Si le personnage actuel n'est pas en vie on passe au prochain membre de l'équipe

Hors boucle:

5. Sauvegarde du score.