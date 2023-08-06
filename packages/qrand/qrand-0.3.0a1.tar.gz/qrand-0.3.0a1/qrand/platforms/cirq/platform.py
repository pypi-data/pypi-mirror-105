##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 13, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from typing import Tuple

from ..circuit import QuantumCircuit
from ..job import QuantumJob
from ..platform import QuantumPlatform, QuantumProtocol


###############################################################################
## CIRQ PLATFORM
###############################################################################
class CirqPlatform(QuantumPlatform):
    def __init__(self) -> None:
        self.ERROR_MSG = f"{self.__class__.__name__}"  # TODO
        raise NotImplementedError(self.ERROR_MSG)

    ############################### PUBLIC API ###############################
    @property
    def job_partition(self) -> Tuple[int, int]:
        raise NotImplementedError(self.ERROR_MSG)

    @property
    def max_bits_per_request_allowed(self) -> int:
        raise NotImplementedError(self.ERROR_MSG)

    def create_circuit(self, num_qubits: int) -> QuantumCircuit:
        raise NotImplementedError(self.ERROR_MSG)

    def create_job(
        self, circuit: QuantumCircuit, num_measurements: int
    ) -> QuantumJob:
        raise NotImplementedError(self.ERROR_MSG)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        raise NotImplementedError(self.ERROR_MSG)
