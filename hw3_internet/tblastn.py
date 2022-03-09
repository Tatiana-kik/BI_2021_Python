# =============================================================================
#
# Tblastn is a python module to search proteins in NCBI databases.
#
# =============================================================================

import requests
from bs4 import BeautifulSoup
import time
import re
import xml.etree.ElementTree as ET
import argparse
import sys

# This is parameters with default valuese for initial PUT request to BLASTN
# for using WGS database.
req_payload_template_wgs = {
    "QUERY": '__fill_me__',
    "db": 'protein',
    "QUERY_FROM": '',
    "QUERY_TO": '',
    "GENETIC_CODE": '1',
    "JOB_TITLE": '__fill_me__',
    "ADV_VIEW": 'true',
    "SUBJECTS": '',
    "stype": 'nucleotide',
    "SUBJECTS_FROM": '',
    "SUBJECTS_TO": '',
    "DATABASE": '__fill_me__',
    "DB_GROUP": '__fill_me__',  # do not use it
    "EQ_MENU": '__fill_me__',
    "NUM_ORG": '1',
    "EQ_TEXT": '',
    "PHI_PATTERN": '',
    "MAX_NUM_SEQ": '50',
    "EXPECT": '0.05',
    "WORD_SIZE": '3',
    "HSP_RANGE_MAX": '0',
    "MATRIX_NAME": 'BLOSUM62',
    "MATCH_SCORES": '1,-2',
    "GAPCOSTS": '11 1',
    "COMPOSITION_BASED_STATISTICS": '2',
    "REPEATS": '4829',
    "TEMPLATE_LENGTH": '0',
    "TEMPLATE_TYPE": '0',
    "I_THRESH": '',
    "DI_THRESH": '',
    "PSI_PSEUDOCOUNT": '',
    "SHOW_OVERVIEW": 'on',
    "SHOW_LINKOUT": 'on',
    "GET_SEQUENCE": 'on',
    "FORMAT_OBJECT": 'Alignment',
    "FORMAT_TYPE": 'HTML',
    "ALIGNMENT_VIEW": 'Pairwise',
    "MASK_CHAR": '2',
    "MASK_COLOR": '1',
    "DESCRIPTIONS": '50',
    "ALIGNMENTS": '50',
    "LINE_LENGTH": '60',
    "NEW_VIEW": 'false',
    "NCBI_GI": 'on',
    "SHOW_CDS_FEATURE": 'false',
    "NUM_OVERVIEW": '50',
    "FORMAT_EQ_TEXT": '',
    "FORMAT_ORGANISM": '',
    "EXPECT_LOW": '',
    "EXPECT_HIGH": '',
    "PERC_IDENT_LOW": '',
    "PERC_IDENT_HIGH": '',
    "QUERY_INDEX": '0',
    "FORMAT_NUM_ORG": '1',
    "CONFIG_DESCR": '2,3,4,5,8,9,10,11,12,13,14',
    "CLIENT": 'web',
    "SERVICE": 'plain',
    "CMD": 'request',
    "PAGE": 'Translations',
    "PROGRAM": 'tblastn',
    "MEGABLAST": '',
    "RUN_PSIBLAST": '',
    "WWW_BLAST_TYPE": '',
    "TWO_HITS": '',
    "UNGAPPED_ALIGNMENT": 'no',
    "BLAST_PROGRAMS": 'tblastn',
    # "DB_DISPLAY_NAME": 'wgs',
    "ORG_DBS": '__fill_me__',
    "SHOW_ORGANISMS": 'on',
    "DBTAXID": '',
    "SAVED_PSSM": '',
    "SELECTED_PROG_TYPE": 'tblastn',
    "SAVED_SEARCH": 'true',
    "BLAST_SPEC": '',
    "MIXED_DATABASE": '',
    "QUERY_BELIEVE_DEFLINE": '',
    "DB_DIR_PREFIX": '',
    "CHECKSUM": '',
    "USER_DATABASE": '',
    "USER_WORD_SIZE": '',
    "USER_MATCH_SCORES": '',
    "USER_FORMAT_DEFAULTS": '',
    "NO_COMMON": '',
    "NUM_DIFFS": '4',
    "NUM_OPTS_DIFFS": '3',
    "UNIQ_DEFAULTS_NAME": '',
    "PAGE_TYPE": 'BlastSearch',
    "USER_DEFAULT_PROG_TYPE": 'tblastn',
    "USER_DEFAULT_MATRIX": '',
}

