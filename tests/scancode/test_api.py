#
# Copyright (c) 2015 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import, print_function

from collections import OrderedDict
import os

from commoncode.testcase import FileBasedTesting
from scancode.api import get_licenses


class TestApi(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_get_license_with_policy_configuration(self):
        config = self.get_test_loc('api/scancode.yml')
        test_file = self.get_test_loc('api/LICENSE.txt')
        result = get_licenses(location=test_file, config_location=config)
        expected = [OrderedDict([
            ('key', u'bsd-new'),
            ('score', 100.0),
            ('short_name', u'BSD-Modified'),
            ('category', u'Attribution'),
            ('owner', u'Regents of the University of California'),
            ('homepage_url',
                u'http://www.opensource.org/licenses/BSD-3-Clause'),
            ('text_url',
             u'http://www.opensource.org/licenses/BSD-3-Clause'),
            ('dejacode_url',
             'https://enterprise.dejacode.com/license_library/Demo/bsd-new/'),
            ('spdx_license_key', u'BSD-3-Clause'),
            ('spdx_url', u'http://spdx.org/licenses/BSD-3-Clause'),
            ('start_line', 4), ('end_line', 12),
            ('policy', u'Restricted License')
        ])]
        assert expected == list(result)
