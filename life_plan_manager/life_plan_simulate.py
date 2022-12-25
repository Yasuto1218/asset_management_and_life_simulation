import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class LifePlanSimulate():
    def __init__(self, **kwargs):
        self.pension_amount = kwargs["pension_amount"]
        self.cost_of_living = kwargs["cost_of_living"]
        self.severance_pay = kwargs["severance_pay"]
        self.current_saving = kwargs["current_saving"]
        self.age = 60 #定年
        self.simulate_age = kwargs["simulate_age"]
        self.x_ticks = np.linspace(-1, 6, 500)
        #車関係
        self.car_purchase_frequency = kwargs["car_purchase_frequency"]
        self.car_price   = kwargs["car_price"]
        #住宅
        self.house_fix_price_a_year = 5000000 / (self.simulate_age - self.age)


    def plot_life_plan_simulate_without_asset_management(self):
        all_property, age_list, all_life_simulate_list = self.life_plan_calc()
        self.plot_figure_of_life_plan(all_property, age_list, all_life_simulate_list)


    def life_plan_calc(self):
        all_property = self.current_saving + self.severance_pay #総資産
        all_property_list = [] #年ごとの残高の確認
        age_list = np.arange(self.age, self.simulate_age + 1)
        
        for age in age_list:
            if age <= 64: #年金支給前
                all_property_list.append(all_property)
                all_property -= self.cost_of_living #生活費がかかるだけ
            else: #年金支給後:
                all_property -= self.cost_of_living  
                all_property += self.pension_amount #年金の支給開始
                all_property_list.append(all_property)

        car_simulation_list, house_fix_simulation_list = self._add_car_house_simulation()
        car_simulation_list = np.array(car_simulation_list)
        house_fix_simulation_list = np.array(house_fix_simulation_list)
        all_property_list = np.array(all_property_list)
        all_life_simulate_list = np.subtract(all_property_list, car_simulation_list)
        all_life_simulate_list = np.subtract(all_life_simulate_list, house_fix_simulation_list)
        return all_property, age_list, all_life_simulate_list


    def _add_car_house_simulation(self):
        #車の購入
        car_simulation_list = [] 
        age_list = np.arange(self.age, self.simulate_age + 1)
        for age in age_list:
            if age %  self.car_purchase_frequency == 0: #年金支給前
                car_simulation_list.append(self.car_price)
            else:
                car_simulation_list.append(0)
        #家の修理
        house_fix_price_a_year = 5000000 / (self.simulate_age + 1 - self.age)
        house_fix_simulation_list = [house_fix_price_a_year] * (self.simulate_age + 1 - self.age)
        return car_simulation_list, house_fix_simulation_list    


    def plot_figure_of_life_plan(self, all_property, age_list, all_life_simulate_list):
        fig = plt.figure(figsize=(10, 7))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.bar(age_list, all_life_simulate_list, alpha=1.0, color='skyblue', label="投資なし")
        plt.ticklabel_format(style='plain',axis='y')
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda v,p: f'{int(v):,d}'))
        plt.title(f'資産額:{all_property:,}円({self.simulate_age}歳時点)', fontsize=14)
        plt.grid()
        plt.yticks(np.arange(round(np.min([all_life_simulate_list]), -6), round(np.max([all_life_simulate_list]), -6), 5000000))
        plt.legend()
        plt.savefig(f'output/simulate_without_invest.jpeg')
        plt.show()


    def plot_figure_of_life_plan_in_invest(self, age_list, all_life_simulate_list, invest_life_plan_simulate_list):
        fig = plt.figure(figsize=(10, 7))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.bar(age_list, invest_life_plan_simulate_list, alpha=1.0, color='dodgerblue', label="投資あり")
        ax1.bar(age_list, all_life_simulate_list, alpha=1.0, color='skyblue', label="投資なし")
        plt.ticklabel_format(style='plain',axis='y')
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda v,p: f'{int(v):,d}'))
        plt.title(f'資産額:{invest_life_plan_simulate_list[-1]:,.0f}円({self.simulate_age}歳時点)', fontsize=14)
        plt.grid()
        plt.yticks(np.arange(round(np.min([all_life_simulate_list]), -6), round(np.max([invest_life_plan_simulate_list]), -6), 5000000))
        plt.legend()
        plt.savefig(f'output/simulate_in_invest.jpeg')
        plt.show()
