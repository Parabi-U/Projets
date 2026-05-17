//Parabi Uddin
public class Algues extends Ressource{
    private int tauxcroix;


    public Algues(int qi,int tdc){
        super("Algues",qi);
        this.tauxcroix = tdc;   
    }

    public void croix(){
        this.setQuantite(this.getQuantite() + this.tauxcroix);
    }

    


}