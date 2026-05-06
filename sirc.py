import numpy as np
import matplotlib.pyplot as plt


class Epidemie:

    def __init__(self, dosis_bei_der_die_hälfte_krank_wird, dauer_der_simulation, erreger_produktion, erregerzerfall, sterberate, volumen, population):

        #Bereich der möglichen id50 werte
        self.id50 = dosis_bei_der_die_hälfte_krank_wird

        #Virenproduktionsrate
        self.sigma = erreger_produktion

        #Viruszerfall 
        self.delta = erregerzerfall

        #sterberate
        self.gamma = sterberate

        # Volumen in m^3
        self.v = volumen

        # Populationsgrösse
        self.population = population

        #Simulationsdauer
        self.dauer_der_simulation = dauer_der_simulation



    def system_definition(self):
        #Vektor welcher Anfangszustand beschreibt 

            system = np.array([[self.population-1],[1],[0],[0]])
            epidemie = np.zeros((4,self.dauer_der_simulation+1))
            epidemie[:,0] = system[:,0]

            return system, epidemie
    
    
    def berechnungTransformationsmatrix(self, id50, c):
        beta = float((c) / (id50 + c))
        
        A = np.array([[1-beta,0,0,0],
                  [beta, 1-self.gamma,0,0],
                  [0,self.gamma,1,0],
                  [0,self.sigma/(self.v*1000000),0,self.delta]])
        
        return A
    
    def simulation(self):

        self.verläufe = []
        
        for j in range(self.id50[0], self.id50[1], 50):
            system, epidemie = self.system_definition()

            for i in range(self.dauer_der_simulation):
                matrix = self.berechnungTransformationsmatrix(j,system[3,0])
                system = matrix@system
                epidemie[:,i+1] = system[:,0]
                print(matrix)
    
            self.verläufe.append(epidemie)
        
        self.verläufe = np.array(self.verläufe)  # (bereich beta, 4, dauer)


        return self.verläufe




    def kontzentrations_plot(self, verläufe):
        t = np.arange(self.dauer_der_simulation+1)
        plt.figure()
        for verlauf in verläufe:
                plt.plot(t, verlauf[3, :], color="green", alpha=0.5)
        #plt.axvline(x=177, color='red', linestyle='-', label='Marker')
        plt.title("Viruskonzentration [pfu/ml]")
        plt.grid()
        plt.show()
        

    def populations_plot(self, verläufe):
        titel = ["Anfällige", "Infizierte", "Entfernte"]
        farben = ["blue", "orange", "red"]
        t = np.arange(self.dauer_der_simulation + 1)

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))  # 1 row, 3 columns

        for k in range(3):
            for verlauf in verläufe:

                axes[k].plot(t, verlauf[k, :], color=farben[k], alpha=0.9)
                
            #axes[k].axvline(x=177, color='red', linestyle='-', label='Marker')
            axes[k].axis([0, self.dauer_der_simulation, 0, self.population])
            axes[k].set_title(titel[k])
            axes[k].grid()
            axes[k].set_xlabel("Tage")
            axes[k].set_ylabel("Populationsgrösse")
            
        plt.tight_layout()
        plt.show()

    