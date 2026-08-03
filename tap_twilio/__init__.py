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


class _SuppressSingerMetricsFilter(logging.Filter):
    """Drop singer METRIC lines (HTTP timers, record counters) unless DEBUG is enabled.

    Demoting levelno to DEBUG is unreliable under Meltano: the extractor stderr is
    captured and re-logged at INFO with the original message text still visible.
    Returning False removes the lines at the source.
    """

    def filter(self, record):
        try:
            message = record.getMessage()
        except Exception:  # pylint: disable=broad-except
            return True
        if not message.startswith('METRIC:'):
            return True
        # Keep metrics only when the singer logger (or root) is at DEBUG.
        singer_logger = logging.getLogger('singer')
        return singer_logger.isEnabledFor(logging.DEBUG) or logging.getLogger().isEnabledFor(logging.DEBUG)


def _configure_quiet_metrics():
    singer_logger = logging.getLogger('singer')
    # Replace any previous demote-only filter from earlier quieter-logging work.
    singer_logger.filters = [
        f for f in singer_logger.filters if not f.__class__.__name__.endswith('MetricToDebugFilter')
        and not isinstance(f, _SuppressSingerMetricsFilter)
    ]
    singer_logger.addFilter(_SuppressSingerMetricsFilter())


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
