import pickle
from visualization import  overlay_graphs

t_last = 300
t_step = 1

res1 = [i[0] for i in pickle.load(open("test_a2_1.pickle", "rb"))][:-1]
res2 = [i[0] for i in pickle.load(open("test_a2_2_049.pickle", "rb"))][:-1]
res10 = [i[0] for i in pickle.load(open("test_a2_10.pickle", "rb"))][:-1]

graph_list = [res1, res2, res10]
label_list = ["a2 = 1", "a2 = 2.049", "a2 = 10"]

overlay_graphs(graph_list, label_list, t_last, t_step)