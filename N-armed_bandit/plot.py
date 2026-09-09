import matplotlib.pyplot as plt

def plot(values: list[list[float]], labels: list[str], 
                 title: str, ylabel: str, filename: str):
    fig, ax = plt.subplots(figsize=(15, 8))

    for value, label in zip(values, labels):
        ax.plot(range(len(value)), value, label=label)
    
    ax.set_xlabel("Step")
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.savefig(filename, dpi=300, bbox_inches="tight")
    return fig