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
3. Système de tours

### Score
Afficher les scores sous forme de liste.

## Système de tours
A chaque tours, on fait : 
1. On vérifie si l'équipe est encore vivant

    1.a. Si elle n'est pas en vie alors on termine le jeu et on enregistre le jeu. 
    
    1.b. 