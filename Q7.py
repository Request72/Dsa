import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

class RouteOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Delivery Route Optimizer")
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.setup_gui()

    def setup_gui(self):
        self.delivery_label = tk.Label(self.root, text="Enter Delivery Points (address,priority):")
        self.delivery_label.pack()

        self.delivery_text = tk.Text(self.root, height=10, width=50)
        self.delivery_text.pack()

        self.algorithm_label = tk.Label(self.root, text="Select Optimization Algorithm:")
        self.algorithm_label.pack()

        self.algorithm_var = tk.StringVar()
        self.algorithm_combobox = ttk.Combobox(self.root, textvariable=self.algorithm_var, values=["Dijkstra", "TSP"])
        self.algorithm_combobox.pack()

        self.vehicle_label = tk.Label(self.root, text="Vehicle Capacity and Constraints:")
        self.vehicle_label.pack()

        self.vehicle_capacity = tk.Entry(self.root)
        self.vehicle_capacity.insert(0, "Capacity")
        self.vehicle_capacity.pack()

        self.optimize_button = tk.Button(self.root, text="Optimize Route", command=self.optimize_route)
        self.optimize_button.pack()

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.status_text = tk.Text(self.root, height=5, width=60)
        self.status_text.pack()

    def parse_delivery_points(self):
        delivery_data = self.delivery_text.get("1.0", tk.END).strip().split('\n')
        nodes = {}
        for entry in delivery_data:
            if entry:
                address, priority = entry.split(',')
                nodes[address] = int(priority)
        return nodes

    def optimize_route(self):
        delivery_points = self.parse_delivery_points()
        if not delivery_points:
            messagebox.showwarning("Warning", "No delivery points provided.")
            return

        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showwarning("Warning", "No algorithm selected.")
            return

        self.status_text.delete(1.0, tk.END)
        self.executor.submit(self.calculate_route, delivery_points, algorithm)

    def calculate_route(self, delivery_points, algorithm):
        G = nx.Graph()
        addresses = list(delivery_points.keys())
        for i in range(len(addresses)):
            for j in range(i+1, len(addresses)):
                distance = random.randint(1, 10)
                G.add_edge(addresses[i], addresses[j], weight=distance)
        
        route = []
        if algorithm == "Dijkstra":
            start_node = addresses[0]
            end_node = addresses[-1]
            try:
                length, path = nx.single_source_dijkstra(G, start_node, end_node)
                route = path
            except nx.NetworkXNoPath:
                route = []

        elif algorithm == "TSP":
            path = nx.approximation.traveling_salesman_problem(G, cycle=False)
            route = path
        
        self.visualize_route(G, route)

    def visualize_route(self, G, route):
        self.canvas.delete("all")

        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=self.canvas, with_labels=True, node_size=500, node_color='skyblue', font_size=10)
        
        if route:
            path_edges = list(zip(route, route[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

        self.status_text.insert(tk.END, f"Optimized Route: {route}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RouteOptimizerGUI(root)
    root.mainloop()
