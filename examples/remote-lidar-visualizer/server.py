"""
  This file is ran on the VM. Make sure to set BNG_HOME!
"""

import socket
import pickle
import time
from datetime import datetime

from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Lidar


class Server:
    def __init__(self, host: str = None, port: str = None) -> None:
        print("INFO::Init")

        self.HOST = '' if host is None else host
        self.PORT = 6555 if port is None else port

        self.scenario_map = 'west_coast_usa'
        self.scenario_name = 'LIDAR Testing'
        self.scenario_desc = 'No description'

        self.vehicle_name = 'ego_vehicle'
        self.vehicle_model = 'etk800'
        self.vehicle_license = 'LIDAR'
        self.vehicle_pos = (-717.121, 101, 118.675)
        self.vehicle_rot = None
        self.vehicle_rot_quat = (0, 0, 0.3826834, 0.9238795)

        print("INFO::Starting & Initializing BeamNG")
        self.beamng = BeamNGpy('localhost', 64256)  # Using BNG_HOME env var
        self.beamng.open(launch=True)
        print("INFO::Connection successful")
        self._init_beamNG()
        print("DONE::Starting & Initializing BeamNG")

    def _init_beamNG(self) -> None:
        self.scenario = Scenario(
            self.scenario_map, self.scenario_name, description=self.scenario_desc
        )

        self.vehicle = Vehicle(
            self.vehicle_name, model=self.vehicle_model, license=self.vehicle_license
        )
        self.lidar_sensor = Lidar()
        self.vehicle.attach_sensor('lidar', self.lidar_sensor)

        self.scenario.add_vehicle(
            self.vehicle, self.vehicle_pos, self.vehicle_rot, self.vehicle_rot_quat
        )
        self.scenario.make(self.beamng)

        self.beamng.load_scenario(self.scenario)

    def start_socket(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()

            print(f"INFO::Socket ready")

            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        print("INFO::New connection ", addr)
                        while conn:
                            try:
                                self.vehicle.poll_sensors()
                            except AssertionError:
                                print("WARN::AssertionError @ poll_sensors()")

                            self._points = self.lidar_sensor.data['points']
                            self._packet = [self._points, self.vehicle.state]
                            conn.sendall(pickle.dumps(self._packet))
                            print("INFO::Sent data! @ ", datetime.now())
                            time.sleep(0.5)
                except ConnectionResetError:
                    print("WARN::Lost connection")

# ==== Main ====
            
def main():
    server = Server()
    server.start_socket()
    
if __name__ == '__main__':
    main()
