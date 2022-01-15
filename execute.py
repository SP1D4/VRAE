
import library_code as lib
''' Welcome to this execution program !!!, You can write any of your code and use the library_code module to check its
    efficiency on some basic parameters that;
    1. How much Time it take to be executed ?
    2. How much Memory it uses to run smoothly ?
    
    The best algorithm on both of these measures will be the winner.............'''

# Defining the codes
from example_prime1 import code1
from example_prime2 import code2
from example_prime3 import code3

# Providing an object of our predefined class in library_code
plt = lib.time_plot([code1, code2, code3], 200)
plt.plot()
plt.loop_complex()
plt.block_prof()
plt.all_plot()

# Memory Profiling
plt_mem = lib.memory_plot([code1, code2, code3], 200)
plt_mem.plot()
plt_mem.loop_complex()
plt_mem.block_prof()
plt_mem.all_plot()