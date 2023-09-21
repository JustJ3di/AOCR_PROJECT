import gurobipy as gp
from gurobipy import GRB
import random
import math
import time
import itertools

#EURISTICA GREEDY  O(n) + O(nLogn) 
def solve_more_pizza_greedy(max_slices, pizza_slices):
    
    selected_pizzas  = [] #Pizze prese
    score = 0              #score
    pizza_slices.sort()
    for i in range(len(pizza_slices) - 1, -1, -1):
        if pizza_slices[i] + score <= max_slices:  #c'è spazio ?
            selected_pizzas.append(i)
            score += pizza_slices[i] #aumento lo score
    return score, selected_pizzas  

#EURISTICA APPROCCIO RANDOM + Raffinamento con opt-2 in O(n^2)

def random_heuristic(max_slices, pizza_slices,num_iter):
    score = 0
    selected_pizzas = []
    # Esegui cerca una soluzione random per un numero di iterazioni desiderato
    for _ in range(num_iter):  
        selection = []
        total_slices = 0

        for i in range(len(pizza_slices)):
            # Scegli casualmente se includere o escludere la pizza corrente(50%)
            if random.random() < 0.5:  
                if total_slices + pizza_slices[i] <= max_slices:
                    selection.append(i)
                    total_slices += pizza_slices[i]
        # Aggiorna la soluzione migliore se viene trovata una selezione con un valore maggiore
        if total_slices > score:  
            score = total_slices
            selected_pizzas = selection

    #raffinamento soluzione trovata (RICERCA LOCALE)
    for j in selected_pizzas:  
        for i in range(len(pizza_slices)):
            if i not in selected_pizzas:
                new_score = score - pizza_slices[j] + pizza_slices[i] #calcolo nuovo score
                if(score + pizza_slices[i] <= max_slices):#caso in cui è possibile aggiungere una pizza        
                    score += pizza_slices[i]
                    selected_pizzas.append(i)
                elif new_score > score and new_score <= max_slices:#caso in cui conviene scambiare due pizze       
                    if j in selected_pizzas:
                        selected_pizzas.remove(j)  #rimuovo la vecchia
                    selected_pizzas.append(i)  #inserisco la nuova pizza
                    score = new_score              #aggiorno lo score
    
    return score


#SOLUZIONE: PROGRAMMAZIONE DINAMICA, RICORSIONE + MEMO  O(n^2)

def dp(max_slices, pizza_slices, pizza_index, memo):
    if pizza_index < 0:
        return 0

    if memo[pizza_index][max_slices]  != -1:
        return memo[pizza_index][max_slices]

    current_pizza_size = pizza_slices[pizza_index]

    if current_pizza_size > max_slices:
        result = dp(max_slices, pizza_slices, pizza_index - 1, memo)
    else:
        include_pizza = current_pizza_size + dp(max_slices - current_pizza_size, pizza_slices, pizza_index - 1, memo)
        exclude_pizza = dp(max_slices, pizza_slices, pizza_index - 1, memo)
        result = max(include_pizza, exclude_pizza)

    memo[pizza_index][max_slices] = result

    return result   


#Approccio in programmazione lineare intera
def solve_more_pizza_PL01(max_slices, pizza_slices):
    # Creazione del modello
    model = gp.Model("MorePizzaProblem")
    # Creazione delle variabili di decisione
    pizza_vars = model.addVars(len(pizza_slices), vtype=GRB.BINARY, name="Pizza")
    # Definizione della funzione obiettivo
    model.setObjective(sum(pizza_slices[i] * pizza_vars[i] for i in range(len(pizza_slices))), sense=GRB.MAXIMIZE)
    # Definizione dei vincoli
    model.addConstr(sum(pizza_slices[i] * pizza_vars[i] for i in range(len(pizza_slices))) <= max_slices)
    # Risoluzione del modello
    model.optimize()
    # Estrazione della soluzione
    score = int(model.objVal)
    selected_pizzas = [i for i, var in enumerate(pizza_vars.values()) if var.x == 1]

    return score, selected_pizzas



#FUNZIONE PER INPUT
def read():
    with open(f'input/b_small.in') as f:
        m, n = f.readline().split(' ')
        return int(m),[int(s) for s in f.readline().split(' ')]
        

max_slices,pizza_slices = read()

start_time = time.time()
score, selected_pizzas = solve_more_pizza_PL01(max_slices, pizza_slices)
end_time = time.time()
print()
print("Score PLI:", score)
print()
#print("Pizze selezionate dal PLI:", selected_pizzas)
#print()
print("Tempo PLI :", end_time-start_time,"sec")
print()
start_time = time.time()
scoregreedy, selected_pizzas = solve_more_pizza_greedy(max_slices, pizza_slices)
end_time = time.time()
print()
print("Score Greedy:", scoregreedy)
print()
#print("Pizze selezionate dal greedy:", selected_pizzas)
#print()
print("Tempo greedy:", end_time-start_time,"sec")
print()
memo = [[-1] * (max_slices +1) for i in range(len(pizza_slices)+1)]
scoredp = dp(max_slices,pizza_slices,len(pizza_slices)-1, memo)
print()
print("Score dp:", scoredp)

print()
k = 1000
start_time = time.time()
scorerandom = random_heuristic(max_slices,pizza_slices, k)
end_time = time.time()
print()
print("Score random:", scorerandom)
print("\nTempo random:",end_time-start_time,"sec\n")

'''
start_time = time.time()
score2, selected_pizzas = improve_solution(max_slices, pizza_slices, score1, selected_pizzas)
end_time = time.time()
print()
print("Score Greedy post improve:", score2)
print()
print("Pizze seleziona post improve:", selected_pizzas)
print()
print("Tempo :", end_time-start_time,"sec")
print()

'''
print("Valutazione euristica:", (abs(score-scoregreedy)*100)/abs(score))

print("\n\n")
