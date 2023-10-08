"""Deterministic grid world"""

import numpy as np
np.random.seed(42)

class GridWorld():
    def __init__(self, deterministic=True, alpha=0.2, exploration_rate=0.3, start=(0,2)):
        self.GRID_ROWS = 3
        self.GRID_COLS = 4
        self.WIN_STATE = (0,3)
        self.LOSE_STATE = (1,3)
        self.state = start
        self.alpha = alpha
        self.exploration_rate = exploration_rate
        self.deterministic = deterministic
        self.states = []
        self.state_values = {(i, j): 0 \
                             for i in range(self.GRID_ROWS) \
                             for j in range(self.GRID_COLS)}
        self.actions = {
            'up': (-1,0),
            'down': (1,0),
            'left': (0,-1),
            'right': (0,1)
        }
        self.rewards = {
            'win_state': 1,
            'lose_state': -1,
            'else': 0
        }
        

    def nextState(self, action):
        """Returns: next state if valid action or current state if invalid"""
        next_state = tuple(x + y for x, y in zip(self.state, self.actions[action]))
        # print("Potential next position: {}".format(next_state))
        if next_state[0] in range(self.GRID_ROWS):
            if next_state[1] in range(self.GRID_COLS):
                if next_state != (1,1):
                    return next_state
        return self.state
    
    def updateValues(self):
        '''
        Returns: updated state values based on
        V(S_t) = V(S_t) + alpha * [V(S_t+1) - V(S_t)]
        alpha = learning rate
        '''
        def __get_reward():
            if self.state == self.WIN_STATE:
                return self.rewards['win_state']
            elif self.state == self.LOSE_STATE:
                return self.rewards['lose_state']
            else: 
                return self.rewards['else']
            
        reward = __get_reward()
        print(self.state,reward)
        for state in reversed(self.states):
            self.state_values[state] = round(self.state_values[state] + self.alpha * \
                (reward - self.state_values[state]),3)
            
        
    def isEnd(self):
        return self.state == self.WIN_STATE or self.state == self.LOSE_STATE

    def play_action(self):
        def __choose_action():
            # Explore
            if np.random.uniform(0,1) <= self.exploration_rate:
                print("Exploring")
                action =  np.random.choice(list(self.actions.keys()))

            # Greedy
            else:
                print("Greedy")
                opt_reward = 0
                print("From", self.state)
                for act in self.actions.keys():
                    next_reward = self.state_values[self.nextState(act)]
                    # print("next reward: ", next_reward)
                    print("Potential action: {} to {} reward {}".format(act, self.nextState(act), next_reward))
                    if next_reward >= opt_reward:
                        opt_reward = max(next_reward, opt_reward)
                        action = act
            return action
        
        action = __choose_action()
        
        self.states.append(self.nextState(action))
        # print("Current position {} chosen action move {}".format(self.state, action)) 
        print("Chosen: move {} from {}".format(action, self.state)) 
        self.state = self.nextState(action)
        
    def play_grid(self,rounds=10):
        for i in range(rounds):
            print("Round {}".format(i))
            
            if self.isEnd():
                print("In end state, update values and reset")
                self.updateValues()
                print(grid.showValues())
                # Reset
                # breakpoint()
                self.states = []
                self.state = (2,0)
            else: 
                print("Not in end state, continue")
                self.play_action()        
                print("to", self.state)
                print("---------------------")

    def showValues(self):
        # breakpoint()
        for i in range(0, self.GRID_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, self.GRID_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')
                
if __name__ == "__main__":
    rounds = 50
    alpha = 0.3
    explr_rate = 0.2
    grid = GridWorld(alpha=alpha, exploration_rate=explr_rate)
    grid.play_grid(rounds=rounds)
    print(grid.showValues())
