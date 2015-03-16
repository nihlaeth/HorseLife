import elements as e


class Main():
    def __init__(self, actions):
        
        self.actions = actions

        self.i = 0


    def display(self):
        print e.title("Main")+"\n\n"

        for action in self.actions:
            print str(self.i)+") "+action
            self.i+=1
        
        choice = e.input(self.i)
        return actions[choice]
