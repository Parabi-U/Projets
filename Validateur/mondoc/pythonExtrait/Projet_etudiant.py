# --- Cellule ---
## Import des bibliothèques nécessaires au projet.
## Ne pas modifier les fichiers "bibliothèque".

## Interpréter cette cellule avant de continuer.

from transition import *
from state import *
import os
import copy
from automateBase import AutomateBase
import itertools

class Automate(AutomateBase):
    pass

# --- Cellule ---


# --- Cellule ---
# Voilà le code de succElem

def succElem(self, state, lettre):
    """ State x str -> set[State]
        rend l'ensemble des états accessibles à partir d'un état state par l'étiquette lettre
    """
    successeurs = set()
    # t: Transitions
    for t in self.getSetTransitionsFrom(state):
        if t.etiquette == lettre:
            successeurs.add(t.stateDest)
    return successeurs

Automate.succElem = succElem

# --- Cellule ---
# A faire par l'étudiant

def succ(self, setStates, lettre):
    """ Automate x set[State] x str -> set[State]
        rend l'ensemble des états accessibles à partir de l'ensemble d'états setStates par l'étiquette lettre
    """
    successeurs = set()
    # t: Transitions
    for state in setStates:
        for t in self.getSetTransitionsFrom(state):
            if t.etiquette == lettre:
                successeurs.add(t.stateDest)
    return successeurs

Automate.succ = succ

# --- Cellule ---
# A faire par l'étudiant

def accepte(self, mot) :
    """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
    """
    courant = self.getSetInitialStates()
    for lettre in mot:
        courant = self.succ(courant, lettre)
        if not courant:
            return False
    return bool(courant & self.getSetFinalStates())

Automate.accepte = accepte

# --- Cellule ---
# A faire par l'étudiant

### On ne prend pas en compte les états non accessibles


def estComplet(self, Alphabet) :
    """ Automate x set[str] -> bool
        rend True si auto est complet pour les lettres de Alphabet, False sinon
        hyp : les éléments de Alphabet sont de longueur 1
    """
    accessibles = set(self.getSetInitialStates())
    pile = list(accessibles)
    while pile:     #Calcul des états accessibles
        s = pile.pop()
        for t in self.getSetTransitionsFrom(s):
            if t.stateDest not in accessibles:
                accessibles.add(t.stateDest)
                pile.append(t.stateDest)
    for s in accessibles:     #On vérifie la complétude
        for a in Alphabet:
            if not self.succElem(s, a):
                return False
    return True

Automate.estComplet = estComplet

# --- Cellule ---
# A faire par l'étudiant

def estDeterministe(self) :
    """ Automate -> bool
        rend True si auto est déterministe, False sinon
    """
    init_states = self.getSetInitialStates()
    if len(init_states) != 1: #On vérifie qu'il n'y a qu'un seul état initial
        return False
    for s in self.allStates:
        transitions_a_partir_de_s = self.getSetTransitionsFrom(s)
        labels_traverse = set()
        for t in transitions_a_partir_de_s:
            if t.etiquette in labels_traverse:
                return False  #Cas avec deux transitions sur la même étiquette
            labels_traverse.add(t.etiquette)
    return True
    
Automate.estDeterministe = estDeterministe

# --- Cellule ---
# A faire par l'étudiant

def completeAutomate(self, Alphabet) :
    """ Automate x str -> Automate
        rend l'automate complété de self, par rapport à Alphabet
    """
    if self.estComplet(Alphabet): #Vérifie si l'automate donné n'est pas déjà complet
        return self 
    auto_complet = copy.deepcopy(self)
    accessibles = set(auto_complet.getSetInitialStates()) 
    pile = list(accessibles)
    while pile:
        s = pile.pop()
        for t in auto_complet.getSetTransitionsFrom(s):   #Déterminer les états accessibles
            if t.stateDest not in accessibles:
                accessibles.add(t.stateDest)
                pile.append(t.stateDest)
    id_puits = auto_complet.nextId()
    puit = State(id_puits, False, False)
    besoin_puits = False
    for s in accessibles:
        for a in Alphabet:
            if not auto_complet.succElem(s, a):
                besoin_puits = True
                auto_complet.addTransition(Transition(s, a, puit))    #Ajoute transition vers le puit
    if besoin_puits:    # Si l'état puits est utilisé, le compléter lui aussi
        auto_complet.addState(puit)
        for a in Alphabet:
            auto_complet.addTransition(Transition(puit, a, puit))
    return auto_complet

