from .exceptions import FormatError
import re
import sys

LTC = 'litecoin'
BTC = 'bitcoin'
BCH = 'bitcoin-cash'
BSV = 'bitcoin-sv'
ETH = 'ethereum'
DOGE = 'dogecoin'

DOCS_URL = 'https://blockchair.com/api/docs'
API_URL = "https://api.blockchair.com/"
TIMEOUT = 10

HEX_CHARS_RE = re.compile(r'^[0-9a-f]{64}$')
DATA_TIME_CHARS_RE = re.compile(
    r'^((20|21)\d\d[-](((0[13578]|1[02])[-](0[1-9]|[12][0-9]|3[01]))|((0[469]|11)[-](0[1-9]|[12][0-9]|3[0]))|((02)[-](0[1-9]|1[0-9]|2[0-8])))\s(([0-1][0-9])|(2[0-3])):[0-5][0-9]:[0-5][0-9])$|^((20|21)\d\d[-](((0[13578]|1[02])[-](0[1-9]|[12][0-9]|3[01]))|((0[469]|11)[-](0[1-9]|[12][0-9]|3[0]))|((02)[-](0[1-9]|1[0-9]|2[0-8]))))$|^((20|21)\d\d[-](0[1-9]|1[012]))$'
)

SORT_BLOCK_LIST_BTC_LTC = [
    'id', 'hash', 'time', 'median_time', 'size', 'stripped_size', 'weight',
    'version', 'nonce', 'bits', 'difficulty', 'transaction_count',
    'witness_count', 'input_count', 'output_count', 'input_total',
    'input_total_usd', 'output_total', 'output_total_usd', 'fee_total',
    'fee_total_usd', 'fee_per_kb', 'fee_per_kb_usd', 'fee_per_kwu',
    'fee_per_kwu_usd', 'cdd_total', 'generation', 'generation_usd', 'reward',
    'reward_usd', 'guessed_miner'
]
SORT_BLOCK_LIST_BCH_BSV = [
    'id', 'hash', 'time', 'median_time', 'size', 'version', 'nonce', 'bits',
    'difficulty', 'transaction_count', 'input_count', 'output_count',
    'input_total', 'input_total_usd', 'output_total', 'output_total_usd',
    'fee_total', 'fee_total_usd', 'fee_per_kb', 'fee_per_kb_usd', 'cdd_total',
    'generation', 'generation_usd', 'reward', 'reward_usd', 'guessed_miner'
]
SORT_BLOCK_LIST_DOGE = SORT_BLOCK_LIST_BCH_BSV + \
    ['is_aux ']
SORT_BLOCK_LIST_ETH = [
    'id', 'time', 'size', 'difficulty', 'gas_used', 'gas_limit', 'uncle_count',
    'transaction_count', 'synthetic_transaction_count', 'call_count',
    'synthetic_call_count', 'value_total', 'value_total_usd',
    'internal_value_total', 'internal_value_total_usd', 'generation',
    'generation_usd', 'uncle_generation', 'uncle_generation_usd', 'fee_total',
    'fee_total_usd', 'reward', 'reward_usd'
]
SORT_TRANSACTION_LIST_BTC_LTC = [
    'block_id', 'id', 'time', 'size', 'weight', 'version', 'lock_time',
    'input_count', 'output_count', 'input_total', 'input_total_usd',
    'output_total', 'output_total_usd', 'fee', 'fee_usd', 'fee_per_kb',
    'fee_per_kb_usd', 'fee_per_kwu', 'fee_per_kwu_usd', 'cdd_total'
]
SORT_TRANSACTION_LIST_BCH_BSV = [
    'block_id', 'id', 'time', 'size', 'version', 'lock_time', 'input_count',
    'output_count', 'input_total', 'input_total_usd', 'output_total',
    'output_total_usd', 'fee', 'fee_usd', 'fee_per_kb', 'fee_per_kb_usd',
    'cdd_total'
]
SORT_TRANSACTION_LIST_ETH = [
    'block_id', 'id', 'index', 'time', 'size', 'call_count', 'value',
    'value_usd', 'internal_value', 'internal_value_usd', 'fee', 'fee_usd',
    'gas_used', 'gas_limit', 'gas_price'
]
SORT_OUTPUT_LIST = [
    'block_id', 'transaction_id', 'index', 'time', 'value', 'value_usd',
    'recipient', 'type', 'spending_block_id', 'spending_transaction_id',
    'spending_index', 'spending_time', 'spending_value_usd',
    'spending_sequence', 'lifespan', 'cdd'
]
SORT_CALL_LIST = [
    'block_id', 'transaction_id', 'index', 'depth', 'time', 'child_call_count',
    'value', 'value_usd'
]
SORT_UNCLE_LIST = [
    'parent_block_id', 'index', 'time', 'size', 'difficulty', 'gas_used',
    'gas_limit', 'generation', 'generation_usd'
]

