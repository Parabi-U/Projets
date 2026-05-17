//Parabi Uddin
import java.util.ArrayList;
public class Crevette extends Herbivore implements Mangeable{

    public Crevette(Terrain t, int l, int c){
        super(t,l,c,"Crevette",5,10);
    }


    public Crevette reproduire(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Crevette && a != this && a.estVivant()) {
                Crevette partenaire = (Crevette) a;
                boolean memeCase = partenaire.getLigne() == this.ligne && partenaire.getColonne() == this.colonne;
                boolean conditions = this.getEnergie() >= 3 && this.getAge() >= 1 && partenaire.getEnergie() >= 3 && partenaire.getAge() >= 1;
                if (memeCase && conditions){ 
                        this.addEnergie(-2);
                        partenaire.addEnergie(-2);;
                        return new Crevette(ter, this.ligne, this.colonne);
                }
            }
        }    
        return null;
    }

    public int getNiveau(){
        return 1;
    }

    public int getValeurNutri(){
        return 2;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents) throws PositionInvalideException {
        this.veillier();
        this.manger();
        Crevette bebe = reproduire(agents);
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'une Crevette");
        }
        seDeplacer();
        return bebe;
    }

}