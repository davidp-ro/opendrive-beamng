"""
This file is part of the opendrive-beamng project.

--------------------------------------------------------------------------------

Server class - deals with initialization, configuring of the environment, sim
launch and socket comms.

Notes:
    - Set `BNG_HOME` env variable to beamNG.tech path

TODO:
    - Switch to select / non-blocking

--------------------------------------------------------------------------------

Copyright 2021 David Pescariu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__version__ = '1.0.0'

import socket
import pickle
import time

from datetime import datetime
from typing import Dict

from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Lidar, Camera

from ..utils.logger import Log


class Server:
    def __init__(self, options: Dict[str, str], host: str = '', port: int = 6555) -> None:
        """
        Initialize the Server

        Args:
            options (Dict[str, str]): Options / Characteristics used to construct 
            the vehicle, scenario, and different sensors
            host (str, optional): IP/Hostname that the server listens for, defaults 
            to '' - loopback / all.
            port (int, optional): Port that the server listens for, defaults to 6555.
        """
        Log.info("Init")

        self.HOST = host
        self.PORT = port

        self.OPTIONS = options

        Log.info("Starting & Initializing BeamNG")
        self.beamng = BeamNGpy('localhost', 64256)  # Using BNG_HOME env var
        self.beamng.open(launch=True)
        Log.info("Connection successful")
        self._init_beamNG()
        Log.done("Starting & Initializing BeamNG")

    def _init_beamNG(self) -> None:
        """
        Initialize beamNG:
            Create the scenario, vehicle, sensors, and load everything
        """
        self.scenario = Scenario(
            self.OPTIONS['scenario_map'],
            self.OPTIONS['scenario_name'],
            description=self.OPTIONS['scenario_desc']
        )

        self.vehicle = Vehicle(
            self.OPTIONS['vehicle_name'],
            model=self.OPTIONS['vehicle_model'],
            license=self.OPTIONS['vehicle_license']
        )
        self.lidar_sensor = Lidar(max_dist=180, vres=24, vangle=25)
        self.vehicle.attach_sensor('lidar', self.lidar_sensor)

        self.front_camera = Camera(
            self.OPTIONS['f_cam_pos'],
            self.OPTIONS['f_cam_dir'],
            self.OPTIONS['f_cam_fov'],
            self.OPTIONS['f_cam_res'],
            colour=True, annotation=True
        )
        self.vehicle.attach_sensor('front_camera', self.front_camera)

        self.scenario.add_vehicle(
            self.vehicle,
            self.OPTIONS['vehicle_pos'],
            self.OPTIONS['vehicle_rot'],
            self.OPTIONS['vehicle_rot_quat']
        )
        self.scenario.make(self.beamng)

        self.beamng.load_scenario(self.scenario)

    def start_socket(self, send_delay: float = 0.369) -> None:
        """
        Initialize the socket and await (blocking) connections

        Args:
            send_delay (float, optional): How long to wait before sending a new
            packet. Defaults to 0.369.

        Packet data - List:
            [0]: vehicle_state
            [1]: lidar_data
            [2]: front_camera_data
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()

            Log.info("Socket ready")

            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        Log.done(f"New connection {addr}")
                        while conn:
                            self.vehicle.poll_sensors()

                            self._points = self.lidar_sensor.data['points']
                            self._camera = self.front_camera.data['colour']

                            self._packet = [
                                self.vehicle.state,
                                self._points,
                                self._camera
                            ]

                            conn.send(pickle.dumps(self._packet))
                            Log.info(f"Sent data! @ {datetime.now()}")
                            time.sleep(send_delay)
                except ConnectionResetError:
                    Log.warn("Lost connection")
                    if input('quit? (y/n)').find('y'):
                        break
