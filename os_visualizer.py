import tkinter as tk
from tkinter import ttk, messagebox

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("OS Visualizer (Interactive & Easy)")
root.geometry("1100x700")
root.configure(bg="#f0f8ff")

style = ttk.Style()
style.theme_use("clam")

# ================= NOTEBOOK =================
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

notebook.add(tab1, text="🧠 Scheduling")
notebook.add(tab2, text="📦 Memory")
notebook.add(tab3, text="⚡ Paging")

# ================= CANVAS =================
canvas = tk.Canvas(root, bg="white", height=300)
canvas.pack(fill="both", expand=True)

# ================= LEGEND =================
legend = tk.Label(root, text="🟡 Running  🔵 Waiting  🟢 Allocated  🔴 Fault  ⚪ Free",
                  bg="#f0f8ff", font=("Arial", 12))
legend.pack()

# ================= STATUS =================
status = tk.StringVar()
status.set("Ready 😊")
ttk.Label(root, textvariable=status).pack()

# ================= EXPLANATION BOX =================
explain_text = tk.Text(root, height=7, bg="#fff8dc", font=("Arial", 11))
explain_text.pack(fill="x")

def explain(msg):
    explain_text.insert(tk.END, msg + "\n")
    explain_text.see(tk.END)

def clear_explain():
    explain_text.delete(1.0, tk.END)

# =====================================================
# 🧠 SCHEDULING
# =====================================================
def run_scheduler():
    try:
        clear_explain()
        processes = entry_p.get().split(',')
        burst = list(map(int, entry_b.get().split(',')))
        quantum = int(entry_q.get())

        if len(processes) != len(burst):
            raise ValueError

        canvas.delete("all")
        status.set("Running Scheduling...")

        remaining = burst[:]
        x = 50
        y = 100

        while True:
            done = True
            for i in range(len(processes)):

                waiting = [p for j, p in enumerate(processes) if remaining[j] > 0 and j != i]
                if waiting:
                    explain(f"🔵 {', '.join(waiting)} are waiting")

                if remaining[i] > 0:
                    done = False

                    exec_time = min(quantum, remaining[i])
                    explain(f"🟡 {processes[i]} is running for {exec_time} units")

                    canvas.create_rectangle(x, y, x + exec_time*50, y+60, fill="#FFD54F")
                    canvas.create_text(x + 25, y+30, text=processes[i], font=("Arial", 11, "bold"))

                    canvas.update()
                    canvas.after(600)

                    x += exec_time * 50
                    remaining[i] -= exec_time

                    if remaining[i] == 0:
                        explain(f"✅ {processes[i]} finished execution")

            if done:
                break

        status.set("✅ Scheduling Completed")

    except:
        messagebox.showerror("Error", "Invalid Scheduling Input!")

frame1 = ttk.Frame(tab1, padding=10)
frame1.pack()

ttk.Label(frame1, text="Processes (P1,P2,P3)").grid(row=0, column=0)
entry_p = ttk.Entry(frame1)
entry_p.grid(row=0, column=1)

ttk.Label(frame1, text="Burst Time (5,3,6)").grid(row=0, column=2)
entry_b = ttk.Entry(frame1)
entry_b.grid(row=0, column=3)

ttk.Label(frame1, text="Quantum").grid(row=0, column=4)
entry_q = ttk.Entry(frame1)
entry_q.grid(row=0, column=5)

ttk.Button(frame1, text="▶ Run", command=run_scheduler).grid(row=0, column=6, padx=10)

# =====================================================
# 📦 MEMORY
# =====================================================
def run_memory():
    try:
        clear_explain()
        blocks = list(map(int, entry_blocks.get().split(',')))
        processes = list(map(int, entry_proc.get().split(',')))

        canvas.delete("all")
        status.set("Running Memory Allocation...")

        y = 30
        for i, block in enumerate(blocks):
            canvas.create_rectangle(50, y, 250, y+50, fill="#E0E0E0")
            canvas.create_text(150, y+25, text=f"Block {i}\n{block}")
            y += 70

        y = 30
        for i, p in enumerate(processes):
            allocated = False
            for j in range(len(blocks)):
                if blocks[j] >= p:
                    blocks[j] -= p

                    canvas.create_rectangle(300, y, 550, y+50, fill="#81C784")
                    canvas.create_text(425, y+25, text=f"P{i} → Block {j}")

                    explain(f"🟢 Process {i} allocated to Block {j}")
                    allocated = True
                    break

            if not allocated:
                canvas.create_text(425, y+25, text=f"P{i} ❌", fill="red")
                explain(f"🔴 Process {i} could NOT be allocated")

            canvas.update()
            canvas.after(600)
            y += 70

        status.set("✅ Memory Allocation Completed")

    except:
        messagebox.showerror("Error", "Invalid Memory Input!")

frame2 = ttk.Frame(tab2, padding=10)
frame2.pack()

ttk.Label(frame2, text="Blocks (100,500,200)").grid(row=0, column=0)
entry_blocks = ttk.Entry(frame2)
entry_blocks.grid(row=0, column=1)

ttk.Label(frame2, text="Process Size (212,417)").grid(row=0, column=2)
entry_proc = ttk.Entry(frame2)
entry_proc.grid(row=0, column=3)

ttk.Button(frame2, text="▶ Run", command=run_memory).grid(row=0, column=4, padx=10)

# =====================================================
# ⚡ PAGING
# =====================================================
def run_paging():
    try:
        clear_explain()
        pages = list(map(int, entry_pages.get().split(',')))
        capacity = int(entry_frames.get())

        canvas.delete("all")
        status.set("Running Paging...")

        memory = []
        faults = 0
        y = 50

        for page in pages:
            if page not in memory:
                if len(memory) < capacity:
                    memory.append(page)
                else:
                    memory.pop(0)
                    memory.append(page)
                faults += 1
                explain(f"🔴 Page {page} caused a FAULT")
                color = "#EF5350"
            else:
                explain(f"🔵 Page {page} already in memory (HIT)")
                color = "#42A5F5"

            canvas.create_text(200, y, text=f"Page {page}", font=("Arial", 12))
            canvas.create_text(400, y, text=f"{memory}", fill=color, font=("Arial", 12, "bold"))
            canvas.create_text(600, y, text=f"Faults: {faults}", fill="red")

            canvas.update()
            canvas.after(600)
            y += 45

        status.set("✅ Paging Completed")

    except:
        messagebox.showerror("Error", "Invalid Paging Input!")

frame3 = ttk.Frame(tab3, padding=10)
frame3.pack()

ttk.Label(frame3, text="Pages (1,2,3)").grid(row=0, column=0)
entry_pages = ttk.Entry(frame3)
entry_pages.grid(row=0, column=1)

ttk.Label(frame3, text="Frames").grid(row=0, column=2)
entry_frames = ttk.Entry(frame3)
entry_frames.grid(row=0, column=3)

ttk.Button(frame3, text="▶ Run", command=run_paging).grid(row=0, column=4, padx=10)

# ================= RUN =================
root.mainloop()