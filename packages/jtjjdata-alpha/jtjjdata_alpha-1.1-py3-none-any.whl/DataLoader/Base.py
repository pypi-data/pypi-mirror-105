
#%%
from abc import ABC,abstractmethod
from . import daily,status
from .config import provider_config
#%%
class BaseProvider(ABC):

    @abstractmethod
    def daily(self,instruments,fields,start_date,end_date):
        """ daily info provider"""
        raise NotImplementedError

class LocalPorvider(BaseProvider):

    def daily(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AShareEODPrices'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fileds: 'preclose', 'open', 'high', 'low', 'close', 'change', 'pctchange',
                    'volume', 'amount', 'adjpreclose', 'adjopen', 'adjhigh', 'adjlow',
                    'adjclose', 'adjfactor', 'avgprice', 'tradestatus'
        """
        return CTDP.get_daily_share_data(instruments,fields,start_date,end_date)
    
    def daily_blocktrade(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AShareBlockTrade'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: block_price	block_volume block_amount block_frequency
        """
        return STDP.get_daily_blocktrade(instruments,fields,start_date,end_date)
    
    def daily_derivative_indi(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AShareEODDerivativeIndicator'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 's_val_mv', 's_dq_mv', 's_pq_high_52w_', 's_pq_low_52w_', 's_val_pe',
                    's_val_pb_new', 's_val_pe_ttm', 's_val_pcf_ocf', 's_val_pcf_ocfttm',
                    's_val_pcf_ncf', 's_val_pcf_ncfttm', 's_val_ps', 's_val_ps_ttm',
                    's_dq_turn', 's_dq_freeturnover', 'tot_shr_today', 'float_a_shr_today',
                    's_dq_close_today', 's_price_div_dps', 's_pq_adjhigh_52w',
                    's_pq_adjlow_52w', 'free_shares_today', 'net_profit_parent_comp_ttm',
                    'net_profit_parent_comp_lyr', 'net_assets_today',
                    'net_cash_flows_oper_act_ttm', 'net_cash_flows_oper_act_lyr',
                    'oper_rev_ttm', 'oper_rev_lyr', 'net_incr_cash_cash_equ_ttm',
                    'net_incr_cash_cash_equ_lyr', 'up_down_limit_status',
                    'lowest_highest_status'
        """
        return CTDP.get_daily_share_deridi(instruments,fields,start_date,end_date)

    def daily_dividend_rec(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AShareEXRightDividendRecord'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 'cash_dividend_ratio', 'bonus_share_ratio', 'rightsissue_ratio',
                    'rightsissue_price', 'conversed_ratio', 'seo_price', 'seo_ratio',
                    'consolidate_split_ratio'
        """
        return STDP.get_daily_share_divdrec(instruments,fields,start_date,end_date)
    
    def daily_l2indicator(self,instruments:list,fields:list,start_date:str,end_date:str):
        """
            table_name: 'AShareL2Indicators'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 's_li_initiativebuyrate', 's_li_initiativebuymoney',
                    's_li_initiativebuyamount', 's_li_initiativesellrate',
                    's_li_initiativesellmoney', 's_li_initiativesellamount',
                    's_li_largebuyrate', 's_li_largebuymoney', 's_li_largebuyamount',
                    's_li_largesellrate', 's_li_largesellmoney', 's_li_largesellamount',
                    's_li_entrustrate', 's_li_entrudifferamount', 's_li_entrudifferamoney',
                    's_li_entrustbuymoney', 's_li_entrustsellmoney',
                    's_li_entrustbuyamount', 's_li_entrustsellamount'
        """
        return CTDP.get_daily_share_l2idi(instruments,fields,start_date,end_date)
    
    def daily_margintrade(self,instruments:list,fields:list,start_date:str,end_date:str):
        """
            table_name: 'AShareMarginTrade'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 's_margin_tradingbalance', 's_margin_purchwithborrowmoney',
                    's_margin_repaymenttobroker', 's_margin_seclendingbalance',
                    's_margin_seclendingbalancevol', 's_margin_salesofborrowedsec',
                    's_margin_repaymentofborrowsec', 's_margin_margintradebalance',
                    's_refin_sl_vol_3d', 's_refin_sl_vol_7d', 's_refin_sl_vol_14d',
                    's_refin_sl_vol_28d', 's_refin_sl_vol_182d', 's_refin_sb_vol_3d',
                    's_refin_sb_vol_7d', 's_refin_sb_vol_14d', 's_sb_vol_28d',
                    's_sb_vol_182d', 's_refin_sl_eod_vol', 's_refin_sb_eod_vol',
                    's_refin_sl_eop_vol', 's_refin_sl_eop_bal', 's_refin_repay_vol'
        """
        return STDP.get_daily_margintrade(instruments,fields,start_date,end_date)

    def daily_moneyflow(self,instruments:list,fields:list,start_date:str,end_date:str):
        """
            table_name: 'AShareMoneyFlow'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 'buy_value_exlarge_order', 'sell_value_exlarge_order',
                    'buy_value_large_order', 'sell_value_large_order',
                    'buy_value_med_order', 'sell_value_med_order', 'buy_value_small_order',
                    'sell_value_small_order', 'buy_volume_exlarge_order',
                    'sell_volume_exlarge_order', 'buy_volume_large_order',
                    'sell_volume_large_order', 'buy_volume_med_order',
                    'sell_volume_med_order', 'buy_volume_small_order',
                    'sell_volume_small_order', 'trades_count', 'buy_trades_exlarge_order',
                    'sell_trades_exlarge_order', 'buy_trades_large_order',
                    'sell_trades_large_order', 'buy_trades_med_order',
                    'sell_trades_med_order', 'buy_trades_small_order',
                    'sell_trades_small_order', 'volume_diff_small_trader',
                    'volume_diff_small_trader_act', 'volume_diff_med_trader',
                    'volume_diff_med_trader_act', 'volume_diff_large_trader',
                    'volume_diff_large_trader_act', 'volume_diff_institute',
                    'volume_diff_institute_act', 'value_diff_small_trader',
                    'value_diff_small_trader_act', 'value_diff_med_trader',
                    'value_diff_med_trader_act', 'value_diff_large_trader',
                    'value_diff_large_trader_act', 'value_diff_institute',
                    'value_diff_institute_act', 's_mfd_inflowvolume',
                    'net_inflow_rate_volume', 's_mfd_inflow_openvolume',
                    'open_net_inflow_rate_volume', 's_mfd_inflow_closevolume',
                    'close_net_inflow_rate_volume', 's_mfd_inflow', 'net_inflow_rate_value',
                    's_mfd_inflow_open', 'open_net_inflow_rate_value', 's_mfd_inflow_close',
                    'close_net_inflow_rate_value', 'tot_volume_bid', 'tot_volume_ask',
                    'moneyflow_pct_volume', 'open_moneyflow_pct_volume',
                    'close_moneyflow_pct_volume', 'moneyflow_pct_value',
                    'open_moneyflow_pct_value', 'close_moneyflow_pct_value',
                    's_mfd_inflowvolume_large_order', 'net_inflow_rate_volume_l',
                    's_mfd_inflow_large_order', 'net_inflow_rate_value_l',
                    'moneyflow_pct_volume_l', 'moneyflow_pct_value_l',
                    's_mfd_inflow_openvolume_l', 'open_net_inflow_rate_volume_l',
                    's_mfd_inflow_open_large_order', 'open_net_inflow_rate_value_l',
                    'open_moneyflow_pct_volume_l', 'open_moneyflow_pct_value_l',
                    's_mfd_inflow_close_large_order', 'close_net_inflow_rate_valu_l',
                    'close_moneyflow_pct_volume_l', 'close_moneyflow_pct_value_l',
                    'buy_value_exlarge_order_act', 'sell_value_exlarge_order_act',
                    'buy_value_large_order_act', 'sell_value_large_order_act',
                    'buy_value_med_order_act', 'sell_value_med_order_act',
                    'buy_value_small_order_act', 'sell_value_small_order_act',
                    'buy_volume_exlarge_order_act', 'sell_volume_exlarge_order_act',
                    'buy_volume_large_order_act', 'sell_volume_large_order_act',
                    'buy_volume_med_order_act', 'sell_volume_med_order_act',
                    'buy_volume_small_order_act', 'sell_volume_small_order_act'
        """
        return CTDP.get_daily_moneyflow(instruments,fields,start_date,end_date) 
    
    def daily_tech_indicator(self,instruments:list,fields:list,start_date:str,end_date:str):
        """
            table_name: 'AShareTechIndicators'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 'volume_ratio_5d', 'vam_1m', 'vam_5m', 'vam_22m', 'vam_60m', 'ama_1w',
                    'ama_1m', 'ama_1q', 'vmacd', 'vmacd_dea', 'vmacd_macd', 'vosc',
                    'tapi_16d', 'tapi_6d', 'vstd_10d', 'vmacd_ema12d', 'vmacd_ema26d',
                    'vrsi_6d', 'vroc_12d', 'sobv', 'vr_26d'
        """
        return CTDP.get_daily_techindi(instruments,fields,start_date,end_date) 
    
    def daily_yield(self,instruments:list,fields:list,start_date:str,end_date:str):
        """
            table_name: 'ASWSIndexEOD'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 'pct_change_d', 'pct_change_w', 'pct_change_m', 'volume_w', 'volume_m',
                    'amount_w', 'amount_m', 'turnover_d', 'turnover_d_float', 'turnover_w',
                    'turnover_w_float', 'turnover_w_ave', 'turnover_w_ave_float',
                    'turnover_m', 'turnover_m_float', 'turnover_m_ave',
                    'turnover_m_ave_float', 'pct_change_ave_100w', 'std_deviation_100w',
                    'variance_100w', 'pct_change_ave_24m', 'std_deviation_24m',
                    'variance_24m', 'pct_change_ave_60m', 'std_deviation_60m',
                    'variance_60m', 'beta_day_1y', 'beta_day_2y', 'alpha_day_1y',
                    'alpha_day_2y', 'beta_100w', 'alpha_100w', 'beta_24m', 'beta_60m',
                    'alpha_24m', 'alpha_60m'
        """
        return CTDP.get_daily_yield(instruments,fields,start_date,end_date) 

    def daily_index(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AIndexEODPrices'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: 'preclose', 'open', 'high', 'low', 'close', 'change', 'pctchange',
                    'volume', 'amount' 
        """
        return CTDP.get_daily_index_data(instruments,fields,start_date,end_date)
    
    def daily_index_industries_eod(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: preclose open high low close change pctchange volume amount
        """
        return CTDP.get_daily_index_industries(instruments,fields,start_date,end_date)

    def daily_aswsindex_eod(self,instruments:list,fields:list,start_date:str,end_date:str):
        """ 
            table_name: 'AIndexIndustriesEODCITICS'
            input:instruments:list,fields:list,start_date:str,end_date:str
            output: DataFrame
            fields: preclose open high low close change pctchange volume amount
        """
        return CTDP.get_daily_aswsindexeod(instruments,fields,start_date,end_date)
    
    def index_member(self,indexcode:str,start_date:str =None,end_date:str = None):
        """
            table_name: 'AIndexMembers'
            input:indexcode:str,start_date:str =None,end_date:str = None
            output: DataFrame
            fields : stockcode,indate,outdate
        """
        return IMP.index_member(indexcode,start_date,end_date)

    def index_member_citics(self,indexcode:str,start_date:str =None,end_date:str = None):
        """
            table_name: 'AIndexMembersCITICS'
            input:indexcode:str,start_date:str =None,end_date:str = None
            output: DataFrame
            fields : stockcode,indate,outdate
        """
        return IMP.index_member_citics(indexcode,start_date,end_date)


CTDP = getattr(daily,provider_config["CTDP"])()
STDP = getattr(daily,provider_config["STDP"])()
IMP = getattr(status,provider_config["IMP"])()
BP = eval(provider_config["BP"])()  