import pickle
from visualization import  overlay_graphs

t_last = 300
t_step = 1

res1 = [i[0] for i in pickle.load(open("test_b2_0_563e-1.pickle", "rb"))][:-1]
res2 = [i[0] for i in pickle.load(open("test_b2_0_563e-2.pickle", "rb"))][:-1]
res3 = [i[0] for i in pickle.load(open("test_b2_0_563e-3.pickle", "rb"))][:-1]
res4 = [i[0] for i in pickle.load(open("test_b2_0_563e-4.pickle", "rb"))][:-1]

graph_list = [res1, res2, res3, res4]
label_list = ["b2 = 0_563e-1", "b2 = 0_563e-2", "b2 = 0_563e-3", "b2 = 0_563e-4"]

overlay_graphs(graph_list, label_list, t_last, t_step)
print()