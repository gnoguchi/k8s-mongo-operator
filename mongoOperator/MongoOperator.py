# Copyright (c) 2018 Ultimaker
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from time import sleep

from mongoOperator.ClusterManager import ClusterManager


class MongoOperator:
    """
    The Mongo operator manages MongoDB replica sets and backups in a Kubernetes cluster.
    """

    def __init__(self, sleep_per_run: float = 5.0) -> None:
        """
        :param sleep_per_run: How many seconds we should sleep after each run.
        """
        self._sleep_per_run = sleep_per_run

    def run_forever(self) -> None:
        """
        Runs the mongo operator forever (until a kill command is received).
        """
        checker = ClusterManager()
        try:
            while True:
                logging.info("**** Running Cluster Check ****")
                try:
                    checker.checkExistingClusters()
                    checker.collectGarbage()
                except Exception as global_exception:
                    logging.exception(global_exception)
                    raise
                logging.info("Checks done, waiting %s seconds", self._sleep_per_run)
                sleep(self._sleep_per_run)
        except KeyboardInterrupt:
            logging.info("Application interrupted...")
        logging.info("Done running operator")
