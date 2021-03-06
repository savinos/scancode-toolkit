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

import os

from commoncode.testcase import FileBasedTesting

from licensedcode import index
from licensedcode.models import Rule

from licensedcode.query import Query
from array import array
from licensedcode import models


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class IndexTesting(FileBasedTesting):
    test_data_dir = TEST_DATA_DIR

    def get_test_rules(self, base, subset=None):
        base = self.get_test_loc(base)
        test_files = sorted(os.listdir(base))
        if subset:
            test_files = [t for t in test_files if t in subset]

        return [Rule(text_file=os.path.join(base, license_key), licenses=[license_key])
                for license_key in test_files]


class TestQueryWithSingleRun(IndexTesting):

    def test_Query_tokens_by_line_from_string(self):
        rule_text = 'Redistribution and use in source and binary forms with or without modification are permitted'
        idx = index.LicenseIndex([Rule(_text=rule_text, licenses=['bsd'])])
        querys = '''
            The
            Redistribution and use in source and binary are permitted

            Athena capital of Grece
            Paris and Athene
            Always'''

        qry = Query(query_string=querys, idx=idx, _test_mode=True)
        result = list(qry.tokens_by_line())
        expected = [
            [],
            [None],
            [12, 0, 6, 3, 2, 0, 1, 10, 7],
            [],
            [None, None, None, None],
            [None, 0, None],
            [None],
        ]

        assert expected == result

        # convert tid to actual token strings
        qtbl_as_str = lambda qtbl: [[None if tid is None else idx.tokens_by_tid[tid] for tid in tids] for tids in qtbl]

        result_str = qtbl_as_str(result)
        expected_str = [
            [],
            [None],
            ['redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted'],
            [],
            [None, None, None, None],
            [None, 'and', None],
            [None],
        ]

        assert expected_str == result_str

        assert {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 6} == qry.line_by_pos

        idx = index.LicenseIndex([Rule(_text=rule_text, licenses=['bsd'])])
        querys = 'and this is not a license'
        qry = Query(query_string=querys, idx=idx, _test_mode=True)
        result = list(qry.tokens_by_line())
        expected = [['and', None, None, None, None, None]]
        assert expected == qtbl_as_str(result)

    def test_Query_tokenize_from_string(self):
        rule_text = 'Redistribution and use in source and binary forms with or without modification are permitted'
        idx = index.LicenseIndex([Rule(_text=rule_text, licenses=['bsd'])])
        querys = '''
            The
            Redistribution and use in source and binary are permitted.

            Athena capital of Grece
            Paris and Athene
            Always'''

        qry = Query(query_string=querys, idx=idx, _test_mode=True)
        qry.tokenize(qry.tokens_by_line())
        # convert tid to actual token strings
        tks_as_str = lambda tks: [None if tid is None else idx.tokens_by_tid[tid] for tid  in tks]

        expected = ['redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', 'and']
        result = tks_as_str(qry.tokens)
        assert expected == result

        expected = [None, 'redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', None, None, None, None, None, 'and', None, None]
        result = tks_as_str(qry.tokens_with_unknowns())
        assert expected == result

        assert 1 == len(qry.query_runs)
        qr1 = qry.query_runs[0]
        assert 0 == qr1.start
        assert 9 == qr1.end
        assert 10 == len(qr1)
        expected = ['redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', 'and']
        result = tks_as_str(qr1.tokens)
        assert expected == result
        expected = [None, 'redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', None, None, None, None, None, 'and']
        result = tks_as_str(qr1.tokens_with_unknowns())
        assert expected == result

    def test_QueryRuns_tokens_with_unknowns(self):
        rule_text = 'Redistribution and use in source and binary forms with or without modification are permitted'
        idx = index.LicenseIndex([Rule(_text=rule_text, licenses=['bsd'])])
        querys = '''
            The
            Redistribution and use in source and binary are permitted.

            Athena capital of Grece
            Paris and Athene
            Always'''

        qry = Query(query_string=querys, idx=idx)
        assert set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == set(qry.matchables)

        assert 1 == len(qry.query_runs)
        qrun = qry.query_runs[0]

        # convert tid to actual token strings
        tks_as_str = lambda tks: [None if tid is None else idx.tokens_by_tid[tid] for tid  in tks]

        expected = ['redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', 'and']
        assert expected == tks_as_str(qrun.tokens)

        expected = [None, 'redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'are', 'permitted', None, None, None, None, None, 'and']
        assert expected == tks_as_str(qrun.tokens_with_unknowns())

        assert 0 == qrun.start
        assert 9 == qrun.end

    def test_QueryRun_does_not_end_with_None(self):
        rule_text = 'Redistribution and use in source and binary forms, with or without modification, are permitted'
        idx = index.LicenseIndex([Rule(_text=rule_text, licenses=['bsd'])])

        querys = '''
            The
            Redistribution and use in source and binary forms, with or without modification, are permitted.

            Always



            bar
             modification
             foo
            '''

        # convert tid to actual token strings
        tks_as_str = lambda tks: [None if tid is None else idx.tokens_by_tid[tid] for tid  in tks]
        qry = Query(query_string=querys, idx=idx)
        expected = [
            None,
            'redistribution', 'and', 'use', 'in', 'source', 'and', 'binary',
            'forms', 'with', 'or', 'without', 'modification', 'are', 'permitted',
            None, None,
            'modification',
            None
        ]
        assert [x for x in expected if x] == tks_as_str(qry.tokens)
        assert expected == tks_as_str(qry.tokens_with_unknowns())

        assert 2 == len(qry.query_runs)
        qrun = qry.query_runs[0]
        expected = ['redistribution', 'and', 'use', 'in', 'source', 'and', 'binary', 'forms', 'with', 'or', 'without', 'modification', 'are', 'permitted']
        assert expected == tks_as_str(qrun.tokens)
        assert 0 == qrun.start
        assert 13 == qrun.end

        qrun = qry.query_runs[1]
        expected = ['modification']
        assert expected == tks_as_str(qrun.tokens)
        assert 14 == qrun.start
        assert 14 == qrun.end

    def test_Query_from_real_index_and_location(self):
        idx = index.LicenseIndex(self.get_test_rules('index/bsd'))
        query_loc = self.get_test_loc('index/querytokens')

        qry = Query(location=query_loc, idx=idx)
        runs = qry.query_runs
        assert len(runs) == 1
        query_run = runs[0]

        expected_lbp = {
            0: 4, 1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 6, 9: 6, 10: 6,
            11: 6, 12: 6, 13: 7, 14: 7, 15: 7, 16: 7, 17: 7, 18: 8, 19: 9, 
            20: 9, 21: 9, 22: 9, 23: 9, 24: 11, 25: 11, 26: 11, 27: 11, 28: 11,
            29: 11, 30: 11, 31: 11, 32: 11, 33: 11, 34: 11, 35: 11, 36: 15
        }

        assert expected_lbp == query_run.line_by_pos

        expected_toks = [
            u'redistribution', u'and', u'use', u'in', u'source', u'and',
            u'binary', u'forms', u'redistributions', u'of', u'source', u'code',
            u'must', u'the', u'this', u'that', u'is', u'not', u'to',
            u'redistributions', u'in', u'binary', u'form', u'must', u'this',
            u'software', u'is', u'provided', u'by', u'the', u'copyright',
            u'holders', u'and', u'contributors', u'as', u'is',
            u'redistributions']

        assert expected_toks == [None if t is None else idx.tokens_by_tid[t] for t in query_run.tokens]

    def test_query_run_tokens_with_junk(self):
        ranked_toks = lambda : ['the', 'is', 'a']
        idx = index.LicenseIndex([Rule(_text='a is the binary')],
                                 _ranked_tokens=ranked_toks)
        assert 2 == idx.len_junk
        assert {'a': 0, 'the': 1, 'binary': 2, 'is': 3, } == idx.dictionary

        # two junks
        q = Query(query_string='a the', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [0, 1] == qrun.tokens
        assert {} == qrun.unknowns_by_pos

        # one junk
        q = Query(query_string='a binary', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [0, 2] == qrun.tokens
        assert {} == qrun.unknowns_by_pos

        # one junk
        q = Query(query_string='binary the', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2, 1] == qrun.tokens
        assert {} == qrun.unknowns_by_pos

        # one unknown at start
        q = Query(query_string='that binary', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2] == qrun.tokens
        assert {-1: 1} == qrun.unknowns_by_pos

        # one unknown at end
        q = Query(query_string='binary that', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2] == qrun.tokens
        assert {0: 1} == qrun.unknowns_by_pos

        # onw unknown in the middle
        q = Query(query_string='binary that a binary', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2, 0, 2] == qrun.tokens
        assert {0: 1} == qrun.unknowns_by_pos

        # onw unknown in the middle
        q = Query(query_string='a binary that a binary', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [0, 2, 0, 2] == qrun.tokens
        assert {1: 1} == qrun.unknowns_by_pos

        # two unknowns in the middle
        q = Query(query_string='binary that was a binary', idx=idx)
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2, 0, 2] == qrun.tokens
        assert {0: 2} == qrun.unknowns_by_pos

        # unknowns at start, middle and end
        q = Query(query_string='hello dolly binary that was a binary end really', idx=idx)
        #                         u     u           u    u            u    u
        qrun = q.query_runs[0]
        assert qrun.line_by_pos
        assert [2, 0, 2] == qrun.tokens
        assert {-1: 2, 0: 2, 2: 2} == qrun.unknowns_by_pos

    def test_query_tokens_are_same_for_different_text_formatting(self):

        test_files = [self.get_test_loc(f) for f in [
            'queryformat/license2.txt',
            'queryformat/license3.txt',
            'queryformat/license4.txt',
            'queryformat/license5.txt',
            'queryformat/license6.txt',
        ]]

        rule_file = self.get_test_loc('queryformat/license1.txt')
        idx = index.LicenseIndex([Rule(text_file=rule_file, licenses=['mit'])])

        q = Query(location=rule_file, idx=idx)
        assert 1 == len(q.query_runs)
        expected = q.query_runs[0]
        for tf in test_files:
            q = Query(tf, idx=idx)
            qr = q.query_runs[0]
            assert expected.tokens == qr.tokens

    def test_query_run_unknowns(self):
        idx = index.LicenseIndex([Rule(_text='a is the binary')])

        assert {'a': 0, 'binary': 1, 'is': 2, 'the': 3} == idx.dictionary
        assert 2 == idx.len_junk

        # multiple unknowns at start, middle and end
        q = Query(query_string='that new binary was sure a kind of the real mega deal', idx=idx)
        # known pos                      0               1         2
        # abs pos                  0   1 2      3   4    5 6    7  8   9    10   11
        expected = {
            - 1: 2,
            0: 2,
            1: 2,
            2: 3,
        }
        assert expected == dict(q.unknowns_by_pos)


class TestQueryWithMultipleRuns(IndexTesting):

    def test_query_runs_from_location(self):
        idx = index.LicenseIndex(self.get_test_rules('index/bsd'))
        query_loc = self.get_test_loc('index/querytokens')
        qry = Query(location=query_loc, idx=idx, line_threshold=3)
        result = [q._as_dict(brief=True) for q in qry.query_runs]

        expected = [
            {
             'start': 0,
             'end': 35,
             'tokens': u'redistribution and use in source ... holders and contributors as is'},
            {
             'start': 36,
             'end': 36,
             'tokens': u'redistributions'}
        ]
        assert expected == result

    def test_query_runs_three_runs(self):
        idx = index.LicenseIndex(self.get_test_rules('index/bsd'))
        query_loc = self.get_test_loc('index/queryruns')
        qry = Query(location=query_loc, idx=idx)
        expected = [
            {'end': 84,
             'start': 0,
             'tokens': u'the redistribution and use in ... 2 1 3 c 4'},
            {'end': 97,
             'start': 85,
             'tokens': u'this software is provided by ... holders and contributors as is'},
            {'end': 98, 'start': 98, 'tokens': u'redistributions'}
        ]

        result = [q._as_dict(brief=True) for q in qry.query_runs]
        assert expected == result

    def test_QueryRun(self):
        idx = index.LicenseIndex([Rule(_text='redistributions in binary form must redistributions in')])
        qry = Query(query_string='redistributions in binary form must redistributions in', idx=idx)
        qruns = qry.query_runs
        assert 1 == len(qruns)
        qr = qruns[0]
        # test
        result = [idx.tokens_by_tid[tid] for tid in qr.tokens]
        expected = ['redistributions', 'in', 'binary', 'form', 'must', 'redistributions', 'in']
        assert expected == result

    def test_query_runs_text_is_correct(self):
        test_rules = self.get_test_rules('query/full_text/idx',)
        idx = index.LicenseIndex(test_rules)
        query_loc = self.get_test_loc('query/full_text/query')
        qry = Query(location=query_loc, idx=idx, line_threshold=3)
        qruns = qry.query_runs
        result = [[u'<None>' if t is None else idx.tokens_by_tid[t] for t in qr.tokens_with_unknowns()] for qr in qruns]

        expected = [
            u'<None> <None> <None> this'.split(),

            u'''redistribution and use in source and binary forms with or
            without modification are permitted provided that the following
            conditions are met redistributions of source code must retain the
            above copyright notice this list of conditions and the following
            disclaimer redistributions in binary form must reproduce the above
            copyright notice this list of conditions and the following
            disclaimer in the documentation and or other materials provided with
            the distribution neither the name of <None> inc nor the names of its
            contributors may be used to endorse or promote products derived from
            this software without specific prior written permission this
            software is provided by the copyright holders and contributors as is
            and any express or implied warranties including but not limited to
            the implied warranties of merchantability and fitness for a
            particular purpose are disclaimed in no event shall the copyright
            owner or contributors be liable for any direct indirect incidental
            special exemplary or consequential damages including but not limited
            to procurement of substitute goods or services loss of use data or
            profits or business interruption however caused and on any theory of
            liability whether in contract strict liability or tort including
            negligence or otherwise arising in any way out of the use of this
            software even if advised of the possibility of such damage'''.split(),
            u'no <None> of'.split(),
        ]
        assert expected == result

    def test_query_runs_with_plain_rule(self):
        rule_text = u'''X11 License
            Copyright (C) 1996 X Consortium Permission is hereby granted, free
            of charge, to any person obtaining a copy of this software and
            associated documentation files (the "Software"), to deal in the
            Software without restriction, including without limitation the
            rights to use, copy, modify, merge, publish, distribute, sublicense,
            and/or sell copies of the Software, and to permit persons to whom
            the Software is furnished to do so, subject to the following
            conditions: The above copyright notice and this permission notice
            shall be included in all copies or substantial portions of the
            Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
            KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
            WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
            NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR
            ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
            CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
            WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
            Except as contained in this notice, the name of the X Consortium
            shall not be used in advertising or otherwise to promote the sale,
            use or other dealings in this Software without prior written
            authorization from the X Consortium. X Window System is a trademark
            of X Consortium, Inc.
        '''
        rule = Rule(_text=rule_text, licenses=['x-consortium'])
        idx = index.LicenseIndex([rule])

        query_loc = self.get_test_loc('detect/simple_detection/x11-xconsortium_text.txt')
        qry = Query(location=query_loc, idx=idx)
        result = [q._as_dict(brief=True) for q in qry.query_runs]
        expected = [{
            'start': 0,
            'end': 216,
            'tokens': u'x11 license copyright c 1996 ... trademark of x consortium inc'
        }]
        assert 217 == len(qry.query_runs[0].tokens)
        assert expected == result

    def test_query_run_has_correct_offset(self):
        rule_dir = self.get_test_loc('query/runs/rules')
        rules = list(models.load_rules(rule_dir))
        idx = index.LicenseIndex(rules)
        query_doc = self.get_test_loc('query/runs/query.txt')
        q = Query(location=query_doc, idx=idx)
        assert len(q.query_runs) == 2
        query_run = q.query_runs[0]
        assert 0 == query_run.start
        assert 0 == query_run.end
        assert [25] == query_run.tokens

        query_run = q.query_runs[1]
        assert 1 == query_run.start
        assert 123 == query_run.end


class TestQueryWithFullIndex(FileBasedTesting):
    test_data_dir = TEST_DATA_DIR

    def test_query_runs_from_rules_should_return_few_runs(self):
        # warning: this  is a long running function which builds ~ 4000 queries
        idx = index.get_index()
        rules_with_multiple_runs = 0
        for rule in idx.rules_by_rid:
            qry = Query(location=rule.text_file, idx=idx, line_threshold=4)
            if len(qry.query_runs) != 1:
                rules_with_multiple_runs += 1
        # uncomment to print which rules are a problem.
        #         print()
        #         print('Multiple runs for rule:', rule.identifier)
        #         for r in runs:
        #             print(r._as_dict(brief=True))
        # print('#Rules with Multiple runs:', rules_with_multiple_runs)
        assert rules_with_multiple_runs < 350

    def test_query_from_binary_lkms_1(self):
        location = self.get_test_loc('query/ath_pci.ko')
        idx = index.get_index()
        result = Query(location, idx=idx)
        assert 7 == len(result.query_runs)

    def test_query_from_binary_lkms_2(self):
        location = self.get_test_loc('query/eeepc_acpi.ko')
        idx = index.get_index()
        result = Query(location, idx=idx)
        assert 259 == len(result.query_runs)
        qr = result.query_runs[5]
        assert 'license gpl' in u' '.join(idx.tokens_by_tid[t] for t in qr.matchable_tokens())

    def test_query_from_binary_lkms_3(self):
        location = self.get_test_loc('query/wlan_xauth.ko')
        idx = index.get_index()
        result = Query(location, idx=idx)
        assert 498 == len(result.query_runs)

    def test_query_run_tokens(self):
        query_s = u' '.join(u'''
        3 unable to create proc entry license gpl description driver author eric depends 2 6 24 19 generic smp mod module acpi bus register driver proc acpi disabled acpi install notify acpi bus get status cache caches create proc entry bus generate proc event acpi evaluate object acpi remove notify remove proc entry acpi bus driver acpi acpi gcc gnu 4 2 3 ubuntu 4 2 3 gcc gnu 4 2 3 ubuntu 4 2 3 current stack pointer current stack pointer this module end usr src modules acpi include linux include asm include asm generic include acpi acpi c posix types 32 h types h types h h h h h
        '''.split())
        idx = index.get_index()
        result = Query(query_string=query_s, idx=idx)
        assert 1 == len(result.query_runs)
        qr = result.query_runs[0]
        assert query_s == u' '.join(idx.tokens_by_tid[t] for t in qr.tokens)

    def test_query_run_matchable_tokens(self):
        query_s = u' '.join(u'''
        3 unable to create proc entry license gpl description driver author eric depends 2 6 24 19 generic smp mod module acpi bus register driver proc acpi disabled acpi install notify acpi bus get status cache caches create proc entry bus generate proc event acpi evaluate object acpi remove notify remove proc entry acpi bus driver acpi acpi gcc gnu 4 2 3 ubuntu 4 2 3 gcc gnu 4 2 3 ubuntu 4 2 3 current stack pointer current stack pointer this module end usr src modules acpi include linux include asm include asm generic include acpi acpi c posix types 32 h types h types h h h h h
        '''.split())
        idx = index.get_index()
        result = Query(query_string=query_s, idx=idx)
        assert 1 == len(result.query_runs)
        qr = result.query_runs[0]
        assert query_s == u' '.join(idx.tokens_by_tid[t] for t in qr.tokens)
