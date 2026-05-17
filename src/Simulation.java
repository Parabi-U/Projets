//Parabi Uddin
import java.util.ArrayList;

public class Simulation {
    private Terrain terrain;
    private ArrayList<AnimalMarin> agents;
    private ArrayList<Ressource> ressources;
    private int nbEtapes;

    public Simulation(int lignes, int colonnes, int nbAlgues, int nbCrevettes, int nbSardines, int nbOursins, int nbThons, int nbRequins, int nbOrques, int nbEtapes) {
        this.terrain = new Terrain(lignes, colonnes);
        this.agents = new ArrayList<>();
        this.ressources = new ArrayList<>();
        this.nbEtapes = nbEtapes;
        initialiser(nbAlgues, nbCrevettes, nbSardines, nbOursins, nbThons, nbRequins, nbOrques);
    }

    private int rand(int max) {
        return (int)(Math.random() * max) + 1;
    }

    // place les algues et les agents aleatoirement sur le terrain
    private void initialiser(int nbAlgues, int nbCrevettes, int nbSardines, int nbOursins, int nbThons, int nbRequins, int nbOrques) {
        for (int i = 0; i < nbAlgues; i++) {
            int l = rand(terrain.nbLignes);
            int c = rand(terrain.nbColonnes);
            if (terrain.caseEstVide(l, c)) {
                Algues alg = new Algues(1, 2);
                terrain.setCase(l, c, alg);
                ressources.add(alg);
            }
        }
        for (int i = 0; i < nbCrevettes; i++){
            agents.add(new Crevette(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
        for (int i = 0; i < nbSardines; i++){
            agents.add(new Sardine(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
        for (int i = 0; i < nbOursins; i++){
            agents.add(new Oursin(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
        for (int i = 0; i < nbThons; i++){
            agents.add(new Thon(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
        for (int i = 0; i < nbRequins; i++){
            agents.add(new Requin(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
        for (int i = 0; i < nbOrques; i++){
            agents.add(new Orque(terrain, rand(terrain.nbLignes), rand(terrain.nbColonnes)));
        }
    }

    // une etape de la simulation
    public void etape(int numEtape) {
        System.out.println("\n========== ETAPE " + numEtape + " ==========");
        ArrayList<AnimalMarin> nouveaux = new ArrayList<>();
        for (AnimalMarin a : agents) {
            if (a.estVivant()) {
            try {
                // Agir = veilliers/ manger / reproduire / se deplacer
                AnimalMarin bebe = a.agir(agents);
                if (bebe != null) {
                    nouveaux.add(bebe);
                }
            } catch (PositionInvalideException e) {
                System.out.println("Erreur deplacement : " + e.getMessage());
            }
        }
    }
        for (Ressource r : ressources) {
            if (r instanceof Algues) {
                ((Algues) r).croix();
            }
        }
        // retirer les morts
        int avantNettoyage = agents.size();
        ArrayList<AnimalMarin> vivants = new ArrayList<>();
        for (AnimalMarin a : agents) {
            if (a.estVivant()) {
                vivants.add(a);
            }
        }
        agents = vivants;
        Stats.incrementerMorts(avantNettoyage - agents.size());
        agents.addAll(nouveaux); // Ajoute tous les nouveaux bebes

        // affichage des informations de l'etape
        terrain.afficher(6);
        System.out.println(terrain);
        System.out.println("Agents vivants : " + agents.size());
        System.out.println("Ressources sur le terrain : " + terrain.compterRessources());
        Stats.afficher();
    }

    // lance toutes les etapes
    public void lancer() {
        System.out.println("=== Debut de la simulation ===");
        terrain.afficher(6);
        for (int i = 1; i <= nbEtapes; i++) {
            etape(i);
            if (agents.isEmpty()) {
                System.out.println("Tous les agents sont morts a l'etape " + i);
                break;
            }
        }
        System.out.println("\n=== Fin ===");
        Stats.afficher();
    }
}