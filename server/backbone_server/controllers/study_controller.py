import connexion
from swagger_server.models.studies import Studies
from datetime import date, datetime
from typing import List, Dict
from six import iteritems


from backbone_server.study.gets import StudiesGet

from backbone_server.connect  import get_connection

import logging

class StudyController():

    @staticmethod
    def download_studies(start=None, count=None):
        """
        fetches studies
        
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """
        get = StudiesGet(get_connection())

        studies = get.get()

        return studies, 200
