# Bienvenue sur le guide de Mmath !
Le but de Mmath est de donner avec la plus grande précision possible la valeur certifiée du sinus de tout nombre réel.

Cette précision théorique est de l'ordre de 10<sup>-100</sup> et utilise les formules de Taylor-Lagrange pour les développements limités et les suites de Cauchy pour en certifier la convergence donc la stabilité et la précision.

Ce module pourra dans l'avenir être complété avec d'autres champs comme le cosinus et la tangente.

## Exemple d'utilisation

### 1. Installation
```shell script
pip install mmath
``` 
ou encore
```shell script
python3 -m pip install mmath
```

### 2. Import
```python
import mmath
```
ou encore
```python
from mmath import *
```

### 3. Obtention du sinus de 45rad
```python
valeur = mmath.Mmath(45).sin
```
ou
```python
valeur = Mmath(45).sin
```
selon les imports.

## DISCLAIMER
Ce module n'a pas vocation à remplacer le module de base math. Il est réalisé à titre scolaire et les auteurs ne sauraient en aucun cas être tenus responsables de sa mauvaise utilisation.