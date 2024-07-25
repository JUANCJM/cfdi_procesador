import tkinter as tk
from tkinter import filedialog,ttk,messagebox
import os
import pandas as pd
from tqdm import tqdm
import re

periodo=int()
path=""
rutaOrigen=""
meses = {"202401":"ENERO","202402":"ENERO","202403":"FEBRERO","202404":"FEBRERO","202405":"MARZO","202406":"MARZO","202407":"ABRIL","202408":"ABRIL","202409":"MAYO","202410":"MAYO","202411":"JUNIO","202412":"JUNIO","202413":"JULIO","202414":"JULIO","202415":"AGOSTO","202416":"AGOSTO","202417":"SEPTIEMBRE","202418":"SEPTIEMBRE","202419":"OCTUBRE","202420":"OCTUBRE","202421":"NOVIEMBRE","202422":"NOVIEMBRE","202423":"DICIEMBRE","202424":"DICIEMBRE"}


def dirOrigen():
    rutaOrigen = filedialog.askopenfilename(title="Seleccionar archivo CSV",
    filetypes=[("Archivos CSV", "*.csv")])
    if rutaOrigen:
        txtOrigen.configure(state='normal')
        txtOrigen.delete('0', tk.END)
        txtOrigen.insert('insert', rutaOrigen)
        txtOrigen.configure(state='readonly')

def procesar():
    if txtOrigen.get()=="":
        messagebox.showwarning(title="Aviso",message="Debe seleccionar la ruta de los archivos.")
    else:
        btnProcesar.config(state="disabled")
        progressListF.config(mode="indeterminate")
        progressListF.start(30)
        path=os.path.dirname(txtOrigen.get())
        lblinfos.config(text=f"Listando archivos de la ruta: {path}")
        window.update()

        excel=pd.read_csv(txtOrigen.get())

        total_rows = excel.shape[0]

        folder=os.walk(path)
        pattern = r".*(ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE).*(\w{13})_(.*).pdf"

        myfiles = dict()


        for root, dirs, files in folder:
            for file in files:
                fname = os.path.join(root, file)
                match = re.search(pattern, fname)
                if match:
                    myfiles[f"{match.group(2)}_{match.group(1)}"] = match.group(3)
                    lblinfos.config(text=f"Mapeando {match.group(1)}")
                window.update()
        progressListF.stop()
        progressListF.config(mode="determinate")

        progressListF["maximum"]=total_rows

        for idx,row in  excel.iterrows():
            rfc=row["RFC"]
            periodo_proc = row["PERIODO_PROC"]    
            quincena = int(periodo_proc) if pd.notna(periodo_proc) else 0
            if quincena>0:
                try:        
                    excel.at[idx,"UUID"]=str(myfiles[f"{rfc}_{meses[str(quincena)]}"])
                except:
                    excel.at[idx,"UUID"]="No encontrado"
            progressListF["value"]=idx+1
            lblinfos.config(text=f"Buscando {rfc} periodo {quincena}")
            window.update()

        lblinfos.config(text="Generando archivo ...")
        window.update()
        
        excel.to_csv(f"{path}/{os.path.splitext(os.path.basename(txtOrigen.get()))[0]}-Procesado.csv")

        lblinfos.config(text="Archivo generado")
        window.update()
        messagebox.showinfo(title="Aviso",message="Proceso Completado")




window=tk.Tk()

window.title("Procesar carpetas")

lblOrigen = tk.Label(window, text="Ruta de origen:")
lblOrigen.grid(column=0, row=0)
txtOrigen = tk.Entry(window, text="", width=85)
txtOrigen.grid(column=0, row=1, padx=5, pady=10,)
txtOrigen.configure(state='readonly')
btnOrgien = tk.Button(window, text="seleccionar origen", command=dirOrigen)
btnOrgien.grid(column=1, row=1, padx=(0,5), pady=10,)

btnProcesar = tk.Button(text="Generar listado",command=procesar)
btnProcesar.grid(column=0, row=2)

lblinfos=tk.Label(window,text="",anchor="w")
lblinfos.grid(column=0,row=3,padx=5,columnspan=2,sticky="we")

progressListF=ttk.Progressbar(window,orient="horizontal",)
progressListF.grid(column=0,row=4,padx=5, pady=10,columnspan=2,sticky="we")

window.mainloop()

'''


'''