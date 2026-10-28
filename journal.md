# SovereignBox — Journal de Bord

> Ce document a pour but de garder une tracabilité de toutes les réfléxions et prises de décisions.
> Celui-ci se verra être modifié tout au long du projet.
> Il permttra au développeur de pouvoir revenir sur des potentiels changements ou améliorations.


---

## Résumé du projet

SovereignBox est un outil de déploiement guidé qui transforme l'intention
d'un utilisateur non-expert en une pile de services auto-hébergés
fonctionnelle, sécurisée et documentée, sur une seule machine locale.

L'utilisateur sélectionne les services qu'il souhaite (par exemple Jellyfin,
Vaultwarden, Nextcloud). L'outil résout les dépendances, vérifie la
faisabilité, génère la configuration d'infrastructure et déploie le tout.
L'utilisateur n'a jamais besoin de comprendre Docker, YAML ou le réseau pour
obtenir un résultat fonctionnel.

---

## Architecture

Trois couches, chacune avec une responsabilité unique :

    ┌──────────────┐
    │  Catalogue   │  Fichiers YAML - données uniquement, pas de logique
    │   (YAML)     │  Une entrée par service, décrivant ses besoins
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Planificateur│  
    │  (Python)    │  
    │              │  
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Exécuteur   │  
    │  (Python →   │  
    │   Docker)    │  
    └──────────────┘
---

## Support d'infrastructure (Docker)

**Décision :** déployer les services sous forme de conteneurs Docker sur
l'hôte. Aucun hyperviseur (Proxmox, VirtualBox) dans le chemin principal.

> Économie de ressources
> Expérience utilisateur moins lourde
> Simplicité de réalisation
> L'usage en réseau local réduit les risques de sécurite auquel Docker s'expose.

---

## Format du catalogue (YAML)

**Décision :** les entrées du catalogue de services sont écrites en YAML (contre JSON).

> Souplesse dans la syntaxe (commentaires, chaines multi-lignes)
> Lisibilité simple 

## Schéma du catalogue 

Chaque entrée de service doit contenir :

| Champ         | Type   | Requis | Rôle                                       |
|---------------|--------|--------|--------------------------------------------|
| `name`        | string | oui    | Nom lisible par un humain                  |
| `description` | string | oui    | Une ligne, ce que le service remplace      |
| `image`       | string | oui    | Image Docker (`nom:tag`)                   |
| `ports`       | liste  | oui    | Mappages de ports (`hôte:conteneur`)       |
| `depends_on`  | liste  | non    | Autres services ou briques requis          |
| `folders`     | liste  | non    | Mappages dossier hôte → conteneur          |
| `resources`   | dict   | oui    | `ram_mb`, `disk_gb`, utilisés par le planner |
| `env`         | dict   | non    | Variables d'environnement                  |
| `notes`       | string | non    | Justification libre                        |


---

## Choix du langage de programmation

**Décision :** le planificateur et l'exécuteur sont écrits en Python (contre bash).


> Manipulation des données mieux gérée
> Pytest sera utile au projet
> Potentielle extension sur d'autres OS simplifiée


---