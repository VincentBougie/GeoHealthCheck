# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2014 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import datetime
import logging
from urllib2 import urlopen

from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from owslib.wcs import WebCoverageService
from owslib.wps import WebProcessingService
from owslib.csw import CatalogueServiceWeb

from enums import RESOURCE_TYPES

LOGGER = logging.getLogger(__name__)


def run_test_resource(resource_type, url):
    """tests a CSW service and provides run metrics"""

    if resource_type not in RESOURCE_TYPES.keys():
        msg = 'Invalid resource type: %s' % resource_type
        LOGGER.error(msg)
        raise RuntimeError(msg)

    title = None
    start_time = datetime.datetime.utcnow()
    message = None


    try:
        if resource_type == 'OGC:WMS':
            ows = WebMapService(url)
        elif resource_type == 'OGC:WFS':
            ows = WebFeatureService(url)
        elif resource_type == 'OGC:WCS':
            ows = WebCoverageService(url)
        elif resource_type == 'OGC:WPS':
            ows = WebProcessingService(url)
        elif resource_type == 'OGC:CSW':
            ows = CatalogueServiceWeb(url)
        elif resource_type == 'WWW:LINK':
            ows = urlopen(url)
            import re
            title_re = re.compile("<title>(.+?)</title>")
            title = title_re.search(ows.read()).group(1)
        success = True
        if resource_type != 'WWW:LINK':
            title = ows.identification.title
    except Exception, err:
        LOGGER.exception(err)
        message = err
        success = False

    end_time = datetime.datetime.utcnow()

    delta = end_time - start_time
    response_time = '%s.%s' % (delta.seconds, delta.microseconds)

    return [title, success, response_time, message, start_time]


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Usage: %s <resource_type> <url>' % sys.argv[0])
        sys.exit(1)

    print(run_test_resource(sys.argv[1], sys.argv[2]))