Automate.completeAutomate = completeAutomate

# --- Cellule ---
# A faire par l'étudiant

def newLabel(S):
    """ set[State] -> str
    """
    labels = [state.label for state in S]
    labels.sort()
    return '{' + ','.join(labels) + '}'

# --- Cellule ---
def determinisation(self) :
    """ Automate -> Automate
    rend l'automate déterminisé d'auto """
    # Ini : set[State]
    Ini = self.getSetInitialStates()
    # fin : bool
    fin = False
    # e : State
    for e in Ini:
        if e.fin:
            fin = True
    lab = newLabel(Ini)
    s = State(0, True, fin, lab)
    A = Automate(set())
    A.addState(s)
    Alphabet = {t.etiquette for t in self.allTransitions}
    Etats = dict()
    Etats[s] = Ini
    A.determinisation_etats(self, Alphabet, [s], 0, Etats, {lab})
    return A

Automate.determinisation = determinisation

# --- Cellule ---
# A faire par l'étudiant (on conserve la spécification de la fonction)

def determinisation_etats(self, auto, Alphabet, ListeEtatsATraiter, i, Etats, DejaVus):
    """ Automate x Automate x set[str] x list[State] x int x dict[State : set[State]], set[str] -> NoneType
    """
    # Si on a traité tous les états, on s'arrête
    if i >= len(ListeEtatsATraiter):
        return
    
    # Récupérer l'état courant à traiter
    etat_courant = ListeEtatsATraiter[i]
    # Récupérer l'ensemble d'états de l'automate original correspondant
    ensemble_etats = Etats[etat_courant]
    
    # Pour chaque lettre de l'alphabet
    for lettre in Alphabet:
        # Calculer l'ensemble des états successeurs
        successeurs = auto.succ(ensemble_etats, lettre)
        
        if successeurs:  # Si l'ensemble n'est pas vide
            # Créer le label pour le nouvel état
            nouveau_label = newLabel(successeurs)
            
            # Vérifier si cet état existe déjà
            etat_existant = None
            for etat in ListeEtatsATraiter:
                if etat.label == nouveau_label:
                    etat_existant = etat
                    break
            
            if etat_existant is None and nouveau_label not in DejaVus:
                # Créer un nouvel état
                # Déterminer si c'est un état final
                est_final = any(etat.fin for etat in successeurs)
                nouvel_etat = State(len(ListeEtatsATraiter), False, est_final, nouveau_label)
                
                # Ajouter le nouvel état à l'automate et aux structures
                self.addState(nouvel_etat)
                ListeEtatsATraiter.append(nouvel_etat)
                Etats[nouvel_etat] = successeurs
                DejaVus.add(nouvel_etat.label)
                
                # Créer la transition
                nouvelle_transition = Transition(etat_courant, lettre, nouvel_etat)
                self.addTransition(nouvelle_transition)
                
            else:
                # L'état existe déjà, créer la transition vers cet état
                if etat_existant is None:
                    # Trouver l'état existant par son label
                    for etat in ListeEtatsATraiter:
                        if etat.label == nouveau_label:
                            etat_existant = etat
                            break
                
                if etat_existant is not None:
                    nouvelle_transition = Transition(etat_courant, lettre, etat_existant)
                    self.addTransition(nouvelle_transition)
    
    # Appel récursif pour traiter le prochain état
    self.determinisation_etats(auto, Alphabet, ListeEtatsATraiter, i + 1, Etats, DejaVus)

    return 

