# %%
from abc import ABC, abstractmethod
from . import daily, status
from .config import provider_config


# %%
class BaseProvider(ABC):

    @abstractmethod
    def daily(self, instruments, fields, start_date, end_date):
        """ daily info provider"""
        raise NotImplementedError


class LocalPorvider(BaseProvider):

    def daily(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fileds: 'preclose', 'open', 'high', 'low', 'close', 'change', 'pctchange',
                    'volume', 'amount', 'adjpreclose', 'adjopen', 'adjhigh', 'adjlow',
                    'adjclose', 'adjfactor', 'avgprice', 'tradestatus'
        """
        return TDP.get_daily_share_data(instruments, fields, start_date, end_date)

    def daily_blocktrade(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fields: block_price	block_volume block_amount block_frequency
        """
        return TDP.get_daily_blocktrade(instruments, fields, start_date, end_date)

    def daily_derivative_indi(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
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
        return TDP.get_daily_share_deridi(instruments, fields, start_date, end_date)

    def daily_dividend_rec(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fields: 'cash_dividend_ratio', 'bonus_share_ratio', 'rightsissue_ratio',
                    'rightsissue_price', 'conversed_ratio', 'seo_price', 'seo_ratio',
                    'consolidate_split_ratio'
        """
        return TDP.get_daily_share_divdrec(instruments, fields, start_date, end_date)

    def daily_l2indicator(self, instruments: list, fields: list, start_date: str, end_date: str):
        """
            fields: 's_li_initiativebuyrate', 's_li_initiativebuymoney',
                    's_li_initiativebuyamount', 's_li_initiativesellrate',
                    's_li_initiativesellmoney', 's_li_initiativesellamount',
                    's_li_largebuyrate', 's_li_largebuymoney', 's_li_largebuyamount',
                    's_li_largesellrate', 's_li_largesellmoney', 's_li_largesellamount',
                    's_li_entrustrate', 's_li_entrudifferamount', 's_li_entrudifferamoney',
                    's_li_entrustbuymoney', 's_li_entrustsellmoney',
                    's_li_entrustbuyamount', 's_li_entrustsellamount'
        """
        return TDP.get_daily_share_l2idi(instruments, fields, start_date, end_date)

    def daily_margintrade(self, instruments: list, fields: list, start_date: str, end_date: str):
        """
            fields: 
        """
        return TDP.get_daily_margintrade(instruments, fields, start_date, end_date)

    def daily_moneyflow(self, instruments: list, fields: list, start_date: str, end_date: str):
        """
            fields: 
        """
        return TDP.get_daily_moneyflow(instruments, fields, start_date, end_date)

    def daily_tech_indicator(self, instruments: list, fields: list, start_date: str, end_date: str):
        """
            fields: 
        """
        return TDP.get_daily_techindi(instruments, fields, start_date, end_date)

    def daily_yield(self, instruments: list, fields: list, start_date: str, end_date: str):
        """
            fields: 
        """
        return TDP.get_daily_yield(instruments, fields, start_date, end_date)

    def daily_index(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fields: 'preclose', 'open', 'high', 'low', 'close', 'change', 'pctchange',
                    'volume', 'amount' 
        """
        return TDP.get_daily_index_data(instruments, fields, start_date, end_date)

    def daily_index_industries_eod(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fields: preclose open high low close change pctchange volume amount
        """
        return TDP.get_daily_index_industries(instruments, fields, start_date, end_date)

    def daily_aswsindex_eod(self, instruments: list, fields: list, start_date: str, end_date: str):
        """ 
            fields: preclose open high low close change pctchange volume amount
        """
        return TDP.get_daily_aswsindexeod(instruments, fields, start_date, end_date)

    def index_member(self, instruments: list, trade_date: str, start_date: str, end_date: str):
        return StatusP.index_member()

    def index_member_citics(self, instruments: list, trade_date: str, start_date: str, end_date: str):
        return StatusP.index_member()


TDP = getattr(daily, provider_config["TDP"])()
StatusP = getattr(status, provider_config["StatusP"])()
BP = eval(provider_config["BP"])()
