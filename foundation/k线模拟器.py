import time
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

try:
    import requests
except ImportError:
    requests = None


class KLineSimulator:
    def __init__(self, start_price=100, days=30, seed=None):
        self.start_price = start_price
        self.days = days
        self.seed = seed
        self.prices = []
        self.dates = []
        self.volumes = []
        self.source_name = "增强模拟数据"
        self.symbol = "SIM"
        self.stock_name = "模拟标的"

    @staticmethod
    def _infer_market(symbol):
        """根据股票代码推断交易所，返回东方财富 secid 前缀。"""
        if symbol.startswith(("6", "9")):
            return "1"  # 上交所
        return "0"  # 深交所 / 北交所

    @staticmethod
    def _safe_int(text, default_value):
        try:
            return int(text)
        except (TypeError, ValueError):
            return default_value

    @staticmethod
    def _moving_average(values, window):
        arr = np.asarray(values, dtype=float)
        ma = np.full(arr.shape, np.nan)
        if arr.size < window:
            return ma
        kernel = np.ones(window, dtype=float) / window
        ma_valid = np.convolve(arr, kernel, mode="valid")
        ma[window - 1:] = ma_valid
        return ma

    def generate_data(self):
        """生成更贴近真实市场的模拟K线：波动聚集 + 跳空 + 肥尾收益。"""
        self.prices = []
        self.dates = []
        self.volumes = []
        self.source_name = "增强模拟数据"
        self.symbol = "SIM"
        self.stock_name = "模拟标的"

        rng = np.random.default_rng(self.seed)
        current_price = self.start_price
        current_date = datetime.now() - timedelta(days=int(self.days * 1.8) + 3)
        volatility = 0.02
        base_vol = 0.016
        prev_return = 0.0
        drift = 0.0003

        while len(self.prices) < self.days:
            current_date += timedelta(days=1)
            if current_date.weekday() >= 5:
                continue  # 仅保留交易日

            # 偶发切换市场状态（趋势变化）
            if rng.random() < 0.08:
                drift = rng.uniform(-0.0015, 0.0018)

            # GARCH风格的波动聚集：大波动后更容易继续大波动
            volatility = 0.12 * base_vol + 0.22 * abs(prev_return) + 0.74 * volatility
            volatility = float(np.clip(volatility, 0.006, 0.06))

            # 隔夜跳空
            overnight_gap = rng.normal(0.0, volatility * 0.35)
            if rng.random() < 0.03:
                overnight_gap += rng.normal(0.0, volatility * 2.5)

            open_price = max(0.5, current_price * np.exp(overnight_gap))

            # 肥尾分布 + 跳跃项，模拟突发消息带来的极端行情
            heavy_tail_noise = rng.standard_t(df=4) * volatility
            jump_term = rng.normal(0.0, volatility * 2.8) if rng.random() < 0.03 else 0.0
            intraday_return = drift + 0.15 * prev_return + heavy_tail_noise + jump_term
            intraday_return = float(np.clip(intraday_return, -0.12, 0.12))

            close_price = max(0.5, open_price * np.exp(intraday_return))

            # 影线长度与波动率、实体长度相关
            candle_range = abs(intraday_return) + volatility * rng.uniform(0.8, 1.8)
            up_wick = candle_range * rng.uniform(0.2, 0.8)
            down_wick = candle_range * rng.uniform(0.2, 0.8)

            high_price = max(open_price, close_price) * (1 + up_wick)
            low_price = min(open_price, close_price) * max(0.001, (1 - down_wick))

            # 成交量与绝对涨跌幅正相关
            volume = 1_000_000 * (1 + 7 * abs(intraday_return) + rng.lognormal(-0.1, 0.35))

            self.prices.append([open_price, high_price, low_price, close_price])
            self.dates.append(current_date)
            self.volumes.append(float(volume))

            current_price = close_price
            prev_return = intraday_return

    def fetch_eastmoney_kline(self, symbol="000001", days=240, adjust="qfq", klt=101, timeout=10):
        """抓取东方财富真实K线数据并写入当前实例。"""
        if requests is None:
            raise ImportError("未安装 requests，请先执行: pip install requests")

        symbol = str(symbol).strip()
        if not (symbol.isdigit() and len(symbol) == 6):
            raise ValueError("股票代码必须是6位数字，例如 600519 或 000001")

        fqt_map = {"none": 0, "qfq": 1, "hfq": 2}
        fqt = fqt_map.get(adjust, 1)

        # 某些网络环境下 https 会偶发断连，增加多协议与多域名兜底。
        url_candidates = [
            "https://push2his.eastmoney.com/api/qt/stock/kline/get",
            "http://push2his.eastmoney.com/api/qt/stock/kline/get",
            "https://push2.eastmoney.com/api/qt/stock/kline/get",
        ]

        market = self._infer_market(symbol)
        alt_market = "1" if market == "0" else "0"
        secid_candidates = [f"{market}.{symbol}", f"{alt_market}.{symbol}"]

        end_date = datetime.now().strftime("%Y%m%d")
        beg_date = (datetime.now() - timedelta(days=max(120, int(days * 2.5)))).strftime("%Y%m%d")

        base_params = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": klt,
            "fqt": fqt,
            "beg": beg_date,
            "end": end_date,
            "lmt": max(30, int(days) * 2),
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        }
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "close",
            "Referer": "https://quote.eastmoney.com/",
        }

        session = requests.Session()
        try:
            # 使用 urllib3 Retry 适配器处理瞬时断连、429、5xx 等情况。
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            retry = Retry(
                total=3,
                connect=3,
                read=3,
                backoff_factor=0.8,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=frozenset(["GET"]),
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
        except Exception:
            pass

        payload = None
        data = None
        error_messages = []

        for secid in secid_candidates:
            for url in url_candidates:
                for attempt in range(1, 4):
                    params = dict(base_params)
                    params["secid"] = secid

                    try:
                        response = session.get(url, params=params, headers=headers, timeout=(5, timeout))
                        response.raise_for_status()
                        payload = response.json()
                        data = payload.get("data") if isinstance(payload, dict) else None

                        if data and data.get("klines"):
                            break

                        error_messages.append(
                            f"{url} secid={secid} 返回空数据"
                        )
                        # 返回空数据通常不是瞬时错误，直接切换下一个 secid/url 组合。
                        break
                    except requests.exceptions.RequestException as exc:
                        msg = (
                            f"{url} secid={secid} attempt={attempt} "
                            f"{exc.__class__.__name__}: {exc}"
                        )
                        error_messages.append(msg)
                        time.sleep(0.6 * attempt)
                    except ValueError as exc:
                        error_messages.append(
                            f"{url} secid={secid} JSON解析失败: {exc}"
                        )
                        break

                if data and data.get("klines"):
                    break
            if data and data.get("klines"):
                break

        if not data or not data.get("klines"):
            tail_errors = " | ".join(error_messages[-4:]) if error_messages else "无详细错误"
            raise RuntimeError(
                "东方财富接口请求失败（已重试并切换协议）。"
                f"\n最近错误: {tail_errors}"
                "\n可尝试: 1) 稍后重试 2) 切换网络/代理 3) 关闭本机抓包或拦截软件"
            )

        prices = []
        dates = []
        volumes = []
        for item in data["klines"]:
            parts = item.split(",")
            if len(parts) < 6:
                continue

            try:
                dt = datetime.strptime(parts[0], "%Y-%m-%d")
                open_p = float(parts[1])
                close_p = float(parts[2])
                high_p = float(parts[3])
                low_p = float(parts[4])
                vol = float(parts[5])
            except (TypeError, ValueError):
                continue

            # 清洗异常记录：非正价格、OHLC逻辑不成立的数据会干扰收益率与波动率。
            if min(open_p, high_p, low_p, close_p) <= 0:
                continue
            if high_p < max(open_p, close_p) or low_p > min(open_p, close_p):
                continue
            vol = max(vol, 0.0)

            prices.append([open_p, high_p, low_p, close_p])
            dates.append(dt)
            volumes.append(vol)

        if not prices:
            raise RuntimeError("解析后无有效K线数据")

        # 防止接口返回超长历史：按日期排序后仅保留最近 N 天。
        rows = sorted(zip(dates, prices, volumes), key=lambda x: x[0])
        keep_days = max(30, int(days))
        rows = rows[-keep_days:]
        dates = [row[0] for row in rows]
        prices = [row[1] for row in rows]
        volumes = [row[2] for row in rows]

        self.prices = prices
        self.dates = dates
        self.volumes = volumes
        self.days = len(prices)
        self.start_price = prices[0][0]
        self.source_name = "东方财富真实数据"
        self.symbol = symbol
        self.stock_name = data.get("name", symbol)

        return len(prices)

    def _classify_last_candle(self):
        open_p, high_p, low_p, close_p = self.prices[-1]
        body = abs(close_p - open_p)
        candle_range = max(high_p - low_p, 1e-9)
        upper_wick = high_p - max(open_p, close_p)
        lower_wick = min(open_p, close_p) - low_p

        body_ratio = body / candle_range
        upper_ratio = upper_wick / candle_range
        lower_ratio = lower_wick / candle_range

        if body_ratio <= 0.12:
            if lower_ratio > 0.45 and upper_ratio < 0.25:
                return "锤子线候选", "下影线明显长于实体，若处于下跌末端可能出现止跌信号。"
            if upper_ratio > 0.45 and lower_ratio < 0.25:
                return "上吊线/倒锤线候选", "上影线较长，表示高位抛压较大，需结合后续K线确认。"
            return "十字星/纺锤线", "实体较小，多空力量暂时平衡，后续方向需看放量突破。"

        if close_p > open_p and body_ratio > 0.6:
            return "大阳线", "买盘主动性强，短线动量偏多。"
        if close_p < open_p and body_ratio > 0.6:
            return "大阴线", "卖压集中释放，短线动量偏空。"
        return "普通实体K线", "趋势延续或震荡中的常见形态，建议结合均线和成交量判断。"

    def _calculate_metrics(self):
        arr = np.asarray(self.prices, dtype=float)
        open_arr = arr[:, 0]
        high_arr = arr[:, 1]
        low_arr = arr[:, 2]
        close_arr = arr[:, 3]

        close_prev = close_arr[:-1]
        close_next = close_arr[1:]
        delta_close = np.diff(close_arr)

        # 避免出现 0 或异常值时的除零警告。
        daily_ret = np.divide(
            delta_close,
            close_prev,
            out=np.zeros_like(delta_close),
            where=close_prev > 0,
        )

        valid_log = (close_prev > 0) & (close_next > 0)
        log_ret = np.log(close_next[valid_log] / close_prev[valid_log])

        total_return = (close_arr[-1] / close_arr[0] - 1) * 100
        annual_vol = np.std(log_ret, ddof=1) * np.sqrt(252) * 100 if log_ret.size > 1 else 0.0

        running_peak = np.maximum.accumulate(close_arr)
        drawdown = close_arr / running_peak - 1
        max_drawdown = drawdown.min() * 100

        tr = np.maximum(
            high_arr - low_arr,
            np.maximum(
                np.abs(high_arr - np.r_[close_arr[0], close_arr[:-1]]),
                np.abs(low_arr - np.r_[close_arr[0], close_arr[:-1]]),
            ),
        )
        atr14 = float(np.mean(tr[-14:])) if tr.size >= 14 else float(np.mean(tr))

        ma5 = self._moving_average(close_arr, 5)
        ma10 = self._moving_average(close_arr, 10)
        ma20 = self._moving_average(close_arr, 20)

        up_days = int(np.sum(daily_ret > 0))
        down_days = int(np.sum(daily_ret < 0))

        return {
            "open": open_arr,
            "high": high_arr,
            "low": low_arr,
            "close": close_arr,
            "daily_ret": daily_ret,
            "total_return": total_return,
            "annual_vol": annual_vol,
            "max_drawdown": max_drawdown,
            "atr14": atr14,
            "ma5": ma5,
            "ma10": ma10,
            "ma20": ma20,
            "up_days": up_days,
            "down_days": down_days,
        }

    def plot_kline(self):
        """绘制K线图（主图+成交量+均线）。"""
        if not self.prices:
            print("暂无数据，请先生成模拟数据或抓取真实数据。")
            return

        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
        plt.rcParams["axes.unicode_minus"] = False

        metrics = self._calculate_metrics()

        fig, (ax_price, ax_vol) = plt.subplots(
            2,
            1,
            figsize=(14, 9),
            sharex=True,
            gridspec_kw={"height_ratios": [3, 1]},
        )

        x = np.arange(len(self.prices))

        # 绘制K线
        for i, (open_p, high_p, low_p, close_p) in enumerate(self.prices):
            # 判断是阳线(涨)还是阴线(跌)
            color = 'red' if close_p >= open_p else 'green'

            # 绘制上下影线
            ax_price.plot([i, i], [low_p, high_p], color=color, linewidth=1)

            # 绘制实体
            body_height = max(abs(close_p - open_p), 1e-5)
            body_bottom = min(open_p, close_p)
            ax_price.bar(
                i,
                body_height,
                width=0.6,
                bottom=body_bottom,
                color=color,
                edgecolor=color,
                alpha=0.85,
            )

            vol = self.volumes[i] if i < len(self.volumes) else 0.0
            ax_vol.bar(i, vol, width=0.6, color=color, alpha=0.5)

        # 绘制均线
        ax_price.plot(x, metrics["ma5"], label="MA5", linewidth=1.2, color="#f39c12")
        ax_price.plot(x, metrics["ma10"], label="MA10", linewidth=1.2, color="#3498db")
        ax_price.plot(x, metrics["ma20"], label="MA20", linewidth=1.2, color="#8e44ad")

        # 设置图表标题和标签
        title = f"{self.stock_name}({self.symbol}) K线图 - {self.source_name}"
        ax_price.set_title(title, fontsize=16, fontweight='bold')
        ax_price.set_ylabel('价格', fontsize=12)
        ax_vol.set_ylabel('成交量', fontsize=11)
        ax_vol.set_xlabel('日期', fontsize=12)

        # 设置x轴标签
        step = max(1, len(self.dates) // 10)
        tick_idx = list(range(0, len(self.dates), step))
        ax_vol.set_xticks(tick_idx)
        ax_vol.set_xticklabels([self.dates[i].strftime('%m-%d') for i in tick_idx], rotation=45)

        # 添加网格
        ax_price.grid(True, linestyle='--', alpha=0.35)
        ax_vol.grid(True, linestyle='--', alpha=0.2)

        # 添加图例说明
        red_patch = Patch(color='red', label='上涨(阳线)')
        green_patch = Patch(color='green', label='下跌(阴线)')
        direction_legend = ax_price.legend(handles=[red_patch, green_patch], loc='upper left')
        ax_price.add_artist(direction_legend)
        ax_price.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    def print_analysis(self):
        """打印更详细的K线分析。"""
        if not self.prices:
            print("暂无数据，请先生成模拟数据或抓取真实数据。")
            return

        metrics = self._calculate_metrics()
        close_arr = metrics["close"]
        daily_ret = metrics["daily_ret"]

        ma5_last = metrics["ma5"][-1]
        ma10_last = metrics["ma10"][-1]
        ma20_last = metrics["ma20"][-1]

        pattern, pattern_desc = self._classify_last_candle()

        print("=" * 74)
        print(f"K线深度解读 | {self.stock_name}({self.symbol})")
        print(f"数据来源: {self.source_name} | 样本天数: {len(self.prices)}")
        print("=" * 74)

        print("一、基础行情")
        print(f"- 起始开盘价: {self.prices[0][0]:.2f}")
        print(f"- 最新收盘价: {close_arr[-1]:.2f}")
        print(f"- 区间总涨跌幅: {metrics['total_return']:.2f}%")
        print(f"- 上涨天数/下跌天数: {metrics['up_days']}/{metrics['down_days']}")

        print("\n二、波动与风险")
        print(f"- 年化波动率(基于对数收益): {metrics['annual_vol']:.2f}%")
        print(f"- 最大回撤: {metrics['max_drawdown']:.2f}%")
        print(f"- ATR14(平均真实波幅): {metrics['atr14']:.2f}")
        print("- 解读: 波动率和ATR越大，短线波动越剧烈，止损空间通常也要更宽。")

        print("\n三、均线结构")
        if np.isnan(ma20_last):
            print("- 样本不足20天，暂无法完整判断 MA5/MA10/MA20 结构。")
        else:
            print(f"- MA5: {ma5_last:.2f} | MA10: {ma10_last:.2f} | MA20: {ma20_last:.2f}")
            if ma5_last > ma10_last > ma20_last:
                print("- 解读: 均线多头排列，趋势偏强。")
            elif ma5_last < ma10_last < ma20_last:
                print("- 解读: 均线空头排列，趋势偏弱。")
            else:
                print("- 解读: 均线交错，市场可能处于震荡或趋势切换阶段。")

        print("\n四、最新一根K线")
        open_p, high_p, low_p, close_p = self.prices[-1]
        day_change = ((close_p / open_p) - 1) * 100
        print(f"- O/H/L/C: {open_p:.2f} / {high_p:.2f} / {low_p:.2f} / {close_p:.2f}")
        print(f"- 当日涨跌幅(开到收): {day_change:.2f}%")
        print(f"- 形态识别: {pattern}")
        print(f"- 形态解释: {pattern_desc}")

        print("\n五、阅读提示")
        print("- 单根K线信号可靠性有限，建议配合趋势、成交量、支撑阻力位共同判断。")
        print("- 若使用真实数据做策略回测，请加入交易成本、滑点和停牌处理。")

        if daily_ret.size > 0:
            win_rate = np.sum(daily_ret > 0) / daily_ret.size * 100
            print(f"- 样本期日线胜率(仅统计涨跌方向): {win_rate:.2f}%")
        print("=" * 74)


def main():
    print("股票K线图模拟器（增强版）")
    print("支持更真实的模拟K线 + 东方财富真实K线抓取")
    print()

    mode = input("请选择数据模式：1=增强模拟, 2=东方财富真实数据 [默认2]: ").strip() or "2"
    days_text = input("请输入K线天数 [默认120]: ").strip()
    days = KLineSimulator._safe_int(days_text, 120)
    days = max(30, days)

    # 创建模拟器实例
    simulator = KLineSimulator(start_price=100, days=days)

    if mode == "2":
        symbol = input("请输入6位股票代码（如 600519 / 000001）[默认000001]: ").strip() or "000001"
        adjust = input("复权方式 none/qfq/hfq [默认qfq]: ").strip().lower() or "qfq"

        try:
            count = simulator.fetch_eastmoney_kline(symbol=symbol, days=days, adjust=adjust)
            print(f"✅ 已抓取 {count} 条真实K线: {simulator.stock_name}({symbol})")
        except Exception as exc:
            print(f"⚠️ 抓取失败，自动回退到增强模拟数据。原因: {exc}")
            simulator.generate_data()
    else:
        simulator.generate_data()

    # 打印分析说明
    simulator.print_analysis()

    # 绘制K线图
    try:
        simulator.plot_kline()
    except ImportError:
        print("注意: 需要安装 matplotlib 和 requests 来运行本程序")
        print("请运行: pip install matplotlib requests")


if __name__ == "__main__":
    main()