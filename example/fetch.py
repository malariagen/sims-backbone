import json
import os
import sys
import csv
import requests
import argparse
import urllib

import openapi_client


class Fetch():

    _auth_token = ''
    _api_client = None

    def __init__(self, config_file):
        # Configure OAuth2 access token for authorization: OauthSecurity
        auth_token = self.get_access_token(config_file)

        configuration = openapi_client.Configuration()
        if auth_token:
            configuration.access_token = auth_token

        configuration.host = self.remote_host_url

        self._api_client = openapi_client.ApiClient(configuration)

    def get_access_token(self, config_file):

        if not self._auth_token:
            with open(config_file) as json_file:
                args = json.load(json_file)
                token_url = args['token_url']
                self.remote_host_url = args['remote_host_url']
                headers = {'service': 'http://localhost/studies'}
                token_response = requests.get(token_url, args,
                                              headers=headers)
                if token_response.status_code == 401:
                    print('Auth failed')
                    sys.exit(1)
                auth_token = token_response.text.split('=')
                token = auth_token[1].split('&')[0]
                self._auth_token = token

        return self._auth_token

    def get_study_details(self):

        study_api = openapi_client.StudyApi(self._api_client)

        studies = study_api.download_studies()

        for study in studies.studies:
            print(repr(study))

    def get_sampling_event_details_by_study(self, study_code):

        sampling_event_api = openapi_client.SamplingEventApi(self._api_client)

        # start and count are not necessary for small result sets but you will need to use
        # them for larger results sets as the API will time out if you try and retrieve too many
        # Note that the first invocation is likely to take longer to respond
        fetched = sampling_event_api.download_sampling_events_by_study(
            study_code, start=0, count=0)

        # See also:
        #    download_sampling_events_by_study
        #    download_sampling_events_by_event_set
        #    download_sampling_events_by_location

        start = 0
        page_size = 100
        all_locations = {}
        all_sampling_events = {}

        while start < fetched.count:
            fetched = sampling_event_api.download_sampling_events_by_study(study_code,
                                                                           start=start,
                                                                           count=page_size)
            start += page_size
            z = {**all_locations, **fetched.locations}
            all_locations = z
            for event in fetched.sampling_events:
                if event.sampling_event_id in all_sampling_events:
                    print('Already seen it')
                all_sampling_events[event.sampling_event_id] = event

        return all_locations, all_sampling_events

    def get_original_samples_by_study(self, study_code):

        os_api = openapi_client.OriginalSampleApi(self._api_client)

        # start and count are not necessary for small result sets but you will need to use
        # them for larger results sets as the API will time out if you try and retrieve too many
        # Note that the first invocation is likely to take longer to respond
        fetched = os_api.download_original_samples_by_study(
            study_code, start=0, count=0)

        # See also:
        #    download_sampling_events_by_study
        #    download_sampling_events_by_event_set
        #    download_sampling_events_by_location

        start = 0
        page_size = 100
        all_original_samples = {}
        while start < fetched.count:
            fetched = os_api.download_original_samples_by_study(study_code,
                                                                start=start,
                                                                count=page_size)
            start += page_size
            for sample in fetched.original_samples:
                all_original_samples[sample.original_sample_id] = sample

        return all_original_samples

    def get_derivative_samples_by_study(self, study_code):

        ds_api = openapi_client.DerivativeSampleApi(self._api_client)

        # start and count are not necessary for small result sets but you will need to use
        # them for larger results sets as the API will time out if you try and retrieve too many
        # Note that the first invocation is likely to take longer to respond
        try:
            fetched = ds_api.download_derivative_samples_by_study(
                study_code, start=0, count=0)
        except openapi_client.rest.ApiException as api_e:
            if api_e.status == 404:
                return {}, {}
            else:
                print(api_e)
                return {}, {}

        # See also:
        #    download_sampling_events_by_study
        #    download_sampling_events_by_event_set
        #    download_sampling_events_by_location

        start = 0
        page_size = 100
        all_derivative_samples = {}
        derivative_sample_map = {}
        while start < fetched.count:
            fetched = ds_api.download_derivative_samples_by_study(study_code,
                                                                  start=start,
                                                                  count=page_size)
            start += page_size
            for sample in fetched.derivative_samples:
                all_derivative_samples[sample.derivative_sample_id] = sample
                if sample.original_sample_id in derivative_sample_map:
                    derivative_sample_map[sample.original_sample_id].append(
                        sample.derivative_sample_id)
                else:
                    derivative_sample_map[sample.original_sample_id] = [
                        sample.derivative_sample_id]

        return all_derivative_samples, derivative_sample_map

    def get_sampling_event_details_by_event_set(self, event_set):

        sampling_event_api = openapi_client.SamplingEventApi(self._api_client)

        fetched = sampling_event_api.download_sampling_events_by_event_set(
            event_set, start=0, count=0)

        if not fetched.count:
            return {}, {}
        start = 0
        page_size = 100
        all_locations = {}
        all_sampling_events = {}
        while start < fetched.count:
            fetched = sampling_event_api.download_sampling_events_by_event_set(event_set,
                                                                               start=start,
                                                                               count=page_size)
            start += page_size
            z = {**all_locations, **fetched.locations}
            all_locations = z
            for event in fetched.sampling_events:
                if event.sampling_event_id in all_sampling_events:
                    print('Already seen it')
                all_sampling_events[event.sampling_event_id] = event

        return all_locations, all_sampling_events

    def get_original_samples_by_event_set(self, event_set_code):

        os_api = openapi_client.OriginalSampleApi(self._api_client)

        fetched = os_api.download_original_samples_by_event_set(
            event_set_code, start=0, count=0)

        start = 0
        page_size = 100
        all_original_samples = {}
        while start < fetched.count:
            fetched = os_api.download_original_samples_by_event_set(event_set_code,
                                                                    start=start,
                                                                    count=page_size)
            start += page_size
            for sample in fetched.original_samples:
                all_original_samples[sample.original_sample_id] = sample

        return all_original_samples

    def get_derivative_samples_by_event_set(self, event_set_code):

        ds_api = openapi_client.DerivativeSampleApi(self._api_client)

        try:
            fetched = ds_api.download_derivative_samples_by_event_set(
                event_set_code, start=0, count=0)
        except openapi_client.rest.ApiException as api_e:
            if api_e.status == 404:
                return {}, {}
            else:
                print(api_e)
                return {}, {}

        start = 0
        page_size = 100
        all_derivative_samples = {}
        derivative_sample_map = {}
        while start < fetched.count:
            fetched = os_api.download_derivative_samples_by_event_set(event_set_code,
                                                                      start=start,
                                                                      count=page_size)
            start += page_size
            for sample in fetched.original_samples:
                all_derivative_samples[sample.derivative_sample_id] = sample
                if sample.original_sample_id in derivative_sample_map:
                    derivative_sample_map[sample.original_sample_id].append(
                        sample.derivative_sample_id)
                else:
                    derivative_sample_map[sample.original_sample_id] = [
                        sample.derivative_sample_id]

        return all_derivative_samples, derivative_sample_map

    def get_attr(self, entity, name):

        if ':' in name:
            (etype, ename) = name.split(':')
            for attr in entity.attrs:
                if attr.attr_type == ename:
                    return attr.attr_value
        else:
            return getattr(entity, name)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--studies', metavar='studies', nargs='+',
                        help='studies to retrieve')
    parser.add_argument('--event-sets', metavar='event_sets', nargs='+',
                        help='event sets to retrieve')
    parser.add_argument('--cols', metavar='cols', nargs='+',
                        help='columns to output - attrs as os.attr_name, ds.attr_name')
    parser.add_argument('config', metavar='config',
                        help='columns to output - attrs as os.attr_name, ds.attr_name')

    args = parser.parse_args()

    fetch = Fetch(args.config)

    all_locations = {}
    all_sampling_events = {}
    all_original_samples = {}
    all_derivative_samples = {}
    derivative_sample_map = {}

    if args.studies:
        for study in args.studies:
            locations, sampling_events = fetch.get_sampling_event_details_by_study(
                study)
            all_locations = {**all_locations, **locations}
            all_sampling_events = {**all_sampling_events, **sampling_events}
            original_samples = fetch.get_original_samples_by_study(study)
            all_original_samples = {**all_original_samples, **original_samples}
            derivative_samples, dsm = fetch.get_derivative_samples_by_study(
                study)
            all_derivative_samples = {**all_derivative_samples, **derivative_samples}
            derivative_sample_map = {**derivative_sample_map, **dsm}

    if args.event_sets:
        for event_set_raw in args.event_sets:
            event_set = urllib.parse.quote_plus(event_set_raw)
            locations, sampling_events = fetch.get_sampling_event_details_by_event_set(
                event_set)
            all_locations = {**all_locations, **locations}
            all_sampling_events = {**all_sampling_events, **sampling_events}
            original_samples = fetch.get_original_samples_by_event_set(
                event_set)
            all_original_samples = {**all_original_samples, **original_samples}
            derivative_samples, dsm = fetch.get_derivative_samples_by_event_set(
                event_set)
            all_derivative_samples = {**all_derivative_samples, **derivative_samples}
            derivative_sample_map = {**derivative_sample_map, **dsm}

    csvfile = csv.writer(sys.stdout)
    row = []
    csvfile = csv.writer(sys.stdout)
    row = []
    for col in args.cols:
        (pref, name) = col.split('.')
        if not pref == 'ds':
            row.append(col)
    for col in args.cols:
        (pref, name) = col.split('.')
        if pref == 'ds':
            row.append(col)
    csvfile.writerow(row)

    for ident, o_sample in all_original_samples.items():
        row = []
        for col in args.cols:
            value = ''
            (pref, name) = col.split('.')
            if pref == 'os':
                value = fetch.get_attr(o_sample, name)
            elif pref == 'se':
                if o_sample.sampling_event_id:
                    if o_sample.sampling_event_id not in all_sampling_events:
                        print(o_sample)
                    value = fetch.get_attr(
                        all_sampling_events[o_sample.sampling_event_id], name)
                else:
                    value = None
            elif pref == 'loc':
                if o_sample.sampling_event_id:
                    se = all_sampling_events[o_sample.sampling_event_id]
                    value = fetch.get_attr(
                        all_locations[se.public_location_id], name)
            if not pref == 'ds':
                row.append(value)

        if o_sample.original_sample_id in derivative_sample_map:
            for d_sample in derivative_sample_map[o_sample.original_sample_id]:
                for col in args.cols:
                    if col.startswith('ds.'):
                        (pref, name) = col.split('.')
                        row.append(fetch.get_attr(d_sample, name))

        csvfile.writerow(row)
