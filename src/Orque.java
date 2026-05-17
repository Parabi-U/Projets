//Parabi Uddin
import java.util.ArrayList;
//predateur en haut de la chaine alimentaire donc ne sont pas mangable
public class Orque extends AnimalMarin{

    public Orque(Terrain t, int l, int c){
        super(t,l,c,"Orca",70,50);
    }

//ne mange pas les animaux de niveau & puisque ils sont trop petits
    public void manger(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Mangeable) {
                Mangeable proie = (Mangeable) a;
                boolean memeCase = a.getLigne() == this.ligne && a.getColonne() == this.colonne;
                boolean conditions = a.estVivant() && proie.getNiveau() == 2;
                if (memeCase && conditions) {
                    this.addEnergie(proie.getValeurNutri());
                    System.out.println("Un Orque à mangé");
                    a.meurt();
                    break;
                }
            }
        }
    }

    public Orque reproduire(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Orque && a != this && a.estVivant()) {
                Orque partenaire = (Orque) a;
                boolean memeCase = partenaire.getLigne() == this.ligne && partenaire.getColonne() == this.colonne;
                boolean conditions = this.getEnergie() >= 25 && this.getAge() >= 15 && partenaire.getEnergie() >= 25 && partenaire.getAge() >= 15;
                if (memeCase && conditions){ 
                        this.addEnergie(-10);
                        partenaire.addEnergie(-10);
                        return new Orque(ter, this.ligne, this.colonne);
                }
            }
        }
         return null;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents)throws PositionInvalideException {
        veillier();
        manger(agents);
        Orque bebe = reproduire(agents);
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'une Orque ");
        }
        seDeplacer();
        return bebe;
    }

}