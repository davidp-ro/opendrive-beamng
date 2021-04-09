"""
This file is part of the opendrive-beamng project.

--------------------------------------------------------------------------------

Files in the server folder are meant to be run well... on the 'server', in my
case just a VM.

Why not just run beamNG on the main machine?
    Well, I (and it seems quite a lot of people) ran into a problem where the 
  sim crashes when `vehicle.poll_sensors()` is called on AMD (GPU) systems, so
  by running in a VM I avoid said issue.

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

from .server import Server

# ==== Main ====
            
def main():
    options = {
        'scenario_map' : 'smallgrid', # west_coast_usa
        'scenario_name' : 'LIDAR Testing',
        'scenario_desc' : 'No description',

        'vehicle_name' : 'ego_vehicle',
        'vehicle_model' : 'etk800',
        'vehicle_license' : 'LIDAR',
        'vehicle_pos' : (1, 1, 1), # -717.121, 101, 118.675
        'vehicle_rot' : None,
        'vehicle_rot_quat' : (0, 0, 0.3826834, 0.9238795),

        'f_cam_pos' : (-0.3, 1, 1.0),
        'f_cam_dir' : (0, 1, 0),
        'f_cam_fov' : 65,
        'f_cam_res' : (852, 480),
    }

    server = Server(options)
    server.start_socket()
    
if __name__ == '__main__':
    main()