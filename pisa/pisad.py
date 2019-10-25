from getopt import getopt
from sys import argv, exit
from signal import signal, SIGINT, SIGQUIT, SIGTERM

from pisa.conf import DB_PATH
from pisa.logger import Logger
from pisa.api import start_api
from pisa.watcher import Watcher
from pisa.builder import Builder
from pisa.conf import BTC_NETWORK
from pisa.responder import Responder
from pisa.db_manager import DBManager
from pisa.tools import can_connect_to_bitcoind, in_correct_network

logger = Logger("Daemon")


def handle_signals(signal_received, frame):
    logger.info("Shutting down PISA")
    # TODO: #11-add-graceful-shutdown: add code to close the db, free any resources, etc.

    exit(0)


if __name__ == '__main__':
    logger.info("Starting PISA")

    signal(SIGINT, handle_signals)
    signal(SIGTERM, handle_signals)
    signal(SIGQUIT, handle_signals)

    opts, _ = getopt(argv[1:], '', [''])
    for opt, arg in opts:
        # FIXME: Leaving this here for future option/arguments
        pass

    if not can_connect_to_bitcoind():
        logger.error("Can't connect to bitcoind. Shutting down")

    elif not in_correct_network(BTC_NETWORK):
        logger.error("bitcoind is running on a different network, check conf.py and bitcoin.conf. Shutting down")

    else:
        try:
            db_manager = DBManager(DB_PATH)

            watcher_appointments_data = db_manager.load_watcher_appointments()
            responder_jobs_data = db_manager.load_responder_jobs()

            watcher = Watcher(db_manager)

            if len(watcher_appointments_data) == 0 and len(responder_jobs_data) == 0:
                logger.info("Fresh bootstrap")

            else:
                logger.info("Bootstrapping from backed up data")
                responder = Responder(db_manager)
                responder.jobs, responder.tx_job_map = Builder.build_jobs(responder_jobs_data)

                watcher.responder = responder
                watcher.appointments, watcher.locator_uuid_map = Builder.build_appointments(watcher_appointments_data)

            # Create an instance of the Watcher and fire the API
            start_api(watcher)

        except Exception as e:
            logger.error("An error occurred: {}. Shutting down".format(e))
            exit(1)

