from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

app = Flask(__name__)

L = [[None for x in range(8)] for y in range(8)]

R = L.copy()
GRACZE = []
BIEZACY_GRACZ = 0
LICZNIK0 = 0
LICZNIK1 = 0
WYGRANA = 0

@app.route('/')
def start():
    return render_template('root.htm')


@app.route('/plansza')
def plansza():
    global L, GRACZE, BIEZACY_GRACZ, LICZNIK1, LICZNIK0, WYGRANA
    sprawdz_wynik()
    if LICZNIK1==0 and LICZNIK0==0:
        L[3][3] = '0'
        L[4][4] = '0'
        L[3][4] = '1'
        L[4][3] = '1'
    legal_moves()
    sprawdz_wynik()
    return render_template('plansza.htm', gracze=GRACZE, gracz=BIEZACY_GRACZ, granie=str(BIEZACY_GRACZ), plansza=L, wynik1=LICZNIK1, wynik0=LICZNIK0, wygrana=WYGRANA)

def sprawdz_linie(dr,dc,r,c):
    global BIEZACY_GRACZ, L
    zmienna = L[r][c]
    zmienna2 = str(BIEZACY_GRACZ)

    if zmienna == zmienna2:
        return True

    if (r+dr) < 0 or (c+dc) > 7 or (r+dr) > 7 or (c+dc) < 0:
        return False

    return sprawdz_linie(dr, dc, r + dr, c + dc)

def boczek(dr,dc,r,c):
    global BIEZACY_GRACZ, L

    if BIEZACY_GRACZ == 1:
        przeciwnik = 0
    else:
        przeciwnik = 1

    if (r + dr) < 0 or (r + dr) > 7:
        return False
    if (c + dc) < 0 or (c + dc) > 7:
        return False
    if L[r+dr][c+dc] != str(przeciwnik):
        return False

    if (r+dr+dr) < 0 or (r+dr+dr) > 7:
        return False
    if (c+dc+dc) < 0 or (c+dc+dc) > 7:
        return False

    return sprawdz_linie(dr, dc, r + dr + dr, c + dc + dc)

def legal_moves():
    global BIEZACY_GRACZ, L
    for j in range(8):
        for i in range(8):
            if L[j][i]!='1' and L[j][i]!='0':
                L[j][i] = '3'
                R[j][i] = '3'
                nw = boczek(-1,-1,j,i)
                nn = boczek(-1,0,j,i)
                ne = boczek(-1,1,j,i)

                ww = boczek(0,-1,j,i)
                ee = boczek(0,1,j,i)

                sw = boczek(1,-1,j,i)
                ss = boczek(1,0,j,i)
                se = boczek(1,1,j,i)

                if nw or nn or ne or ww or ee or sw or ss or se:
                    print(R[j][i])
                    L[j][i] = '2'
                else:
                    print("błagam nie podmieniaj")
            else:
                print(R[i][j])

@app.route('/new')
def new():
    return render_template('new.htm')


@app.route('/reset', methods=['POST'])
def reset():
    global L, R, GRACZE, LICZNIK0, LICZNIK1
    LICZNIK0 = 0
    LICZNIK1 = 0
    GRACZE = []
    GRACZE.append(request.form['gracz1'])
    GRACZE.append(request.form['gracz2'])
    L = [[None for x in range(8)] for y in range(8)]
    R = L.copy()
    return redirect('/plansza')

def sprawdz_wynik():
    global L, LICZNIK1, LICZNIK0, WYGRANA
    LICZNIK0 = (sum(x.count('0') for x in L))
    LICZNIK1 = (sum(x.count('1') for x in L))
    WYGRANA = (sum(x.count('2') for x in L))

@app.route('/ruch/<gracz>/<int:X>/<int:Y>')
def ruch(gracz, X, Y):
    global L, BIEZACY_GRACZ, GRACZE
    L[X][Y] = str(gracz)
    obracamy(X,Y)
    BIEZACY_GRACZ += 1
    BIEZACY_GRACZ %= len(GRACZE)

    return redirect('/plansza')

def obrocLinie(dr,dc,r,c):
    global L, BIEZACY_GRACZ

    if (r + dr) < 0 or (r + dr) > 7:
        return False
    if (c + dc) < 0 or (c + dc) > 7:
        return False

    if L[r+dr][c+dc]=='3' or L[r+dr][c+dc]=='2' or L[r+dr][c+dc] is None:
        return False

    if L[r+dr][c+dc]==str(BIEZACY_GRACZ):
        return True
    else:
        if obrocLinie(dr,dc,r + dr,c + dc):
            print("obracam")
            L[r+dr][c+dc] = str(BIEZACY_GRACZ)
            return True
        else:
            return False

def obracamy(r,c):

    obrocLinie(-1, -1, r, c)
    obrocLinie(-1, 0, r, c)
    obrocLinie(-1, 1, r, c)

    obrocLinie(0, -1, r, c)
    obrocLinie(0, 1, r, c)

    obrocLinie(1, -1, r, c)
    obrocLinie(1, 0, r, c)
    obrocLinie(1, 1, r, c)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5124', debug=True)