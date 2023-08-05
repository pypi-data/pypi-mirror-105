"""A toolbox for parsing potentially corrupted photodiode events."""

__version__ = 'v0.6dev0'


from pd_parser.parse_pd import (find_pd_params, parse_pd, parse_audio, # noqa
                                add_pd_off_events, add_relative_events,  # noqa
                                add_events_to_raw, pd_parser_save_to_bids,
                                simulate_pd_data)  # noqa