QUERY_BLOCK_LIST_BTC_LTC = SORT_BLOCK_LIST_BTC_LTC + \
    ['coinbase_data_bin', 'coinbase_data_hex']
QUERY_BLOCK_LIST_BCH_BSV_DOGE = SORT_BLOCK_LIST_BCH_BSV + \
    ['coinbase_data_bin', 'coinbase_data_hex']
QUERY_BLOCK_LIST_ETH = SORT_BLOCK_LIST_ETH + \
    ['hash', 'miner', 'extra_data_bin', 'extra_data_hex']
QUERY_TRANSACTION_LIST_BTC_LTC = SORT_TRANSACTION_LIST_BTC_LTC + \
    ['hash', 'is_coinbase', 'has_witness']
QUERY_TRANSACTION_LIST_BCH_BSV = SORT_TRANSACTION_LIST_BCH_BSV + \
    ['hash', 'is_coinbase']
QUERY_TRANSACTION_LIST_ETH = SORT_TRANSACTION_LIST_ETH + \
    ['hash', 'type', 'sender', 'recipient', 'input_hex', 'input_bin']
QUERY_OUTPUT_LIST = SORT_OUTPUT_LIST + \
    ['script_bin', 'is_spent', 'is_spendable', 'is_from_coinbase', 'script_hex']
QUERY_CALL_LIST = SORT_CALL_LIST + \
    ['failed', 'fail_reason', 'type', 'sender', 'recipient', 'transferred']
QUERY_UNCLE_LIST = SORT_UNCLE_LIST + \
    ['hash', 'miner', 'extra_data_hex', 'extra_data_bin']

py_version = sys.version_info[0]
if py_version >= 3:
    # Python 3.0 and later
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.parse import urlencode
else:
    # Python 2.x
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib import urlencode


def call_api(resource, chain='bitcoin', data=None, api_url=None):
    api_url = API_URL if api_url is None else api_url
    try:
        payload = None if data is None else urlencode(data)
        if py_version >= 3 and payload is not None:
            payload = payload.encode('UTF-8')
        response = urlopen(api_url + chain + resource,
                           payload, timeout=TIMEOUT).read()
        return handle_response(response)
    except HTTPError as e:
        raise e


def handle_response(response):
    """Urllib returns different types in Python 2 and 3 (str vs bytes)"""
    if isinstance(response, str):
        return response
    else:
        return response.decode('utf-8')


def is_valid_chain(chain):
    if not (chain is BTC or chain is BCH or chain is LTC or chain is BSV or
            chain is ETH or chain is DOGE):
        raise FormatError(
            "Incorrect chain value. Currently supports BTC, BCH, BSV, LTC, ETH, DOGE."
        )


