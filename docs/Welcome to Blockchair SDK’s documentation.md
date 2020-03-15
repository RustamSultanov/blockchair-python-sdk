Welcome to Blockchair SDK’s documentation!
======================================================================================================================

 *class* `Blockchair`   Class for simple and dificult calls with filters, sorts, limits, and offset can be used as a paginator.
 
 Initialize object for work with API. For example `blockchair_api = Blockchair()` 
 
 `chain` :   possible values are BSV, BTC, BCH, LTC, ETH.

 `query`
    :   list of lists filters parametrs like `[['id',1,3,'strict'],['coinbase_data_bin','~','hello']]`.
 `offset`
    :   a natural number from 1 to 10000.

 `sort`
    :   list of lists sorts parametrs like `[['id','desc'],['size','asc']]`.
 
 `limit`
    :   a natural number from 1 to 100.



  `clear_state()`
    :   Сlear out the number of state for new request.

 `get_address`(*address*)
    :   Takes an address returns an array with one element (if the address is found), in that case the address is the key,
        :   and the value is an array consisting of the following
            elements

        Parameters:
        **address** (*str*) – a coin address
        Return dict:
        the address info what you find

 `get_block`(*block\_info*)
    :   Takes a block\_info and returns the block and addition
        information.

        Parameters:

        **block\_info** – a block id(int) or hash(str) that you want
        know the block

        Return dict:

        the block and transactions in block (only for Ethereum -
        synthetic\_transactions,uncles) what you find

 `get_blocks`(*mempool=None*)
    :   Get a list of blocks that you find.

        Parameters:

        **mempool** (*str*) – the request from mempool of blocks or no
        (Default value = None)

 `get_blocks_dashboards`(*block\_info\_list*)
    :   Takes a list block\_info\_list and returns the blocks and
        addition information.

        Parameters:

        **block\_info\_list** (*list*) – a list of block id(int) or
        hash(str) that you want know the blocks

        Return dict:

        the blocks and transactions in blocks (only for Ethereum -
        synthetic\_transactions,uncles) what you find

 `get_calls`()
    :   Get a list of ethereum calls.

        Raises:

        APIError

 `get_latest_block`()
    :   Get the latest block info.

        Return dict:

        the latest block info. If chain ethereum return array of last 6
        blocks.

 `get_nodes`()
    :   Get the nodes for a given coin

        Parameters:

        **chain** (*str*) – chain to look up, possible values are
        bitcoin-sv, bitcoin, bitcoin-cash,litecoin,

        Return dict:

        returns data on networks stats

        Raises:

        APIError

 `get_outputs`(*mempool=None*)
    :   Get a list of outputs in blockchain.

        Parameters:

        **mempool** – the request from mempool of blocks or no (Default
        value = None).

        Raises:

        APIError

 `get_priority`(*tx\_hash*)
    :   Takes a tx\_hash for mempool transactions shows priority
        (position) (for Bitcoin - by fee\_per\_kwu, for Bitcoin Cash -
        by fee\_per\_kb, for Ethereum - by gas\_price) over other
        transactions (out\_of mempool transactions).

        Parameters:

        **tx\_hash** (*str*) – a hash of an unconfirmed transaction

        Return dict:

        the unconfirmed transaction priority what you find

 `get_raw_tx`(*tx\_hash*)
    :   Takes an transaction hash and returns the hex raw transaction

        Parameters:

        **tx\_hash** (*str*) – the uncle hash that you find the uncle

        Return dict:

        the raw transaction what you find

 `get_stats`()
    :   Get the stats for a given coin

        Return dict:

        returns a dictinary with blockchain statistics

 `get_transaction`(*tx\_info*)
    :   Takes a tx\_info and returns an array with identifiers or hashes
        of transactions used as keys, and arrays of elements as keys.

        Parameters:

        **tx\_info** – an internal blockchair-id(int) or a hash of a
        transaction(str) that you want know the transaction

        Return dict:

        the transaction what you find

 `get_transactions`(*mempool=None*)
    :   Get a list of transactions in blocks that you find.

        Parameters:

        **mempool** – the request from mempool of blocks or no (Default
        value = None)

 `get_txs`(*tx\_info\_list*)
    :   Takes a list tx\_info\_list and returns an array with
        identifiers or hashes of transactions used as keys, and arrays
        of elements as keys.

        Parameters:

        **tx\_info\_list** (*list*) – a list of an internal
        blockchair-id(int) or a hash of a transactions(str) that you
        want know the transactions.

        Return dict:

        the transactions what you find.

 `get_uncle`(*uncle\_hash*)
    :   Takes an uncle\_hash and returns the information about uncle

        Parameters:

        **uncle\_hash** (*str*) – the uncle hash that you find the uncle

        Return dict:

        the uncle what you find

 `get_uncles`()
    :   Get a list of ethereum uncles.

        Raises:

        APIError

 `get_uncles_by_hash`(*uncle\_hash\_list*)
    :   Takes a list of uncle\_hash and returns the information about
        uncles

        Parameters:

        **uncle\_hash\_list** (*list*) – the list of uncle hash(str)
        that you find the uncles

        Return dict:

        the uncles what you find

 `next`(*incr=None*)
    :   Set a number of next iteration in offset.

        Parameters:

        **incr** (*int*) – the number of iteration in offset (Default
        value = None)



 `push_broadcast_tx`(*tx*)
    :   Takes a signed transaction hex binary (and chain) and broadcasts
        it to the chain network.

        Parameters:

        **tx** (*str*) – hex encoded transaction

        Return dict:

        returns a dictinary with transaction hash or error 400


