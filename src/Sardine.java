//Parabi Uddin
import java.util.ArrayList;
public class Sardine extends Herbivore implements Mangeable{

    public Sardine(Terrain t, int l, int c){
        super(t,l,c,"Sardine",7,12);
    }

    public Sardine reproduire(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Sardine && a != this && a.estVivant()) {
                Sardine partenaire = (Sardine) a;
                boolean memeCase = partenaire.getLigne() == this.ligne && partenaire.getColonne() == this.colonne;
                boolean conditions = this.getEnergie() >= 5 && this.getAge() >= 2 && partenaire.getEnergie() >= 5 && partenaire.getAge() >= 2;
                if (memeCase && conditions){ 
                        this.addEnergie(-3);
                        partenaire.addEnergie(-3);
                        return new Sardine(ter, this.ligne, this.colonne);
                }
            }
        }
        return null;
    }

    public int getNiveau(){
        return 1;
    }

    public int getValeurNutri(){
        return 3;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents)throws PositionInvalideException {
        veillier();
        manger();
        Sardine bebe = reproduire(agents);
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'une Sardine ");
        }
        seDeplacer();
        return bebe;
    }

}