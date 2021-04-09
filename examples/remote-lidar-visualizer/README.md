# Remote LIDAR Visualizer using sockets

This is an example of how to use beamNGpy remotely

---

### Why?

I (and it seems quite a lot of people) ran into a problem where the sim crashes when `vehicle.poll_sensors()` is called on AMD (GPU) systems

### How to use?

- Install dependencies (`beamngpy`, `opengl`)

- Server:
  - Set `BNG_HOME` env variable to beamNG.tech path
  - If you need, change the port the server listens on
  - `python server.py`

- Client:
  - Set the `SERVER` variable to the server's IP Address
  - `python client.py`


#### Note: 
I tested this with beamNG.tech, I'm not sure if there's any differences with beamNG.research
