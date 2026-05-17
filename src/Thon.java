//Parabi Uddin
import java.util.ArrayList;
public class Thon extends AnimalMarin implements Mangeable{

    public Thon(Terrain t, int l, int c){
        super(t,l,c,"Thon",23,30);
    }

    public void manger(ArrayList<AnimalMarin> agents){
        for (AnimalMarin a : agents) {
            if (a instanceof Mangeable){
                Mangeable proie = (Mangeable) a;
                boolean memeCase = a.getLigne() == this.ligne && a.getColonne() == this.colonne;
                boolean conditions = a.estVivant() && proie.getNiveau() < this.getNiveau();
                if(memeCase && conditions){
                    this.addEnergie(proie.getValeurNutri());
                    System.out.println("Un Thon à mangé");
                    a.meurt();
                    break;
                }
        }    
    }
    }

    public Thon reproduire(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Thon && a != this && a.estVivant()) {
                Thon partenaire = (Thon) a;
                boolean memeCase = partenaire.getLigne() == this.ligne && partenaire.getColonne() == this.colonne;
                boolean conditions = this.getEnergie() >= 15 && this.getAge() >= 6 && partenaire.getEnergie() >= 15 && partenaire.getAge() >= 6;
                if (memeCase && conditions){ 
                    this.addEnergie(-7);
                    partenaire.addEnergie(-7);
                    return new Thon(ter, this.ligne, this.colonne);
                }
            }
        }
        return null;
    }

    public int getNiveau(){
        return 2;
    }

    public int getValeurNutri(){
        return 10;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents) throws PositionInvalideException{
        veillier();
        manger(agents);
        Thon bebe = reproduire(agents);
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'un Thon ");
        }
        seDeplacer();
        return bebe;
    }
}