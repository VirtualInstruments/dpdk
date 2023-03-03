# SPDX-License-Identifier: BSD-3-Clause
# Copyright(c) 2010-2014 Intel Corporation
# Copyright(c) 2022-2023 PANTHEON.tech s.r.o.
# Copyright(c) 2022-2023 University of New Hampshire

"""
A node is a generic host that DTS connects to and manages.
"""

from framework.config import (
    BuildTargetConfiguration,
    ExecutionConfiguration,
    NodeConfiguration,
)
from framework.logger import DTSLOG, getLogger
from framework.remote_session import OSSession, create_session


class Node(object):
    """
    Basic class for node management. This class implements methods that
    manage a node, such as information gathering (of CPU/PCI/NIC) and
    environment setup.
    """

    main_session: OSSession
    config: NodeConfiguration
    name: str
    _logger: DTSLOG
    _other_sessions: list[OSSession]

    def __init__(self, node_config: NodeConfiguration):
        self.config = node_config
        self.name = node_config.name
        self._logger = getLogger(self.name)
        self.main_session = create_session(self.config, self.name, self._logger)

        self._other_sessions = []

        self._logger.info(f"Created node: {self.name}")

    def set_up_execution(self, execution_config: ExecutionConfiguration) -> None:
        """
        Perform the execution setup that will be done for each execution
        this node is part of.
        """
        self._set_up_execution(execution_config)

    def _set_up_execution(self, execution_config: ExecutionConfiguration) -> None:
        """
        This method exists to be optionally overwritten by derived classes and
        is not decorated so that the derived class doesn't have to use the decorator.
        """

    def tear_down_execution(self) -> None:
        """
        Perform the execution teardown that will be done after each execution
        this node is part of concludes.
        """
        self._tear_down_execution()

    def _tear_down_execution(self) -> None:
        """
        This method exists to be optionally overwritten by derived classes and
        is not decorated so that the derived class doesn't have to use the decorator.
        """

    def set_up_build_target(
        self, build_target_config: BuildTargetConfiguration
    ) -> None:
        """
        Perform the build target setup that will be done for each build target
        tested on this node.
        """
        self._set_up_build_target(build_target_config)

    def _set_up_build_target(
        self, build_target_config: BuildTargetConfiguration
    ) -> None:
        """
        This method exists to be optionally overwritten by derived classes and
        is not decorated so that the derived class doesn't have to use the decorator.
        """

    def tear_down_build_target(self) -> None:
        """
        Perform the build target teardown that will be done after each build target
        tested on this node.
        """
        self._tear_down_build_target()

    def _tear_down_build_target(self) -> None:
        """
        This method exists to be optionally overwritten by derived classes and
        is not decorated so that the derived class doesn't have to use the decorator.
        """

    def create_session(self, name: str) -> OSSession:
        """
        Create and return a new OSSession tailored to the remote OS.
        """
        session_name = f"{self.name} {name}"
        connection = create_session(
            self.config,
            session_name,
            getLogger(session_name, node=self.name),
        )
        self._other_sessions.append(connection)
        return connection

    def close(self) -> None:
        """
        Close all connections and free other resources.
        """
        if self.main_session:
            self.main_session.close()
        for session in self._other_sessions:
            session.close()
        self._logger.logger_exit()
