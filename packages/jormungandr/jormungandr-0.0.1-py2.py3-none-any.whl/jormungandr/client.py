"""base client for api calls"""

from typing import Dict, Optional, List, Tuple

import requests
import time


class BaseClient:
    def __init__(self, testnet: bool = False):

        """
        Midgard API Client Constructor.

        :param testnet: Select Testnet to query. False = Mainnet.
        :type testnet: bool
        """
        _base_url = "https://midgard.thorchain.info/"
        self.HEALTH = _base_url + "v2/health"
        self.POOLS = _base_url + "v2/pools"
        # NOTE - there is a distinction between POOLS and POOL!!!
        self.POOL = _base_url + "v2/pool"
        self.HISTORY = _base_url + "v2/history"
        self.HISTORIC_DEPTH_PRICE = _base_url + "v2/history/depths"
        self.NODES = _base_url + "v2/nodes"
        self.ACTIONS = _base_url + "v2/actions"
        self.MEMBERS_LIST = _base_url + "v2/members"
        # NOTE - there is a desticntion between members and member!!!
        self.MEMBER_DETAILS = _base_url + "v2/member"  # /{address}
        self.STATS = _base_url + "v2/stats"
        self.NETWORK = _base_url + "v2/network"

    def _get_response_json(self, url_query: str) -> Dict:
        """
        """
        try:
            r = requests.get(url_query)
            response_dict = r.json()

            return response_dict

        # TODO: make more specific
        except Exception as e:
            print("Opps!", e.__class_, "occured.")
            print(e)

    def get_pool_list(self) -> Dict:

        """
        Returns a dictionary containing details for LP pools.

        Source:
        https://testnet.midgard.thorchain.info/v2/doc#operation/GetPools
        """

        return self._get_response_json(self.POOLS)

    def get_pool_details_data(self, asset: str) -> Dict:

        """
        Returns details of the pool: depths, price, 24h volume, APY.
        Note: Asset names follow pattern: <chain>.<asset>, `BNB.BTC`  

        :param asset: String for asset, Example: BNB.TOMOB-1E1.

        Source:
        https://testnet.midgard.thorchain.info/v2/doc#operation/GetPools
        """

        return self._get_response_json(self.POOL + f"/{asset}")

    def get_pool_statistics(self, asset: str) -> Dict:

        # TODO update Doc string
        """
        Returns statistics about the pool. 

        For drill down of historic values use XXX

        :param asset: String for asset, Example: BNB.TOMOB-1E1.

        Source:
        https://testnet.midgard.thorchain.info/v2/doc#operation/GetPools
        """

        return self._get_response_json(self.POOL + f"/{asset}/stats")

    # TODO - add better handling for historic data here...
    # need time / date helper functions.
    def get_pool_depth_price_history(self, asset: str) -> Dict:

        # TODO update Doc string
        """
        NOTE: this function is incomplete, additional time/date functionality will be added in the future.

        Returns the asset and rune depths and price. The values report the state
        at the end of each interval.

        :param asset: String for asset, Example: BNB.TOMOB-1E1.

        Source:
        https://testnet.midgard.thorchain.info/v2/doc#operation/GetDepthHistory
        """

        return self._get_response_json(self.HISTORIC_DEPTH_PRICE + f"/{asset}")

    def get_pool_earnings_history(self, asset: str) -> Dict:

        #
        """
        NOTE: This function is incomplete - time functionality needs to be added.
        Returns earning data for the specified interval.

        NOTE: if using invervals only first 400 observations will be returned.

        """
        return self._get_response_json(self.HISTORY + "/earnings")

    def get_pool_swap_history(self, asset: Optional[str]) -> Dict:
        # TODO: Add time functionality...
        """
        Returns swap count, volume, fees, slip in specified interval. 
        If pool is not specified returns for all pools.
        Source:
            https://testnet.midgard.thorchain.info/v2/doc#operation/GetSwapHistory
        """
        return self._get_response_json(self.HISTORY + "/swaps")

    def get_TVL_history(self) -> Dict:
        # TODO - add time funcs
        """
        Total Value Locked History

        Returns total pool depths, total bonds, and total value locked in specified interval.
        Total Value Locked = Total Bonds + 2 * Total Pool Depths
        """

        return self._get_response_json(self.HISTORY + "/tvl")

    def get_liquidity_change_history(self) -> Dict:
        # TODO - Add time funcs
        """
        Returns withdrawals and deposits for given time interval. 
        If pool is not specified returns for all pools.
        
        Source: 
            https://testnet.midgard.thorchain.info/v2/doc#operation/GetLiquidityHistory
        """
        return self._get_response_json(self.HISTORY + "/liquidity_changes")

    def get_node_list(self) -> Dict:
        """
        Nodes List
        Returns a list of Node public keys and adresses.
        
        """

        return self._get_response_json(self.NODES)

    def get_network_data(self) -> Dict:

        """
        Returns a dictionary containing data on ThorChain Network.

        Source:
        https://testnet.midgard.thorchain.info/v2/doc#operation/GetNetworkData 
        """

        return self._get_response_json(self.NETWORK)

    def get_actions_list() -> Dict:

        # TODO - add support for pagination and filters!
        """
        Actions List
        List actions along with their related transactions. 
        An action is generated by one or more inbound transactions with the
        intended action set in the transaction memo.
        The action may result in one or more outbound transactions.
        Results are paginated by sets of 50. Filters may be applied to query actions.
        
        Source: 
            https://testnet.midgard.thorchain.info/v2/doc#operation/GetActions
        """

        return self._get_response_json(self.ACTIONS)

    def get_members_list(self):

        """

        """

        return _get_response_json(self.MEMBERS_LIST)

    def get_member_details(self, address: Optional[str]):

        """
        Source:
            https://testnet.midgard.thorchain.info/v2/doc#operation/GetMemberDetail
        """
        return _get_response_json(self.MEMBER_DETAILS)
