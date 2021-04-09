"""
This file is part of the opendrive-beamng project.

--------------------------------------------------------------------------------

Deals with logging, atm only to the console

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

class Log:
    @staticmethod
    def info(msg: str) -> None:
        print(f"opendrive::INFO::{msg}")

    @staticmethod
    def done(msg: str) -> None:
        print(f"\u001b[32mopendrive::DONE::{msg}\u001b[0m")

    @staticmethod
    def warn(msg: str) -> None:
        print(f"\u001b[33mopendrive::WARN::{msg}\u001b[0m")

    @staticmethod
    def fail(msg: str, fatal: bool) -> None:
        print(f"\u001b[31mopendrive::FAIL::{msg}\u001b[0m")
        if fatal:
            import sys
            sys.exit(1)
