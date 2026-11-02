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

## Menu principal

### Configuration

1. Création d'un personnage
    - Son nom ? (Obligatoire)
    - Sa vie ? (Obligatoire)
    - Sa puissance d'attaque ? (Obligatoire)
    - Sa puissance de défense ? (Obligatoire)
    - Es-ce que c'est un ennemi ? (Par défaut : False)

2. Modification d'un personnage
    - Afficher la liste ID des personnages
    - Choisir un nombre

    A. Modification du personnage
    - Son nom ? (Laisser vide si pas de modification)
    - Sa vie ? (Laisser vide si pas de modification)
    - Sa puissance d'attaque ? (Laisser vide si pas de modification)
    - Sa puissance de défense ? (Laisser vide si pas de modification)
    - Es-ce que c'est un ennemi ? (Laisser vide si pas de modification)

3. Supprimer un personnage
    - Afficher la liste ID des personnages
    - Choisir un nombre
    - Confirmer la suppression

4. Création d'un item
    - Son nom ? (Obligatoire)
    - Son bonus d'attaque ? (Obligatoire)
    - Son bonus de défense ? (Obligatoire)
    - Sa durabilité ? (Obligatoire)

5. Modifier un item
    - Afficher la liste ID des items
    - Choisir un nombre

    A. Modification de l'item
    - Son nom ? (Laisser vide si pas de modification)
    - Son bonus d'attaque ? (Laisser vide si pas de modification)
    - Son bonus de défense ? (Laisser vide si pas de modification)
    - Sa durabilité ? (Laisser vide si pas de modification)

6. Supprimer un item
    - Afficher la liste ID des items
    - Choisir un nombre
    - Confirmer la suppression


7. Supprimer un score
    - Afficher la liste ID des scores
    - Choisir un nombre
    - Confirmer la suppression

### Jouer

1. Combien de cooéquipiers au total ?
2. Choisir les personnages (Si l'équipe n'est pas complet)
    1. Afficher la liste ID des personnages
    2. Choisir ID
    Si le choix n'est pas valide, alors on repasse a l'étape 2
    Si le choix est valide alors on passe a l'étape 3

3. Système de tours

### Score
Afficher les scores sous forme de liste.

## Système de tours

Au début de la partie :
1. On vérifie l'équipe complet
    - Si l'équipe est invalide alors on retourne dans le menu principale
    - Sinon on passe a la prochaine étape
2. On vérifie le monstre actuel
    - Si la liste des monstres de config est vide, alors on termine le jeu.
    - Sinon on passe au système de tours

A chaque tours, on fait (BOUCLE) :
1. Tant que l'équipe est encore vivant
    Boucle :
    - Si la vie de tous les équipiers est supérieur à 0 alors on continue le tours
    - Sinon on termine la partie (5.)
2. Gestion du personnage prinicipal
    - Si aucun personnage principale n'est choisie alors on choisie aléatoirement le personnage dans la liste.
    - Si le personnage principale choisi est invalide, alors on termine la partie avec un message de notification.

3. Attaque Personnage principale

    1. Le personnage actuel frappe le méchant
        - Puissance d'attaque = ``Puissance d'attaque du personnage - Puissance de défense du méchant``

    2. Vérifier la vie du méchant actuel.
    Si le méchant actuel n'est pas en vie, on passe au prochain méchant aléatoire.

4. Attaque du méchant
    1. Le personnage actuel frappe le méchant
        - Puissance d'attaque = ``Puissance d'attaque du personnage - Puissance de défense du méchant``

    2. Vérifier la vie du personnage actuel.
    Si le personnage actuel n'est pas en vie on passe au prochain membre de l'équipe

Hors boucle:

5. Sauvegarde du score.