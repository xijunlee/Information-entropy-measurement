from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
filename = "./test"
host = host_subplot(111, axes_class=AA.Axes)
plt.subplots_adjust(right=0.88)
par1 = host.twinx()

host.set_xlim(1,9)
host.set_ylim(7, 11)

host.set_xlabel("Subset of original data")
host.set_ylabel("Entropy (/bit)")
   
par1.set_ylabel("Accuracy (%)")

p1, = host.plot([1,2,3,4,5,6,7,8,9], [7.64,8.63,9.22,9.63,9.95,10.21715,10.43,10.63,10.79], label="Entropy",marker='o',lw=1,ls='--')
p2, = par1.plot([1,2,3,4,5,6,7,8,9], [0.34,0.49,0.505,0.57375,0.586,0.61571,0.6275,0.63,0.64], label="Accuracy",marker='^',lw=1)

par1.set_ylim(0.3,0.7)

   

host.axis["left"].label.set_color(p1.get_color())
par1.axis["right"].label.set_color(p2.get_color())

    
plt.legend(bbox_to_anchor=(0., 1.02, 1., 1.02), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.text(1.5,10.5,r'SVM',fontsize=30)
plt.grid()
plt.draw()
plt.show()
plt.savefig(filename + '.pdf')
