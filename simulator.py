import heapq
import random

from event import Event, ARRIVE, TRY, FINISH
from station import Station


class Simulator:
    def __init__(self, N, K, lambd, tau, T_max, i_max=10):
        self.N = N
        self.K = K
        self.lambd = lambd
        self.tau = tau
        self.T_max = T_max
        self.i_max = i_max

        self.time = 0.0
        self.events = []
        self.stations = [Station(i, K) for i in range(N)]

        self.channel_busy = False
        self.current_station_id = None
        self.tx_counter = 0

        self.success_packets = 0
        self.lost_packets = 0
        self.total_arrivals = 0

        self.times = []
        self.throughputs = []
        self.mean_clients_history = []
        self.loss_rates = []

    def add_event(self, event):
        heapq.heappush(self.events, event)

    def schedule_arrive(self, station_id):
        delay = random.expovariate(self.lambd)
        self.add_event(Event(self.time + delay, ARRIVE, station_id))

    def init_events(self):
        for station in self.stations:
            self.schedule_arrive(station.id)

    def total_clients(self):
        return sum(station.queue for station in self.stations)

    def record_stats(self):
        if self.time > 0:
            self.times.append(self.time)
            self.throughputs.append(self.success_packets / self.time)
            self.mean_clients_history.append(self.total_clients() / self.N)
            self.loss_rates.append(
                self.lost_packets / self.total_arrivals if self.total_arrivals > 0 else 0
            )

    def schedule_backoff(self, station):
        if station.state >= self.i_max:
            if station.queue > 0:
                station.queue -= 1
            self.lost_packets += 1
            station.state = 1
            station.try_scheduled = False
            station.transmitting = False
            station.current_tx_id = 0
            return

        mean_backoff = (2 ** station.state) * self.tau
        delay = random.expovariate(1 / mean_backoff)

        station.state += 1
        station.try_scheduled = True
        station.transmitting = False
        station.current_tx_id = 0

        self.add_event(Event(self.time + delay, TRY, station.id))

    def handle_arrive(self, event):
        station = self.stations[event.station_id]

        self.total_arrivals += 1
        self.schedule_arrive(station.id)

        if station.queue >= station.K:
            self.lost_packets += 1
            return

        station.queue += 1

        if not station.try_scheduled and not station.transmitting:
            station.try_scheduled = True
            self.add_event(Event(self.time, TRY, station.id))

    def handle_try(self, event):
        station = self.stations[event.station_id]
        station.try_scheduled = False

        if station.queue == 0 or station.transmitting:
            return

        if not self.channel_busy:
            self.channel_busy = True
            self.current_station_id = station.id

            self.tx_counter += 1
            station.current_tx_id = self.tx_counter
            station.transmitting = True

            self.add_event(Event(self.time + 1, FINISH, station.id, station.current_tx_id))

        else:
            # Collision : la station déjà en transmission et la nouvelle station échouent toutes les deux.
            old_station = self.stations[self.current_station_id]

            old_station.transmitting = False
            old_station.current_tx_id = 0

            self.channel_busy = False
            self.current_station_id = None

            self.schedule_backoff(old_station)
            self.schedule_backoff(station)

    def handle_finish(self, event):
        station = self.stations[event.station_id]

        # Ignore les anciens FINISH après collision.
        if not station.transmitting:
            return

        if event.tx_id != station.current_tx_id:
            return

        self.channel_busy = False
        self.current_station_id = None

        station.transmitting = False
        station.current_tx_id = 0

        if station.queue > 0:
            station.queue -= 1
            station.state = 1
            self.success_packets += 1

        if station.queue > 0 and not station.try_scheduled:
            station.try_scheduled = True
            self.add_event(Event(self.time, TRY, station.id))

    def run(self):
        self.init_events()

        while self.events:
            event = heapq.heappop(self.events)

            if event.time > self.T_max:
                break

            self.time = event.time

            if event.event_type == ARRIVE:
                self.handle_arrive(event)

            elif event.event_type == TRY:
                self.handle_try(event)

            elif event.event_type == FINISH:
                self.handle_finish(event)

            self.record_stats()

        return {
            "time": self.time,
            "success_packets": self.success_packets,
            "lost_packets": self.lost_packets,
            "total_arrivals": self.total_arrivals,
            "throughput": self.success_packets / self.time if self.time > 0 else 0,
            "loss_rate": self.lost_packets / self.total_arrivals if self.total_arrivals > 0 else 0,
            "times": self.times,
            "throughputs": self.throughputs,
            "mean_clients_history": self.mean_clients_history,
            "loss_rates": self.loss_rates,
        }