# This is parameters with default values for initial PUT request to BLASTN
# for using NT database.
# NOTE:  This fields looks like for search in WGS, but there are some
#        differents, that difficult to catch. Therefore we are using separate
#        list of parmeters.
# TODO:  Make universal list parameters for every database.
req_payload_template_nt = {
    "QUERY": "__fill_me__",
    "db": "protein",
    "QUERY_FROM": "",
    "QUERY_TO": "",
    "GENETIC_CODE": "1",
    "JOB_TITLE": '__fill_me__',
    "ADV_VIEW": "true",
    "SUBJECTS": "",
    "stype": "nucleotide",
    "SUBJECTS_FROM": "",
    "SUBJECTS_TO": "",
    "DATABASE": "__fill_me__",
    "EQ_MENU": "__fill_me__",
    "NUM_ORG": "1",
    "EQ_TEXT": "",
    "PHI_PATTERN": "",
    "MAX_NUM_SEQ": "100",
    "EXPECT": "0.05",
    "WORD_SIZE": "6",
    "HSP_RANGE_MAX": "0",
    "MATRIX_NAME": "BLOSUM62",
    "MATCH_SCORES": "1,-2",
    "GAPCOSTS": "11 1",
    "COMPOSITION_BASED_STATISTICS": "2",
    "FILTER": "L",
    "REPEATS": "4829",
    "TEMPLATE_LENGTH": "0",
    "TEMPLATE_TYPE": "0",
    "I_THRESH": "",
    "DI_THRESH": "",
    "PSI_PSEUDOCOUNT": "",
    "SHOW_OVERVIEW": "on",
    "SHOW_LINKOUT": "true",
    "GET_SEQUENCE": "true",
    "FORMAT_OBJECT": "Alignment",
    "FORMAT_TYPE": "HTML",
    "ALIGNMENT_VIEW": "Pairwise",
    "MASK_CHAR": "2",
    "MASK_COLOR": "1",
    "DESCRIPTIONS": "100",
    "ALIGNMENTS": "100",
    "LINE_LENGTH": "60",
    "NEW_VIEW": "false",
    "NCBI_GI": "true",
    "SHOW_CDS_FEATURE": "false",
    "NUM_OVERVIEW": "100",
    "FORMAT_EQ_TEXT": "",
    "FORMAT_ORGANISM": "",
    "EXPECT_LOW": "",
    "EXPECT_HIGH": "",
    "PERC_IDENT_LOW": "",
    "PERC_IDENT_HIGH": "",
    "QUERY_INDEX": "0",
    "FORMAT_NUM_ORG": "1",
    "CONFIG_DESCR": "2,3,4,5,8,9,10,11,12,13,14",
    "CLIENT": "web",
    "SERVICE": "plain",
    "CMD": "request",
    "PAGE": "Translations",
    "PROGRAM": "tblastn",
    "MEGABLAST": "",
    "RUN_PSIBLAST": "",
    "WWW_BLAST_TYPE": "",
    "TWO_HITS": "",
    "UNGAPPED_ALIGNMENT": "no",
    "BLAST_PROGRAMS": "tblastn",
    "DB_DISPLAY_NAME": "",
    "ORG_DBS": "",
    "SHOW_ORGANISMS": "",
    "DBTAXID": "",
    "SAVED_PSSM": "",
    "SELECTED_PROG_TYPE": "tblastn",
    "SAVED_SEARCH": "true",
    "BLAST_SPEC": "",
    "MIXED_DATABASE": "",
    "QUERY_BELIEVE_DEFLINE": "",
    "DB_DIR_PREFIX": "",
    "CHECKSUM": "",
    "USER_DATABASE": "",
    "USER_WORD_SIZE": "",
    "USER_MATCH_SCORES": "",
    "USER_FORMAT_DEFAULTS": "",
    "NO_COMMON": "",
    "NUM_DIFFS": "0",
    "NUM_OPTS_DIFFS": "0",
    "UNIQ_DEFAULTS_NAME": "",
    "PAGE_TYPE": "BlastSearch",
    "USER_DEFAULT_PROG_TYPE": "tblastn",
    "USER_DEFAULT_MATRIX": ""
}


