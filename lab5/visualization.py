import matplotlib.pyplot as plt
import numpy as np


def draw_graphs(res, x_max, t_max, x_step, t_step):
    # Графики
    lenres = len(res)
    t_last = len(res[0])
    res_cutted = [i[0:t_last:] for i in res]  # обрезаем неинтересную часть графика

    # -- Трехмерный
    x, y = np.mgrid[0:lenres:1, 0:t_last:1]
    z = np.array([np.array(i) for i in res_cutted])

    fig_3d = plt.figure()
    xyz = fig_3d.add_subplot(111, projection='3d')
    xyz.plot_surface(x, y, z, cmap='inferno')
    fig_3d.show()

    # -- Проекции
    fig, (first_graph, second_graph) = plt.subplots(
        nrows=1, ncols=2,
        figsize=(8, 4))

    # ------- Первая cm - K
    x = list(np.arange(0, 10, x_step))
    x_cutted = x[:t_last:]
    step1 = 10
    for i in res_cutted[::step1]:
        first_graph.plot(x_cutted, i)
    first_graph.plot(x_cutted, res_cutted[-1])
    first_graph.set_xlabel("x, cm")
    first_graph.set_ylabel("T, K")
    first_graph.grid()

    # ------- Вторая sec - K
    step2 = 5
    te = list(range(0, t_max, t_step))
    for i in np.arange(0, x_max / 3, 0.2 * step2):
        line = [j[int(i / x_step)] for j in res]
        second_graph.plot(te, line[:-1])
    second_graph.set_xlabel("t, sec")
    second_graph.set_ylabel("T, K")
    second_graph.grid()
    fig.show()


def overlay_graphs(graph_list, label_list, t_max, t_step):
    fig, second_graph = plt.subplots(
        nrows=1, ncols=1,
        figsize=(8, 4))
    te = list(range(0, t_max, t_step))
    for cur_graph in graph_list:
        second_graph.plot(te, cur_graph)
    second_graph.set_xlabel("t, sec")
    second_graph.set_ylabel("T, K")
    second_graph.legend(label_list)
    second_graph.grid()
    fig.show()

def overlay_graphs_different_step(graph_list, label_list, t_max, t_step):
    fig, second_graph = plt.subplots(
        nrows=1, ncols=1,
        figsize=(8, 4))
    for i in range(len(graph_list)):
        second_graph.plot(list(range(0, t_max, t_step[i])), graph_list[i])
    second_graph.set_xlabel("t, sec")
    second_graph.set_ylabel("T, K")
    second_graph.legend(label_list)
    second_graph.grid()
    fig.show()
