import pickle
from visualization import  overlay_graphs_different_step

t_last = 300

res1 = [i[0] for i in pickle.load(open("test_t_step1.pickle", "rb"))][:-1]
res5 = [i[0] for i in pickle.load(open("test_t_step5.pickle", "rb"))][:-1]
res10 = [i[0] for i in pickle.load(open("test_t_step10.pickle", "rb"))][:-1]

graph_list = [res1, res5, res10]
t_step = [1, 5, 10]
label_list = ["t step 1", "t step 5", "t step 10"]

overlay_graphs_different_step(graph_list, label_list, t_last, t_step)
