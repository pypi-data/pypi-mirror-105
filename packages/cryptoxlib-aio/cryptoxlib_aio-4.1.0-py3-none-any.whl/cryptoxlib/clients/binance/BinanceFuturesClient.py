import ssl
import logging
from typing import List, Optional

from cryptoxlib.CryptoXLibClient import CryptoXLibClient
from cryptoxlib.clients.binance.BinanceCommonClient import BinanceCommonClient
from cryptoxlib.clients.binance.BinanceFuturesWebsocket import BinanceUSDSMFuturesWebsocket, BinanceUSDSMFuturesTestnetWebsocket
from cryptoxlib.clients.binance import enums
from cryptoxlib.clients.binance.functions import map_pair
from cryptoxlib.Pair import Pair
from cryptoxlib.WebsocketMgr import WebsocketMgr, Subscription

LOG = logging.getLogger(__name__)


class BinanceUSDSMFuturesClient(BinanceCommonClient):
    REST_API_URI = "https://fapi.binance.com/"
    FAPI_V1 = "fapi/v1/"
    FAPI_V2 = "fapi/v2/"
    FUTURES = "futures/data/"

    def __init__(self, api_key: str = None, sec_key: str = None, api_trace_log: bool = False,
                 ssl_context: ssl.SSLContext = None) -> None:
        super().__init__(api_key = api_key, sec_key = sec_key, api_trace_log = api_trace_log, ssl_context = ssl_context)

    def _get_rest_api_uri(self) -> str:
        return BinanceUSDSMFuturesClient.REST_API_URI

    def _get_websocket_mgr(self, subscriptions: List[Subscription], startup_delay_ms: int = 0,
                           ssl_context = None) -> WebsocketMgr:
        return BinanceUSDSMFuturesWebsocket(subscriptions = subscriptions, binance_client = self, api_key = self.api_key,
                                sec_key = self.sec_key, ssl_context = ssl_context)

    async def ping(self) -> dict:
        return await self._create_get("ping", api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_exchange_info(self) -> dict:
        return await self._create_get("exchangeInfo", api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_time(self) -> dict:
        return await self._create_get("time", api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_orderbook(self, pair: Pair, limit: enums.DepthLimit = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
        })

        if limit:
            params['limit'] = limit.value

        return await self._create_get("depth", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_trades(self, pair: Pair, limit: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit
        })

        return await self._create_get("trades", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_historical_trades(self, pair: Pair, limit: int = None, from_id: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "fromId": from_id
        })

        return await self._create_get("historicalTrades", params = params, headers = self._get_header(), api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_aggregate_trades(self, pair: Pair, limit: int = None, from_id: int = None,
                                   start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "fromId": from_id,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("aggTrades", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_candlesticks(self, pair: Pair, interval: enums.Interval, limit: int = None,
                               start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if interval:
            params['interval'] = interval.value

        return await self._create_get("klines", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_cont_contract_candlesticks(self, pair: Pair, interval: enums.Interval,
                                             contract_type: enums.ContractType, limit: int = None,
                               start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "pair": map_pair(pair),
            "contractType": contract_type.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if interval:
            params['interval'] = interval.value

        return await self._create_get("continuousKlines", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_index_price_candlesticks(self, pair: Pair, interval: enums.Interval,
                                             limit: int = None,
                               start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "pair": map_pair(pair),
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if interval:
            params['interval'] = interval.value

        return await self._create_get("indexPriceKlines", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_mark_price_candlesticks(self, pair: Pair, interval: enums.Interval,
                                             limit: int = None,
                               start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if interval:
            params['interval'] = interval.value

        return await self._create_get("markPriceKlines", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_mark_price(self, pair: Pair = None) -> dict:
        params = {}
        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("premiumIndex", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_fund_rate_history(self, pair: Pair = None, limit: int = None,
                                    start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("fundingRate", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_24h_price_ticker(self, pair: Pair = None) -> dict:
        params = {}
        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("ticker/24hr", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_price_ticker(self, pair: Pair = None) -> dict:
        params = {}
        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("ticker/price", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_orderbook_ticker(self, pair: Pair = None) -> dict:
        params = {}
        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("ticker/bookTicker", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    # Not maintained by binance, will be removed in the future
    async def get_all_liquidation_orders(self, pair: Pair = None, limit: int = None,
                                    start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("allForceOrders", params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_open_interest(self, pair: Pair) -> dict:
        params = {
            "symbol": map_pair(pair)
        }

        return await self._create_get("openInterest", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_open_interest_hist(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "period": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("openInterestHist", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FUTURES)

    async def get_top_long_short_account_ratio(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "period": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("topLongShortAccountRatio", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FUTURES)

    async def get_top_long_short_position_ratio(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "period": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("topLongShortPositionRatio", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FUTURES)

    async def get_global_long_short_account_ratio(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "period": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("globalLongShortAccountRatio", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FUTURES)

    async def get_taker_long_short_ratio(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "period": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("takerlongshortRatio", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FUTURES)

    async def get_blvt_candlesticks(self, pair: Pair, interval: enums.Interval,
                                     limit: int = None, start_tmstmp_ms: int = None, end_tmstmp_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "interval": interval.value,
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms
        })

        return await self._create_get("lvtKlines", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_index_info(self, pair: Pair = None) -> dict:
        params = {}
        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("indexInfo", headers = self._get_header(), params = params, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def change_position_type(self, dual_side_position: bool, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "dualSidePosition": "true" if dual_side_position else "false",
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_post("positionSide/dual", headers = self._get_header(), params = params, signed = True,
                                       api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_position_type(self, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("positionSide/dual", headers = self._get_header(), params = params, signed = True,
                                       api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_all_orders(self, pair: Pair, order_id: int = None, limit: int = None, start_tmstmp_ms: int = None,
                             end_tmstmp_ms: int = None, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "orderId": order_id,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms,
            "limit": limit,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("allOrders", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def create_order(self, pair: Pair, side: enums.OrderSide, type: enums.OrderType,
                           position_side: enums.PositionSide = None,
                           quantity: str = None,
                           price: str = None,
                           stop_price: str = None,
                           time_in_force: enums.TimeInForce = None,
                           new_client_order_id: str = None,
                           reduce_only: bool = None,
                           close_position: bool = None,
                           activation_price: str = None,
                           callback_rate: str = None,
                           working_type: enums.WorkingType = None,
                           price_protect: bool = None,
                           new_order_response_type: enums.OrderResponseType = None,
                           recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "side": side.value,
            "type": type.value,
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "newClientOrderId": new_client_order_id,
            "activationPrice": activation_price,
            "callbackRate": callback_rate,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        if price_protect is not None:
            params['priceProtect'] = "true" if price_protect else "false"

        if working_type is not None:
            params['workingType'] = working_type.value

        if position_side is not None:
            params['positionSide'] = position_side.value

        if reduce_only is not None:
            params['reduceOnly'] = "true" if reduce_only else "false"

        if close_position is not None:
            params['closePosition'] = "true" if close_position else "false"

        if time_in_force is not None:
            params['timeInForce'] = time_in_force.value

        if new_order_response_type is not None:
            params['newOrderRespType'] = new_order_response_type.value

        return await self._create_post("order", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_order(self, pair: Pair, order_id: int = None, orig_client_order_id: int = None,
                        recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "orderId": order_id,
            "origClientOrderId": orig_client_order_id,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("order", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def cancel_order(self, pair: Pair, order_id: int = None, orig_client_order_id: str = None,
                           recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "orderId": order_id,
            "origClientOrderId": orig_client_order_id,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_delete("order", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def cancel_all_orders(self, pair: Pair, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_delete("allOpenOrders", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def auto_cancel_orders(self, pair: Pair, countdown_time_ms: int, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "countdownTime": countdown_time_ms,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_delete("countdownCancelAll", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_open_order(self, pair: Pair, order_id: int = None, orig_client_order_id: int = None,
                        recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "orderId": order_id,
            "origClientOrderId": orig_client_order_id,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("openOrder", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_all_open_orders(self, pair: Pair, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("openOrders", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_balance(self, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("balance", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V2)

    async def get_account(self, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("account", headers = self._get_header(), params = params, signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V2)

    async def change_init_leverage(self, pair: Pair, leverage: int, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "leverage": leverage,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_post("leverage", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def change_margin_type(self, pair: Pair, margin_type: enums.MarginType, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "marginType": margin_type.value,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_post("marginType", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def update_isolated_position_margin(self, pair: Pair, quantity: str, type: int,
                                              position_side: enums.PositionSide = None, recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "amount": quantity,
            "type": type,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        if position_side is not None:
            params['positionSide'] = position_side.value

        return await self._create_post("positionMargin", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_position_margin_change_history(self, pair: Pair, limit: int = None, type: int = None,
                                                 start_tmstmp_ms: int = None, end_tmstmp_ms: int = None,
                                                 recv_window_ms: int = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "type": type,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms,
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        return await self._create_get("positionMargin/history", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_position(self, pair: Pair = None, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "recvWindow": recv_window_ms,
            "timestamp": self._get_current_timestamp_ms()
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("positionRisk", headers = self._get_header(), params = params, signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V2)

    async def get_account_trades(self, pair: Pair, limit: int = None, from_id: int = None,
                                 start_tmstmp_ms: int = None, end_tmstmp_ms: int = None,
                                 recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "limit": limit,
            "fromId": from_id,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms,
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        return await self._create_get("userTrades", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_income_history(self, pair: Pair = None, limit: int = None,
                                 income_type: enums.IncomeType = None,
                                 start_tmstmp_ms: int = None, end_tmstmp_ms: int = None,
                                 recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms,
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        if income_type is not None:
            params['incomeType'] = income_type.value

        return await self._create_get("income", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_notional_and_leverage_brackets(self, pair: Pair = None, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("leverageBracket", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_adl_quantile(self, pair: Pair = None, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("adlQuantile", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_force_orders(self, pair: Pair = None, limit: int = None, auto_close_type: enums.AutoCloseType = None,
                                 start_tmstmp_ms: int = None, end_tmstmp_ms: int = None,
                                 recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "limit": limit,
            "startTime": start_tmstmp_ms,
            "endTime": end_tmstmp_ms,
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        if auto_close_type is not None:
            params['autoCloseType'] = auto_close_type.value

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("forceOrders", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_api_trading_status(self, pair: Pair = None, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        if pair is not None:
            params['symbol'] = map_pair(pair)

        return await self._create_get("apiTradingStatus", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_commission_rate(self, pair: Pair, recv_window_ms: Optional[int] = None) -> dict:
        params = CryptoXLibClient._clean_request_params({
            "symbol": map_pair(pair),
            "timestamp": self._get_current_timestamp_ms(),
            "recvWindow": recv_window_ms
        })

        return await self._create_get("commissionRate", params = params, headers = self._get_header(), signed = True, api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def get_listen_key(self):
        return await self._create_post("listenKey", headers = self._get_header(), api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)

    async def keep_alive_listen_key(self, listen_key: str):
        return await self._create_put("listenKey", headers = self._get_header(), api_variable_path = BinanceUSDSMFuturesClient.FAPI_V1)


class BinanceUSDSMFuturesTestnetClient(BinanceUSDSMFuturesClient):
    REST_API_URI = "https://testnet.binancefuture.com/"

    def __init__(self, api_key: str = None, sec_key: str = None, api_trace_log: bool = False,
                 ssl_context: ssl.SSLContext = None) -> None:
        super().__init__(api_key = api_key, sec_key = sec_key, api_trace_log = api_trace_log, ssl_context = ssl_context)

    def _get_rest_api_uri(self) -> str:
        return BinanceUSDSMFuturesTestnetClient.REST_API_URI

    def _get_websocket_mgr(self, subscriptions: List[Subscription], startup_delay_ms: int = 0,
                           ssl_context = None) -> WebsocketMgr:
        return BinanceUSDSMFuturesTestnetWebsocket(subscriptions = subscriptions, binance_client = self,
                                            api_key = self.api_key,
                                            sec_key = self.sec_key, ssl_context = ssl_context)


class BinanceCOINMFuturesClient(BinanceCommonClient):
    def __init__(self, api_key: str = None, sec_key: str = None, api_trace_log: bool = False,
                 ssl_context: ssl.SSLContext = None) -> None:
        raise Exception("COIN-M Futures are not implemented at the moment!")


class BinanceCOINMFuturesTestnetClient(BinanceCommonClient):
    def __init__(self, api_key: str = None, sec_key: str = None, api_trace_log: bool = False,
                 ssl_context: ssl.SSLContext = None) -> None:
        raise Exception("COIN-M Futures are not implemented at the moment!")