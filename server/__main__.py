#!/usr/bin/env python3

import connexion

from openapi_server import encoder

from backbone_server.model.study import PartnerSpeciesIdentifier
from backbone_server.model.study import Taxonomy
from backbone_server.model.study import Study
from backbone_server.model.attr import Attr
from backbone_server.model.individual import Individual
from backbone_server.model.location import Location
from backbone_server.model.sampling_event import SamplingEvent
from backbone_server.model.event_set import EventSet
from backbone_server.model.event_set_note import EventSetNote
from backbone_server.model.original_sample import OriginalSample
from backbone_server.model.original_sample import original_sample_attr_table
from backbone_server.model.derivative_sample import DerivativeSample

def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Backbone'})
    app.run(port=8080, use_reloader=True)


if __name__ == '__main__':
    main()
