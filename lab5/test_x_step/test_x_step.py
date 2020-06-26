import pickle
from visualization import  overlay_graphs

t_last = 300
t_step = 1

res1 = [i[0] for i in pickle.load(open("test_x_step1.pickle", "rb"))][:-1]
res0_1 = [i[0] for i in pickle.load(open("test_x_step0_1.pickle", "rb"))][:-1]
res0_01 = [i[0] for i in pickle.load(open("test_x_step0_01.pickle", "rb"))][:-1]

graph_list = [res1, res0_1, res0_01]
label_list = ["x step 1", "x step 0.1", "x step 0.01"]

overlay_graphs(graph_list, label_list, t_last, t_step)