Automate.determinisation_etats = determinisation_etats

# --- Cellule ---
def complementaire(self, Alphabet):
    """ Automate x set[str] -> Automate
        rend  l'automate acceptant le complémentaire du langage de self
    """
    
    auto_det = self
    if not self.estDeterministe():
        auto_det = self.determinisation()
    
    auto_complet = auto_det.completeAutomate(Alphabet)
    
    nouveaux_etats = set()
    for etat in auto_complet.allStates:
        nouvel_etat = State(etat.id, etat.init, not etat.fin, etat.label)
        nouveaux_etats.add(nouvel_etat)
    
    nouvelles_transitions = set()
    
    mapping_etats = {}
    for etat_old, etat_new in zip(auto_complet.allStates, nouveaux_etats):
        mapping_etats[etat_old] = etat_new
    
    for transition in auto_complet.allTransitions:
        nouvelle_transition = Transition(
            mapping_etats[transition.stateSrc],
            transition.etiquette,
            mapping_etats[transition.stateDest]
        )
        nouvelles_transitions.add(nouvelle_transition)
    
    return Automate(nouvelles_transitions, nouveaux_etats, f"Complémentaire de {self.label}")
    

Automate.complementaire = complementaire   

# --- Cellule ---
def intersection(self, auto2):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'intersection des langages des deux automates
    """
    auto1 = self

    # Alphabet = intersection des alphabets
    alphabet = {t.etiquette for t in auto1.allTransitions} & \
               {t.etiquette for t in auto2.allTransitions}

    # ---- Création automate avec état factice ----
    intermediaire = State(0, False, False, "intermediaire")
    newAuto = Automate(set(), set(), "intersection")
    newAuto.addState(intermediaire)

    # Correspondance: (id1,id2) → State
    mapping = {}

    file = []

    # ---- États initiaux du produit ----
    for s1 in auto1.getSetInitialStates():
        for s2 in auto2.getSetInitialStates():
            key = (s1.id, s2.id)

            new_id = newAuto.nextId()
            new_state = State(new_id,
                              True,
                              s1.fin and s2.fin,  # DIFFÉRENCE: ET logique
                              f"{s1.label}_{s2.label}")

            newAuto.addState(new_state)
            mapping[key] = new_state
            file.append((s1, s2))

    # ---- BFS ----
    for (s1, s2) in file:
        pass  # nous ne voulons pas pop intermediaire, c'était juste pour nextId

    while file:
        s1, s2 = file.pop(0)
        ep = mapping[(s1.id, s2.id)]

        for a in alphabet:
            succ1 = auto1.succ({s1}, a)
            succ2 = auto2.succ({s2}, a)

            # Pour l'intersection : si un automate n'a pas de transition,
            # l'autre non plus, donc on continue
            if not succ1 or not succ2:
                continue

            for t1 in succ1:
                for t2 in succ2:
                    key = (t1.id, t2.id)

                    if key not in mapping:
                        new_id = newAuto.nextId()
                        new_state = State(new_id,
                                          False,
                                          t1.fin and t2.fin,  # DIFFÉRENCE: ET logique
                                          f"{t1.label}_{t2.label}")
                        newAuto.addState(new_state)
                        mapping[key] = new_state
                        file.append((t1, t2))

                    newAuto.addTransition(Transition(ep, a, mapping[key]))

    # ---- Retirer l'état factice ----
    newAuto.removeState(intermediaire)

    return newAuto

Automate.intersection = intersection

# --- Cellule ---
#À faire par l'étudiant
def union(self, auto2):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'union des langages des deux automates
    """
    auto1 = self

    # Alphabet = union des alphabets
    alphabet = {t.etiquette for t in auto1.allTransitions} | \
               {t.etiquette for t in auto2.allTransitions}

    # ---- Création automate avec état factice ----
    intermediaire = State(0, False, False, "intermediaire")
    newAuto = Automate(set(), set(), "union")
    newAuto.addState(intermediaire)

    # Correspondance: (id1,id2) → State
    mapping = {}

    file = []

    # ---- États initiaux du produit ----
    for s1 in auto1.getSetInitialStates():
        for s2 in auto2.getSetInitialStates():

            key = (s1.id, s2.id)

            new_id = newAuto.nextId()
            new_state = State(new_id,
                              True,
                              s1.fin or s2.fin,
                              f"{s1.label}_{s2.label}")

            newAuto.addState(new_state)
            mapping[key] = new_state
            file.append((s1, s2))

    # ---- BFS ----
    for (s1, s2) in file:
        pass  # nous ne voulons pas pop intermediaire, c’était juste pour nextId

    while file:
        s1, s2 = file.pop(0)
        ep = mapping[(s1.id, s2.id)]

        for a in alphabet:

            succ1 = auto1.succ({s1}, a)
            succ2 = auto2.succ({s2}, a)

            # Pour l’union : si aucune transition → aucun successeur
            if not succ1:
                continue
            if not succ2:
                continue

            for t1 in succ1:
                for t2 in succ2:

                    key = (t1.id, t2.id)

                    if key not in mapping:
                        new_id = newAuto.nextId()
                        new_state = State(new_id,
                                          False,
                                          t1.fin or t2.fin,
                                          f"{t1.label}_{t2.label}")
                        newAuto.addState(new_state)
                        mapping[key] = new_state
                        file.append((t1, t2))

                    newAuto.addTransition(Transition(ep, a, mapping[key]))

    # ---- Retirer l’état factice ----
    newAuto.removeState(intermediaire)

    return newAuto

