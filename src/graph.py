import json

import matplotlib.pyplot as plt

def create_graph(input_path: str, output_path: str):
    with open(input_path) as f:
        data = json.load(f)

    date = []
    kcal = []
    time = []
    for val in data:
        date.append(val["read_file_name"].replace("2020-", "").replace(".png", ""))
        kcal.append(val["kcal"])
        time.append(val["time"])

    kcal = [float(str(k).replace("error", "0")) for k in kcal]
    time = [float(str(t).replace("error", "0")) for t in time]

    
    fig = plt.figure(figsize=(15, 5))
    ax1 = fig.add_subplot(111)
    ln1=ax1.plot(date, kcal,'C0',label=r'kcal')
    ax2 = ax1.twinx()
    ln2=ax2.plot(date, time,'C1',label=r'time')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc='lower right')
    ax1.set_xlabel('date')
    ax1.set_ylabel(r'kcal')
    ax1.grid(True)
    ax2.set_ylabel(r'time')
    plt.savefig(output_path) 

if __name__ == '__main__':
    create_graph("output/ocr_result.json", "output/graph.png")