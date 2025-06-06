# BrainCache

**BrainCache** est une librairie Python simple et flexible pour le cache mémoire ou fichier des objets Python, avec support TTL (expiration), backends interchangeables, décorateur facile pour la mise en cache des fonctions, et nettoyage automatique.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation rapide](#utilisation-rapide)
- [Backends disponibles](#backends-disponibles)
- [Décorateur de cache](#décorateur-de-cache)
- [Nettoyage automatique](#nettoyage-automatique)
- [Exemples avancés](#exemples-avancés)
- [Bugs connus / Limitations](#bugs-connus--limitations)
- [Roadmap](#roadmap)
- [Licence](#licence)

---

## Fonctionnalités

- Mise en cache mémoire ou fichier, interchangeable
- Support du TTL (expiration automatique des valeurs)
- Décorateur pour cacher facilement les résultats de fonctions
- Nettoyage automatique des entrées expirées (thread dédié)
- API simple et intuitive

---

## Installation

```bash
git clone https://github.com/jallow-2693/BrainCache.git
cd BrainCache
# (Optionnel) Installation dans le site-packages
pip install .
```

---

## Utilisation rapide

### 1. Import et cache mémoire (par défaut)

```python
from braincache import BrainCache

cache = BrainCache()
cache.set('ma_cle', 'ma_valeur', ttl=10)  # expire dans 10 secondes

value = cache.get('ma_cle')
if value:
    print("Valeur trouvée :", value)
else:
    print("Valeur expirée ou absente")
```

### 2. Utilisation du backend fichier

```python
from braincache.backend.file import FileBackend
from braincache import BrainCache

cache = BrainCache(backend=FileBackend('mon_cache.json'))
cache.set('user_id', 1234, ttl=3600)  # expire dans 1h
print(cache.get('user_id'))
```

---

## Backends disponibles

- **MemoryBackend** (cache en RAM, volatil)
- **FileBackend** (persistance sur disque, fichier JSON)

Changer de backend :  
```python
from braincache.backend.memory import MemoryBackend
from braincache.backend.file import FileBackend
from braincache import BrainCache

# Cache mémoire (défaut)
cache = BrainCache()

# Cache fichier
cache_fichier = BrainCache(backend=FileBackend('cache.json'))
```

---

## Décorateur de cache

Cache les résultats d'une fonction automatiquement selon ses arguments :

```python
from braincache import cache

@cache(ttl=60)  # cache pendant 60 secondes
def calcul_lourd(x, y):
    print("Calcul en cours…")
    return x * y

# Premier appel : lance le calcul
resultat = calcul_lourd(2, 5)
# Appel suivant : résultat depuis le cache tant que TTL non expiré
resultat = calcul_lourd(2, 5)
```

---

## Nettoyage automatique

Pour assurer que les clés expirées sont supprimées périodiquement, utilise le `CacheCleaner` (thread en arrière-plan) :

```python
from braincache.cleaner import CacheCleaner
from braincache import BrainCache

cache = BrainCache()
cleaner = CacheCleaner(cache, interval=60)  # nettoyage toutes les 60 secondes
cleaner.start()

# ... ton code ...

cleaner.stop()  # Arrête le thread proprement à la fin
```

---

## Exemples avancés

### Supprimer une clé

```python
cache.delete('ma_cle')
```

### Vider tout le cache

```python
cache.clear()
```

### Vérifier l'existence d'une entrée

```python
if cache.has('autre_cle'):
    print("Clé présente !")
```

---

## Bugs connus / Limitations

- Le backend fichier ne supporte que les valeurs JSON-sérialisables.
- Pas de gestion multi-processus sur le backend fichier (thread-safe seulement).
- Le décorateur de cache peut produire des collisions de clés si les arguments sont des objets complexes non hashables.
- Les exceptions lors de l'accès disque (backend fichier) ne sont pas catchées partout.
- Pas de support natif pour Redis/Memcached (PR bienvenues !).

---

## Roadmap

- [ ] Ajout de tests unitaires
- [ ] Backend Redis/Memcached
- [ ] Nettoyage automatique intégré pour le backend fichier
- [ ] Ajout de logs optionnels
- [ ] Support Python >=3.7

---

## Licence

MIT

---

**Auteur** : [jallow-2693](https://github.com/jallow-2693)

N'hésite pas à ouvrir une issue pour toute question, suggestion ou bug !