# looking for search status
# return:  WAITING, READY, ...
def _find_status_in_html(content):

    # print(content)

    ''' Page should content some text like this:
        <!--
        QBlastInfoBegin
            Status=WAITING
        QBlastInfoEnd
        -->
    '''
    # looking for this text
    a = r'[\S\n\t\v ]*'  # any scharacters
    pattern = f'<!--{a}QBlastInfoBegin{a}Status={a}QBlastInfoEnd{a}-->'
    found = re.findall(pattern, content)
    if not found:
        return '__no_status_found_1__'
    # looking for 'Status=...'
    found = re.findall(r'Status=[\w]*', found[0])
    if not found:
        return '__no_status_found_2__'
    # get status value
    if len(found[0]) < len('Status='):
        return '__no_status_found_3__'
    status = found[0][7:]
    return status


# looking for search info
# return a dictionary
def _find_search_info_in_html(content):

    '''
    Page for initial request or page with status=WAITING
      should content some text like this:

        <table id="statInfo" class="WAITING">
            <tr><td>Request ID</td><td> <b>27M603HD013</b></td></tr>
            <tr class="odd"><td>Status</td><td>Searching</td></tr>
            <tr><td>Submitted at</td><td>Sat Mar  5 16:06:08 2022</td></tr>
            <tr class="odd"><td>Current time</td>
                            <td>Sat Mar 05 16:06:10 2022</td></tr>
            <tr><td>Time since submission</td><td>00:00:01</td></tr>
        </table>
    '''

    # some checking
    if not content:
        return {}

    # looking for statInfo table
    soup = BeautifulSoup(content, 'html.parser')
    stat_info_table = soup.find(lambda tag: tag.name == 'table' and
                                tag.has_attr('id') and
                                tag['id'] == "statInfo")

    if not stat_info_table:
        # print(content)
        return {}

    # get info from table cells
    tds = stat_info_table.find_all('td')
    sinfo = {}
    for i in range(len(tds)):
        if i % 2 == 1:
            k = tds[i - 1].text.strip()
            v = tds[i].text.strip()
            sinfo[k] = v

    return sinfo


# return list of structs Alignment
def _parse_xml_report(xml_string):

    # Remove the default namespace definition (xmlns="http://some/namespace")
    xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xml_string, count=1)

    # get root of XML
    xml_root = ET.fromstring(xmlstring)

    # get list of hits
    xml_hits = xml_root.findall('BlastOutput2/report/Report/' +
                                'results/Results/search/Search/hits/Hit')
    if not xml_hits:
        return []

    # go through 'hits' and built the alignment structure
    alignments = []
    for hit in xml_hits:

        # get common info for several matches
        seq_id = hit.find('description/HitDescr/id')
        seq_accession = hit.find('description/HitDescr/accession')
        seq_title = hit.find('description/HitDescr/title')
        seq_length = hit.find('len')
        xml_match = hit.findall('hsps/Hsp')

        for match in xml_match:

            alignment = {}

            # store common info for several matches
            if seq_id is not None:
                alignment['seq_id'] = seq_id.text
            if seq_accession is not None:
                alignment['seq_accession'] = seq_accession.text
            if seq_title is not None:
                alignment['seq_title'] = seq_title.text
            if seq_length is not None:
                alignment['seq_length'] = seq_length.text

            # list of needed parameters
            key_list = ['bit-score', 'score', 'evalue', 'identity',
                        'positive', 'query-from', 'query-to', 'hit-from',
                        'hit-to', 'hit-frame', 'align-len', 'gaps',
                        'qseq', 'hseq', 'midline']

            # get and store parameters
            for key in key_list:
                match_val = match.find(key)
                # print(f'    {key}:  {match_val.text}')
                if match_val is not None:
                    alignment[key] = match_val.text
            alignments.append(alignment)

    return alignments


# print alignments result in console
def tblastn_print_result(alignments):

    print(f'Tblastn Alignments ({len(alignments)}):')
    cnt = 1
    for ali in alignments:
        print(f'  --- {cnt} ---')
        cnt += 1
        for key in ali:
            max_val_len = 40
            spaces = ' ' * (15 - len(key))
            dotes = '...' if len(ali[key]) > max_val_len else ''
            print(f'  {key}:{spaces}{ali[key][:max_val_len]} {dotes}')


