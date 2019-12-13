#  Copyright (c) 2018 Sony Pictures Imageworks Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""
Project: opencue Library

Module: render_partition.py - opencue Library implementation of a render_partition

"""

from opencue import Cuebot
from opencue.compiled_proto import renderPartition_pb2


class RenderPartition(object):
    def __init__(self, render_partition=None):
        """Host class initialization"""
        self.data = render_partition
        self.stub = Cuebot.getStub('renderPartition')


    def setMaxResources(self, cores, memory, gpu):
        return self.stub.SetMaxResources(
            renderPartition_pb2.RenderPartSetMaxResourcesRequest(
                render_partition=self.data,
                cores=cores,
                memory=memory,
                gpu=gpu)) 

    @property
    def job(self):
        """Returns the job of the render_partition
        @rtype: str
        @return: job
        """
        if not hasattr(self, "__job"):
            self.__job = self.data.job
        return self.__job

    def delete(self):
        """Delete the render_partition from the cuebot"""
        self.stub.Delete(renderPartition_pb2.RenderPartDeleteRequest(render_partition=self.data), timeout=Cuebot.Timeout)