import numpy as np
import random
import matplotlib.pyplot as plt

# Berlin52
coords = np.array([
    [565,575],[25,185],[345,750],[945,685],[845,655],[880,660],[25,230],
    [525,1000],[580,1175],[650,1130],[1605,620],[1220,580],[1465,200],
    [1530,5],[845,680],[725,370],[145,665],[415,635],[510,875],[560,365],
    [300,465],[520,585],[480,415],[835,625],[975,580],[1215,245],[1320,315],
    [1250,400],[660,180],[410,250],[420,555],[575,665],[1150,1160],[700,580],
    [685,595],[685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
    [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],[830,610],
    [605,625],[595,360],[1340,725],[1740,245]
])

n = 52
dist = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        dist[i,j] = np.sqrt(((coords[i]-coords[j])**2).sum())

def tour_len(t):
    return sum(dist[t[i], t[(i+1)%n]] for i in range(n))

def aco(rho, it=80, m=20, alpha=1, beta=2):
    tau = np.ones((n,n)) * 0.1
    np.fill_diagonal(tau, 0)
    eta = np.array([[1/dist[i,j] if i!=j else 0 for j in range(n)] for i in range(n)])
    best = float('inf')
    
    for _ in range(it):
        tours, lens = [], []
        for __ in range(m):
            start = random.randint(0,n-1)
            tour = [start]
            vis = {start}
            cur = start
            while len(tour) < n:
                cand = [c for c in range(n) if c not in vis]
                p = [tau[cur,c]**alpha * eta[cur,c]**beta for c in cand]
                p = np.array(p) / np.sum(p)
                nxt = np.random.choice(cand, p=p)
                tour.append(nxt)
                vis.add(nxt)
                cur = nxt
            L = tour_len(tour)
            tours.append(tour)
            lens.append(L)
            best = min(best, L)
        tau *= (1 - rho)
        for t, L in zip(tours, lens):
            delta = 100/L
            for i in range(n):
                a, b = t[i], t[(i+1)%n]
                tau[a,b] += delta
                tau[b,a] += delta
    return best

rho_vals = [0.1, 0.3, 0.5, 0.7, 0.9]
print("\nBerlin52 (Optimum=7542)\n")
for r in rho_vals:
    runs = [aco(r) for _ in range(5)]
    m, s = np.mean(runs), np.std(runs)
    print(f"ρ={r}: {m:.0f} ± {s:.0f} → {(m-7542)/7542*100:.1f}% über Optimum")