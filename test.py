import matplotlib.pyplot as plt

for dpi in [72,100,144]:

    fig,ax = plt.subplots(figsize=(1.5,2), dpi=dpi)
    ax.set_title("fig.dpi={}".format(dpi))

    ax.set_ylim(-2,2)
    ax.set_xlim(-2,2)
    print(fig.get_size_inches()*fig.dpi)
    spd=fig.get_size_inches()*fig.dpi
    spd=spd[0]/4

    ax.scatter([0],[0], s=spd**2, 
               marker="s", linewidth=0, label="100 points^2")
    ax.scatter([0],[0], s=10**2, 
               linewidth=0, label="100 points^2")
    ax.scatter([1],[0], s=(10*72./fig.dpi)**2, 
               marker="s", linewidth=0, label="100 pixels^2")

    ax.legend(loc=8,framealpha=1, fontsize=8)

    #fig.savefig("fig{}.png".format(dpi), bbox_inches="tight")

plt.show() 