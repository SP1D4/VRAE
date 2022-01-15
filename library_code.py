import matplotlib.pyplot as plt
import numpy as np
import time
import tracemalloc
import re

# Some of the useful fonts
font = {'family': 'monospace',
        'color': 'black',
        'weight': 'normal',
        'size': 12,
        }

font_tlt = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }


# A color changer function that we use later to lighten the color
def adjust_color(color, amount=1.8):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1], )), c[2])


class time_plot:

    def __init__(self, codes, repeat):
        self.codes = codes
        self.repeat = repeat
        self.color_plot = 'White'
        self.color_loop = 'White'

    # Plotting all the timings in various runs
    def plot(self):
        self.fig_def, self.ax = plt.subplots(figsize=(9, 7))
        val = input('Type y to set colors for Time plot otherwise Enter: ')
        back_color = {}

        # Look of all the Codes given in list format
        for seq, code in enumerate(self.codes):
            code = re.sub('</', '', code)
            code = re.sub('/>', '', code)
            Time = []
            for empt in range(self.repeat):
                start = time.perf_counter_ns()
                exec(code)
                end = time.perf_counter_ns()
                Time.append(end - start)

            x = np.arange(self.repeat)
            y = np.array(Time)
            Y = [np.mean(Time)] * self.repeat
            if val == 'y':
                color = input('Enter the color:')
                self.ax.plot(x, y, color=color, label='Code ' + str(seq + 1))
                self.ax.plot(x, Y, color=color, linestyle=':')
                back_color[np.mean(Time)] = adjust_color(color)  # Here we use a dictionary to store color

            else:
                self.axis = self.ax.plot(x, y, label='Code ' + str(seq + 1))
                self.ax.plot(x, Y, color=self.axis[0].get_color(), linestyle=':')
                back_color[np.mean(Time)] = adjust_color(self.axis[0].get_color())

        else:
            self.ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax.set_xlabel('Execution of Codes', fontdict=font)
            self.ax.set_ylabel('Timings (in nanoseconds)', fontdict=font)
            self.ax.set_title('Execution Time Profile', fontdict=font_tlt)
            self.ax.grid()

            self.color_plot = back_color[min(back_color.keys())]

    # Works to plot the running time of
    def loop_complex(self):

        self.fig1, self.ax1 = plt.subplots(figsize=(9, 7))
        back_color = {}
        val = input('Type y to set colors to Time loop complex otherwise Enter: ')
        for i, code in enumerate(self.codes):

            Times = np.zeros(1, dtype='int64')
            for repeat in range(self.repeat):

                pattern = '</[^>]+/>'
                info = re.sub(pattern, '', code)
                spt = info.split('\n') + ['</', '/>']
                loop = code
                for splits in spt:
                    loop = loop.replace(splits, '')

                exec(info)
                Time = []

                exec('''start = time.perf_counter_ns() ;''' + loop + '''; end = time.perf_counter_ns();'''
                     + '''Time.append(end - start)''')

                Times = np.add(Times, Time)
            Times = Times / self.repeat

            x = np.arange(len(Times))
            y = np.array(Times)
            if val == 'y':
                color = input('Enter the color:')
                self.ax1.plot(x, y, color=color, label='Loop ' + str(i + 1))
                back_color[np.mean(y)] = adjust_color(color)

            else:
                self.axis1 = self.ax1.plot(x, y, label='Loop ' + str(i + 1))
                back_color[np.mean(y)] = adjust_color(self.axis1[0].get_color())

        else:
            self.ax1.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax1.set_xlabel('Number of loop in execution', fontdict=font)
            self.ax1.set_ylabel('Timings (in nanoseconds)', fontdict=font)
            self.ax1.set_title('Execution Time of Loops', fontdict=font_tlt)
            self.ax1.grid()

            self.color_loop = back_color[min(back_color.keys())]


    def block_prof(self, deep=False):
        self.fig2, self.ax2 = plt.subplots(figsize=(9, 7))
        val = input('Type y to set colors for Time block profiling otherwise Enter: ')

        Data = []
        for code in self.codes:

            code = re.sub('</', '', code)
            code = re.sub('/>', '', code)
            Times = np.zeros(1, dtype='int64')
            for rep in range(self.repeat):
                if deep:
                    pattern = r'\n(?![ \t]{3,})'
                else:
                    pattern = r'\n(?![ \t]+)'
                blocks = re.split(pattern, code)
                while '' in blocks: blocks.remove('')
                Time = []

                for i in blocks:
                    start = time.perf_counter_ns()
                    exec(i)
                    end = time.perf_counter_ns()
                    Time.append(end - start)
                Times = np.add(Times, Time)
            Times = Times / self.repeat
            Data.append(Times)

        # Data Plotting
        barwidth = 1 / (len(Data) + 1)

        for bars in range(len(Data)):

            bar = np.arange(0, len(Data[0]), 1)
            bar = bar + (barwidth * bars)
            if val == 'y':
                color = input('Enter the color:')
                self.ax2.bar(bar, Data[bars], width=barwidth, label='Code ' + str(bars + 1), color=color)
            else:
                self.ax2.bar(bar, Data[bars], width=barwidth, label='Code ' + str(bars + 1))

        else:
            self.ax2.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax2.set_xlabel('Blocks Time Analysis', fontdict=font)
            self.ax2.set_ylabel('Timings (in nanoseconds)', fontdict=font)
            plt.xticks([t + barwidth * (len(Data) - 1) / 2 for t in range(len(Data[0]))],
                       ['Block' + str(i + 1) for i in range(len(Data[0]))])
            self.ax2.set_title('Time Profiling of Blocks', fontdict=font_tlt)
            self.ax2.grid()

    def plotting(self):
        plt.show()

    def all_plot(self):
        self.fig_all = plt.figure(figsize=(11, 7.5))
        
        fig_def_present = 1
        fig1_present = 1
        fig2_present = 1
        
        # Check the presence of all self.figures
        try:
            self.fig_def
        except AttributeError:
            fig_def_present = 0
        
        try:
            self.fig1
        except AttributeError:
            fig1_present = 0
        
        try:
            self.fig2
        except AttributeError:
            fig2_present = 0

        if fig_def_present + fig1_present + fig2_present == 3:
            gs = self.fig_all.add_gridspec(nrows=2, ncols=2)

        else:
            gs = self.fig_all.add_gridspec(nrows=1, ncols=2)

        # Run the self.figures
        try:
            self.fig_def
        except AttributeError:
            pass

        else:
            self.ax.figure = self.fig_all
            self.fig_all.axes.append(self.ax)
            self.fig_all.add_axes(self.ax)
            self.ax.set_facecolor(self.color_plot)

            if fig1_present + fig2_present == 2:
                dummy1 = self.fig_all.add_subplot(gs[:, 1])
                pos1_all = dummy1.get_position()
                pos2_all = [pos1_all.x0 + 0.14, pos1_all.y0, pos1_all.width / 0.49, pos1_all.height / 1.05]
                self.ax.set_position(pos2_all)

            else:
                dummy1 = self.fig_all.add_subplot(gs[0, 0])
                pos1 = dummy1.get_position()
                pos2 = [pos1.x0, pos1.y0, pos1.width/0.49, pos1.height / 1.05]
                self.ax.set_position(pos2)

            dummy1.remove()
            plt.close(self.fig_def)

        try:
            self.fig1
        except AttributeError:
            pass

        else:
            self.ax1.figure = self.fig_all
            self.fig_all.axes.append(self.ax1)
            self.fig_all.add_axes(self.ax1)
            self.ax1.set_facecolor(self.color_loop)

            if fig_def_present + fig2_present == 2:
                dummy2 = self.fig_all.add_subplot(gs[1, 0])
                post1_all = dummy2.get_position()
                post2_all = [post1_all.x0 - 0.02, post1_all.y0 - 0.04, post1_all.width / 0.8, post1_all.height / 1.1]
                self.ax1.set_position(post2_all)

            else:
                if fig_def_present:
                    dummy2 = self.fig_all.add_subplot(gs[0, 1])
                    post1 = dummy2.get_position()
                    post2 = [post1.x0 + 0.425, post1.y0, post1.width / 0.5, post1.height / 1.1]
                    self.ax1.set_position(post2)

                else:
                    dummy2 = self.fig_all.add_subplot(gs[0, 0])
                    post1 = dummy2.get_position()
                    post2 = [post1.x0, post1.y0, post1.width / 0.5, post1.height / 1.1]
                    self.ax1.set_position(post2)

            dummy2.remove()
            plt.close(self.fig1)

        try:
            self.fig2
        except AttributeError:
            pass

        else:
            self.ax2.figure = self.fig_all
            self.fig_all.axes.append(self.ax2)
            self.fig_all.add_axes(self.ax2)

            if fig_def_present + fig1_present == 2:
                dummy3 = self.fig_all.add_subplot(gs[0, 0])
                posts1_all = dummy3.get_position()
                posts2_all = [posts1_all.x0 - 0.02, posts1_all.y0 , posts1_all.width / 0.8, posts1_all.height / 1.1]
                self.ax2.set_position(posts2_all)

            else:
                dummy3 = self.fig_all.add_subplot(gs[0, 1])
                posts1 = dummy3.get_position()
                posts2 = [posts1.x0 + 0.425, posts1.y0, posts1.width / 0.5, posts1.height / 1.1]
                self.ax2.set_position(posts2)

            dummy3.remove()
            plt.close(self.fig2)

        plt.show()


