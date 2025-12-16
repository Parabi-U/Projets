#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>  // Pour getch() sur Windows
#include <windows.h> // Pour Sleep()

#define HAUTEUR 22
#define LARGEUR 10
#define VIDE '.'

/* Structure pour une case */
struct une_case {
    int colonne;
    int ligne;
};

/* Structure pour une pièce */
struct piece {
    int pos_ligne, pos_colonne;
    struct une_case la_piece[4];
    char type;
};

/* Plateau de jeu */
char plateau[HAUTEUR][LARGEUR];

/* Tableau des pièces Tetris */
struct une_case tab_pieces[7][4] = {
    {{0, 0}, {1, 0}, {0, 1}, {1, 1}}, /* O */
    {{0, 0}, {1, 0}, {2, 0}, {3, 0}}, /* I */
    {{0, 0}, {0, 1}, {0, 2}, {1, 2}}, /* L */
    {{1, 0}, {1, 1}, {1, 2}, {0, 2}}, /* J */
    {{0, 0}, {1, 0}, {1, 1}, {2, 1}}, /* Z */
    {{1, 0}, {2, 0}, {0, 1}, {1, 1}}, /* S */
    {{1, 0}, {0, 1}, {1, 1}, {2, 1}}  /* T */
};

/* Caractères pour afficher les pièces */
char piece_chars[] = {'O', 'I', 'L', 'J', 'Z', 'S', 'T'};

/* Initialiser le plateau */
void initialiser_plateau() {
    int i, j;
    for (i = 0; i < HAUTEUR; i++) {
        for (j = 0; j < LARGEUR; j++) {
            plateau[i][j] = VIDE;
        }
    }
}

/* Afficher le plateau */
void afficher_plateau(struct piece *current) {
    int i, j, k;
    char temp_plateau[HAUTEUR][LARGEUR];
    
    system("cls"); // Effacer l'écran (Windows)
    
    /* Copier le plateau */
    for (i = 0; i < HAUTEUR; i++) {
        for (j = 0; j < LARGEUR; j++) {
            temp_plateau[i][j] = plateau[i][j];
        }
    }
    
    /* Ajouter la pièce courante */
    if (current != NULL) {
        for (k = 0; k < 4; k++) {
            int ligne = current->pos_ligne + current->la_piece[k].ligne;
            int colonne = current->pos_colonne + current->la_piece[k].colonne;
            if (ligne >= 0 && ligne < HAUTEUR && colonne >= 0 && colonne < LARGEUR) {
                temp_plateau[ligne][colonne] = current->type;
            }
        }
    }
    
    /* Afficher le plateau */
    printf("\n");
    for (i = 0; i < HAUTEUR; i++) {
        printf("|");
        for (j = 0; j < LARGEUR; j++) {
            printf("%c", temp_plateau[i][j]);
        }
        printf("|\n");
    }
    printf("+");
    for (j = 0; j < LARGEUR; j++) {
        printf("-");
    }
    printf("+\n");
    
    printf("\nControles:\n");
    printf("q: gauche  d: droite\n");
    printf("z: rotation gauche  c: rotation droite\n");
    printf("s: descendre  espace: descente rapide\n");
    printf("x: quitter\n");
}

/* Initialiser une pièce */
void initialiser_piece(struct piece *p, int indice) {
    int i;
    p->pos_colonne = LARGEUR / 2 - 1;
    p->pos_ligne = 0;
    for (i = 0; i < 4; i++) {
        p->la_piece[i] = tab_pieces[indice][i];
    }
    p->type = piece_chars[indice];
}

/* Vérifier collision */
int peut_descendre(struct piece *p) {
    int i;
    for (i = 0; i < 4; i++) {
        int nouvelle_ligne = p->pos_ligne + p->la_piece[i].ligne + 1;
        int colonne = p->pos_colonne + p->la_piece[i].colonne;
        
        if (nouvelle_ligne >= HAUTEUR || 
            (colonne >= 0 && colonne < LARGEUR && 
             nouvelle_ligne >= 0 && plateau[nouvelle_ligne][colonne] != VIDE)) {
            return 0;
        }
    }
    return 1;
}

/* Descendre une pièce */
int descendre_piece(struct piece *p) {
    if (peut_descendre(p)) {
        p->pos_ligne++;
        return 1;
    }
    return 0;
}

/* Déplacer à gauche */
int deplacer_gauche(struct piece *p) {
    int i;
    for (i = 0; i < 4; i++) {
        int nouvelle_colonne = p->pos_colonne + p->la_piece[i].colonne - 1;
        int ligne = p->pos_ligne + p->la_piece[i].ligne;
        
        if (nouvelle_colonne < 0 || 
            (ligne >= 0 && ligne < HAUTEUR && 
             nouvelle_colonne >= 0 && plateau[ligne][nouvelle_colonne] != VIDE)) {
            return 0;
        }
    }
    p->pos_colonne--;
    return 1;
}

/* Déplacer à droite */
int deplacer_droite(struct piece *p) {
    int i;
    for (i = 0; i < 4; i++) {
        int nouvelle_colonne = p->pos_colonne + p->la_piece[i].colonne + 1;
        int ligne = p->pos_ligne + p->la_piece[i].ligne;
        
        if (nouvelle_colonne >= LARGEUR || 
            (ligne >= 0 && ligne < HAUTEUR && 
             nouvelle_colonne >= 0 && plateau[ligne][nouvelle_colonne] != VIDE)) {
            return 0;
        }
    }
    p->pos_colonne++;
    return 1;
}

