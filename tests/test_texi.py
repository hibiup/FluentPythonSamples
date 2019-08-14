import random
import collections
import queue
import argparse
import time

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time texi_id action')


# BEGIN TAXI_PROCESS
def taxi_process(texi_id, trips, start_time=0):
    # text_process 首先返回包含发车时间 (start_time) 的 Event 以便主程序打印信息
    # 然后停留在这里等待主程序的下一次调用(send)，当主程序再次调用此协程时同时输入一个 time 参数表示接到客人的时间。
    time = yield Event(start_time, texi_id, 'leave garage')

    for i in range(trips):
        # 协程首先返回包含客人的时间的事件给主程序以打印出接客信息，然后挂起等待下一个（卸客）事件
        # 当主程序再次回到这里的时候（卸客）同样会传入一个时戳，协程将它记为 drop_time
        drop_time = yield Event(time, texi_id, 'pick up passenger')

        # 协程返回下车事件（包含 drop_time)以便主程序打印信息，然后再次挂起等待下一事件。
        # 收到下一事件的时间戳，覆盖 time，然后回到循环的开头，循环的开头如果认为今天的任务全部结束了，那么结束循环，否则该 time 被认为是再一次接到客人的时间．
        time = yield Event(drop_time, texi_id, 'drop off passenger')  # <5>

    # 如果循环结束，那么最后一个时间戳被作为是放工时间．生成并返回放工事件
    yield Event(time, texi_id, 'going home')  # <6>
    # end of taxi process # <7>
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:
    def __init__(self, texis_map):
        self.events = queue.PriorityQueue()  # PriorityQueue 取值的时候会自动按最小优先排序取值
        self.texis = dict(texis_map)

    def run(self, end_time):  # <1>
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
        for _, proc in sorted(self.texis.items()):  # <2>
            first_event = next(proc)  # <3>
            self.events.put(first_event)  # <4>

        '''
        循环从 PriorityQueue 中取得需要最优先处理的协程（根据 time 排序），然后计算并 send() 下一个随机时间. 循环直到处理完全部事件。
        '''
        sim_time = 0  # <5>
        while sim_time < end_time:  # <6>
            if self.events.empty():  # <7>
                print('*** end of events ***')
                break

            current_event = self.events.get()  # <8>
            sim_time, texi_id, previous_action = current_event  # <9>
            print('taxi:', texi_id, texi_id * '   ', current_event)  # <10>
            active_proc = self.texis[texi_id]  # <11>
            next_time = sim_time + compute_duration(previous_action)  # <12>
            try:
                next_event = active_proc.send(next_time)  # <13>
            except StopIteration:
                del self.texis[texi_id]  # <14>
            else:
                self.events.put(next_event)  # <15>
        else:  # <16>
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR


# 辅助函数. 计算下一次事件的时间
def compute_duration(previous_action):
    if previous_action in ['leave garage', 'drop off passenger']:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    # 产生随机时间间隔
    return int(random.expovariate(1/interval)) + 1


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')

    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)