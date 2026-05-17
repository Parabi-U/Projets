//Parabi Uddin
import java.util.ArrayList;
public class Oursin extends Herbivore implements Mangeable{

    public Oursin(Terrain t, int l, int c){
        super(t,l,c,"Oursin",10,10);
   }

    public Oursin(Oursin parent) {
        super(parent.ter, parent.ligne, parent.colonne, parent.getEspece(), 10, 10);
    }

//reproduction asexuelle donc ils se reproduivent par clonage
    public Oursin Reproduire() {
        if (this.getEnergie() >= 9 && this.getAge() >= 4) {
            this.addEnergie(-6);
            return new Oursin(this);
        }
        return null;
    }

    public int getNiveau(){
        return 1;
    }

    public int getValeurNutri(){
        return 1;
    }

    public AnimalMarin agir(ArrayList<AnimalMarin> agents)throws PositionInvalideException {
        veillier();
        manger();
        Oursin bebe = Reproduire();
        if (bebe != null) {
            Stats.incrementerReproductions();
            System.out.println("Naissance d'un Oursin ");
        }
        seDeplacer();
        return bebe;
    }

}