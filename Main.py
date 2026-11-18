import sys, matplotlib.pyplot as plt, networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA ===
# AFD completo (equivale al AFND con epsilon de la clase: reconoce solo la palabra "ab")
#   q0 = estado inicial
#   q1 = ya se leyó "a"
#   q2 = ya se leyó "ab"  (estado final)
#   q3 = estado trampa (la palabra ya no puede ser aceptada)
states = {"q0","q1","q2","q3"}
alphabet = {"a","b"}
delta = {("q0","a"):"q1",
        ("q0","b"):"q3",
        ("q1","a"):"q3",
        ("q1","b"):"q2",
        ("q2","a"):"q3",
        ("q2","b"):"q3",
        ("q3","a"):"q3",
        ("q3","b"):"q3"}

q0, F = "q0", {"q2"}

# === Simulación ===
def run(s):
    q, steps = q0, [q0]
    for i,ch in enumerate(s):
        if (q,ch) not in delta: raise ValueError(f"Sin transición desde {q} con '{ch}' en pos {i}")
        q = delta[(q,ch)]; steps.append(q)
    return steps, steps[-1] in F

# === Grafo y layout ===
G = nx.MultiDiGraph(); G.add_nodes_from(states)
for (q,a),p in delta.items(): G.add_edge(q,p,key=a,label=a)
pos = {"q0":(0,0), "q1":(1.5,0), "q2":(3,0), "q3":(1.5,-1.6)}   # posiciones fijas del dibujo

# === Dibujo por paso ===
def _mid(p1,p2,o=0.10):
    (x1,y1),(x2,y2)=p1,p2; mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; nx_,ny_=dy,-dx; L=(nx_**2+ny_**2)**0.5 or 1
    return mx+o*nx_/L, my+o*ny_/L

def draw_step(current, idx, sym=None):
    plt.clf(); nodes=list(G.nodes())
    nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_size=[900 if n==current else 600 for n in nodes],linewidths=[3 if n in F else 1 for n in nodes],edgecolors="black")
    nx.draw_networkx_labels(G,pos)
    seen={}
    for u,v,k,d in G.edges(keys=True,data=True):
        if u == v:
            x, y = pos[u]
            j = seen.get((u, u), 0); seen[(u, u)] = j + 1

            rad  = 2.2 if j % 2 == 0 else -2.2    # bucle visible fuera del círculo
            dx   = 0.10                           # ancho del arco
            offy = 0.34 if j % 2 == 0 else -0.34  # etiqueta junto al bucle

            loop = FancyArrowPatch((x - dx, y), (x + dx, y),
                connectionstyle=f"arc3,rad={rad}",
                arrowstyle='-|>', mutation_scale=18, linewidth=1.2,
                shrinkA=6, shrinkB=6, zorder=5, clip_on=False)
            plt.gca().add_patch(loop)

            plt.text(x, y + offy, d["label"], fontsize=10, ha="center", va="center")
            continue
        i=seen.get((u,v),0); seen[(u,v)]=i+1; rad = 0.18 if i % 2 == 0 else -0.18
        nx.draw_networkx_edges(G,pos,edgelist=[(u,v)],connectionstyle=f"arc3,rad={rad}",arrows=True,arrowstyle='-|>',arrowsize=20)
        lx,ly=_mid(pos[u],pos[v],0.14 if i%2==0 else -0.14); plt.text(lx,ly,d['label'],fontsize=11,ha='center',va='center')
    plt.axis('off'); plt.xlim(-0.6,3.6); plt.ylim(-2.4,0.9); plt.title(f"Paso {idx}: {current}" + (f" | '{sym}'" if sym else "")); plt.pause(1.0)

# === main ===
if __name__=='__main__':
    s = sys.argv[1] if len(sys.argv)>1 else input("Cadena (a/b): ").strip()
    try:
        steps, ok = run(s); print("ACEPTA" if ok else "RECHAZA", f"(estado final: {steps[-1]})")
        plt.ion(); draw_step(steps[0],0)
        for i,ch in enumerate(s,1): draw_step(steps[i],i,ch)
        plt.ioff(); plt.show()
    except Exception as e:
        print("RECHAZA:", e)
