import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from create_table_fpdf2 import PDF




def generateNoise(minval, maxval):
     return np.random.uniform(minval, maxval)
 

def calculate_performance_metrics(time, target, yest):
    
    delta_t = np.diff(time, prepend=0)  

    # Hata hesaplaması
    error = target - yest

    # İstenen performans ölçütlerini hesaplayalım
    ise = np.sum(error**2 * delta_t)
    iae = np.sum(np.abs(error) * delta_t)
    itae = np.sum(time * np.abs(error) * delta_t)
    itse = np.sum(time * error**2 * delta_t)

    return ise, iae, itse, itae

        
class Plotter:
    def __init__(self, xlabel='X Ekseni', ylabel='Y Ekseni', title=None):
        self.x_data = []
        self.y_data = []
        self.labels = []
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        plt.style.use('seaborn-dark')  

    def addplot(self, x, y, label=None):
        """
        Verilen x ve y verilerini, belirtilen etiketle birlikte grafik üzerine çizer.

        Parametreler:
        x (list): x eksenindeki değerlerin listesi.
        y (list): y eksenindeki değerlerin listesi.
        label (str, optional): Veri setinin etiketi. Varsayılan olarak None.

        Dönüş:
        None
        """
        self.x_data.append(x)
        self.y_data.append(y)
        self.labels.append(label)

    def show(self, time=None):
        """
        Önceden eklenen tüm veri setlerini tek bir grafik üzerine çizer.

        Parametreler:
        time (list, optional): x ekseninin çizdirileceği zaman aralığı. 
                              Varsayılan olarak None (tüm veri setini çizer).

        Dönüş:
        None
        """
        plt.figure(figsize=(10, 4))
        for i in range(len(self.x_data)):
            if time:
                # Zaman aralığına göre x verilerini filtrele
                start, end = time
                x_subset = []
                y_subset = []
                for idx, val in enumerate(self.x_data[i]):
                    if start <= val <= end:
                        x_subset.append(val)
                        y_subset.append(self.y_data[i][idx])
                plt.plot(x_subset, y_subset, label=self.labels[i])
            else:
                plt.plot(self.x_data[i], self.y_data[i], label=self.labels[i])
        
        plt.xlabel(self.xlabel, fontsize=14)
        plt.ylabel(self.ylabel, fontsize=14)
        plt.title(self.title, fontsize=14)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.grid(visible=True)
        plt.legend(fontsize=12)
        
        # Zaman aralığına göre x eksenini ayarla
        if time:
            plt.xlim(time)

        plt.show()
        
        
        
class Tablo:
    def __init__(self, *headers):
        self.headers = headers
        self.data = []

    def adddata(self, *args):
        if len(args) != len(self.headers):
            raise ValueError("Number of values provided doesn't match number of headers")
        self.data.append(args)

    def show(self):
        print(tabulate(self.data, headers=self.headers, tablefmt="presto"))

    def createpdf(self, filename='tablo.pdf'):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Times", size=10)

        data = [self.headers] + self.data
        pdf.create_table(table_data=data, title='Error Values', cell_width='uneven', x_start=25)
        pdf.ln()
        pdf.output(filename)        




class Subplotter:
    def __init__(self, sumplot):
        self.sumplot = sumplot
        self.subplot_count = 0
        self.fig = plt.figure()


        

    def addsubplot(self, x_data, y_data, title='', xlabel='', ylabel=''):
        """
        Verilen x ve y verilerini yeni bir subplot olarak ekler.

        Parametreler:
        x_data (list): x eksenindeki değerlerin listesi.
        y_data (list): y eksenindeki değerlerin listesi.
        title (str, optional): Subplot başlığı. Varsayılan olarak boştur.
        xlabel (str, optional): x ekseninin etiketi. Varsayılan olarak boştur.
        ylabel (str, optional): y ekseninin etiketi. Varsayılan olarak boştur.

        Dönüş:
        None
        """
        self.subplot_count += 1
        ax = self.fig.add_subplot(self.sumplot, 1, self.subplot_count)
        for i in range(len(x_data)):
            ax.plot(x_data[i], y_data[i])
        ax.set_title(title, fontsize=14)
        ax.set_xlabel(xlabel, fontsize=14)
        ax.set_ylabel(ylabel, fontsize=14)        
        #ax.tick_params(axis='both', which='major', labelsize=12)
        
        ax.grid(visible=True)
       

    def show(self):
        """
        Eklenen tüm subplotları tek bir sütun halinde gösterir.

        Parametreler:
        None

        Dönüş:
        None
        """
        plt.tight_layout()
        plt.show()
        
def customFilter(sample, x_array=None):
    b = np.full(10, 1/10)  # FIR filtresinin katsayıları
    
    
    
    if x_array is None:
        x_array = np.zeros_like(b)
    
    # x_array dizisini kaydırın
    x_array = np.roll(x_array, 1)
    x_array[-1] = sample
    
    
    filteredSignal = np.sum(x_array * b)
    
    return filteredSignal, x_array