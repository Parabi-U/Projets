//Parabi Uddin
import java.util.ArrayList;
public abstract class AnimalMarin{ 
    protected Terrain ter;
    protected int ligne;
    protected int colonne;
    private String espece;
    private int age;
    private boolean vivant = true;
    private int age_max;
    private int energie;


    public AnimalMarin(Terrain t, int l, int c, String esp, int agem, int e){
        this.ter = t;
        this.ligne = l;
        this.colonne = c;
        this.espece = esp;
        this.age = 0;
        this.age_max = agem;
        this.energie = e;
    }


    public void veillier(){
        if(this.age < this.age_max && this.energie > 0){
            this.age ++;
            this.energie --;
        }
        else{
            this.age ++;
            this.energie --;
            this.meurt();
        }

    }

    public void meurt(){
        this.vivant = false;
        System.out.println("Un " + this.espece + " est mort");
    }

    public abstract AnimalMarin agir(ArrayList<AnimalMarin> agents)throws PositionInvalideException ;

    public double distance(int lig, int col) {
        int dLig = this.ligne - lig;
        int dCol = this.colonne - col;
        return Math.sqrt(dLig*dLig + dCol*dCol);
    }

    public void seDeplacer(int l, int c) throws PositionInvalideException {
        if (this.ter.sontValides(l, c)) {
            this.ligne = l;
            this.colonne = c;
            this.energie--;
        }
        else{
            throw new PositionInvalideException(l, c);
        }
    }

    public void seDeplacer(){
        this.ligne = (int)(Math.random()*this.ter.nbLignes) + 1;
        this.colonne = (int)(Math.random()*this.ter.nbColonnes) + 1;
        this.energie --;
    }


    public void addEnergie(int add){
        this.energie += add;
    }


    public int getLigne(){ 
        return this.ligne;
        }

    public int getColonne(){
        return this.colonne;
    }

    public boolean estVivant(){ 
        return this.vivant; 
    }
    public String getEspece(){
        return this.espece; 
    }
    public int getAge(){
         return this.age; 
    }
    public int getEnergie(){
        return this.energie;
    }

}