Automate.union = union



# --- Cellule ---
# A faire par l'etudiant

def concatenation (self, auto):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage la concaténation des langages des deux automates
    """
    #Copie des deux automates pour ne rien modifier
    A = copy.deepcopy(self)
    B = copy.deepcopy(auto)
    prefixe = A.nextId()
    B.prefixStates(prefixe)
    newAuto = Automate(set(), set(), "")    # Construction nouvel automate contenant les deux automates
    
    for s in A.allStates:   # Ajout états et transitions de A
        newAuto.addState(s)
    for t in A.allTransitions:
        newAuto.addTransition(t)
        
    for s in B.allStates:   # Ajout états et transitions de B
        newAuto.addState(s)
    for t in B.allTransitions:
        newAuto.addTransition(t)
        
    finalsA = A.getSetFinalStates()
    initialsB = B.getSetInitialStates()
    finalsB = B.getSetFinalStates()
    
    for sf in finalsA:
        sf.fin = False

        # Pour chaque transition issue des états initiaux de B
        for si in initialsB:
            for t in B.getSetTransitionsFrom(si):
                # Ajouter la même transition en partant de sf
                newAuto.addTransition(Transition(sf, t.etiquette, t.stateDest))

        # Si un état initial de B est final → sf devient final
        for si in initialsB:
            if si.fin:
                sf.fin = True

    # États finaux du résultat = états finaux de B
    for sf in finalsB:
        sf.fin = True

    return newAuto
    
Automate.concatenation = concatenation

# --- Cellule ---
def etoile (self):
    """ Automate  -> Automate
    rend l'automate acceptant pour langage l'étoile du langage de l'automate appelant
    """
    A = copy.deepcopy(self)    #Copie automate d'origine
    
    new_id = A.nextId()    #Création nouvel état initial-final
    newInit = State(new_id, init=True, fin=True, label=f"initEtoile_{new_id}")

    # Créer l’automate résultat
    newAuto = Automate(set(), set(), "")
    
    for s in A.allStates:        # Ajout états et transitions de A
        newAuto.addState(s)
    for t in A.allTransitions:
        newAuto.addTransition(t)
        
    newAuto.addState(newInit)    # Ajout du nouvel état initial-final
    initialA = A.getSetInitialStates()
    for s in initialA:
        s.init = False
    for si in initialA:
        for t in A.getSetTransitionsFrom(si):
            newAuto.addTransition(Transition(newInit, t.etiquette, t.stateDest))
    finalsA = A.getSetFinalStates()

    for sf in finalsA:
        sf.fin = True 
        for si in initialA:
            for t in A.getSetTransitionsFrom(si):
                newAuto.addTransition(Transition(sf, t.etiquette, t.stateDest))

    return newAuto

Automate.etoile = etoile


# --- Cellule ---
def alphabet_fichier(nom):
    """ Fichier -> set[str]
    renvoie l'ensemble des lettres apparaissant dans le texte du fichier. 
    Chaque chaine de l'ensemble construit est de taille 1."""
    # A : set[str]
    A = set()
    with open(nom) as fichier:
        # ligne : str
        for ligne in fichier:
            # c : str de taille 1
            for c in ligne:
                A.add(c)
    return A

