from station import Station
from event import Event, ARRIVE, TRY, FINISH

s = Station(0, K=5)

print("Station :", s.id)
print("File :", s.queue)
print("Etat :", s.state)

e = Event(2.5, ARRIVE, 0)

print("Event :", e)