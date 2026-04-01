import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random


class KLineSimulator:
    def __init__(self, start_price=100, days=30):
        self.start_price = start_price
        self.days = days
        self.prices = []
        self.dates = []

    def generate_data(self):
        """生成模拟的股票价格数据"""
        current_price = self.start_price
        current_date = datetime.now() - timedelta(days=self.days)

        for i in range(self.days):
            # 随机波动，模拟真实市场
            change_percent = random.uniform(-0.05, 0.05)  # ±5%的日波动
            new_price = current_price * (1 + change_percent)

            # 生成当日的开盘、最高、最低、收盘价
            open_price = current_price
            close_price = new_price
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.0)

            self.prices.append([open_price, high_price, low_price, close_price])
            self.dates.append(current_date)
            current_price = new_price
            current_date += timedelta(days=1)

    def plot_kline(self):
        """绘制K线图"""
        fig, ax = plt.subplots(figsize=(12, 8))

        # 绘制K线
        for i, (date, (open_p, high_p, low_p, close_p)) in enumerate(zip(self.dates, self.prices)):
            # 判断是阳线(涨)还是阴线(跌)
            color = 'red' if close_p >= open_p else 'green'

            # 绘制上下影线
            ax.plot([i, i], [low_p, high_p], color=color, linewidth=1)

            # 绘制实体
            body_height = abs(close_p - open_p)
            body_bottom = min(open_p, close_p)
            ax.bar(i, body_height, width=0.6, bottom=body_bottom,
                   color=color, edgecolor=color, alpha=0.8)

        # 设置图表标题和标签
        ax.set_title('股票K线图模拟器', fontsize=16, fontweight='bold')
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('价格', fontsize=12)

        # 设置x轴标签
        ax.set_xticks(range(0, len(self.dates), max(1, len(self.dates) // 10)))
        ax.set_xticklabels([d.strftime('%m-%d') for d in self.dates[::max(1, len(self.dates) // 10)]], rotation=45)

        # 添加网格
        ax.grid(True, linestyle='--', alpha=0.6)

        # 添加图例说明
        red_patch = plt.Rectangle((0, 0), 1, 1, color='red', label='上涨(阳线)')
        green_patch = plt.Rectangle((0, 0), 1, 1, color='green', label='下跌(阴线)')
        ax.legend(handles=[red_patch, green_patch], loc='upper left')

        plt.tight_layout()
        plt.show()

    def print_analysis(self):
        """打印简单的K线分析"""
        print("=" * 50)
        print("K线图分析指南")
        print("=" * 50)
        print("1. 红色K线 = 阳线（收盘价 > 开盘价，股票上涨）")
        print("2. 绿色K线 = 阴线（收盘价 < 开盘价，股票下跌）")
        print("3. K线实体 = 开盘价到收盘价之间的部分")
        print("4. K线上影线 = 当日最高价到实体上端的部分")
        print("5. K线下影线 = 当日最低价到实体下端的部分")
        print()
        print("形态识别:")
        print("- 大阳线: 实体长，涨幅大")
        print("- 大阴线: 实体长，跌幅大")
        print("- 十字星: 开盘价≈收盘价，多空平衡")
        print("- 锤子线: 下影线长，实体小，可能见底信号")
        print("- 上吊线: 上影线长，实体小，可能见顶信号")
        print()
        print("当前模拟数据:")
        print(f"起始价格: {self.prices[0][0]:.2f}")
        print(f"最终价格: {self.prices[-1][-1]:.2f}")
        print(f"总涨跌幅: {((self.prices[-1][-1] / self.prices[0][0]) - 1) * 100:.2f}%")
        print("=" * 50)


def main():
    print("股票K线图模拟器")
    print("这是一个帮助新手学习K线图的工具")
    print()

    # 创建模拟器实例
    simulator = KLineSimulator(start_price=100, days=30)

    # 生成数据
    simulator.generate_data()

    # 打印分析说明
    simulator.print_analysis()

    # 绘制K线图
    try:
        simulator.plot_kline()
    except ImportError:
        print("注意: 需要安装matplotlib库来显示图表")
        print("请运行: pip install matplotlib")


if __name__ == "__main__":
    main()