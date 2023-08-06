# ============================================================================
# @Time :  
# @Author: Wufei
# @File: creditprice.py
# ============================================================================
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import sympy as sy
from scipy.optimize import root
from joblib import Parallel, delayed

#定义接受率函数
class credit_price:
    def __init__(self, ld, d = 1, rl = 0.05, rf = 0.04, score='score', interest='r', flag='accept', y = 'flagy'):
        '''
        :param ld: 违约损失率
        :param d: 调整好人概率参数
        :param rl: 市场利率下限
        :param rf: 无风险利率
        '''
        self.ld = ld
        self.d = d
        self.rl = rl
        self.rf = rf
        self.score = score
        self.interest = interest
        self.flag = flag
        self.y = y
        return

    def q1(self, data, a, b, c):
        '''
        :param data: 原始数据
        :param a: 参数1
        :param b: 参数2
        :param c: 参数3
        :return: 接受率向量
        '''
        y = (1 + np.exp(-(a-c*data['p'])))*np.exp(a-b*(data['r']-self.rl)-c*data['p'])/(1 + np.exp(a-b*(data['r']-self.rl)-c*data['p']))
        return y.ravel()

    def q(self, r ,p, a, b, c):
        '''
        :param r: 利率
        :param p: 好人概率
        :param a: 参数1
        :param b: 参数2
        :param c: 参数3
        :return: 接受率
        '''
        return (1 + np.exp(-(a - c * p))) * np.exp(a-b*(r - self.rl)-c * p) / (1 + np.exp(a - b * (r - self.rl) - c * p))

    def data_transform(self, data):
        '''
        :param data: DataFrame
        :param score: 评分变量名
        :param interest: 利率变量名
        :param flag: 接受度变量名，接受取1，不接受取0
        :param y: 好坏标签，坏为1，好为0，无标签为空
        :return:DataFrame，包含4列
        '''
        data1 = data.copy()
        score_point = sorted(list(set(np.nanpercentile(data1[self.score], range(0,101,5), interpolation='midpoint'))))
        score_point[0] = - np.inf
        score_point[-1] = np.inf
        interest_point = sorted(list(set(np.nanpercentile(data1[self.interest], range(0, 101, 5), interpolation='midpoint'))))
        interest_point[0] = - np.inf
        interest_point[-1] = np.inf
        data1[self.score + '1'] = pd.cut(data1[self.score], bins=score_point, right=False)
        data1[self.interest + '1'] = pd.cut(data1[self.interest], bins=interest_point, right=False)
        data_t1 = data1.groupby(by=[self.score + '1', self.interest + '1'])[[self.score, self.interest]].mean()
        data_t2 = data1.groupby(by = [self.score + '1', self.interest + '1'])[[self.flag]].apply(lambda x: 1 - x.sum() / x.count()).rename(columns={self.flag: 'q'})
        data_t3 = data1.groupby(by=[self.score + '1', self.interest + '1'])[[self.y]].apply(lambda x: 1 - x.sum() / x.count()).rename(columns={self.y: 'p'})
        data_t = pd.concat([data_t1, data_t2, data_t3], axis=1)
        data_t.rename(columns={self.score : 'score', self.interest: 'r'})
        data_t = data_t[['score', 'r', 'q', 'p']]
        # data_t['p_adj'] = data_t['p'] / ((1 - data_t['p'])* np.exp(data_t['r'] + data_t['p']))
        data_t.dropna(how='any', axis=0, inplace=True)

        data_p1 = data1.groupby(self.score + '1')[[self.y]].apply(lambda x: 1 - x.sum() / x.count()).rename(columns={self.y: 'p'})
        data_p2 = data1.groupby(by=self.score + '1')[[self.score]].apply(lambda x: x.mean())
        data_p = pd.concat([data_p1, data_p2], axis=1)
        data_p.dropna(how='any', axis=0, inplace=True)

        return data_t, data_p

    def calc_abc(self, data_t):
        intecept, pred = curve_fit(self.q1, data_t[['p', 'r']], data_t['q'], method='trf', bounds=(0, np.inf))
        return intecept


    def func_r(self, r, p, a, b, c):
        y = r + self.ld + ((- b * self.q(r, p, a, b, c) * (self.ld + self.rf) * ((1 - p) * np.exp(self.d * r) + p)) - p * (1 + np.exp(-a + c * p)) \
            * np.exp(a - b * (r - self.rl) - c * p)) / (self.d * (1 - p) * np.exp(self.d * r) * (1 + np.exp(-a + c * p)) * np.exp(a - b * (r - self.rl) - c * p) \
            + p * b)
        return y
    #通过root求解利率
    def calc_r_table(self, data):
        data_t, data_p = self.data_transform(data)
        a, b, c = self.calc_abc(data_t)
        r_list =  Parallel(n_jobs=-1)(
            delayed(root)(self.func_r, [0.2], (p, a, b, c), method = 'krylov', tol = 1e-3)
            for p in data_p.p.values.tolist()
            )
        r_list1 = [i.x[0] for i in r_list]
        data_p['pred_r'] = r_list1
        return data_p
    #任一好人概率下的风险定价
    def calc_r(self, p, data):
        data_t, data_p = self.data_transform(data)
        a, b, c = self.calc_abc(data_t)
        r = root(self.func_r, [0.2], (p,a,b,c), method = 'krylov', tol = 1e-3).x[0]
        return r

def calc(ld, d = 1, rl = 0.05, rf = 0.04, score='score', interest='r', flag='accept', y = 'flagy'):
    f = credit_price(ld, d = 1, rl = 0.05, rf = 0.04, score='score', interest='r', flag='accept', y = 'flagy')
    return f
#测试
# if __name__ == '__main__':
    np.random.seed(123)
    score = 650 + 100 * np.random.randn(1000)
    price = 0.2 + 0.1 * np.random.randn(1000)
    flag = np.random.randint(2, size=1000)
    flagy = np.random.binomial(1, 0.2, size=flag[flag == 1].shape[0])
    data = pd.DataFrame(columns=['score', 'r', 'accept', 'flagy'])
    data['score'] = score
    data['r'] = price
    data['accept'] = flag
    data.loc[data.accept == 1, 'flagy'] = flagy
#     cp = credit_price(ld=0.5, d = 1, rl = 0.05, rf = 0.04, score='score', interest='r', flag='accept', y = 'flagy')
#     print(cp.calc_r_table(data))
#     print(cp.calc_r(0.6))