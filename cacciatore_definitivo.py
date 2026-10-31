import math
import os
from datetime import datetime

def is_prime(num):
    """Verifica se un numero è primo puro."""
    if num < 2: return False
    if num in (2, 3, 5, 7): return True
    if num % 2 == 0 or num % 3 == 0 or num % 5 == 0 or num % 7 == 0: return False
    for i in range(11, int(math.isqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True

def fattorizza(num):
    """Restituisce i fattori primi di un numero composto per capire lo stato."""
    fattori = []
    d = 2
    temp = num
    while d * d <= temp:
        while temp % d == 0:
            fattori.append(d)
            temp //= d
        d += 1
    if temp > 1:
        fattori.append(temp)
    return fattori

def cacciatore_dinamico(n):
    base = n * (n + 1)
    
    # 1. Clausola di salvaguardia per numeri molto bassi
    if base < 100:
        for j in [-1, 1, -5, 5, -3, 3]:
            candidato = base + j
            if candidato > 1 and is_prime(candidato):
                return candidato, j, "Primo Puro", [candidato]
    
    # 2. Generazione della cartuccera espansa di Jolly (32 potenziali vie di fuga)
    jolly_potenziali = [
        -1, 1, -5, 5, -7, 7, -11, 11, -13, 13, -17, 17, -19, 19, -23, 23, -29, 29,
        -31, 31, -37, 37, -41, 41, -43, 43, -47, 47, -49, 49, -53, 53
    ]
    jolly_sicuri = []
    
    for j in jolly_potenziali:
        nuovo_valore = base + j
        if nuovo_valore % 2 == 0: continue 
        if nuovo_valore % 3 == 0: continue 
        if nuovo_valore % 5 == 0: continue 
        if nuovo_valore % 7 == 0: continue 
        if nuovo_valore % 11 == 0: continue 
        if nuovo_valore % 13 == 0: continue 
        if nuovo_valore % 17 == 0: continue 
        if nuovo_valore % 19 == 0: continue 
        jolly_sicuri.append(j)
    
    if not jolly_sicuri:
        jolly_sicuri = [1, -5, 7, -11, 23, -29, 31, -31, 37, -37, 41, -41, 43, -43, 47, -47]

    # 3. Test prioritario: cerchiamo PRIMA i Primi Puri in tutta la lista
    semiprimo_riserva = None
    jolly_riserva = None
    scomp_riserva = None
    
    for j in jolly_sicuri:
        candidato = base + j
        if is_prime(candidato):
            return candidato, j, "Primo Puro", [candidato]
        
        # Se incontriamo un semiprimo, lo annotiamo ma continuiamo a cercare un Primo
        if semiprimo_riserva is None:
            f = fattorizza(candidato)
            if len(f) == 2:
                semiprimo_riserva = candidato
                jolly_riserva = j
                scomp_riserva = f

    # Se non abbiamo trovato nessun Primo Puro, usiamo la riserva Semiprima
    if semiprimo_riserva is not None:
        return semiprimo_riserva, jolly_riserva, "Semiprimo", scomp_riserva
    
    # 4. STRATEGIA ESTREMA: Espansione a spirale dinamica
    distanza = 55
    while True:
        for segno in [-1, 1]:
            j_estremo = distanza * segno
            candidato = base + j_estremo
            if candidato % 3 != 0 and candidato % 5 != 0 and candidato % 7 != 0:
                if is_prime(candidato):
                    return candidato, j_estremo, "Primo Puro", [candidato]
                f = fattorizza(candidato)
                if len(f) == 2:
                    return candidato, j_estremo, "Semiprimo", f
        distanza += 2

# --- BLOCCO DI ESECUZIONE CON STATISTICHE E SALVATAGGIO ---
print("="*60)
print("     IL CACCIATORE DI PRIMI DINAMICO AUTOREGOLANTE")
print("="*60)

start_n = int(input("Inserisci il valore INIZIALE di n: "))
end_n = int(input("Inserisci il valore FINALE di n: "))
print("-"*60)

totale_numeri = end_n - start_n + 1
conteggio_verdi = 0
conteggio_gialli = 0
jolly_utilizzati = []
record_jolly_alto = 0

report_lines = []
report_lines.append(f"Cacciatore Report - Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Range analizzato: n = {start_n} to {end_n} (Total: {totale_numeri})\n")
report_lines.append(f"{'n':<10} | {'Formula & Jolly':<25} | {'Risultato':<18} | Status")
report_lines.append("-" * 75)

for n in range(start_n, end_n + 1):
    risultato, jolly_usato, stato, scomposizione = cacciatore_dinamico(n)
    segno = f"+ {jolly_usato}" if jolly_usato >= 0 else f"- {abs(jolly_usato)}"
    formula_str = f"[{n}·({n}+1)] {segno}"
    
    jolly_utilizzati.append(abs(jolly_usato))
    if abs(jolly_usato) > record_jolly_alto:
        record_jolly_alto = abs(jolly_usato)
    
    if stato == "Primo Puro":
        conteggio_verdi += 1
        print(f"n = {n:4} | {formula_str:<22} = {risultato:<12} -> 🟢 {stato}")
        report_lines.append(f"n = {n:<6} | {formula_str:<25} | {risultato:<18} | [PRIME]")
    elif stato == "Semiprimo":
        conteggio_gialli += 1
        fattori_str = " × ".join(map(str, scomposizione))
        print(f"n = {n:4} | {formula_str:<22} = {risultato:<12} -> 🟡 {stato} ({fattori_str})")
        report_lines.append(f"n = {n:<6} | {formula_str:<25} | {risultato:<18} | [SEMIPRIME] ({fattori_str})")

# Calcolo Statistiche Finali
perc_verdi = (conteggio_verdi / totale_numeri) * 100
perc_gialli = (conteggio_gialli / totale_numeri) * 100
media_jolly = sum(jolly_utilizzati) / len(jolly_utilizzati)

stat_block = f"""
========================= STATISTICHE FINALI =========================
Total numbers scanned: {totale_numeri}
🟢 Primi Puri (Green):  {conteggio_verdi} ({perc_verdi:.2f}%)
🟡 Semiprimi (Yellow):  {conteggio_gialli} ({perc_gialli:.2f}%)
🔴 Composti (Red):      0 (0.00%) -> Success Rate: 100.00% 🎉

Average Jolly Distance: {media_jolly:.2f}
Highest Jolly Distance: {record_jolly_alto}
======================================================================
"""
print(stat_block)

# Aggiungiamo le statistiche al report e salviamo sul Desktop del Mac
report_lines.append("\n" + stat_block)
desktop_path = os.path.expanduser("~/Desktop/cacciatore_report.txt")
try:
    with open(desktop_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"💾 Report salvato con successo sulla Scrivania: {desktop_path}\n")
except Exception:
    pass
