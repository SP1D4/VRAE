from main import code
import re
import matplotlib.pyplot as plt
import time
import tracemalloc
import numpy as np

end_attach = str(''';current, peak = tracemalloc.get_traced_memory(); end = time.perf_counter_ns(); tracemalloc.stop()'''
            + '''; fig.canvas.restore_region(bg); Time.append((end-start)/10**6); Mem.append(current/10**3);'''
            + '''ln.set_ydata(Time[len(Time)-100:]); lin.set_ydata(Mem[len(Mem)-100:]); ax[0].draw_artist(ln);'''
            + '''ax[1].draw_artist(lin);fig.canvas.blit(fig.bbox); fig.canvas.flush_events()''')

start = '''start = time.perf_counter_ns(); tracemalloc.start();'''

infos = str('''x = np.arange(100); fig, ax = plt.subplots(2); ax[0].grid(); ax[1].grid();'''
            + ''' ax[0].set_ylabel('Execution Time (in ms)', font='monospace'); ax[0].set_ylim(0, 100);'''
            + '''ax[1].set_ylabel('Memory Usage (in KB)', font='monospace'); ax[1].set_ylim(-10, 50);'''
            + '''(ln,) = ax[0].plot(x, x, animated=True, color='firebrick');'''
            + '''(lin,) = ax[1].plot(x, x, animated=True, color='firebrick'); plt.show(block=False);'''
            + '''plt.pause(0.1); bg = fig.canvas.copy_from_bbox(fig.bbox); ax[0].draw_artist(ln);'''
            + '''ax[1].draw_artist(lin); fig.canvas.blit(fig.bbox); Time = [0]*100; Mem = [0]*100''')

code = re.sub('/%', infos, code)
code = re.sub('</', start, code)
code = re.sub('/>', end_attach, code)
exec(code)