# --- Cellule ---
# C'est une fonction, pas une méthode

def auto_flottant(Alphabet):
    """set[str] -> Automate
        prend en entrée en ensemble de chaines de caractères (chacune de taille 1),
        et renvoie l'automate acceptant les nombres décimaux."""
    
    q0 = State(0, init=True, fin=False, label="start")         # Création différents États
    q1 = State(1, init=False, fin=False, label="int")
    q2 = State(2, init=False, fin=False, label="comma")
    q3 = State(3, init=False, fin=True,  label="frac")

    auto = Automate(set(), set(), "auto_flottant")       # Création Automate vide
    
    for s in [q0, q1, q2, q3]:    # Ajout des états
        auto.addState(s)

    # Définition des transitions
    # tous les chiffres dans Alphabet :
    digits = {c for c in Alphabet if c.isdigit()}

    # q0 → q1 par un chiffre
    for d in digits:
        auto.addTransition(Transition(q0, d, q1))

    # q1 → q1 sur chiffre
    for d in digits:
        auto.addTransition(Transition(q1, d, q1))

    # q1 → q2 sur virgule
    if ',' in Alphabet:
        auto.addTransition(Transition(q1, ',', q2))

    # q2 → q3 sur chiffre
    for d in digits:
        auto.addTransition(Transition(q2, d, q3))

    # q3 → q3 sur chiffre
    for d in digits:
        auto.addTransition(Transition(q3, d, q3))
    return auto

# --- Cellule ---
def liste_flottants(auto, nom):
    """ Automate x Fichier -> list[str]
        renvoie la liste des nombres décimaux, sous forme de chaines de caractères, apparaissant
        dans l'ordre de lecture dans le fichier.
    """
    resultat = []

    # On récupère l'ensemble des états initiaux (normalement un seul)
    initiaux = auto.getSetInitialStates()

    with open(nom, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.rstrip("\n")
            n = len(ligne)
            i = 0

            # On parcourt la ligne caractère par caractère
            while i < n:
                etats_courants = initiaux
                mot_courant = ""

                dernier_mot_valide = None
                dernier_j = i

                j = i

                # On essaie de lire un nombre décimal à partir de i
                while j < n:
                    c = ligne[j]

                    # Ensemble des états atteignables avec ce caractère
                    etats_suivants = auto.succ(etats_courants, c)

                    if not etats_suivants:
                        break  # plus de transition possible → on s'arrête ici

                    mot_courant += c
                    etats_courants = etats_suivants

                    # Si au moins un état est final → mot valide pour l'instant
                    if any(s.fin for s in etats_courants):
                        dernier_mot_valide = mot_courant
                        dernier_j = j

                    j += 1

                # Si on a détecté un mot valide (atteint un état final)
                if dernier_mot_valide is not None:
                    resultat.append(dernier_mot_valide)
                    i = dernier_j + 1  # on avance après le flottant trouvé
                else:
                    i += 1  # sinon on avance d'un caractère

    return resultat
    
    return

# --- Cellule ---


