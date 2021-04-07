import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

dfsf = pd.read_csv("../Datasets/1044.txt", delimiter = "\t")
dfgs = pd.read_csv("../Datasets/outg.csv")
dfgd = pd.read_csv("../Datasets/outd.csv")

app = Flask(__name__)


#Algorithm
def algo():
    common_syps = ["Fever", "Nausea", "Cough", "Pain", "Muscle Weakness", "Vomiting"]
    sym_now = common_syps
    [print(i) for i in common_syps]

    total_sym_p_have=[]
    print("Do u have any of symptoms above : ")
    u_have_more_sym = int(input("enter 1 for YES, O for NO : "))

    while(u_have_more_sym):
        nos = int(input("enter the no. of symptoms u have : "))
        uni_syms = set()
        sym_current = []
        for i in range(nos):
            sym = input("enter the name of symptom u have : ")
            total_sym_p_have.append(sym)
            sym_current.append(sym)
        #print("sym_current", sym_current)
        for each_sym in sym_current:
            #------------finding top most 4 disease acc to given symptom ----------------
            t4d = list(dfgs[dfgs["MeSH Symptom Term"]==each_sym]["MeSH Disease Term"][:4])
            #------------finding most freq syms in acc with t4d -------------------------
            #-----next possible symptoms-------
            for dis in t4d:
                t4ds = list(dfgd[dfgd["MeSH Disease Term"]==dis]["MeSH Symptom Term"][:4])
                uni_syms = uni_syms.union(set(t4ds))
        uni_syms = list(uni_syms)
        #print(uni_syms)
        df = pd.DataFrame(columns = dfsf.columns)
        for each_sym in uni_syms:
                df = df.append(dfsf[dfsf["MeSH Symptom Term"]==each_sym])
        df.sort_values(by=["PubMed occurrence"], ascending=False,inplace = True)
        #print(df)
        top15_sym = list(df["MeSH Symptom Term"][:15])
        #------------------------display top 15-----------
        print("\n--------- SEE IF U HAVE MORE SYMPTOMS FROM ANY OF GIVEN BELOW ------------------------ \n")
        [print(i) for i in top15_sym]
        print("\nDo u more symptoms ..??")
        print("\nenter 1 for yes, for NO enter 0 :")
        u_have_more_sym = int(input("\n enter 0 or 1 : "))
        # if dont have then make u_have_more_sym = 0
        # else goto top of while loop again
    print("\n Total symptoms Patient Have : ", len(total_sym_p_have))
    [print(i) for i in total_sym_p_have]
    return total_sym_p_have



@app.route('/out')
def out():
    out = algo()
    return jsonify(symptoms=out)

if __name__ == "__main__":    
    app.run(debug = True)