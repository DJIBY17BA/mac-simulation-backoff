class Station:
    def __init__(self, station_id, K):
        self.id = station_id
        self.K = K

        self.queue = 0
        self.state = 1

        self.transmitting = False
        self.try_scheduled = False
        self.current_tx_id = 0