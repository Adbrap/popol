# ----- initialisation des modules -----#
import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import math
#from playsound import playsound
import webbrowser
import random
# ----- initialisation des modules -----#
activ = False
activactiv = False
antholemuscler = False
compteurjson = 1

def confirmer(event,arg1,placeA,data,url):
    global compteurjson
    arg1 = arg1.drop(range(0, placeA - 1))
    arg1 = arg1.reset_index(drop=True)
    arg1.to_json(f'json_recent/{compteurjson}.json')
    #webbrowser.open(url)

def Indicateurs(event):
    global antholemuscler
    antholemuscler = True
# ----- initialisation des fonctions lies au boutons -----#

# ----- initialisation des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE

w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialisation des couleurs du modules pystyle -----#

# ----- initialisation des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
#end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15000))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialisation des temps de recherches -----#

# ----- initialisation de l'API key et ticker -----#
api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
#api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
# ----- initialisation de l'API key et ticker -----#

# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
# ----- fonction pour trouver les point intersection de la ligne de coup et de la Courbe -----#

# ----- fonction Principale -----#
def Finder_IETE(time1, time_name1, start, end, start2, TETE, lettre):
    global ticker
    global antholemuscler
    global compteurjson
    # while True:
    i = 0
    fa = 0
    fb = 1
    fc = 1
    fd = 2
    fe = 2
    ff = 3
    fg = 3
    compteur = 0
    compteur2 = 0
    compteur3 = 0
    a = 0
    # ----- Appel des données Polygon.io OHLC et creation du DF -----#
    while i != 1:

        with my_lock:

            # api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
            api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
            data = requests.get(api_url_OHLC).json()
            df = pd.DataFrame(data['results'])

            api_url_OHLC2 = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start2}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
            data2 = requests.get(api_url_OHLC2).json()
            df2 = pd.DataFrame(data2['results'])


        # ----- creation des locals(min/max) -----#
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        local_max1 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min1 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]

        local_max2 = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min2 = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        # ----- creation des locals(min/max) -----#

        # ----- suppression des points morts de la courbe -----#
        test_min = []
        test_max = []

        # if local_min[0] > local_max[0]:
        #        local_max = local_max[1:]
        #        print('On a supprimer le premier point')
        #
        q = 0
        p = 0

        len1 = len(local_min)
        len2 = len(local_max)
        while p < len1 - 5 or p < len2 - 5:
            if local_min[p + 1] < local_max[p]:
                test_min.append(local_min[p])
                local_min = np.delete(local_min, p)

                p = p - 1
            if local_max[p + 1] < local_min[p + 1]:
                test_max.append(local_max[p])
                local_max = np.delete(local_max, p)

                p = p - 1
            p = p + 1

            len1 = len(local_min)
            len2 = len(local_max)

        highs = df.iloc[local_max, :]
        lows = df.iloc[local_min, :]
        highs1 = df.iloc[test_max, :]
        lows1 = df.iloc[test_min, :]

        decalage = 0
        # ----- suppression des points morts de la courbe -----#

        # ----- initialisation des pointeurs de la figure -----#
        print(len(df.iloc[local_max, :]))
        while i != 1:
            if ((len(df.iloc[local_max, :])) - (ff)) > 1 and ((len(df.iloc[local_min, :])) - (ff)) > 1:

                A = float(highs['c'].iloc[fa])
                B = float(lows['c'].iloc[fb])
                C = float(highs['c'].iloc[fc])
                D = float(lows['c'].iloc[fd])
                E = float(highs['c'].iloc[fe])
                F = float(lows['c'].iloc[ff])
                G = float(highs['c'].iloc[fg])

                data_A = []
                data_B = []
                data_C = []
                data_D = []
                data_E = []
                data_F = []
                data_G = []
                # ----- initialisation des pointeurs de la figure -----#

                # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#
                if C > E:
                    differ = (C - E)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas
                if C < E:
                    differ = (E - C)
                    pas = (local_max[fe] - local_max[fc])
                    suite = differ / pas
                # ----- determination du 'PAS' de la pente de la LDC pour la prolonger plus loins que C et E -----#

                # ----- PRINT affichage dans la console -----#
                Write.Print(f"  >> RECHERCHE IETE:", Colors.white, interval=0.000)
                Write.Print(f"  {ticker}", Colors.green, interval=0.000)
                Write.Print(f"  {time1} {time_name1} {start}", Colors.cyan, interval=0.000)
                Write.Print("  <<", Colors.white, interval=0.000)
                print('')
                # ----- PRINT affichage dans la console -----#

                # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#
                rouge = []
                vert = []
                bleu = []

                rouge.append(local_max[fa])
                rouge.append(local_min[fb])
                rouge.append(local_max[fc])
                rouge.append(local_min[fd])
                rouge.append(local_max[fe])
                rouge.append(local_min[ff])
                rouge.append(local_max[fg])

                vert.append(local_max[fa])
                vert.append(local_max[fc])
                vert.append(local_max[fe])
                vert.append(local_max[fg])

                i = 0
                for i in range(local_min[fa]-1, len(df)):
                    bleu.append(i)


                mirande2 = df.iloc[vert, :]
                mirande = df.iloc[rouge, :]
                mirande3 = df.iloc[bleu, :]

                local_max_pp = argrelextrema(mirande3['c'].values, np.greater, order=1, mode='clip')[0]
                local_min_pp = argrelextrema(mirande3['c'].values, np.less, order=1, mode='clip')[0]

                # ----- creation des differentes courbe: rouge(surlignage figure), vert(ligne de coup), bleu(la figure en zoomer)-----#

                # ----- determiner la direction pente LDC et allongement apres E et C -----#
                if activ == True:
                    fig1 = plt.figure(figsize=(10, 7))
                    plt.plot([], [], " ")
                    fig1.patch.set_facecolor('#17DE17')
                    fig1.patch.set_alpha(0.3)
                    plt.title(f'IETE : {ticker} {start} | {end}', fontweight="bold", color='black')
                    mirande3['c'].plot(color=['blue'], label='Clotures')
                    mirande['c'].plot(color=['red'], label='Clotures', alpha=0.3)
                    plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    plt.text(local_max[fg], G, f"G {round(G,5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                    #mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                    plt.scatter(local_max[fa], A, color='blue')
                    plt.scatter(local_min[fb], B, color='blue')
                    plt.scatter(local_max[fc], C, color='blue')
                    plt.scatter(local_min[fd], D, color='blue')
                    plt.scatter(local_max[fe], E, color='blue')
                    plt.scatter(local_min[ff], F, color='blue')
                    plt.scatter(local_max[fg], G, color='blue')
                    plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                    # plt.scatter(x=low.index, y=low["c"])
                    plt.show()








                if E > C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] - ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] + ((suite * (local_max[fg] - local_max[fe])))
                if E < C:
                    mirande2['c'].values[0] = mirande2['c'].values[1] + ((suite * (local_max[fc] - local_max[fa])))
                    mirande2['c'].values[3] = mirande2['c'].values[2] - ((suite * (local_max[fg] - local_max[fe])))
                if E == C:
                    mirande2['c'].values[0] = df['c'].values[local_max[fc]]
                    mirande2['c'].values[3] = df['c'].values[local_max[fe]]
                # ----- determiner la direction pente LDC et allongement apres E et C -----#

                # ----- transformer le tableau en DF avec les donnée du DF reel -----#
                vert1 = {'c': vert}
                vert2 = pd.DataFrame(data=vert1)
                rouge1 = {'c': rouge}
                rouge2 = pd.DataFrame(data=rouge1)
                bleu1 = {'c': bleu}
                bleu2 = pd.DataFrame(data=bleu1)
                # ----- transformer le tableau en DF avec les donnée du DF reel -----#

                # ----- preparation des deux courbes pour determiner intersection de I et J -----#
                # --- premiere droite cotée gauche ---#
                AI = [local_max[fa], mirande2['c'].iloc[0]]
                BI = [local_max[fc], mirande2['c'].iloc[1]]
                # --- premiere droite coté gauche ---#

                # --- deuxieme droite coté gauche ---#
                CI = [local_max[fa], A]
                DI = [local_min[fb], B]
                # I = line_intersection((AI, BI), (CI, DI))
                # --- deuxieme droite coté gauche ---#

                # --- premiere droite cotée droit ---#
                AJ = [local_max[fe], mirande2['c'].iloc[2]]
                BJ = [local_max[fg], mirande2['c'].iloc[3]]
                # --- premiere droite cotée droit ---#

                # --- deuxieme droite coté droit ---#
                CJ = [local_max[fg], G]
                DJ = [local_min[ff], F]
                # J = line_intersection((AJ, BJ), (CJ, DJ))
                # --- deuxieme droite coté droit ---#
                # ----- preparation des deux courbes pour determiner intersection de I et J -----#

                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!
                pop = 0
                verif = 0

                for pop in range(0, len(test_min)):
                    if test_min[pop] > local_max[fa] and test_min[pop] < local_max[fg]:
                        verif = verif + 1
                pop = 0
                for pop in range(0, len(test_max)):
                    if test_max[pop] > local_max[fa] and test_max[pop] < local_max[fg]:
                        verif = verif + 1
                # ----- verification qu'il n'y est pas de point mort dans la figure -----# ------------------- VERIFIER !!


                # ----- condition pour que l'ordre des point de la figure soit respecter -----#
                ordre = False
                if local_max[fa] < local_min[fb] < local_max[fc] < local_min[fd] < local_max[fe] < local_min[ff]:
                    ordre = True
                # ----- condition pour que l'ordre des point de la figure soit respecter -----#

                # ----- condition pour que la tete fasse au minimum 2.8% -----#
                mini_pourcent = False
                if ((((C + E) / 2) - D) * 100) / D >= 2.8:
                    mini_pourcent = True
                # ----- condition pour que la tete fasse au minimum 2.8% -----#

                # ----- condition pour garantir la forme de l'iete  -----#
                if (C - B) < (C - D) and (C - B) < (E - D) and (E - F) < (E - D) and (E - F) < (C - D) and B > D and F > D and B < C and F < E and A >= mirande2['c'].iloc[0] and verif == 0 and ordre == True and mini_pourcent == True:
                # ----- condition pour garantir la forme de l'iete  -----#

                    # ----- essaye de determiner les point d'intersection de la LDC -----#
                    try:
                        J = line_intersection((AJ, BJ), (CJ, DJ))
                        I = line_intersection((AI, BI), (CI, DI))
                        moyenne_tete = ((C - D) + (E - D)) / 2
                        moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                        moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
                        moyenne_des_epaule = ((E - F) + (J[1] - F)) + ((E - F) + (J[1] - F)) / 4
                        accept = True
                    except:
                        accept = False
                        # ----- essaye de determiner les point d'intersection de la LDC -----#
                    trouver = False
                    if accept == True:
                        if I[1] > B and J[1] > F and moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule2 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and moyenne_epaule2 >= moyenne_tete / 4 and G >= 1 and accept == True:
                            for i in range(local_min[ff] + 1, local_max[fg]):
                                if df['c'].iloc[i] >= J[1] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                    # if df['c'].iloc[i] > df['c'].iloc[local_min[ff]] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                    placejaune = i
                                    trouver = True
                            if trouver == True:
                                local_max89 = argrelextrema(mirande3['c'].values, np.greater, order=1, mode='clip')[0]
                                local_min89 = argrelextrema(mirande3['c'].values, np.less, order=1, mode='clip')[0]

                                highs89 = mirande3.iloc[local_max89, :]
                                lows89 = mirande3.iloc[local_min89, :]


                                compteur2 = compteur2 +1
                                fig1 = plt.figure(figsize=(10, 7))
                                plt.plot([], [], " ")
                                fig1.patch.set_facecolor('#17DE17')
                                fig1.patch.set_alpha(0.3)
                                plt.title(f'IETE : {ticker}', fontweight="bold", color='black')
                                mirande3['c'].plot(color=['blue'], label='Clotures')
                                mirande['c'].plot(color=['red'], label='Clotures', alpha=0.3)
                                plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                                plt.scatter(local_max[fa], A, color='blue')
                                plt.scatter(local_min[fb], B, color='blue')
                                plt.scatter(local_max[fc], C, color='blue')
                                plt.scatter(local_min[fd], D, color='blue')
                                plt.scatter(local_max[fe], E, color='blue')
                                plt.scatter(local_min[ff], F, color='blue')
                                plt.scatter(local_max[fg], G, color='blue')
                                plt.scatter(I[0], I[1], color='green')
                                plt.scatter(J[0], J[1], color='green')
                                plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red',
                                            label='100% objectif')
                                plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black',
                                            label='25% objectif')
                                plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                #plt.scatter(x=highs89.index, y=highs89['c'], alpha=0.5)
                                #plt.scatter(x=lows89.index, y=lows89['c'], alpha=0.5)
                                button_width = 0.2
                                button_height = 0.075
                                button_space = 0.05
                                # Création du bouton pour acheter
                                button_ax = plt.axes([0.9 - button_width, 0.001, button_width, button_height], facecolor='none')
                                button = plt.Button(button_ax, 'Confirmer', color='white', hovercolor='lightgray')
                                button.on_clicked(lambda event: confirmer(event,df,local_max[fa],data,api_url_OHLC))

                                button_ax2 = plt.axes([0.125, 0.001, button_width, button_height],facecolor='none')
                                button2 = plt.Button(button_ax2, 'Indicateurs', color='white', hovercolor='lightgray')
                                button2.on_clicked(Indicateurs)


                                # plt.scatter(x=low.index, y=low["c"])
                                if activactiv == True:
                                    plt.show()
                                if activactiv == False:
                                    compteurjson = compteurjson + 1
                                    arg1 = df.drop(range(0, local_max[fa] - 1))
                                    arg1 = arg1.reset_index(drop=True)
                                    arg1.to_json(f'json_recent/{lettre}{random.randint(10**11, (10**12)-1)}.json')

                                # ----- creation variable des moyennes de la tete et epaules  pour les prochaines conditions-----#
                                if accept == True:
                                    moyenne_epaule1 = ((I[1] - B) + (C - B)) / 2
                                    moyenne_epaule2 = ((E - F) + (J[1] - F)) / 2
                                    moyenne_des_epaule = ((E - F) + (J[1] - F)) + ((E - F) + (J[1] - F)) / 4
                                    moyenne_tete = ((C - D) + (E - D)) / 2
                                # ----- creation variable des moyennes de la tete et epaules  pour les prochaines conditions-----#

                                    tuche = 0
                                    noo = 0
                                    place_pc = 0
                                    point_max = J[0] + ((J[0] - I[0]))
                                    point_max = int(round(point_max, 0))

                                    # ----- creation de la fonction Moyenne mobile  -----#
                                    def sma(data, window):
                                        sma = data.rolling(window=window).mean()
                                        return sma

                                    df['sma_20'] = sma(df['c'], 20)
                                    df['sma_50'] = sma(df['c'], 50)
                                    df['sma_100'] = sma(df['c'], 100)
                                    df.tail()
                                    # ----- creation de la fonction Moyenne mobile  -----#
                                    # ----- creation de la fonction RSI  -----#

                                    def rsi(df, periods=14, ema=True):

                                        close_delta = df['c'].diff()

                                        # Make two series: one for lower closes and one for higher closes
                                        up = close_delta.clip(lower=0)
                                        down = -1 * close_delta.clip(upper=0)

                                        if ema == True:
                                            # Use exponential moving average
                                            ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                                            ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
                                        else:
                                            # Use simple moving average
                                            ma_up = up.rolling(window=periods, adjust=False).mean()
                                            ma_down = down.rolling(window=periods, adjust=False).mean()

                                        rsi = ma_up / ma_down
                                        rsi = 100 - (100 / (1 + rsi))
                                        return rsi

                                    df2['rsi'] = rsi(df2)
                                    df['rsi'] = rsi(df)

                                    def bb(data, sma, window):
                                        std = data.rolling(window=window).std()
                                        upper_bb = sma + std * 2
                                        lower_bb = sma - std * 2
                                        return upper_bb, lower_bb

                                    df['upper_bb'], df['lower_bb'] = bb(df['c'], df['sma_20'], 20)
                                    df.tail()

                                    def createMACD(df):
                                        df['e26'] = pd.Series.ewm(df['c'], span=26).mean()
                                        df['e12'] = pd.Series.ewm(df['c'], span=12).mean()
                                        df['MACD'] = df['e12'] - df['e26']
                                        df['e9'] = pd.Series.ewm(df['MACD'], span=9).mean()
                                        df['HIST'] = df['MACD'] - df['e9']

                                    createMACD(df)

                                    # ----- creation de la fonction RSI  -----#
                                    trouver = False
                                    for i in range(local_min[ff]+1,local_max[fg]+5):
                                        if df['c'].iloc[i] >= J[1] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                        #if df['c'].iloc[i] > df['c'].iloc[local_min[ff]] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                                            placejaune = i
                                            trouver = True
                                # ----- condition pour filtrer iete  -----#
                                if I[1] > B :#and J[1] > F and moyenne_epaule1 <= moyenne_tete / 2 and moyenne_epaule2 <= moyenne_tete / 2 and moyenne_epaule1 >= moyenne_tete / 4 and moyenne_epaule2 >= moyenne_tete / 4 and accept == True and G >= J[1] and trouver == True:# and df['c'].values[-2] <= J[1] + (moyenne_tete) / 4 and df['c'].values[-2] >= J[1] and df['c'].values[-1] <= J[1] + (moyenne_tete) / 4 and df['c'].values[-1] >= J[1]:
                                # ----- condition pour filtrer iete  -----#
                                    if antholemuscler == True:
                                        compteur3 = compteur3 +1
                                        # ----- systeme de notation des iete en fonction de la beaute et de la perfection de realisation  -----#
                                        note = 0
                                        pourcentage_10_tete = (10 * (local_max[fe] - local_max[fc]))/100
                                        pourcentage_10_ep1 = (20 * (local_max[fc] - I[0])) / 100
                                        pourcentage_10_ep2 = (20 * (J[0] - local_max[fe])) / 100
                                        pourcentage_20_moy_epaule = (30 * moyenne_des_epaule) / 100

                                        debugage = []
                                        if local_min[fd] < (local_max[fc] + local_max[fe])/2 + pourcentage_10_tete and local_min[fd] > (local_max[fc] + local_max[fe])/2 - pourcentage_10_tete : # D doit etre au millieu (10% de marge)
                                            note = note + 3
                                            debugage.append(1)

                                        if local_min[fb] < (I[0] + local_max[fc])/2 + pourcentage_10_ep1 and local_min[fb] > (I[0] + local_max[fc])/2 - pourcentage_10_ep1: # B doit etre au millieu (10% de marge)
                                            note = note + 1
                                            debugage.append(2)

                                        if local_min[ff] < (J[0] + local_max[fe])/2 + pourcentage_10_ep2 and local_min[ff] > (J[0] + local_max[fe])/2 - pourcentage_10_ep2: # F doit etre au millieu (10% de marge)
                                            note = note + 1
                                            debugage.append(3)

                                        if moyenne_epaule1 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule1 > moyenne_des_epaule - pourcentage_20_moy_epaule and moyenne_epaule2 < moyenne_des_epaule + pourcentage_20_moy_epaule and moyenne_epaule2 > moyenne_des_epaule - pourcentage_20_moy_epaule : # les epaules doivent etre de presque meme hauteur
                                            note = note + 1
                                            debugage.append(4)

                                        if B < F :
                                            if (((F - B) *100) / moyenne_tete) <= 30:
                                                note = note + 2
                                                debugage.append(5)


                                        if B > F:
                                            if (((B - F) *100) / moyenne_tete) <= 30:
                                                note = note + 2
                                                debugage.append(5)

                                        if B == F:
                                            note = note + 2
                                            debugage.append(5)

                                        if (local_max[fe] - local_max[fc]) > local_max[fc] - I[0] and (local_max[fe] - local_max[fc]) > J[0] - local_max[fe]: # tete plus large que les 2 epaules
                                            note = note + 0.5
                                            debugage.append(6)

                                        debugage1 = 'NULL'
                                        if debugage == True:
                                            debugage1 = 'Atteint en Volatilitée'
                                        if debugage == False:
                                            debugage1 = 'Pas atteint en Volatilitée'

                                        #if il y a pas de bruit:
                                            #note = note + 1.5
                                # --    --- systeme de notation des iete en fonction de la beaute et de la perfection de realisation  -----#

                                        # ----- initialisation des données d'aide -----#
                                        #playsound('note.wav')
                                        moins50p = J[1] - ((moyenne_tete) / 2)
                                        plus_grand = round((J[1] + (moyenne_tete) / 2), 5)
                                        plus_petit = round(df['c'].iloc[placejaune], 5)
                                        pourcent_chercher = ((plus_grand - plus_petit) / plus_petit)*100
                                        pourcent_chercher = round(pourcent_chercher, 2)
                                        pourcent_perdu = ((round(G, 5)-round(F, 5))*100)/round(G, 5)
                                        pourcent_perdu = round(pourcent_perdu, 2)
                                        pertenet = 0.005 * G
                                        if pertenet < 1:
                                            pertenet = 1
                                        pertenet = pertenet * 2  # 2 fois puisque maker et taker
                                        pertenet_pourcent = (pertenet * 100) / 500
                                        pourcent_chercher2 = pourcent_chercher - pertenet_pourcent
                                        pourcent_chercher2 = round(pourcent_chercher2, 2)

                                        pourcent_perdu = pourcent_perdu - pertenet_pourcent
                                        pourcent_perdu = round(pourcent_perdu, 2)
                                        # ----- initialisation des données d'aide -----#



                                        # ----- creer la figure et l'affichage MATPLOTLIB -----#
                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        time_name2 = time_name1
                                        duree_figure = (placejaune - local_max[fa])*time1
                                        if duree_figure >= 75 and time_name1 == 'minute':
                                            duree_figure = duree_figure /60
                                            time_name2 = 'heure'


                                        if duree_figure >= 1440 and time_name1 == 'hour':
                                            duree_figure = duree_figure /24
                                            time_name2 = 'jour'

                                        trouver2 = False
                                        trouver3 = False
                                        duree_achat = 0
                                        for i in range(placejaune, mirande3.index[-1]):
                                            if df['c'].iloc[i] < F and trouver3 == False and trouver2 == False:
                                                placerouge = i
                                                trouver3 = True
                                                duree_achat = (placerouge - placejaune) * time1

                                            if df['h'].iloc[i] >= J[1] + (((moyenne_tete) / 2)) and trouver2 == False and trouver3 == False:
                                                placevert = i
                                                trouver2 = True
                                                duree_achat = (placevert - placejaune) * time1




                                        time_name3 = time_name1
                                        if duree_achat >= 75 and time_name1 == 'minute':
                                            duree_achat = duree_achat / 60
                                            time_name3 = 'heure'


                                        if duree_achat >= 1440 and time_name1 == 'hour':
                                            duree_achat = duree_achat / 24
                                            time_name3 = 'jour'

                                        noir = []
                                        for i in range(placejaune - 1, mirande3.index[-1]):
                                            noir.append(i)
                                        mirande4 = df.iloc[noir, :]
                                        noir1 = {'c': noir}
                                        noir2 = pd.DataFrame(data=noir1)

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1}  | +{pourcent_chercher}% BRUT | +{pourcent_chercher2}% NET | -{pourcent_perdu}% NET | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], label='Clotures')
                                        mirande4['h'].plot(color=['green'], alpha=0.3, label='Highs')
                                        mirande4['l'].plot(color=['red'], alpha=0.3, label='Lows')
                                        #df['sma_20'].plot(label='Ema 20', linestyle='-', linewidth=1.2, color='green')
                                        #df['sma_50'].plot(label='Ema 50', linestyle='-', linewidth=1.2, color='red')
                                        #df['sma_100'].plot(label='Ema 100', linestyle='-', linewidth=1.2, color='blue')
                                        # mirande['c'].plot(color=['#FF0000'])
                                        mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3, color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange', label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        taille_diviser = (local_max[fe] - local_max[fc]) / (local_min[fd] - local_max[fc])
                                        # point_max = J[0]+((J[0] - I[0])/taille_diviser)
                                        point_max = J[0] + ((J[0] - I[0]))
                                        point_max = int(round(point_max, 0))
                                        # plt.scatter(point_max, df['c'].values[int(round(point_max, 0))], color='red',label='Max temps realisation')
                                        plt.legend()
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(J[0], J[1] + (moyenne_tete) / 2, f"{round((J[1] + (moyenne_tete) / 2), 5)}", ha='left', style='normal', size=10.5, color='orange', wrap=True)
                                        plt.text(J[0], moins50p, f"{round(moins50p, 5)}", ha='left',style='normal', size=10.5, color='purple', wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fd], D, f"D {round(D, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[ff], F, f"F  {round(F, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        #plt.text(local_max[fg], G, f"G", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(placejaune, df['c'].iloc[placejaune], f"  BUY  {round(df['c'].iloc[placejaune], 5)}", ha='left', style='normal', size=10.5, color='red',
                                         wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        # test_valeur = df['c'].iloc[round(J[0]) + 1]
                                        # plt.text(round(J[0]), df['c'].iloc[round(J[0])], f"J+1 {test_valeur}", ha='left',style='normal', size=10.5, color='#00FF36', wrap=True)
                                        #plt.scatter(len(df['c']) - 1, df['c'].values[-1], color='blue', label='liveprice')
                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['h'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')
                                        plt.scatter(local_max[fa], A, color='blue')
                                        plt.scatter(local_min[fb], B, color='blue')
                                        plt.scatter(local_max[fc], C, color='blue')
                                        plt.scatter(local_min[fd], D, color='blue')
                                        plt.scatter(local_max[fe], E, color='blue')
                                        plt.scatter(local_min[ff], F, color='blue')
                                        plt.savefig(f'/home/mat/Bureau/musculage/0.png')
                                        plt.show()
                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        plt.bar(df['v'][(mirande3.index[0]):(mirande3.index[-1]) + 1].index, df['v'].values[(mirande3.index[0]):(mirande3.index[-1]) + 1])
                                        plt.scatter(placejaune, df['v'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['v'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['v'].values[placerouge], color='red', label='SELL')

                                        plt.text(local_max[fa], df['v'].values[local_max[fa]], "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fb], df['v'].values[local_min[fb]], "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fc], df['v'].values[local_max[fc]], "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[fd], df['v'].values[local_min[fd]], "D", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_max[fe], df['v'].values[local_max[fe]], "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
                                        plt.text(local_min[ff], df['v'].values[local_min[ff]], "F", ha='left', style='normal', size=10.5, color='red',
                                         wrap=True)
                                        plt.savefig(f'/home/mat/Bureau/musculage/1.png')
                                        plt.show()
                                        #----- creer la figure et l'affichage MATPLOTLIB -----#


                                        # -----------------------lire et connaitre nom de image et enregistrer image (pour remplacer le plt.show)--------------------------#
                                        # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'r')
                                        # compteur_nombre_image = int(file.read())
                                        # file.close()
                                        # file = open('/home/mat/Bureau/logi3_direct/compteur_images.txt', 'w')
                                        # compteur_nombre_image = compteur_nombre_image + 1
                                        # file.write(f'{compteur_nombre_image}')
                                        # file.close()
                                        # plt.savefig(f'images/figure_{compteur_nombre_image}.png'
                                        # -----------------------lire et connaitre nom de image et enregistrer image (pour remplacer le plt.show)--------------------------#

                                        fig = plt.figure(figsize=(10, 7))
                                        # fig.patch.set_facecolor('#17abde'
                                        plt.plot([], [], ' ')
                                        plt.subplot(2, 1, 1)
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        df['rsi'].iloc[(local_min[fa] - 1):(local_max[ff] + 5)].plot(color=['purple'], alpha=0.6)
                                        plt.axhline(y=30, alpha=0.3, color='black')
                                        plt.axhline(y=70, alpha=0.3, color='black')
                                        plt.axhline(y=50, linestyle='--', alpha=0.3, color='grey')
                                        plt.legend(['Rsi'])

                                        plt.text(local_max[fa], df['rsi'].iloc[local_max[fa]], "A", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fb], df['rsi'].iloc[local_min[fb]], "B", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fc], df['rsi'].iloc[local_max[fc]], "C", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fd], df['rsi'].iloc[local_min[fd]], "D", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fe], df['rsi'].iloc[local_max[fe]], "E", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[ff], df['rsi'].iloc[local_min[ff]], "F", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fg], df['rsi'].iloc[local_max[fg]], "G", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.scatter(placejaune, df['rsi'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['rsi'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['rsi'].values[placerouge], color='red', label='SELL')
                                        a2 = plt.subplot(2, 1, 2)

                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                                    color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                                    label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/2.png')
                                        plt.show()


                                        fig = plt.figure(figsize=(10, 7))

                                        #fig.patch.set_facecolor('#17abde')


                                        plt.plot([], [], ' ')

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label ='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label ='Ligne de coup')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)



                                        width = .4
                                        width2 = .05

                                        #define up and down prices
                                        up = mirande3[mirande3.c >= mirande3.o]
                                        down = mirande3[mirande3.c < mirande3.o]

                                        #define colors to use
                                        col1 = 'green'
                                        col2 = 'red'

                                        #plot up prices9
                                        plt.bar(up.index, up.c - up.o, width, bottom=up.o, color=col1, label ='Bougies Japonnaises')
                                        plt.bar(up.index, up.h - up.c, width2, bottom=up.c, color=col1)
                                        plt.bar(up.index, up.l - up.o, width2, bottom=up.o, color=col1)

                                        #plot down prices
                                        plt.bar(down.index, down.c - down.o, width, bottom=down.o, color=col2)
                                        plt.bar(down.index, down.h - down.o, width2, bottom=down.o, color=col2)
                                        plt.bar(down.index, down.l - down.c, width2, bottom=down.c, color=col2)
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY', s=100)
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL', s=100)

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL', s=100)


                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/3.png')
                                        plt.show()
#-------------------            ----    --------------------------------------------------- boolinger--------------------------------------------------------#
                                        fig = plt.figure(figsize=(10, 7))

                                        # fig.patch.set_facecolor('#17abde')

                                        plt.plot([], [], ' ')

                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | {start} | {end} | {start2} |', fontweight="bold", color='black')
                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)

                                        df['upper_bb'].iloc[(local_max[fa] - 1):(local_max[fg]) + 5].plot(label='Haut Band', linestyle='--', linewidth=1, color='red')
                                        df['sma_20'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Ema 20', linestyle='-', linewidth=1.2, color='grey')
                                        df['lower_bb'].iloc[(local_max[fa]-1):(local_max[fg]) + 5].plot(label='Bas Band', linestyle='--', linewidth=1, color='green')
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/4.png')
                                        plt.show()
# ------------------            ----    ---------------------------------------------------- boolinger--------------------------------------------------------#

                                        fig = plt.figure(figsize=(10, 7))

                                        # fig.patch.set_facecolor('#17abde')

                                        plt.plot([], [], ' ')
                                        plt.subplot(2, 1, 1)
                                        plt.title(f'IETE : {ticker} | {time1} {time_name1} | +{pourcent_chercher}% | {duree_figure} {time_name2} | {duree_achat} {time_name3} |', fontweight="bold", color='black')
                                        plt.bar(df['HIST'][(local_max[fa]-2):(local_max[fg]) + 7].index,df['HIST'].values[(local_max[fa]-2):(local_max[fg]) + 7], color='purple', alpha=0.6)
                                        df['MACD'].iloc[(local_max[fa] - 2):(local_max[fg] + 7)].plot(color=['blue'], alpha=0.6)
                                        df['e9'].iloc[(local_max[fa] - 2):(local_max[fg] + 7)].plot(color=['red'], alpha=0.6)
                                        plt.text(local_max[fa], df['HIST'].iloc[(local_max[fa])], "A", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fb], df['HIST'].iloc[(local_min[fb])], "B", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fc], df['HIST'].iloc[(local_max[fc])], "C", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[fd], df['HIST'].iloc[(local_min[fd])], "D", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fe], df['HIST'].iloc[(local_max[fe])], "E", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_min[ff], df['HIST'].iloc[(local_min[ff])], "F", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        plt.text(local_max[fg], df['HIST'].iloc[(local_max[fg])], "G", ha='left', style='normal', size=10.5, color='blue', wrap=True)
                                        #plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        #plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
                                        plt.scatter(placejaune, df['HIST'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['HIST'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['HIST'].values[placerouge], color='red', label='SELL')




                                        plt.legend(['Macd','Signal','histogramme'])
                                        a2 = plt.subplot(2, 1, 2)

                                        mirande3['c'].plot(color=['blue'], alpha=0.3, label='Clotures')
                                        mirande2['c'].plot(color=['green'], alpha=0.3, linestyle='--', label='Ligne de coup')
                                        plt.text(local_max[fa], A, "A", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fb], B, "B", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fc], C, "C", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[fd], D, "D", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fe], E, "E", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_min[ff], F, "F", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(local_max[fg], G, "G", ha='left', style='normal', size=10.5, color='black',
                                                 wrap=True)
                                        plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='black', wrap=True)
                                        plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
                                        plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3,
                                            color='black', label='75% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 2, linestyle='--', alpha=0.3, color='orange',
                                            label='50% objectif')
                                        plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
                                        plt.axhline(y=moins50p, linestyle='--', alpha=0.3, color='purple', label='-50% objectif')
                                        plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)

                                        plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
                                        if trouver2 == True:
                                            plt.scatter(placevert, df['c'].values[placevert], color='green', label='SELL')

                                        if trouver3 == True:
                                            plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')

                                        plt.legend()
                                        plt.savefig(f'/home/mat/Bureau/musculage/5.png')
                                        plt.show()

                # --            ---     enregister des données inutiles -----#
                                        data_A.append(A)
                                        data_B.append(B)
                                        data_C.append(C)
                                        data_D.append(D)
                                        data_E.append(E)
                                        data_F.append(F)
                                        data_F.append(G)
                                        data_A_ = pd.DataFrame(data_A, columns=['A'])
                                        data_B_ = pd.DataFrame(data_B, columns=['B'])
                                        data_C_ = pd.DataFrame(data_C, columns=['C'])
                                        data_D_ = pd.DataFrame(data_D, columns=['D'])
                                        data_E_ = pd.DataFrame(data_E, columns=['E'])
                                        data_F_ = pd.DataFrame(data_E, columns=['F'])
                                        data_G_ = pd.DataFrame(data_E, columns=['G'])
                                        df_IETE = pd.concat([data_A_, data_B_, data_C_, data_D_, data_E_, data_F_, data_G_], axis=1)
                                        # ----- enregister des données inutiles -----#
                                        antholemuscler = False

                fa = fa + 1
                fb = fb + 1
                fc = fc + 1
                fd = fd + 1
                fe = fe + 1
                ff = ff + 1
                fg = fg + 1
                print(f'{compteur} iete on etaient trouvés')
                print(f'{compteur2} reussite')
                print(f'{compteur3} big reussite')
                print('----------------------------------------------------------------------', flush=True)
            else:
                print('pas assez de place pour continuer')
                i = 1
