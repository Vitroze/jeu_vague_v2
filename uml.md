```mermaid
classDiagram
    %% ===== Héritage =====
    Entity <|-- Enemy
    Entity <|-- Character
    Item <|-- Equipable
    Item <|-- Consumable

    %% ===== Composition / Association =====
    Game *-- "1" Player
    Game *-- "1" Vague
    Player o-- "*" Character : team
    Player o-- "*" Item : inventory
    Vague o-- "*" Enemy : monsters
    Enemy o-- "*" Item : dropables
    Character o-- "*" Equipable : equipement
    Game ..> Affichage : utilise
    Affichage ..> Vue : affiche

    class Game {
        +Player player
        +MongoClient mongoClient
        +Vague vague
        +SaveGame()
        +LoadGame()
        +LaunchGame()
        +ShowLeaderboard()
        +Exit()
    }

    class Vague {
        +int vague_actuel
        +List~Enemy~ monsters
        +PickEnemies(vague: Vague)
        +PlayVague()
        +GetDifficulty() int
    }

    class Player {
        +String name
        +int score
        +List~Character~ team
        +List~Item~ inventory
        +CreateTeam()
        +PickCharacter() Character
        +IsTeamAlive() bool
        +CheckInventory()
        +UseItem(item: Item)
    }

    class Entity {
        <<abstract>>
        +String name
        +int hp
        +int maxHp
        +int attack
        +int defense
        +IsAlive() bool
        +TakeDamage(amount: int)
        +Heal(amount: int)
        +Attack(target: Entity)
        +PlayTurn()*
    }

    class Enemy {
        +List~Item~ dropables
        +DropLoot() List~Item~
        +PlayTurn() «override»
    }

    class Character {
        +List~Equipable~ equipement
        +/attack: int
        +/defense: int
        +EquipItem(item: Equipable)
        +UnequipItem(item: Equipable)
        +IsSlotAvailable(slot_name: String) bool
        +GetEquipment(slot_name: String) Equipable
        +ProjectDamage(target: Entity) int
        +PlayTurn() «override»
    }

    class Item {
        <<abstract>>
        +String name
        +String description
        +int dropRate
        +String rarity
        +String item_type
        +Dictionary~String, int~ stats
    }

    class Equipable {
    }

    class Consumable {
        +Use(target: Entity)
    }

    class Affichage {
        +DisplayVue(vue: Function)
        +ShowError(error: String)
        +create_info_box(titre: String, info: String, box_color: String, text_color: String) Panel
        +create_select_box(titre: String, items: List~Item~, index: int, box_color: String, text_color: String, hover_color: String) Panel
    }

    class Vue {
        <<File>>
        +VueInventaire(inventaire: List~Item~, team: List~Character~)
        +VueTourJoueur(team: List~Character~, perso: Character, ennemis: List~Enemy~)
        +VueChoixCible(team: List~Character~, perso: Character, ennemis: List~Enemy~)
        +VueInfoTour(team: List~Character~, event: String, ennemis: List~Enemy~)
        +VueSelectionEquipe(team: List~Character~, listSelection: List~Character~)
        +VueEcranTitre()
        +VueLeaderboard(scores: Scores)
        +VueGameOver()
        +VueChargerSauvegarde()
        +VueQuitter()
    }