/* Rotation à gauche */
void rotation_gauche(struct piece *p) {
    int i;
    struct piece temp = *p;
    
    for (i = 0; i < 4; i++) {
        int temp_col = temp.la_piece[i].colonne;
        temp.la_piece[i].colonne = temp.la_piece[i].ligne;
        temp.la_piece[i].ligne = -temp_col;
    }
    
    /* Vérifier collision */
    for (i = 0; i < 4; i++) {
        int colonne = temp.pos_colonne + temp.la_piece[i].colonne;
        int ligne = temp.pos_ligne + temp.la_piece[i].ligne;
        
        if (colonne < 0 || colonne >= LARGEUR || ligne >= HAUTEUR || 
            (ligne >= 0 && plateau[ligne][colonne] != VIDE)) {
            return;
        }
    }
    
    *p = temp;
}

/* Rotation à droite */
void rotation_droite(struct piece *p) {
    int i;
    struct piece temp = *p;
    
    for (i = 0; i < 4; i++) {
        int temp_col = temp.la_piece[i].colonne;
        temp.la_piece[i].colonne = -temp.la_piece[i].ligne;
        temp.la_piece[i].ligne = temp_col;
    }
    
    /* Vérifier collision */
    for (i = 0; i < 4; i++) {
        int colonne = temp.pos_colonne + temp.la_piece[i].colonne;
        int ligne = temp.pos_ligne + temp.la_piece[i].ligne;
        
        if (colonne < 0 || colonne >= LARGEUR || ligne >= HAUTEUR || 
            (ligne >= 0 && plateau[ligne][colonne] != VIDE)) {
            return;
        }
    }
    
    *p = temp;
}

/* Fixer la pièce sur le plateau */
void fixer_piece(struct piece *p) {
    int i;
    for (i = 0; i < 4; i++) {
        int ligne = p->pos_ligne + p->la_piece[i].ligne;
        int colonne = p->pos_colonne + p->la_piece[i].colonne;
        
        if (ligne >= 0 && ligne < HAUTEUR && colonne >= 0 && colonne < LARGEUR) {
            plateau[ligne][colonne] = p->type;
        }
    }
}

/* Supprimer les lignes complètes */
int supprimer_lignes() {
    int i, j, k;
    int lignes_supprimees = 0;
    
    for (i = HAUTEUR - 1; i >= 0; i--) {
        int ligne_complete = 1;
        
        for (j = 0; j < LARGEUR; j++) {
            if (plateau[i][j] == VIDE) {
                ligne_complete = 0;
                break;
            }
        }
        
        if (ligne_complete) {
            lignes_supprimees++;
            for (k = i; k > 0; k--) {
                for (j = 0; j < LARGEUR; j++) {
                    plateau[k][j] = plateau[k-1][j];
                }
            }
            
            for (j = 0; j < LARGEUR; j++) {
                plateau[0][j] = VIDE;
            }
            
            i++; // Re-vérifier la même ligne après décalage
        }
    }
    
    return lignes_supprimees;
}

/* Vérifier si la partie est perdue */
int partie_perdue() {
    int j;
    for (j = 0; j < LARGEUR; j++) {
        if (plateau[0][j] != VIDE) {
            return 1;
        }
    }
    return 0;
}

int main() {
    srand(time(NULL));
    initialiser_plateau();
    
    int running = 1;
    int score = 0;
    
    printf("=== TETRIS (Version Console) ===\n");
    printf("Appuyez sur une touche pour commencer...\n");
    getch();
    
    while (running) {
        struct piece current;
        int piece_type = rand() % 7;
        initialiser_piece(&current, piece_type);
        
        int descente_OK = 1;
        
        while (descente_OK && running) {
            afficher_plateau(&current);
            printf("Score: %d\n", score);
            
            if (_kbhit()) { // Vérifier si une touche est pressée
                char key = getch();
                
                switch(key) {
                    case 'q':
                        deplacer_gauche(&current);
                        break;
                    case 'd':
                        deplacer_droite(&current);
                        break;
                    case 'z':
                        rotation_gauche(&current);
                        break;
                    case 'c':
                        rotation_droite(&current);
                        break;
                    case 's':
                        if (!descendre_piece(&current)) {
                            descente_OK = 0;
                        }
                        break;
                    case ' ':
                        while (descendre_piece(&current)) {
                            // Descente rapide
                        }
                        descente_OK = 0;
                        break;
                    case 'x':
                        running = 0;
                        break;
                }
            }
            
            // Attendre un peu
            Sleep(100);
            
            // Faire descendre automatiquement de temps en temps
            static int counter = 0;
            counter++;
            if (counter >= 10) {
                if (!descendre_piece(&current)) {
                    descente_OK = 0;
                }
                counter = 0;
            }
        }
        
        if (running) {
            // Fixer la pièce
            fixer_piece(&current);
            
            // Supprimer les lignes
            int lignes = supprimer_lignes();
            if (lignes > 0) {
                score += lignes * 100;
            }
            
            // Vérifier game over
            if (partie_perdue()) {
                afficher_plateau(NULL);
                printf("\n=== GAME OVER ===\n");
                printf("Score final: %d\n", score);
                running = 0;
            }
        }
    }
    
    printf("\nAppuyez sur une touche pour quitter...\n");
    getch();
    
    return 0;
}