class memory_plot:

    def __init__(self, codes, repeat):
        self.codes = codes
        self.repeat = repeat
        self.color_plot = 'White'
        self.color_loop = 'White'

    # Plotting all the timings in various runs
    def plot(self):
        self.fig_def, self.ax = plt.subplots(figsize=(9, 7))
        val = input('Type y to set colors for Memory plot otherwise Enter: ')
        back_color = {}

        # Look of all the Codes given in list format
        for seq, code in enumerate(self.codes):
            code = re.sub('</', '', code)
            code = re.sub('/>', '', code)
            Memory = []
            for empt in range(self.repeat):
                tracemalloc.start()
                exec(code)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                Memory.append(current/10**3)

            x = np.arange(self.repeat)
            y = np.array(Memory)
            Y = [np.mean(Memory)] * self.repeat
            if val == 'y':
                color = input('Enter the color:')
                self.ax.plot(x, y, color=color, label='Code ' + str(seq + 1))
                self.ax.plot(x, Y, color=color, linestyle=':')
                back_color[np.mean(Memory)] = adjust_color(color)  # Here we use a dictionary to store color

            else:
                self.axis = self.ax.plot(x, y, label='Code ' + str(seq + 1))
                self.ax.plot(x, Y, color=self.axis[0].get_color(), linestyle=':')
                back_color[np.mean(Memory)] = adjust_color(self.axis[0].get_color())

        else:
            self.ax.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax.set_xlabel('Execution of Codes', fontdict=font)
            self.ax.set_ylabel('Memory Usage (in KB)', fontdict=font)
            self.ax.set_title('Memory Usage Profile', fontdict=font_tlt)
            self.ax.grid()

            self.color_plot = back_color[min(back_color.keys())]

    # Works to plot the running time of
    def loop_complex(self):

        self.fig1, self.ax1 = plt.subplots(figsize=(9, 7))
        back_color = {}
        val = input('Type y to set colors to Memory loop complex otherwise Enter: ')
        for i, code in enumerate(self.codes):

            Times = np.zeros(1, dtype='int64')
            for repeat in range(self.repeat):

                pattern = '</[^>]+/>'
                info = re.sub(pattern, '', code)
                spt = info.split('\n') + ['</', '/>']
                loop = code
                for splits in spt:
                    loop = loop.replace(splits, '')

                exec(info)
                Memory = []

                exec('''tracemalloc.start() ;''' + loop + '''; current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop();'''
                     + '''Memory.append(current/10**3)''')

                Times = np.add(Times, Memory)
            Times = Times / self.repeat

            x = np.arange(len(Times))
            y = np.array(Times)
            if val == 'y':
                color = input('Enter the color:')
                self.ax1.plot(x, y, color=color, label='Loop ' + str(i + 1))
                back_color[np.mean(y)] = adjust_color(color)

            else:
                self.axis1 = self.ax1.plot(x, y, label='Loop ' + str(i + 1))
                back_color[np.mean(y)] = adjust_color(self.axis1[0].get_color())

        else:
            self.ax1.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax1.set_xlabel('Number of loop in execution', fontdict=font)
            self.ax1.set_ylabel('Memory Usage (in KB)', fontdict=font)
            self.ax1.set_title('Memory Usage of Loops', fontdict=font_tlt)
            self.ax1.grid()

            self.color_loop = back_color[min(back_color.keys())]

    def block_prof(self, deep=False):
        self.fig2, self.ax2 = plt.subplots(figsize=(9, 7))
        val = input('Type y to set colors for Memory block profiling otherwise Enter: ')

        Data = []
        for code in self.codes:

            code = re.sub('</', '', code)
            code = re.sub('/>', '', code)
            Times = np.zeros(1, dtype='int64')
            for rep in range(self.repeat):
                if deep:
                    pattern = r'\n(?![ \t]{3,})'
                else:
                    pattern = r'\n(?![ \t]+)'
                blocks = re.split(pattern, code)
                while '' in blocks: blocks.remove('')
                Memory = []

                for i in blocks:
                    tracemalloc.start()
                    exec(i)
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    Memory.append(current/10**3)
                Times = np.add(Times, Memory)
            Times = Times / self.repeat
            Data.append(Times)

        # Data Plotting
        barwidth = 1 / (len(Data) + 1)

        for bars in range(len(Data)):

            bar = np.arange(0, len(Data[0]), 1)
            bar = bar + (barwidth * bars)
            if val == 'y':
                color = input('Enter the color:')
                self.ax2.bar(bar, Data[bars], width=barwidth, label='Code ' + str(bars + 1), color=color)
            else:
                self.ax2.bar(bar, Data[bars], width=barwidth, label='Code ' + str(bars + 1))

        else:
            self.ax2.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            self.ax2.set_xlabel('Blocks Memory Analysis', fontdict=font)
            self.ax2.set_ylabel('Memory Usage (in KB)', fontdict=font)
            plt.xticks([t + barwidth * (len(Data) - 1) / 2 for t in range(len(Data[0]))],
                       ['Block' + str(i + 1) for i in range(len(Data[0]))])
            self.ax2.set_title('Memory Profiling of Blocks', fontdict=font_tlt)
            self.ax2.grid()

    def plotting(self):
        plt.show()

    def all_plot(self):
        self.fig_all = plt.figure(figsize=(11, 7.5))

        fig_def_present = 1
        fig1_present = 1
        fig2_present = 1

        # Check the presence of all self.figures
        try:
            self.fig_def
        except AttributeError:
            fig_def_present = 0

        try:
            self.fig1
        except AttributeError:
            fig1_present = 0

        try:
            self.fig2
        except AttributeError:
            fig2_present = 0

        if fig_def_present + fig1_present + fig2_present == 3:
            gs = self.fig_all.add_gridspec(nrows=2, ncols=2)

        else:
            gs = self.fig_all.add_gridspec(nrows=1, ncols=2)

        # Run the self.figures
        try:
            self.fig_def
        except AttributeError:
            pass

        else:
            self.ax.figure = self.fig_all
            self.fig_all.axes.append(self.ax)
            self.fig_all.add_axes(self.ax)
            self.ax.set_facecolor(self.color_plot)

            if fig1_present + fig2_present == 2:
                dummy1 = self.fig_all.add_subplot(gs[:, 1])
                pos1_all = dummy1.get_position()
                pos2_all = [pos1_all.x0 + 0.14, pos1_all.y0, pos1_all.width / 0.49, pos1_all.height / 1.05]
                self.ax.set_position(pos2_all)

            else:
                dummy1 = self.fig_all.add_subplot(gs[0, 0])
                pos1 = dummy1.get_position()
                pos2 = [pos1.x0, pos1.y0, pos1.width / 0.49, pos1.height / 1.05]
                self.ax.set_position(pos2)

            dummy1.remove()
            plt.close(self.fig_def)

        try:
            self.fig1
        except AttributeError:
            pass

        else:
            self.ax1.figure = self.fig_all
            self.fig_all.axes.append(self.ax1)
            self.fig_all.add_axes(self.ax1)
            self.ax1.set_facecolor(self.color_loop)

            if fig_def_present + fig2_present == 2:
                dummy2 = self.fig_all.add_subplot(gs[1, 0])
                post1_all = dummy2.get_position()
                post2_all = [post1_all.x0 - 0.02, post1_all.y0 - 0.04, post1_all.width / 0.8, post1_all.height / 1.1]
                self.ax1.set_position(post2_all)

            else:
                if fig_def_present:
                    dummy2 = self.fig_all.add_subplot(gs[0, 1])
                    post1 = dummy2.get_position()
                    post2 = [post1.x0 + 0.425, post1.y0, post1.width / 0.5, post1.height / 1.1]
                    self.ax1.set_position(post2)

                else:
                    dummy2 = self.fig_all.add_subplot(gs[0, 0])
                    post1 = dummy2.get_position()
                    post2 = [post1.x0, post1.y0, post1.width / 0.5, post1.height / 1.1]
                    self.ax1.set_position(post2)

            dummy2.remove()
            plt.close(self.fig1)

        try:
            self.fig2
        except AttributeError:
            pass

        else:
            self.ax2.figure = self.fig_all
            self.fig_all.axes.append(self.ax2)
            self.fig_all.add_axes(self.ax2)

            if fig_def_present + fig1_present == 2:
                dummy3 = self.fig_all.add_subplot(gs[0, 0])
                posts1_all = dummy3.get_position()
                posts2_all = [posts1_all.x0 - 0.02, posts1_all.y0, posts1_all.width / 0.8, posts1_all.height / 1.1]
                self.ax2.set_position(posts2_all)

            else:
                dummy3 = self.fig_all.add_subplot(gs[0, 1])
                posts1 = dummy3.get_position()
                posts2 = [posts1.x0 + 0.425, posts1.y0, posts1.width / 0.5, posts1.height / 1.1]
                self.ax2.set_position(posts2)

            dummy3.remove()
            plt.close(self.fig2)

        plt.show()
