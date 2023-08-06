from dscal.calculus import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk 

class graph(calculus):
    def __init__(self,*expression:list):
        '''Access graphs for tkinter GUI applications directly , power of dscal.calculus'''
        '''Example
            from dscal.tkcal import graph
            from tkinter import *

            root=Tk()

            expr_graph=graph('sinx','cosx','x')

            expr_graph_canvas=expr_graph.get_graph2D(root)

            expr_graph_canvas.get_tk_widget().pack(side=LEFT,fill=BOTH,expand=True)

            expr_graph_canvas3D=expr_graph.get_graph3D(root)

            expr_graph_canvas3D.get_tk_widget().pack(side=LEFT,fill=BOTH,expand=True)

            root.mainloop() '''
        super().__init__(*expression)
        
    def get_graph2D(self,master,limit=[-10,10]):    
        '''Get FigureCanvasTkAgg figure with 2D projection.'''
        self.figure2=plt.figure()
        x=np.arange(limit[0],limit[1],0.01)
        plt.plot(x,x*0,label='x-axis')
        try:
            vals=[]
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                vals.append(max(list(y)))
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-(max(vals)),max(vals),0.01)
            plt.plot(y_vals*0,y_vals,label='y-axis')
        except ValueError:
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y,label=self.expressions_[i])
            y_vals=np.arange(-20,20,0.01)
            plt.plot(y_vals*0,y_vals,label='y-axis')    
        plt.legend()
        return FigureCanvasTkAgg(self.figure2,master)


    def get_graph3D(self,master,limit=[-10,10],surface_plot=0,colormap=plt.cm.hsv):
        '''Get FigureCanvasTkAgg figure with 3D projection.'''
        x=np.arange(limit[0],limit[1],0.01)
        if surface_plot==1:
            self.figure3=plt.figure()
            a=self.figure3.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                a.plot_trisurf(x,y*y,y,cmap=colormap)
            plt.show()
        elif surface_plot==0:
            self.figure3=plt.figure()
            a=self.figure3.add_subplot(111,projection='3d')
            for i in range(len(self.expressions)):
                y=ne.evaluate(self.expressions[i])
                plt.plot(x,y*y,y,label=f'{self.expressions[i]}')
        return FigureCanvasTkAgg(self.figure3,master)

    def __add__(self, *others):
        '''Adds graph instances assigning to a new object.'''
        expressions_sum=self.expressions_
        for ex in others:
            expressions_sum+=ex.expressions_
        return graph(*expressions_sum)

    def __str__(self):
        return super().__str__()
    