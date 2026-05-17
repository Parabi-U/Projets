//Parabi Uddin
import java.util.ArrayList;
public class Requin extends AnimalMarin implements Mangeable{

    public Requin(Terrain t, int l, int c){
        super(t,l,c,"Requin",30,35);
    }

    public Requin(Terrain t, int l, int c,String esp,int agem, int e){
        super(t,l,c,esp,agem,e);
    }


    public void manger(ArrayList<AnimalMarin> agents){
        for (AnimalMarin a : agents) {
            if (a instanceof Mangeable){
                Mangeable proie = (Mangeable) a;
                boolean memeCase = a.getLigne() == this.ligne && a.getColonne() == this.colonne;
                boolean conditions = a.estVivant() && proie.getNiveau() < this.getNiveau();
                if(memeCase && conditions){
                    this.addEnergie(proie.getValeurNutri());
                    System.out.println("Un Requin à mangé");
                    a.meurt();
                    break;
                }
        }    
    }
    }

    public Requin reproduire(ArrayList<AnimalMarin> agents) {
        for (AnimalMarin a : agents) {
            if (a instanceof Requin && a != this && a.estVivant()) {
                Requin partenaire = (Requin) a;
                boolean memeCase = partenaire.getLigne() == this.ligne && partenaire.getColonne() == this.colonne;
                boolean conditions = this.getEnergie() >= 23 && this.getAge() >= 15 && partenaire.getEnergie() >= 23 && partenaire.getAge() >= 15;
                if (memeCase && conditions){ 
                        this.addEnergie(-9);
                        partenaire.addEnergie(-9);
                        return new Requin(ter, this.ligne, this.colonne);
                }
            }
        }
        return null;
    }

    public int getNiveau(){
        return 2;
    }

    public int getValeurNutri(){
        return 8;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents)throws PositionInvalideException {
        veillier();
        manger(agents);
        Requin bebe = reproduire(agents);
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'un Requin ");
        }
        seDeplacer();
        return bebe;
}

}