def is_valid_query(query_list):
    if isinstance(query_list, list):
        if len(query_list) <= 5:
            for elem in query_list:
                if isinstance(elem, list):
                    if 1 < len(elem) <= 4:
                        if len(elem) == 2:
                            if elem[0] == 'time':
                                if type(elem[1]) == str:
                                    if bool(DATA_TIME_CHARS_RE.match(elem[1])):
                                        continue
                                    else:
                                        raise FormatError(
                                            '''Incorrect format of field 'time'. Must be 'YYYY-MM-DD HH:ii:ss' or 'YYYY-MM-DD' or 'YYYY-MM'.''')
                                else:
                                    mesg = '''Incorrect type of field 'time' parametr.  You take ''' + \
                                        type(elem[1]).__name__ + \
                                        ". Must be str."
                                    raise FormatError(mesg)
                            else:
                                if type(elem[1]) == int or type(elem[1]) == str or type(elem[1]) == float:
                                    continue
                                else:
                                    mesg = '''Incorrect type of query parametr.  You take ''' + \
                                        type(
                                            elem[1]).__name__ + ". Must be str, int or float. Check your list."
                                    raise FormatError(mesg)
                        elif len(elem) == 3:
                            if elem[0] == 'time':
                                if type(elem[1]) == str:
                                    if bool(DATA_TIME_CHARS_RE.match(elem[1])):
                                        if elem[2] == '<=' or elem[2] == '>=' or elem[2] == '<' or elem[2] == '>':
                                            continue
                                        else:
                                            raise FormatError(
                                                '''Incorrect inequality parametr. Must be '<=', '>=', '<' or '>'.''')
                                    else:
                                        raise FormatError(
                                            '''Incorrect format of field 'time'. Must be 'YYYY-MM-DD HH:ii:ss' or 'YYYY-MM-DD' or 'YYYY-MM'.''')
                                else:
                                    mesg = '''Incorrect type of field 'time' parametr.  You take ''' + \
                                        type(elem[1]).__name__ + \
                                        ". Must be str."
                                    raise FormatError(mesg)
                            else:
                                if type(elem[1]) == int or type(elem[1]) == float:
                                    if elem[2] == '<=' or elem[2] == '>=' or elem[2] == '<' or elem[2] == '>':
                                        continue
                                    else:
                                        raise FormatError(
                                            '''Incorrect inequality parametr. Must be '<=', '>=', '<' or '>'.''')
                                elif type(elem[1]) == str:
                                    if elem[1] == '^' or elem[1] == '~':
                                        if type(elem[2]) == str:
                                            continue
                                        else:
                                            mesg = '''Incorrect type of query parametr.  You take ''' + \
                                                type(elem[2]).__name__ + \
                                                ". Must be str."
                                            raise FormatError(mesg)
                                    else:
                                        raise FormatError(
                                            '''Incorrect search parametr. Must be '^' or '~'.''')
                                else:
                                    mesg = '''Incorrect type of query parametr.  You take ''' + \
                                        type(elem[1]).__name__ + \
                                        ". Must be str, int or float."
                                    raise FormatError(mesg)
                        elif len(elem) == 4:
                            if elem[0] == 'time':
                                if type(elem[1]) == str:
                                    if bool(DATA_TIME_CHARS_RE.match(elem[1])) and bool(DATA_TIME_CHARS_RE.match(elem[2])):
                                        if elem[3] == 'strict' or elem[3] == 'non-strict':
                                            continue
                                        else:
                                            raise FormatError(
                                                '''Incorrect inequality parametr. Must be 'strict' or 'non-strict'.''')
                                    else:
                                        raise FormatError(
                                            '''Incorrect format of field 'time'. Must be 'YYYY-MM-DD HH:ii:ss' or 'YYYY-MM-DD' or 'YYYY-MM'.''')
                                else:
                                    mesg = '''Incorrect type of field 'time' parametr.  You take ''' + \
                                        type(elem[1]).__name__ + \
                                        ". Must be str."
                                    raise FormatError(mesg)
                            else:
                                if type(elem[1]) == int or type(elem[1]) == float or type(elem[1]) == int or type(elem[1]) == float:
                                    if elem[3] == 'strict' or elem[3] == 'non-strict':
                                        continue
                                    else:
                                        raise FormatError(
                                            '''Incorrect inequality parametr. Must be 'strict' or 'non-strict'.''')
                                else:
                                    mesg = '''Incorrect type of query parametr.  You take ''' + \
                                        type(elem[1]).__name__ + ' ,'+type(elem[2]
                                                                           ).__name__ + ". Must be int or float."
                                    raise FormatError(mesg)
                    else:
                        raise FormatError(
                            'Len of element query list must be maximum 4, minimum 2')
                else:
                    mesg = "Incorrect query value. You take " + \
                        type(elem).__name__ + ". Must be list"
                    raise FormatError(mesg)
            else:
                return True
        else:
            raise FormatError('Len of query list must be maximum 5')
    else:
        mesg = "Incorrect query value. You take " + \
            type(query_list).__name__ + ". Must be list"
        raise FormatError(mesg)


