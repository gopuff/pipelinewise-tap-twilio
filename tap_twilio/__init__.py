#!/usr/bin/env python3

import logging
import sys
import json
import argparse
import singer
from singer import metadata, utils
from tap_twilio.client import TwilioClient
from tap_twilio.discover import discover
from tap_twilio.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
    'account_sid',
    'auth_token',
    'start_date',
    'user_agent'
]


class _SingerMetricToDebugFilter(logging.Filter):
    """Demote singer METRIC lines (HTTP timers, record counters) from INFO to DEBUG."""

    def filter(self, record):
        try:
            message = record.getMessage()
        except Exception:  # pylint: disable=broad-except
            return True
        if message.startswith('METRIC:'):
            record.levelno = logging.DEBUG
            record.levelname = 'DEBUG'
        return True


def _configure_quiet_metrics():
    singer_logger = logging.getLogger('singer')
    if not any(isinstance(f, _SingerMetricToDebugFilter) for f in singer_logger.filters):
        singer_logger.addFilter(_SingerMetricToDebugFilter())


def do_discover():
    LOGGER.info('Starting discover')
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info('Finished discover')


@singer.utils.handle_top_exception(LOGGER)
def main():
    _configure_quiet_metrics()

    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    with TwilioClient(parsed_args.config['account_sid'],
                      parsed_args.config['auth_token'],
                      parsed_args.config['user_agent']) as client:

        state = {}
        if parsed_args.state:
            state = parsed_args.state

        config = parsed_args.config
        if parsed_args.discover:
            do_discover()
        elif parsed_args.catalog:
            sync(client=client,
                 config=config,
                 catalog=parsed_args.catalog,
                 state=state)

if __name__ == '__main__':
    main()
