import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy.stats import gaussian_kde 


class AssetManagementSimulate():

    def __init__(self, **kwargs):
        self.interest_rate = kwargs["interest_rate"]
        self.rate_risk = kwargs["rate_risk"]
        self.operational_term_list = [5, 10, 20, 30]
        self.invest_mumber_of_divesion = kwargs["invest_mumber_of_divesion"]
        self.simulation_term = kwargs["simulation_term"]
        self.simulate_size = 100000
        self.total_investment_amount = kwargs["total_investment_amount"]
        self.reserve_amount_a_year = self.total_investment_amount / self.invest_mumber_of_divesion #総投資額/分割回数(年)
        self.target_profit_margin = kwargs["target_profit_margin"]
        self.acceptable_risk = kwargs["acceptable_risk"]
        self.x = np.linspace(-1, 6, 500)


    #投資シミュレーションの結果を返す
    def investment_result_cals(self):
        result_list = np.array([])
        result = np.array([])
        for i in np.arange(1, self.simulation_term + 1): #for文1周で1年分10000サンプル
            #平均が収益、標準偏差がリスクの正規分布を10000回サンプリングする
            random_rate_list = np.random.normal(loc=self.interest_rate, scale=self.rate_risk, size=self.simulate_size) 
            if i == 1 : #初年度　リストを作成
                result = self.reserve_amount_a_year * random_rate_list
                result_list = result
            elif i <= self.invest_mumber_of_divesion: #投資期間なら (投資結果 + 積立額) * rate
                result = (result + self.reserve_amount_a_year) * random_rate_list
                result_list = np.vstack((result_list, result))
            else:
                result = result * random_rate_list
                result_list = np.vstack((result_list, result))
        return result_list


    #投資の分布を結果をプロット
    def _plot_installment_investment_return_distribution(self, result_list):
        plt.figure(figsize=(10,7))
        ax = plt.subplot()
        per_list = []
        loss_per_list = []
        loss_average_list = []
        for term in self.operational_term_list:
            how_many_times = result_list[term-1,:] / (self.total_investment_amount)
            density_result = gaussian_kde(how_many_times) #密度推定
            ax.plot(self.x, density_result(self.x), label=f'運用:{term}年')
            percentage = len(how_many_times[how_many_times >= self.target_profit_margin]) / len(how_many_times) #目標とする運用に達する確率
            per_list.append(percentage)
            loss_per = len(how_many_times[how_many_times <= self.acceptable_risk]) / len(how_many_times) #元本割れする確率
            loss_per_list.append(loss_per)
            loss_average = np.mean(how_many_times[how_many_times < 1]- 1)
            loss_average_list.append(loss_average)
          
        plt.title(f'分割投資 : 年利{(self.interest_rate - 1) * 100:.1f}%, リスク{self.rate_risk * 100}%の商品利益確率', fontsize=18)
        plt.legend(bbox_to_anchor=(0.95, 0.1), loc='lower right', borderaxespad=0, fontsize=16)
        plt.savefig('output/invest_simulate_distribution.jpeg')
        # plt.savefig(f'output/分割投資 : 年利{(self.interest_rate - 1) * 100:.1f}%, リスク{self.rate_risk * 100}%の商品利益確率.jpeg')
        plt.show()
        
        for i in [f'{term}年後に資産が{self.target_profit_margin:,}倍以上になる確率{per * 100:.1f}%' for term, per in zip(self.operational_term_list, per_list)]:
            print(i)
        print('\n')
        for i in [f'{term}年後に資産が{np.round((1 - self.acceptable_risk) * 100)}%以上減少している確率{per * 100:.1f}%' for term, per in zip(self.operational_term_list, loss_per_list)]:
            print(i)
        print('\n')
        for i in [f'{term}年後に元本割れした場合の損失の平均 : {loss_average}' for term, loss_average in zip(self.operational_term_list, loss_average_list)]:
            print(i)


    #シミュレーション結果を受けて分割投資の分布をプロット
    def plot_installment_investment_distribution(self):
        result_list = self.investment_result_cals()
        self._plot_installment_investment_return_distribution(result_list)


    def average_profit_list(self):
        result_list = self.investment_result_cals()
        result_mean = result_list.mean(axis=1)
        x = np.arange(1, self.simulation_term+1)
        invest_list = [self.reserve_amount_a_year * i if i <= self.invest_mumber_of_divesion else self.total_investment_amount for i in x]
        average_profit_list = result_mean - np.array(invest_list)
        return average_profit_list

    
    def median_profit_list(self):
        result_list = self.investment_result_cals()
        result_median = np.median(result_list, axis=1)
        x = np.arange(1, self.simulation_term+1)
        invest_list = [self.reserve_amount_a_year * i if i <= self.invest_mumber_of_divesion else self.total_investment_amount for i in x]
        median_profit_list = result_median - np.array(invest_list)
        return median_profit_list


    def simulate_plot(self):
        result_list = self.investment_result_cals()
        result_mean = result_list.mean(axis=1)
        result_median = np.median(result_list, axis=1)
        result_std = result_list.std(axis=1)
        x = np.arange(1, self.simulation_term+1)
        
        result_upper = result_std * 1.64 + result_mean
        result_lower = result_std * -1.64 + result_mean
        fig = plt.figure(figsize=(12, 7))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(x, result_mean, label='平均') 
        ax1.plot(x, result_median,c="b", label="中央値", alpha=0.7) #中央値
        ax1.plot(x, [self.reserve_amount_a_year * i if i <= self.invest_mumber_of_divesion else self.total_investment_amount for i in x], label="投資元本", alpha=0.7) #単純投資合計額

        ax1.fill_between(x, result_upper, result_lower, color='g', alpha=0.1, label='90信頼区間') #信頼区間

        plt.ticklabel_format(style='plain',axis='y')
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda v,p: f'{int(v):,d}'))
        plt.title(f'分割投資 : 年利{(self.interest_rate - 1)* 100:.1f}%, リスク{self.rate_risk * 100}%、{self.invest_mumber_of_divesion}年で投資額{self.total_investment_amount:,}円', fontsize=18)
        plt.grid()
        # plt.yticks(np.arange(np.round(result_lower, -6), np.round(result_upper, -6), 2000000))
        plt.legend(bbox_to_anchor=(0.25, 0.95), loc='upper right', borderaxespad=0, fontsize=16)
        plt.savefig(f'output/年利{(self.interest_rate - 1)* 100:.1f}%, リスク{self.rate_risk * 100}%、{self.invest_mumber_of_divesion}年で投資額{self.total_investment_amount:,}円.jpeg')
        plt.savefig('output/invest_simulate.jpeg')
        plt.show()

