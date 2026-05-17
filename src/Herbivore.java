//Parabi Uddin
public abstract class Herbivore extends AnimalMarin{

    public Herbivore(Terrain t, int l, int c,String esp, int agem, int e){
        super(t,l,c,esp,agem,e);

    }

    public void manger() {
        Ressource r = ter.getCase(this.ligne, this.colonne);
        if (r instanceof Algues) {
            Algues algue = (Algues) r;
            algue.setQuantite(algue.getQuantite() - 1);
            this.addEnergie(1);
            System.out.println("Un herbivore à mangé");
            if (algue.getQuantite() <= 0) {
                ter.viderCase(this.ligne, this.colonne);
            }
    }

    }
}