# ----- fonction Principale -----#

# ----- traduction francais anglais pour appel polygon -----#
minute = "minute"
heure = "hour"
jour = "day"
# ----- traduction francais anglais pour appel polygon -----#
TETE = 2.909
databax = ['A', 'AA', 'AAA', 'AAAU', 'AAC', 'AACG', 'AACI', 'AACIU', 'AADI', 'AADR', 'AAIC', 'AAIC', 'AAIC', 'AAIN', 'AAL', 'AAMC', 'AAME', 'AAN', 'AAOI', 'AAON', 'AAP', 'AAPL', 'AAT', 'AAU', 'AAWW', 'AAXJ', 'AB', 'ABB', 'ABBV', 'ABC', 'ABCB', 'ABCL', 'ABCM', 'ABEO', 'ABEQ', 'ABEV', 'ABG', 'ABIO', 'ABM', 'ABNB', 'ABOS', 'ABR', 'ABSI', 'ABST', 'ABT', 'ABUS', 'ABVC', 'AC', 'ACA', 'ACAB', 'ACACU', 'ACAD', 'ACAH', 'ACAHU', 'ACAQ', 'ACAX', 'ACAXR', 'ACAXU', 'ACB', 'ACBA', 'ACBAU', 'ACCD', 'ACCO', 'ACEL', 'ACER', 'ACES', 'ACET', 'ACGL', 'ACGLN', 'ACGLO', 'ACHC', 'ACHL', 'ACHR', 'ACHV', 'ACI', 'ACIO', 'ACIU', 'ACIW', 'ACLS', 'ACLX', 'ACM', 'ACMR', 'ACN', 'ACNB', 'ACON', 'ACOR', 'ACP', 'ACQR', 'ACQRU', 'ACR', 'ACRE', 'ACRO', 'ACRS', 'ACRX', 'ACSI', 'ACST', 'ACT', 'ACTG', 'ACTV','ACU', 'ACV', 'ACVA', 'ACVF', 'ACWI', 'ACWV', 'ACWX', 'ACXP', 'ADAG', 'ADAL', 'ADALU', 'ADAP', 'ADBE', 'ADC', 'ADCT', 'ADER', 'ADERU', 'ADES', 'ADEX', 'ADFI', 'ADI', 'ADIL', 'ADIV', 'ADM', 'ADMA', 'ADME', 'ADMP', 'ADN', 'ADNT', 'ADOC', 'ADOCR', 'ADP', 'ADPT', 'ADRE', 'ADRT', 'ADSE', 'ADSK', 'ADT', 'ADTH', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVM', 'ADX', 'ADXN', 'AE', 'AEAE', 'AEAEU', 'AEE', 'AEF', 'AEFC', 'AEG', 'AEHL', 'AEHR', 'AEI', 'AEIS', 'AEL', 'AEM', 'AEMB', 'AEMD', 'AENZ', 'AEO', 'AEP', 'AEPPZ', 'AER', 'AES', 'AESC', 'AESR', 'AEVA', 'AEY', 'AEYE', 'AEZS', 'AFAR', 'AFARU', 'AFB', 'AFBI', 'AFCG', 'AFG', 'AFGB', 'AFGC', 'AFGD', 'AFGE', 'AFIB', 'AFIF', 'AFK', 'AFL', 'AFLG', 'AFMC', 'AFMD', 'AFRI', 'AFRM', 'AFSM', 'AFT', 'AFTR', 'AFTR', 'AFTY', 'AFYA', 'AG', 'AGAC', 'AGAC', 'AGBA', 'AGCO', 'AGD', 'AGE', 'AGEN', 'AGFS', 'AGFY', 'AGG', 'AGGH', 'AGGR', 'AGGRU', 'AGGY', 'AGI', 'AGIH', 'AGIL', 'AGIO', 'AGL', 'AGLE', 'AGM', 'AGMH', 'AGNC', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGNG', 'AGO', 'AGOV', 'AGOX', 'AGQ', 'AGR', 'AGRH', 'AGRI', 'AGRO', 'AGRX', 'AGS', 'AGTI', 'AGX', 'AGYS', 'AGZ', 'AGZD', 'AHCO', 'AHG', 'AHH', 'AHHX', 'AHI', 'AHOY', 'AHRN', 'AHRNU', 'AHT','AHYB', 'AI', 'AIA', 'AIB', 'AIBBR', 'AIBBU', 'AIC', 'AIEQ', 'AIF', 'AIG', 'AIH', 'AIHS', 'AILG', 'AILV', 'AIM', 'AIMBU', 'AIMC', 'AIMD', 'AIN', 'AINC', 'AIO', 'AIP', 'AIQ', 'AIR', 'AIRC', 'AIRG', 'AIRI', 'AIRR', 'AIRS', 'AIRT', 'AIRTP', 'AIT', 'AIU', 'AIV', 'AIVI', 'AIVL', 'AIZ', 'AIZN', 'AJG', 'AJRD', 'AJX', 'AJXA', 'AKA', 'AKAM', 'AKAN', 'AKBA', 'AKR', 'AKRO', 'AKTS', 'AKTX', 'AKU', 'AKYA', 'AL', 'ALB', 'ALC', 'ALCC', 'ALCO', 'ALDX', 'ALE', 'ALEC', 'ALEX', 'ALG', 'ALGM', 'ALGN', 'ALGS', 'ALGT', 'ALHC', 'ALIM', 'ALIT', 'ALK', 'ALKS', 'ALKT', 'ALL', 'ALLE', 'ALLG', 'ALLK', 'ALLO', 'ALLR', 'ALLT', 'ALLY', 'ALNY', 'ALOR', 'ALORU', 'ALOT', 'ALPA', 'ALPAU', 'ALPN', 'ALPP', 'ALR', 'ALRM', 'ALRN', 'ALRS', 'ALSA', 'ALSAR', 'ALSAU', 'ALSN', 'ALT', 'ALTG', 'ALTL', 'ALTO', 'ALTR', 'ALTU', 'ALTUU', 'ALTY', 'ALV', 'ALVO', 'ALVR', 'ALX', 'ALXO', 'ALYA', 'ALZN', 'AM', 'AMAL', 'AMAM', 'AMAO', 'AMAT', 'AMAX', 'AMBA', 'AMBC', 'AMBO', 'AMBP', 'AMC', 'AMCR', 'AMCX', 'AMD', 'AME', 'AMED', 'AMEH', 'AMG', 'AMGN', 'AMH', 'AMJ', 'AMK', 'AMKR', 'AMLP', 'AMLX', 'AMN', 'AMNB', 'AMND', 'AMOM', 'AMOT', 'AMOV', 'AMP', 'AMPE', 'AMPG', 'AMPH', 'AMPL', 'AMPS', 'AMPY', 'AMR', 'AMRC', 'AMRK', 'AMRN', 'AMRS', 'AMRX', 'AMS', 'AMSC', 'AMSF', 'AMST', 'AMSWA', 'AMT', 'AMTB', 'AMTD', 'AMTI', 'AMTX', 'AMUB', 'AMWD', 'AMWL', 'AMX', 'AMYT', 'AMZA', 'AMZN', 'AN', 'ANAB', 'ANDE', 'ANEB', 'ANET', 'ANEW', 'ANF', 'ANGH', 'ANGI', 'ANGL', 'ANGN', 'ANGO', 'ANIK', 'ANIP', 'ANIX', 'ANNX', 'ANPC', 'ANSS', 'ANTE', 'ANTX', 'ANVS', 'ANY', 'ANZU', 'ANZUU', 'AOA', 'AOD', 'AOGO', 'AOK', 'AOM', 'AOMR', 'AON', 'AOR', 'AORT', 'AOS', 'AOSL', 'AOTG', 'AOUT', 'AP', 'APA', 'APAC', 'APACU', 'APAM', 'APCA', 'APCX', 'APD', 'APDN', 'APEI', 'APEN', 'APG', 'APGB', 'APH', 'API', 'APLD', 'APLE', 'APLS', 'APLT', 'APM', 'APMI', 'APMIU', 'APO', 'APOG', 'APP', 'APPF', 'APPH', 'APPN', 'APPS', 'APRE', 'APRN', 'APRZ', 'APT', 'APTM', 'APTMU', 'APTO', 'APTV', 'APTX', 'APVO', 'APWC', 'APXI','APXIU', 'APYX', 'AQB', 'AQGX', 'AQMS', 'AQN', 'AQNA', 'AQNB', 'AQNU', 'AQST', 'AQUA', 'AQWA', 'AR', 'ARAV', 'ARAY', 'ARB', 'ARBE', 'ARBG', 'ARBK', 'ARBKL', 'ARC', 'ARCB', 'ARCC', 'ARCE', 'ARCH', 'ARCM', 'ARCO', 'ARCT', 'ARDC', 'ARDS', 'ARDX', 'ARE', 'AREB', 'AREC', 'AREN', 'ARES', 'ARGD', 'ARGO', 'ARGT', 'ARGX', 'ARHS', 'ARI', 'ARIS', 'ARIZ', 'ARIZR', 'ARKF', 'ARKG', 'ARKK', 'ARKO', 'ARKQ', 'ARKR', 'ARKW', 'ARKX', 'ARL', 'ARLO', 'ARLP', 'ARMK', 'ARMP', 'ARMR', 'ARNC', 'AROC', 'AROW', 'ARQQ', 'ARQT', 'ARR', 'ARRW', 'ARRWU', 'ARRY', 'ARTE', 'ARTEU', 'ARTL', 'ARTNA', 'ARTW', 'ARVL', 'ARVN', 'ARW', 'ARWR', 'ARYD', 'ARYE', 'ASA', 'ASAI', 'ASAN', 'ASB', 'ASC', 'ASCA', 'ASCAR', 'ASCAU', 'ASCB', 'ASCBR', 'ASCBU', 'ASEA', 'ASET', 'ASG', 'ASGI', 'ASGN', 'ASH', 'ASHR', 'ASHS', 'ASHX', 'ASIX', 'ASLE', 'ASLN', 'ASM', 'ASMB', 'ASML', 'ASND', 'ASNS', 'ASO', 'ASPA', 'ASPN', 'ASPS', 'ASPU', 'ASPY', 'ASR', 'ASRT', 'ASRV', 'ASTC', 'ASTE', 'ASTI', 'ASTL', 'ASTR', 'ASTS', 'ASUR', 'ASX', 'ASXC', 'ASYS', 'ATAI', 'ATAK', 'ATAKR', 'ATAKU', 'ATAQ', 'ATCO', 'ATCOL', 'ATCX', 'ATEC', 'ATEK', 'ATEN', 'ATER', 'ATEX', 'ATFV', 'ATGE', 'ATHA', 'ATHE', 'ATHM', 'ATHX', 'ATI', 'ATIF', 'ATIP', 'ATKR', 'ATLC', 'ATLCL', 'ATLCP', 'ATLO', 'ATMP', 'ATNF', 'ATNI', 'ATNM', 'ATNX', 'ATO', 'ATOM', 'ATOS', 'ATR', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATSG', 'ATTO', 'ATUS', 'ATVI', 'ATXI', 'ATXS', 'ATY', 'AU', 'AUB', 'AUBN', 'AUD', 'AUDC', 'AUGX', 'AUGZ', 'AUID', 'AUMN', 'AUPH', 'AUR', 'AURA', 'AURC', 'AUSF', 'AUST', 'AUTL', 'AUUD', 'AUVI', 'AUVIP', 'AUY', 'AVA', 'AVAC', 'AVACU', 'AVAH', 'AVAL', 'AVAV', 'AVB', 'AVD', 'AVDE', 'AVDL', 'AVDV', 'AVDX', 'AVEM', 'AVES', 'AVGO', 'AVGR', 'AVHI', 'AVHIU', 'AVID', 'AVIG', 'AVIR', 'AVIV', 'AVK', 'AVLV', 'AVMU', 'AVNS', 'AVNT', 'AVNW', 'AVO', 'AVPT', 'AVRE', 'AVRO', 'AVSC', 'AVSD', 'AVSE', 'AVSF', 'AVSU', 'AVT', 'AVTE', 'AVTR', 'AVTX', 'AVUS', 'AVUV', 'AVXL', 'AVY', 'AWAY', 'AWF', 'AWH', 'AWI', 'AWK', 'AWP', 'AWR', 'AWRE', 'AWX', 'AWYX', 'AX', 'AXAC','AXDX', 'AXGN', 'AXL', 'AXLA', 'AXNX', 'AXON', 'AXP', 'AXR', 'AXS', 'AXSM', 'AXTA', 'AXTI', 'AY', 'AYI', 'AYRO', 'AYTU', 'AYX', 'AZ', 'AZEK', 'AZN', 'AZO', 'AZPN', 'AZRE', 'AZTA', 'AZUL', 'AZYO', 'AZZ', 'B', 'BA', 'BAB', 'BABA', 'BAC', 'BACA', 'BAD', 'BAFN', 'BAH', 'BAK', 'BAL', 'BALL', 'BALT', 'BALY', 'BAM', 'BANC', 'BAND', 'BANF', 'BANFP', 'BANR', 'BANX', 'BAOS', 'BAP', 'BAPR', 'BAR', 'BARK', 'BASE', 'BATL', 'BATRA', 'BATRK', 'BATT', 'BAUG', 'BAX', 'BB', 'BBAI', 'BBAR', 'BBAX', 'BBBY', 'BBC', 'BBCA', 'BBCP', 'BBD', 'BBDC', 'BBDO', 'BBEU', 'BBGI', 'BBH', 'BBIG', 'BBIN', 'BBIO', 'BBJP', 'BBLG', 'BBLN', 'BBMC', 'BBN', 'BBP', 'BBRE', 'BBSA', 'BBSC', 'BBSI', 'BBU', 'BBUC', 'BBUS', 'BBVA', 'BBW', 'BBWI', 'BBY', 'BC', 'BCAB', 'BCAN', 'BCAT', 'BCBP', 'BCC', 'BCD', 'BCDA', 'BCE', 'BCEL', 'BCH', 'BCI', 'BCIM', 'BCLI', 'BCM', 'BCML', 'BCO', 'BCOV', 'BCOW', 'BCPC', 'BCRX', 'BCS', 'BCSA', 'BCSAU', 'BCSF', 'BCTX', 'BCV', 'BCX', 'BCYC', 'BDC', 'BDCX', 'BDCZ', 'BDEC', 'BDJ', 'BDL', 'BDN', 'BDRY', 'BDSX', 'BDTX', 'BDX', 'BDXB', 'BE', 'BEAM', 'BEAT', 'BECN', 'BECO', 'BEDU', 'BEDZ', 'BEEM', 'BEKE', 'BELFA', 'BELFB', 'BEN', 'BEP', 'BEPC', 'BEPH', 'BEPI', 'BERY', 'BERZ', 'BEST', 'BETZ', 'BFAC', 'BFAM', 'BFC', 'BFEB', 'BFH', 'BFI', 'BFIN', 'BFIT', 'BFIX', 'BFK', 'BFLY', 'BFOR', 'BFRI', 'BFS', 'BFST', 'BFTR', 'BFZ', 'BG', 'BGB', 'BGCP', 'BGFV', 'BGH', 'BGI', 'BGLD', 'BGNE', 'BGR', 'BGRN', 'BGRY', 'BGS', 'BGSF', 'BGSX', 'BGT', 'BGX', 'BGXX', 'BGY', 'BH', 'BHAC', 'BHACU', 'BHAT', 'BHB', 'BHC', 'BHE', 'BHF', 'BHFAL', 'BHFAM', 'BHFAN', 'BHFAO', 'BHFAP', 'BHG', 'BHIL', 'BHK', 'BHLB', 'BHP', 'BHR', 'BHV', 'BHVN', 'BIB', 'BIBL', 'BICK', 'BIDS', 'BIDU', 'BIG', 'BIGC', 'BIGZ', 'BIIB', 'BIL', 'BILI', 'BILL', 'BILS', 'BIMI', 'BIO', 'BIOC', 'BIOL', 'BIOR', 'BIOS', 'BIOX', 'BIP', 'BIPC', 'BIPH', 'BIPI', 'BIRD', 'BIS', 'BIT', 'BITE', 'BITF', 'BITI', 'BITO', 'BITQ', 'BITS', 'BIV', 'BIVI', 'BIZD', 'BJ', 'BJAN', 'BJDX']

#databax2 = ['BJK' ,'BJRI', 'BJUL', 'BJUN', 'BK', 'BKAG', 'BKCC', 'BKCH', 'BKCI', 'BKD', 'BKE', 'BKEM', 'BKES', 'BKF', 'BKH', 'BKHY', 'BKI', 'BKIE', 'BKIS', 'BKKT', 'BKLC', 'BKLN', 'BKMC', 'BKN', 'BKNG', 'BKR', 'BKSB', 'BKSC', 'BKSE', 'BKSY', 'BKT', 'BKTI', 'BKU', 'BKUI', 'BKUS', 'BKYI', 'BL', 'BLBD', 'BLBX', 'BLCM', 'BLCN', 'BLCO', 'BLD', 'BLDE', 'BLDG', 'BLDP', 'BLDR', 'BLE', 'BLES', 'BLEU', 'BLEUR', 'BLEUU', 'BLFS', 'BLFY', 'BLHY', 'BLI', 'BLIN', 'BLK', 'BLKB', 'BLKC', 'BLMN', 'BLND', 'BLNG', 'BLNGU', 'BLNK', 'BLOK', 'BLPH', 'BLRX', 'BLTE', 'BLU', 'BLUA', 'BLUE', 'BLV', 'BLW', 'BLX', 'BLZE', 'BMA', 'BMAC', 'BMAQ', 'BMAQR', 'BMAQU', 'BMAR', 'BMAY', 'BMBL', 'BME', 'BMEA', 'BMED', 'BMEZ', 'BMI', 'BMO', 'BMRA', 'BMRC', 'BMRN', 'BMTX', 'BMY', 'BND', 'BNDC', 'BNDD', 'BNDW', 'BNDX', 'BNE', 'BNED', 'BNGE', 'BNGO', 'BNIX', 'BNIXR', 'BNKD', 'BNKU', 'BNL', 'BNNR', 'BNNRU', 'BNO', 'BNOV', 'BNOX', 'BNR', 'BNRG', 'BNS', 'BNSO', 'BNTC', 'BNTX', 'BNY', 'BOAC', 'BOAT', 'BOC', 'BOCN', 'BOCNU', 'BOCT', 'BODY', 'BOE', 'BOH', 'BOIL', 'BOKF', 'BOLT', 'BON', 'BOND', 'BOOM', 'BOOT', 'BORR', 'BOSC', 'BOSS', 'BOTJ', 'BOTZ', 'BOUT', 'BOWL', 'BOX', 'BOXD', 'BOXL', 'BP', 'BPAC', 'BPACU', 'BPMC', 'BPOP', 'BPOPM', 'BPRN', 'BPT', 'BPTH', 'BPTS', 'BPYPM', 'BPYPN', 'BPYPO', 'BPYPP', 'BQ', 'BR', 'BRAC', 'BRACR', 'BRACU', 'BRAG', 'BRBR', 'BRBS', 'BRC', 'BRCC', 'BRD', 'BRDG', 'BRDS', 'BREZ', 'BREZR', 'BRF', 'BRFH', 'BRFS', 'BRID', 'BRIV', 'BRIVU', 'BRKH', 'BRKHU', 'BRKL', 'BRKR', 'BRKY', 'BRLI', 'BRLT', 'BRMK', 'BRN', 'BRO', 'BROG', 'BROS', 'BRP', 'BRQS', 'BRSP', 'BRT', 'BRTX', 'BRW', 'BRX', 'BRY', 'BRZE', 'BRZU', 'BSAC', 'BSAQ', 'BSBK', 'BSBR', 'BSCE', 'BSCN', 'BSCO', 'BSCP', 'BSCQ', 'BSCR', 'BSCS', 'BSCT', 'BSCU', 'BSCV', 'BSDE', 'BSEA', 'BSEP', 'BSET', 'BSFC', 'BSGA', 'BSGAR', 'BSGAU', 'BSGM', 'BSIG', 'BSJN', 'BSJO', 'BSJP', 'BSJQ', 'BSJR', 'BSJS', 'BSJT', 'BSL', 'BSM', 'BSMN', 'BSMO', 'BSMP', 'BSMQ', 'BSMR', 'BSMS', 'BSMT', 'BSMU', 'BSMV', 'BSMX', 'BSQR', 'BSRR', 'BST','BSTP', 'BSTZ', 'BSV', 'BSVN', 'BSX', 'BSY', 'BTA', 'BTAI', 'BTAL', 'BTB', 'BTBD', 'BTBT', 'BTCM', 'BTCS', 'BTCY', 'BTEC', 'BTEK', 'BTF', 'BTG', 'BTHM', 'BTI', 'BTMD', 'BTO', 'BTOG', 'BTT', 'BTTR', 'BTTX', 'BTU', 'BTWN', 'BTWNU', 'BTZ', 'BUD', 'BUFB', 'BUFD', 'BUFF', 'BUFG', 'BUFQ', 'BUFR', 'BUFT', 'BUG', 'BUI', 'BUL', 'BULZ', 'BUR', 'BURL', 'BUSE', 'BUYZ', 'BUZZ', 'BV', 'BVH', 'BVN', 'BVS', 'BVXV', 'BW', 'BWA', 'BWAC', 'BWACU', 'BWAQR', 'BWAQU', 'BWAY', 'BWB', 'BWBBP', 'BWC', 'BWCAU', 'BWEN', 'BWFG', 'BWG', 'BWMN', 'BWMX', 'BWNB', 'BWSN', 'BWV', 'BWX', 'BWXT', 'BWZ', 'BX', 'BXC', 'BXMT', 'BXMX', 'BXP', 'BXRX', 'BXSL', 'BY', 'BYD', 'BYFC', 'BYLD', 'BYM', 'BYN', 'BYND', 'BYNO', 'BYNOU', 'BYRN', 'BYSI', 'BYTE', 'BYTS', 'BYTSU', 'BZ', 'BZFD', 'BZH', 'BZQ', 'BZUN', 'C', 'CAAP', 'CAAS', 'CABA', 'CABO', 'CAC', 'CACC', 'CACG', 'CACI', 'CADE', 'CADL', 'CAE', 'CAF', 'CAG', 'CAH', 'CAKE', 'CAL', 'CALB', 'CALF', 'CALM', 'CALT', 'CALX', 'CAMP', 'CAMT', 'CAN', 'CANE', 'CANF', 'CANG', 'CANO', 'CAPE', 'CAPL', 'CAPR', 'CAR', 'CARA', 'CARE', 'CARG', 'CARR', 'CARS', 'CARV', 'CARZ', 'CASA', 'CASH', 'CASI', 'CASS', 'CASY', 'CAT', 'CATC', 'CATH', 'CATO', 'CATY', 'CB', 'CBAN', 'CBAT', 'CBAY', 'CBD', 'CBFV', 'CBH', 'CBIO', 'CBL', 'CBLS', 'CBNK', 'CBOE', 'CBON', 'CBRE', 'CBRG', 'CBRGU', 'CBRL', 'CBSE', 'CBSH', 'CBT', 'CBU', 'CBZ', 'CC', 'CCAI', 'CCAIU', 'CCAP', 'CCB', 'CCBG', 'CCCC', 'CCCS', 'CCD', 'CCEL', 'CCEP', 'CCF', 'CCI', 'CCJ', 'CCK', 'CCL', 'CCLP', 'CCM', 'CCNE', 'CCNEP', 'CCO', 'CCOI', 'CCOR', 'CCRD', 'CCRN', 'CCRV', 'CCS', 'CCSI', 'CCTS', 'CCU', 'CCV', 'CCVI', 'CCZ', 'CD', 'CDAK', 'CDAQ', 'CDAQU', 'CDAY', 'CDC', 'CDE', 'CDL', 'CDLX', 'CDMO', 'CDNA', 'CDNS', 'CDRE', 'CDRO', 'CDTX', 'CDW', 'CDX', 'CDXC', 'CDXS', 'CDZI', 'CDZIP', 'CE', 'CEAD', 'CEE', 'CEF', 'CEFA', 'CEFD', 'CEFS', 'CEG', 'CEI', 'CEIX', 'CELC', 'CELH', 'CELU', 'CELZ', 'CEM', 'CEMB', 'CEMI', 'CEN', 'CENN', 'CENT', 'CENTA', 'CENX', 'CEPU','CEQP', 'CERE', 'CERS', 'CERT', 'CET', 'CETX', 'CETXP', 'CEV', 'CEVA', 'CEW', 'CF', 'CFA', 'CFB', 'CFBK', 'CFCV', 'CFFE', 'CFFI', 'CFFN', 'CFFS', 'CFG', 'CFIV', 'CFIVU', 'CFLT', 'CFMS', 'CFO', 'CFR', 'CFRX', 'CFSB', 'CG', 'CGA', 'CGABL', 'CGAU', 'CGBD', 'CGC', 'CGCP', 'CGDV', 'CGEM', 'CGEN', 'CGGO', 'CGGR', 'CGNT', 'CGNX', 'CGO', 'CGRN', 'CGTX', 'CGUS', 'CGW', 'CGXU', 'CHAA', 'CHAU', 'CHB', 'CHCI', 'CHCO', 'CHCT', 'CHD', 'CHDN', 'CHE', 'CHEA', 'CHEAU', 'CHEF', 'CHEK', 'CHGG', 'CHGX', 'CHH', 'CHI', 'CHIC', 'CHIE', 'CHIH', 'CHII', 'CHIK', 'CHIM', 'CHIQ', 'CHIR', 'CHIS', 'CHIU', 'CHIX', 'CHK', 'CHKP', 'CHMG', 'CHMI', 'CHN', 'CHNA', 'CHNR', 'CHPT', 'CHRA', 'CHRB', 'CHRD', 'CHRS', 'CHRW', 'CHS', 'CHSCL', 'CHSCM', 'CHSCN', 'CHSCO', 'CHSCP', 'CHT', 'CHTR', 'CHUY', 'CHW', 'CHWY', 'CHX', 'CHY', 'CI', 'CIA', 'CIB', 'CIBR', 'CID', 'CIDM', 'CIEN', 'CIF', 'CIFR', 'CIG', 'CIGI', 'CIH', 'CII', 'CIIG', 'CIIGU', 'CIK', 'CIL', 'CIM', 'CINF', 'CING', 'CINT', 'CIO', 'CION', 'CIR', 'CISO', 'CITE', 'CITEU', 'CIVB', 'CIVI', 'CIX', 'CIZ', 'CIZN', 'CJJD', 'CKPT', 'CKX', 'CL', 'CLAA', 'CLAR', 'CLAY', 'CLAYU', 'CLB', 'CLBK', 'CLBR', 'CLBT', 'CLDL', 'CLDT', 'CLDX', 'CLEU', 'CLF', 'CLFD', 'CLGN', 'CLH', 'CLIN', 'CLINR', 'CLINU', 'CLIR', 'CLIX', 'CLLS', 'CLM', 'CLMT', 'CLNE', 'CLNN', 'CLNR', 'CLOE', 'CLOER', 'CLOEU', 'CLOI', 'CLOU', 'CLOV', 'CLPR', 'CLPS', 'CLPT', 'CLRB', 'CLRC', 'CLRCR', 'CLRCU', 'CLRG', 'CLRO', 'CLS', 'CLSA', 'CLSC', 'CLSD', 'CLSE', 'CLSK', 'CLSM', 'CLST', 'CLTL', 'CLVR', 'CLVT', 'CLW', 'CLWT', 'CLX', 'CLXT', 'CM', 'CMA', 'CMAX', 'CMBM', 'CMBS', 'CMC', 'CMCA', 'CMCAU', 'CMCL', 'CMCM', 'CMCO', 'CMCSA', 'CMCT', 'CMDY', 'CME', 'CMF', 'CMG', 'CMI', 'CMLS', 'CMMB', 'CMP', 'CMPO', 'CMPR', 'CMPS', 'CMPX', 'CMRA', 'CMRE', 'CMRX', 'CMS', 'CMSA', 'CMSC', 'CMSD', 'CMT', 'CMTG', 'CMTL', 'CMU', 'CN', 'CNA', 'CNBS', 'CNC', 'CNCR', 'CNDA', 'CNDB', 'CNDT', 'CNET', 'CNEY', 'CNF', 'CNFR', 'CNFRL', 'CNGL', 'CNGLU', 'CNHI', 'CNI', 'CNK', 'CNM','CNMD', 'CNNE', 'CNO', 'CNOB', 'CNOBP', 'CNP', 'CNQ', 'CNRG', 'CNS', 'CNSL', 'CNSP', 'CNTA', 'CNTB', 'CNTG', 'CNTX', 'CNTY', 'CNX', 'CNXA', 'CNXC', 'CNXN', 'CNXT', 'CNYA', 'CO', 'COCO', 'COCP', 'CODA', 'CODI', 'CODX', 'COE', 'COEP', 'COF', 'COFS', 'COGT', 'COHN', 'COHU', 'COIN', 'COKE', 'COLB', 'COLD', 'COLL', 'COLM', 'COM', 'COMB', 'COMM', 'COMP', 'COMS', 'COMSP', 'COMT', 'CONN', 'CONX', 'CONXU', 'COO', 'COOK', 'COOL', 'COOLU', 'COOP', 'COP', 'COPX', 'CORN', 'CORP', 'CORR', 'CORS', 'CORT', 'COSM', 'COST', 'COTY', 'COUR', 'COW', 'COWZ', 'CP', 'CPA', 'CPAA', 'CPAAU', 'CPAC', 'CPB', 'CPE', 'CPER', 'CPF', 'CPG', 'CPHC', 'CPHI', 'CPI', 'CPII', 'CPIX', 'CPK', 'CPLP', 'CPNG', 'CPOP', 'CPRI', 'CPRT', 'CPRX', 'CPS', 'CPSH', 'CPSI', 'CPSS', 'CPT', 'CPTK', 'CPTN', 'CPUH', 'CPZ', 'CQP', 'CQQQ', 'CR', 'CRAI', 'CRAK', 'CRBN', 'CRBP', 'CRBU', 'CRC', 'CRCT', 'CRDF', 'CRDL', 'CRDO', 'CREC', 'CRECU', 'CREG', 'CRESY', 'CREX', 'CRF', 'CRGE', 'CRGY', 'CRH', 'CRI', 'CRIS', 'CRIT', 'CRK', 'CRKN', 'CRL', 'CRM', 'CRMD', 'CRMT', 'CRNC', 'CRNT', 'CRNX', 'CRON', 'CROX', 'CRPT', 'CRS', 'CRSP', 'CRSR', 'CRT', 'CRTO', 'CRUS', 'CRUZ', 'CRVL', 'CRVS', 'CRWD', 'CRWS', 'CRYP', 'CRZN', 'CRZNU', 'CS', 'CSA', 'CSAN', 'CSB', 'CSBR', 'CSCO', 'CSD', 'CSF', 'CSGP', 'CSGS', 'CSH', 'CSII', 'CSIQ', 'CSL', 'CSLM', 'CSLMR', 'CSM', 'CSML', 'CSPI', 'CSQ', 'CSR', 'CSSE', 'CSSEN', 'CSSEP', 'CSTA', 'CSTE', 'CSTL', 'CSTM', 'CSTR', 'CSV', 'CSWC', 'CSWI', 'CSX', 'CTA', 'CTAS', 'CTBB', 'CTBI', 'CTDD', 'CTEC', 'CTEX', 'CTG', 'CTGO', 'CTHR', 'CTIB', 'CTIC', 'CTKB', 'CTLP', 'CTLT', 'CTMX', 'CTO', 'CTOS', 'CTR', 'CTRA', 'CTRE', 'CTRM', 'CTRN', 'CTS', 'CTSH', 'CTSO', 'CTV', 'CTVA', 'CTXR', 'CUBA', 'CUBB', 'CUBE', 'CUBI', 'CUBS', 'CUE', 'CUEN', 'CUK', 'CULL', 'CULP', 'CURE', 'CURI', 'CURO', 'CURV', 'CUT', 'CUTR', 'CUZ', 'CVAC', 'CVAR', 'CVBF', 'CVCO', 'CVCY', 'CVE', 'CVEO', 'CVGI', 'CVGW', 'CVI', 'CVII', 'CVLG', 'CVLT', 'CVLY', 'CVM', 'CVNA', 'CVR', 'CVRX', 'CVS', 'CVT']

#minute = [15,20,25,30,35,40,45,50,55,75,90,105,135,150,165,195,210,225,255,270,285,315,330,345,375,390,405,435,450,465,495,510,525,555,570,585]
for data in databax:
    ticker = f'{data}'
    #liste_date=['05-20', '05-21', '05-22', '05-23', '05-24', '05-25', '05-26', '05-27', '05-28', '05-29', '05-30', '05-31', '06-01', '06-02', '06-03', '06-04', '06-05', '06-06', '06-07', '06-08', '06-09', '06-10', '06-11', '06-12', '06-13', '06-14', '06-15', '06-16', '06-17', '06-18', '06-19', '06-20', '06-21', '06-22', '06-23', '06-24', '06-25', '06-26', '06-27', '06-28', '06-29', '06-30', '07-01', '07-02', '07-03', '07-04', '07-05', '07-06', '07-07', '07-08', '07-09', '07-10', '07-11', '07-12', '07-13', '07-14', '07-15', '07-16', '07-17']
    liste_date = ['01-01']
    #liste_date=['01-01', '01-02', '01-03', '01-04', '01-05', '01-06', '01-07', '01-08', '01-09', '01-10', '01-11', '01-12', '01-13', '01-14', '01-15', '01-16', '01-17', '01-18', '01-19', '01-20', '01-21', '01-22', '01-23', '01-24', '01-25', '01-26', '01-27', '01-28', '01-29', '01-30', '01-31', '02-01', '02-02', '02-03', '02-04', '02-05', '02-06', '02-07', '02-08', '02-09', '02-10', '02-11', '02-12', '02-13', '02-14', '02-15', '02-16', '02-17', '02-18', '02-19', '02-20', '02-21', '02-22', '02-23', '02-24', '02-25', '02-26', '02-27', '02-28', '03-01', '03-02', '03-03', '03-04', '03-05', '03-06', '03-07', '03-08', '03-09', '03-10', '03-11', '03-12', '03-13', '03-14', '03-15', '03-16', '03-17', '03-18', '03-19', '03-20', '03-21', '03-22', '03-23', '03-24', '03-25', '03-26', '03-27', '03-28', '03-29', '03-30', '03-31', '04-01', '04-02', '04-03', '04-04', '04-05', '04-06', '04-07', '04-08', '04-09', '04-10', '04-11', '04-12', '04-13', '04-14', '04-15', '04-16', '04-17', '04-18', '04-19', '04-20', '04-21', '04-22', '04-23', '04-24', '04-25', '04-26', '04-27', '04-28', '04-29', '04-30', '05-01', '05-02', '05-03', '05-04', '05-05', '05-06', '05-07', '05-08', '05-09', '05-10', '05-11', '05-12', '05-13', '05-14', '05-15', '05-16', '05-17', '05-18', '05-19', '05-20', '05-21', '05-22', '05-23', '05-24', '05-25', '05-26', '05-27', '05-28', '05-29', '05-30', '05-31', '06-01', '06-02', '06-03', '06-04', '06-05', '06-06', '06-07', '06-08', '06-09', '06-10', '06-11', '06-12', '06-13', '06-14', '06-15', '06-16', '06-17', '06-18', '06-19', '06-20', '06-21', '06-22', '06-23', '06-24', '06-25', '06-26', '06-27', '06-28', '06-29', '06-30', '07-01', '07-02', '07-03', '07-04', '07-05', '07-06', '07-07', '07-08', '07-09', '07-10', '07-11', '07-12', '07-13', '07-14', '07-15', '07-16', '07-17', '07-18', '07-19', '07-20', '07-21', '07-22', '07-23', '07-24', '07-25', '07-26', '07-27', '07-28', '07-29', '07-30', '07-31', '08-01', '08-02', '08-03', '08-04', '08-05', '08-06', '08-07', '08-08', '08-09', '08-10', '08-11', '08-12', '08-13', '08-14', '08-15', '08-16', '08-17', '08-18', '08-19', '08-20', '08-21', '08-22', '08-23', '08-24', '08-25', '08-26', '08-27', '08-28', '08-29', '08-30', '08-31', '09-01', '09-02', '09-03', '09-04', '09-05', '09-06', '09-07', '09-08', '09-09', '09-10', '09-11', '09-12', '09-13', '09-14', '09-15', '09-16', '09-17', '09-18', '09-19', '09-20', '09-21', '09-22', '09-23', '09-24', '09-25', '09-26', '09-27', '09-28', '09-29', '09-30']
    for date in liste_date :
        th1 = Process(target=Finder_IETE, args=(15,"minute",f'2023-{date}','2023-10-03',f'2023-{date}',TETE,'A'))
        th2 = Process(target=Finder_IETE,args=(20, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'B'))
        th3 = Process(target=Finder_IETE,args=(25, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'C'))
        th4 = Process(target=Finder_IETE,args=(30, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'D'))
        th5 = Process(target=Finder_IETE,args=(35, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'E'))
        th6 = Process(target=Finder_IETE,args=(40, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'F'))
        th7 = Process(target=Finder_IETE,args=(45, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'G'))
        th8 = Process(target=Finder_IETE,args=(50, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'H'))
        th9 = Process(target=Finder_IETE,args=(55, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'I'))
        th10 = Process(target=Finder_IETE,args=(75, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'J'))
        th11 = Process(target=Finder_IETE,args=(90, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'K'))
        th12 = Process(target=Finder_IETE,args=(105, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'L'))
        th13 = Process(target=Finder_IETE,args=(135, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'M'))
        th14 = Process(target=Finder_IETE,args=(150, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'N'))
        th15 = Process(target=Finder_IETE,args=(165, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'O'))
        th16 = Process(target=Finder_IETE,args=(195, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'P'))
        th17 = Process(target=Finder_IETE,args=(210, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Q'))
        th18 = Process(target=Finder_IETE,args=(225, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'R'))
        th19 = Process(target=Finder_IETE,args=(255, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'S'))
        th20 = Process(target=Finder_IETE,args=(270, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'T'))
        th21 = Process(target=Finder_IETE,args=(285, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'U'))
        th22 = Process(target=Finder_IETE,args=(315, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'V'))
        th23 = Process(target=Finder_IETE,args=(330, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'W'))
        th24 = Process(target=Finder_IETE,args=(345, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'X'))
        th25 = Process(target=Finder_IETE,args=(375, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Y'))
        th26 = Process(target=Finder_IETE,args=(390, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'Z'))
        th27 = Process(target=Finder_IETE,args=(405, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'AA'))
        th28 = Process(target=Finder_IETE,args=(435, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'BB'))
        th29 = Process(target=Finder_IETE,args=(450, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'CC'))
        th30 = Process(target=Finder_IETE,args=(465, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'DD'))
        th31 = Process(target=Finder_IETE,args=(495, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'EE'))
        th32 = Process(target=Finder_IETE,args=(510, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'FF'))
        th33 = Process(target=Finder_IETE,args=(525, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'GG'))
        th34 = Process(target=Finder_IETE,args=(555, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'HH'))
        th35 = Process(target=Finder_IETE,args=(570, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'II'))
        th36 = Process(target=Finder_IETE,args=(585, "minute", f'2023-{date}', '2023-10-03', f'2023-{date}', TETE,'JJ'))

        th1.start()
        th2.start()
        th3.start()
        th4.start()
        th5.start()
        th6.start()
        th7.start()
        th8.start()
        th9.start()
        th10.start()
        th11.start()
        th12.start()
        th13.start()
        th14.start()
        th15.start()
        th16.start()
        th17.start()
        th18.start()
        th19.start()
        th20.start()
        th21.start()
        th22.start()
        th23.start()
        th24.start()
        th25.start()
        th26.start()
        th27.start()
        th28.start()
        th29.start()
        th30.start()
        th31.start()
        th32.start()
        th33.start()
        th34.start()
        th35.start()
        th36.start()


        th1.join()
        th2.join()
        th3.join()
        th4.join()
        th5.join()
        th6.join()
        th7.join()
        th8.join()
        th9.join()
        th10.join()
        th11.join()
        th12.join()
        th13.join()
        th14.join()
        th15.join()
        th16.join()
        th17.join()
        th18.join()
        th19.join()
        th20.join()
        th21.join()
        th22.join()
        th23.join()
        th24.join()
        th25.join()
        th26.join()
        th27.join()
        th28.join()
        th29.join()
        th30.join()
        th31.join()
        th32.join()
        th33.join()
        th34.join()
        th35.join()
        th36.join()
















