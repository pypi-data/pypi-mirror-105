#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'mayanqiong'

from typing import Optional, Union

from pandas import DataFrame

from tqsdk.api import TqApi, TqAccount, TqSim, TqKq
from tqsdk import utils


def twap_table(api: TqApi, symbol: str, target_pos: int, duration: float, min_volume_each_step: int, max_volume_each_step: int,
         account: Optional[Union[TqAccount, TqKq, TqSim]] = None):
    """
    返回基于 twap 策略的计划任务时间表。下单需要配合 TargetPosScheduler 使用。

    Args:
        api (TqApi): TqApi实例，该task依托于指定api下单/撤单

        symbol (str): 拟下单的合约 symbol, 格式为 交易所代码.合约代码,  例如 "SHFE.cu1801"

        target_pos (int): 目标持仓手数

        duration (int): 算法执行的时长，以秒为单位，时长可以跨非交易时间段，但是不可以跨交易日
        * 设置为 60*10, 可以是 10:10～10:15 + 10:30~10:35

        min_volume_each_step (int): 调整持仓手数最小值，每步调整的持仓手数默认在最小和最大值中产生

        max_volume_each_step (int): 调整持仓手数最大值，每步调整的持仓手数默认在最小和最大值中产生

        account (TqAccount/TqKq/TqSim): [可选]指定发送下单指令的账户实例, 多账户模式下，该参数必须指定

    Returns:
        pandas.DataFrame: 本函数返回一个 pandas.DataFrame 实例. 表示一份计划任务时间表。每一行表示一项目标持仓任务，包含以下列:

            + interval: 当前这项任务的持续时间长度，单位为秒
            + target_pos: 当前这项任务的目标持仓
            + price: 当前这项任务的下单价格模式，支持 PASSIVE（排队价），ACTIVE（对价），None（不下单，表示暂停一段时间）

    Example1::

        from tqsdk import TqApi, TargetPosScheduler
        from tqsdk.algorithm import twap_table

        api = TqApi(auth="信易账户,用户密码")
        quote = api.get_quote("CZCE.MA109")

        # 设置twap任务参数
        time_table = twap(api, "CZCE.MA105", -100, 600, 1, 5)  # 目标持仓 -100 手，600s 内完成
        print(time_table.to_string())

        target_pos_sch = TargetPosScheduler(api, "CZCE.MA105", time_table)
        # 启动循环
        while not target_pos_sch.is_finished():
            api.wait_update()
        api.close()


    Example2::

        from tqsdk import TqApi, TargetPosScheduler
        from tqsdk.algorithm import twap_table

        api = TqApi(auth="信易账户,用户密码")
        quote = api.get_quote("CZCE.MA109")

        # 设置 twap 任务参数，
        time_table = twap_table(api, "CZCE.MA105", -100, 600, 1, 5)  # 目标持仓 -100 手，600s 内完成

        # 定制化调整 time_table，例如希望第一项任务延迟 10s 再开始下单
        # 可以在 time_table 的头部加一行
        time_table = pandas.concat([
            DataFrame([[10, 10, None]], columns=['interval', 'target_pos', 'price']),
            time_table
        ], ignore_index=True)

        target_pos_sch = TargetPosScheduler(api, "CZCE.MA105", time_table)
        while not target_pos_sch.is_finished():
            api.wait_update()

        # 获取 target_pos_sch 实例所有的成交列表
        print(target_pos_sch.trades_df)

        # 利用成交列表，您可以计算出策略的各种表现指标，例如：
        average_trade_price = sum(scheduler.trades_df['price'] * scheduler.trades_df['volume']) / sum(scheduler.trades_df['volume'])
        print("成交均价:", average_trade_price)
        api.close()
    """
    account = api._account._check_valid(account)
    if account is None:
        raise Exception(f"多账户模式下, 需要指定账户实例 account")
    min_volume_each_step = int(min_volume_each_step)
    max_volume_each_step = int(max_volume_each_step)
    if max_volume_each_step <= 0 or min_volume_each_step <= 0:
        raise Exception("请调整参数, min_volume_each_step、max_volume_each_step 必须是大于 0 的整数。")
    if min_volume_each_step > max_volume_each_step:
        raise Exception("请调整参数, min_volume_each_step 必须小于 max_volume_each_step。")

    pos = api.get_position(symbol, account)
    target_pos = int(target_pos)
    delta_pos = target_pos - pos.pos
    volume = abs(delta_pos)  # 总的下单手数

    # 得到有效的手数序列和时间间隔序列
    if volume < max_volume_each_step:
        interval_list, volume_list = [duration], [volume]
    else:
        # 先确定 volume_list 长度，interval 大小，再生成 volume_list 随机列表
        volume_list_length = volume * 2 // (min_volume_each_step + max_volume_each_step)
        interval = duration / volume_list_length
        if interval < 3:
            raise Exception("请调整参数, 每次下单时间间隔不能小于3s, 将单次下单手数阈值调大或者增长下单时间。")
        min_interval = int(max(3, interval - 2))
        max_interval = int(interval * 2 - max(3, interval - 2))
        interval_list = _gen_random_list(duration, volume_list_length, min_interval, max_interval)
        volume_list = _gen_random_list(volume, volume_list_length, min_volume_each_step, max_volume_each_step)

    time_table = DataFrame(columns=['interval', 'volume', 'price'])
    for index, volume in enumerate(volume_list):
        assert interval_list[index] >= 3
        active_interval = 2
        time_table = time_table.append([
            {"interval": interval_list[index] - active_interval, "volume": volume, "price": "PASSIVE"},
            {"interval": active_interval, "volume": 0, "price": "ACTIVE"}
        ], ignore_index=True)
    time_table['volume'] = time_table['volume'].mul(-1 if delta_pos < 0 else 1)
    time_table['target_pos'] = time_table['volume'].cumsum()
    time_table['target_pos'] = time_table['target_pos'].add(pos.pos)
    time_table.drop(columns=['volume'], inplace=True)
    time_table = time_table.astype({'target_pos': 'int64', 'interval': 'float64'})
    return time_table


def _gen_random_list(sum_val: int, length: int, min_val: int, max_val: int):
    """
    生成随机列表，参数应该满足：min_val * length <= sum_val <= max_val * length
    :param int sum_val: 列表元素之和
    :param int length: 列表长度
    :param int min_val: 列表元素最小值
    :param int max_val: 列表元素最大值
    :return: 整型列表，满足 sum(list) = sum_val, len(list) == length, min_val < any_item(list) < max_val
    """
    assert min_val * length <= sum_val <= max_val * length
    if length == 1:
        return [sum_val]
    result_list = [utils.RD.randint(min_val, max_val) for _ in range(length)]
    while sum(result_list) != sum_val:
        diff = sum_val - sum(result_list)
        sign = 1 if diff > 0 else -1
        for i in range(length):
            temp = result_list[i] + sign
            if min_val <= temp <= max_val:
                result_list[i] = temp
                if sum(result_list) == sum_val:
                    break
    assert len(result_list) == length
    assert sum(result_list) == sum_val
    return result_list