def is_valid_block_query(query_list, query_block_list=QUERY_BLOCK_LIST_BTC_LTC):
    for query in query_list:
        field = query[0]
        if field in query_block_list:
            continue
        else:
            raise FormatError('''Incorrect query field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_tx_query(query_list, query_tx_list=QUERY_TRANSACTION_LIST_BTC_LTC):
    for query in query_list:
        field = query[0]
        if field in query_tx_list:
            continue
        else:
            raise FormatError('''Incorrect query field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_output_query(query_list, query_output_list=QUERY_OUTPUT_LIST):
    for query in query_list:
        field = query[0]
        if field in query_output_list:
            continue
        else:
            raise FormatError('''Incorrect query field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_call_query(query_list, query_call_list=QUERY_CALL_LIST):
    for query in query_list:
        field = query[0]
        if field in query_call_list:
            continue
        else:
            raise FormatError('''Incorrect query field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_uncle_query(query_list, query_uncle_list=QUERY_UNCLE_LIST):
    for query in query_list:
        field = query[0]
        if field in query_uncle_list:
            continue
        else:
            raise FormatError('''Incorrect query field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_uncle_sort(sort_list, sort_uncle_list=SORT_UNCLE_LIST):
    for sort in sort_list:
        field = sort[0]
        if field in sort_uncle_list:
            continue
        else:
            raise FormatError('''Incorrect sort field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_call_sort(sort_list, sort_call_list=SORT_CALL_LIST):
    for sort in sort_list:
        field = sort[0]
        if field in sort_call_list:
            continue
        else:
            raise FormatError('''Incorrect sort field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_output_sort(sort_list, sort_output_list=SORT_OUTPUT_LIST):
    for sort in sort_list:
        field = sort[0]
        if field in sort_output_list:
            continue
        else:
            raise FormatError('''Incorrect sort field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_block_sort(sort_list, sort_block_list=SORT_BLOCK_LIST_BTC_LTC):
    for sort in sort_list:
        field = sort[0]
        if field in sort_block_list:
            continue
        else:
            raise FormatError('''Incorrect sort field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_tx_sort(sort_list, sort_tx_list=SORT_TRANSACTION_LIST_BTC_LTC):
    for sort in sort_list:
        field = sort[0]
        if field in sort_tx_list:
            continue
        else:
            raise FormatError('''Incorrect sort field. You take field "''' +
                              field + '''". Check your field in API docs. '''+DOCS_URL)
    else:
        return True


def is_valid_sort(sort_list):
    if isinstance(sort_list, list):
        if len(sort_list) <= 2:
            for elem in sort_list:
                if isinstance(elem, list):
                    if len(elem) == 2:
                        if type(elem[0]) == str:
                            if elem[1] == 'desc' or elem[1] == 'asc':
                                continue
                            else:
                                raise FormatError(
                                    '''Incorrect sort parametr. Must be 'asc' or 'desc'. Check your list.''')
                        else:
                            mesg = "Incorrect type of sort field. You take " + \
                                type(elem[0]).__name__ + ". Must be str"
                            raise FormatError(mesg)
                    else:
                        raise FormatError('Len of element sort list must be 2')
                else:
                    mesg = "Incorrect sort value. You take " + \
                        type(elem).__name__ + ". Must be list"
                    raise FormatError(mesg)
            else:
                return True
        else:
            raise FormatError('Len of sort list must be 1 or 2')
    else:
        mesg = "Incorrect sort value. You take " + \
            type(sort_list).__name__ + ". Must be list"
        raise FormatError(mesg)


def is_valid_limit(limit):
    if isinstance(limit, int):
        if limit <= 100:
            if 0 <= limit:
                return True
            else:
                raise FormatError('Incorrect limit value.')
        else:
            raise FormatError(
                "Limit value can't be larger than 100. Please use export functions to get larger amounts of data.")
    else:
        mesg = "Incorrect limit value. You take " + \
            type(limit).__name__ + ". Must be int"
        raise FormatError(mesg)


def is_valid_offset(offset):
    if isinstance(offset, int):
        if offset <= 10000:
            if 0 <= offset:
                return True
            else:
                raise FormatError('Incorrect offset value.')
        else:
            raise FormatError(
                "Offset value can't be larger than 10000. Please use export functions to get larger amounts of data.")
    else:
        mesg = "Incorrect offset value. You take " + \
            type(offset).__name__ + ". Must be int"
        raise FormatError(mesg)


def uses_only_hash_chars(string):
    return bool(HEX_CHARS_RE.match(string))


def is_valid_hash(string):
    string = str(string)  # in case of being passed an int
    if len(string.strip()) == 64 and uses_only_hash_chars(string):
        return True
    else:
        raise FormatError("Incorrect block hash. Please, check your hash")


def is_valid_ethereum_hash(string):
    string = str(string)
    hex_chars_re = re.compile(r'^0x[0-9a-f]{64}$')
    if len(string.strip()) == 66 and bool(hex_chars_re.match(string)):
        return True
    else:
        raise FormatError("Incorrect block hash. Please, check your hash")


def is_valid_addr(string):
    hex_chars_re = re.compile(r'[0-9a-zA-Z\-]*')
    if (25 < len(string) < 35) and bool(hex_chars_re.match(string)):
        return True
    else:
        raise FormatError("Incorrect address. Please, check your address")


def is_valid_ethereum_addr(string):
    hex_chars_re = re.compile('^0x[0-9a-fA-F]{40}$')
    if bool(hex_chars_re.match(string)):
        return True
    else:
        raise FormatError(
            "Incorrect ethereum address. Please, check your address")


def is_valid_block_num(block_num):
    if 0 <= block_num <= 10**8:  # hackey approximation
        return True
    else:
        raise FormatError("Incorrect block id. Please, check your id")


def is_valid_blockchair_id(block_num):
    if 0 <= block_num:
        return True
    else:
        raise FormatError(
            "Incorrect transaction blockchair id. Please, check your id")


def search_value(d, key, default=None):
    """Return a value corresponding to the specified key in the (possibly
    nested) dictionary d. If there is no item with that key, return
    default."""
    stack = [iter(d.items())]
    while stack:
        for k, v in stack[-1]:
            if isinstance(v, dict):
                stack.append(iter(v.items()))
                break
            elif k == key:
                return v
        else:
            stack.pop()
    return default