# return payload for HTTP request
def _prepare_payload(seq, db, taxid):

    # fill some params according to db value
    if db == 'wgs':
        req_payload = req_payload_template_wgs
        req_payload['DATABASE'] = 'Whole_Genome_Shotgun_contigs'
        req_payload['DB_GROUP'] = 'wgsOrg'
        req_payload['ORG_DBS'] = 'orgDbsOnly_wgs'
        req_payload['MAX_NUM_SEQ'] = '50'
        req_payload['EXPECT'] = '0.05'
        req_payload['WORD_SIZE'] = '3'
    elif db == 'nt':
        req_payload = req_payload_template_nt
        req_payload['DATABASE'] = 'nt'
        req_payload['ORG_DBS'] = ''
        req_payload["MAX_NUM_SEQ"] = '100'
        req_payload["EXPECT"] = '0.05'
        req_payload["WORD_SIZE"] = '6'
    else:
        return []

    # fill some common parameters
    job_name = f'Custom search:  seq="{seq}", db="{db}", taxid="{taxid}"'
    req_payload['QUERY'] = seq
    req_payload['EQ_MENU'] = taxid
    req_payload['JOB_TITLE'] = job_name

    return req_payload


# looking for sequence in NCBI databases
# return:  [list-of-alignments], 'error-text'
def tblastn_find(seq, db, taxid, verbose=0, seconds=60):

    # check incomming parameters
    if db not in ['wgs', 'nt']:
        return [], 'unsupported database, supported:  \'wgs\' and \'nt\' only'

    URI = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi'

    payload = _prepare_payload(seq, db, taxid)

    if verbose == 2:
        print()
        cnt = 0
        for k, v in payload.items():
            print(f'    -- {cnt} -- {k}:  {v}')
            cnt += 1
        print()

    # send initial POST request
    rep = requests.post(URI, data=payload, timeout=seconds)

    # looking for statInfo table and get RID from it
    sinfo = _find_search_info_in_html(rep.text)
    k = 'Request ID'
    if k not in sinfo:
        return [], 'no Reqiest ID for initial request found'
    rid = sinfo['Request ID']

    req_uri = URI + '?CMD=Get&RID=' + rid

    if verbose:
        print(f'  Reqiuest ID:    {rid}')
        print(f'  Reqiuest URI:   {req_uri}')

    # request search status by RID, waiting for READY
    start_time = time.time()
    while time.time() - start_time < seconds:

        rep = requests.get(req_uri, timeout=seconds)

        status = _find_status_in_html(rep.text)
        # print("Search status: ", status)

        if status == 'WAITING':
            pass
        elif status == 'READY':
            break
        else:
            return [], f'unexpected searching status={status}.'

        if verbose:
            sinfo = _find_search_info_in_html(rep.text)
            sstatus = sinfo['Time since submission']
            sys.stdout.write(f'\r  Search status:  WAITING, {sstatus} ...')
            sys.stdout.flush()

        time.sleep(3)

    if status == 'WAITING':
        return [], f'awaiting {seconds} sec expired'
    elif status != 'READY':
        return [], f'unexpected searching status={status}'

    if verbose:
        print(f'\n  Search status:  {status}\n')

    # get file with found alignments in XML format
    req = URI + '?RESULTS_FILE=on&' + \
                f'RID={rid}&FORMAT_TYPE=XML2_S&FORMAT_OBJECT=Alignment&CMD=Get'
    rep = requests.get(req, timeout=seconds)

    # for test and debug - store XML to file
    f = open("/tmp/tblastn_report.xml", "w")
    f.write(rep.text)
    f.close()

    # parse XML with alignments
    alignments = _parse_xml_report(rep.text)
    if not alignments:
        return [], 'unexpected error:  no hits in READY reply'

    return alignments, ''


# single app mode
if __name__ == "__main__":

    # tune application arguments
    descr = 'tblastn - looking for sequence in NCBI databases'
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('-s', '--sequence', help='Protein sequence',
                        required=True)
    parser.add_argument('-d', '--database', help='NCBI database name',
                        required=True)
    parser.add_argument('-t', '--taxon', help='Taxon ID', required=True)
    parser.add_argument('-w', '--seconds', help='Awaiting duration, sec',
                        required=False, nargs='?', const=1, default='60')
    args = vars(parser.parse_args())

    # check arguments
    print('\nRequest data:\n')
    print(f'  Protein sequence:  {args["sequence"]}')
    print(f'  NCBI database:     {args["database"]}')
    print(f'  Taxon ID:          {args["taxon"]}')
    print(f'  Max awaiting, s:   {args["seconds"]}')

    # do request
    print('\nDo request:\n')
    alignments, etext = tblastn_find(args['sequence'],
                                     args['database'],
                                     args['taxon'],
                                     verbose=1,
                                     seconds=int(args['seconds']))
    print('\nResult:\n')

    if etext:
        print(f'\n  Error:  {etext}')
    else:
        tblastn_print_result(alignments)
