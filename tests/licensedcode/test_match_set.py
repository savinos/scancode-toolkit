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

from unittest.case import TestCase

from intbitset import intbitset

from licensedcode import match_set
from licensedcode.models import Thresholds


class FilterTesting(TestCase):

    def test_compare_sets_tids_sets(self):
        thresholds = Thresholds(high_len=3, low_len=0, length=3, min_high=2, small=False, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3, 4, 6])
        ilow, ihigh = intbitset(), intbitset([3, 4, 6])

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert candidate

    def test_compare_sets_tids_sets_match_with_less_than_high_len(self):
        thresholds = Thresholds(high_len=3, low_len=0, length=3, min_high=2, small=False, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3, 4])
        ilow, ihigh = intbitset(), intbitset([3, 4, 6])

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)
        assert not candidate
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert candidate

    def test_compare_sets_tids_sets_non_exact_match_with_less_than_min_high(self):
        thresholds = Thresholds(high_len=3, low_len=0, length=3, min_high=2, small=False, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3])
        ilow, ihigh = intbitset(), intbitset([3, 4, 6])

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)
        assert not candidate
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert not candidate

    def test_compare_sets_tids_sets_exact_match_with_less_than_ilow_len(self):
        thresholds = Thresholds(high_len=3, low_len=1, length=3, min_high=2, small=False, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3, 4, 6])
        ilow, ihigh = intbitset([1]), intbitset([3, 4, 6])
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)

        assert not candidate
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert candidate

    def test_compare_sets_tids_sets_match_with_more_than_min_and_low_len(self):
        thresholds = Thresholds(high_len=3, low_len=1, length=4, min_high=2, small=False, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3, 4, 6])
        ilow, ihigh = intbitset([1]), intbitset([3, 4, 6])

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)
        assert not candidate
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert candidate

    def test_compare_sets_tids_sets_match_with_small_rule(self):
        thresholds = Thresholds(high_len=3, low_len=1, length=4, min_high=2, small=True, min_len=2, max_gap_skip=0)
        qlow, qhigh = intbitset(), intbitset([3, 4, 6])
        ilow, ihigh = intbitset([1]), intbitset([3, 4, 6])

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert not candidate

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)
        assert not candidate

        thresholds = Thresholds(high_len=3, low_len=1, length=4, min_high=2, small=False, min_len=2, max_gap_skip=0)
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert candidate

        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=True)
        assert not candidate

        thresholds = Thresholds(high_len=3, low_len=1, length=4, min_high=4, small=False, min_len=2, max_gap_skip=0)
        candidate = match_set.compare_sets(qhigh, qlow, ihigh, ilow, thresholds, match_set.tids_sets_intersector, match_set.tids_set_counter, exact=False)
        assert not candidate
