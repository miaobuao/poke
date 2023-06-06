# 导入库
import numpy as np
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from scipy import stats
from scipy.stats import skew
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier as RFC

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Simhei']
plt.rcParams['axes.unicode_minus'] = False
pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 500)
np.set_printoptions(threshold=np.inf)


class Processing:
    def __init__(self):
        pass

    def processing(self, input_path='data_ori.xlsx', output_path='df_data_process_end.csv'):
        df_data = pd.read_excel(input_path, index_col=[0])

        my_features=['AMT_DAY_USED','BEN_HEAD','BEN_HEAD_TYPE','BEN_TYPE','CL_OWNER_PAY_AMT','CL_SELF_CAT_PAY_AMT','CL_SOCIAL_PAY_AMT','CL_THIRD_PARTY_PAY_AMT','CLSH_HOSP_CODE','COPAY_PCT','CRT_USER','CSR_REMARK','CWF_AMT_DAY','DIAG_CODE','FX_RATE','INCUR_DATE_FROM','INCUR_DATE_TO','INVOICE_RTN_IND','KIND_CODE','MBR_NO','MBR_TYPE','MEMBER_EVENT','NO_OF_YR','ORG_PRES_AMT','POHO_NO','POLICY_CNT','PRI_CORR_BRKR_NAME','PROV_CODE','PROV_DEPT','PROV_LEVEL','PROV_NAME','RCV_DATE','SCMA_OID_BEN_TYPE','SCMA_OID_CL_LINE_STATUS','SCMA_OID_CL_STATUS','SCMA_OID_CL_TYPE','SCMA_OID_COUNTRY_TREATMENT','SCMA_OID_PROD_TYPE','SUB_AMT','TOTAL_RECEIPT_AMT','WORKPLACE_NAME']
        df_data = df_data[my_features]

        # datetime64[ns] 转换为 Object 对象
        df_data['INCUR_DATE_FROM'] = df_data['INCUR_DATE_FROM'].dt.strftime('%Y-%m-%d')
        df_data['INCUR_DATE_TO'] = df_data['INCUR_DATE_TO'].dt.strftime('%Y-%m-%d')
        df_data['RCV_DATE'] = df_data['RCV_DATE'].dt.strftime('%Y-%m-%d')

        # 对标签列进行处理，删除标签为'CL_LINE_STATUS_PV'、'CL_LINE_STATUS_PD'的数据
        # print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())
        drop_value_list = ['CL_LINE_STATUS_PV', 'CL_LINE_STATUS_PD']
        drop_idx_list = [i for i, v in df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'].items() if v in drop_value_list]
        df_data = df_data.drop(axis=0, index=drop_idx_list, inplace=False)

        # 对标签进行编码(LabelEncoder)
        y = df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS']  # 获得标签列（保存一分后面用得到）

        le = LabelEncoder()  # 实例化，即创建对象
        le = le.fit(y)  # 导入数据
        label = le.transform(y)  # tranform接口调取结果,也可以直接使用fit_transform接口一步到位
        # 把处理好的标签，赋值回原数据矩阵
        df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'] = label

        # 标签列改名为 FRAUD
        df_data.rename(columns={'SCMA_OID_CL_LINE_STATUS': 'FRAUD'}, inplace=True)

        # 缺失值处理
        df_data = self.missing_value_processing(df_data)

        # 异常值处理
        digital_features = list(df_data.select_dtypes(include=['float64', 'int64']).columns)
        unrequired_process_features = ['MBR_NO', 'POLICY_CNT', 'PROV_CODE']
        digital_features = [item for idx, item in enumerate(digital_features) if
                            item not in unrequired_process_features]

        del_index_list = self.outlier_value_processing(df_data['CL_OWNER_PAY_AMT'])
        # print(del_index_list)
        df_data.drop(index=del_index_list, inplace=True)
        # print(len(df_data))

        del_index_list = self.outlier_value_processing(df_data['CL_SELF_CAT_PAY_AMT'])
        df_data.drop(index=del_index_list, inplace=True)
        # print(len(df_data))

        del_index_list = self.outlier_value_processing(df_data['CL_THIRD_PARTY_PAY_AMT'])
        df_data.drop(index=del_index_list, inplace=True)
        # print(len(df_data))

        # 'POHO_NO'中出现异常值(出现了非数值数据)，删除
        df_data['POHO_NO'] = pd.to_numeric(df_data['POHO_NO'], errors='coerce')
        # 删除包含NaN值的行
        df_data = df_data.dropna()
        # 将col1列转换回Object类型
        df_data['POHO_NO'] = df_data['POHO_NO'].astype(str)
        df_data['POHO_NO'].value_counts()

        # 删除无关列
        del_field_list = ['MEMBER_EVENT', 'PRI_CORR_BRKR_NAME', 'SCMA_OID_CL_TYPE', 'SCMA_OID_PROD_TYPE',
                          'INCUR_DATE_FROM', 'INCUR_DATE_TO']
        df_data = df_data.drop(del_field_list, axis=1)
        # FX_RATE 字段也删除（所有数据该列值都是同一个）
        df_data = df_data.drop(['FX_RATE'], axis=1)

        # 哑变量处理
        df_data = self.dummy_variable_processing(df_data)

        # log 纠编 & 标准化
        df_data = self.log_processing(df_data)

        # 对 ORG_PRES_AMT 进行换算，变为数值¶
        def replace_of_squares(x):
            if x.startswith("RMB "):
                x = x.lstrip("RMB ")

                return float(x)
            else:
                x = x.lstrip("USD ")
                return float(x) * 7

        df_data['ORG_PRES_AMT'] = df_data['ORG_PRES_AMT'].apply(replace_of_squares)
        df_data['ORG_PRES_AMT'].sort_values()
        df_data = df_data.dropna(axis=0, subset=['ORG_PRES_AMT'])

        # 显示结果
        df_data.isna().sum()
        df_data['ORG_PRES_AMT'].value_counts()

        # 标准化处理(0-1)
        trans = MinMaxScaler()  # 归一化[0,1]

        df_data[['ORG_PRES_AMT']] = trans.fit_transform(df_data[['ORG_PRES_AMT']])

        # 特征选择
        # df_data = self.feature_selection(df_data)
        df_data.to_csv(output_path, index=False)

    def missing_value_processing(self, df_data):
        # 缺失值处理
        # 查看缺失值数据类型
        # for key, value in df_data.isna().sum().to_dict().items():
        #     if (value != 0):
                # print("%-20s" % key, "%-15s" % df_data[key].dtypes, df_data[key].isna().sum())

        # 删除 AMT_DAY_USED 字段(缺失值太多)
        df_data = df_data.drop(['AMT_DAY_USED'], axis=1)
        # 删除 CSR_REMARK 列
        df_data = df_data.drop(['CSR_REMARK'], axis=1)

        # 填充其他的缺失值数据（只有一条缺失值的删除整行数据）
        fill_list = ['BEN_HEAD_TYPE', 'KIND_CODE', 'PROV_DEPT']
        for i in fill_list:
            df_data.loc[:, i] = df_data.loc[:, i].fillna('Unkonwn')  # Unkonwn    26378

        df_data.loc[:, 'INVOICE_RTN_IND'] = df_data.loc[:, 'INVOICE_RTN_IND'].fillna('N')
        df_data.loc[:, 'INVOICE_RTN_IND'] = df_data.loc[:, 'INVOICE_RTN_IND'].replace('nan', 'N')
        # df_data['INVOICE_RTN_IND'].unique()
        # print("\n填充后 df_data['INVOICE_RTN_IND'] 的值统计:\n%s" % df_data['INVOICE_RTN_IND'].value_counts())

        # 以下字段缺失值数量少，直接删除有缺失值所在行
        del_field_null_list = ['CRT_USER', 'PROV_NAME', 'PROV_CODE', 'PROV_LEVEL', 'CLSH_HOSP_CODE']
        for i in del_field_null_list:
            df_data = df_data.dropna(axis=0, subset=[i])

        # 删掉(值太多且关联性不大)
        del_field_list = ['PROV_NAME', 'WORKPLACE_NAME']
        df_data = df_data.drop(del_field_list, axis=1)

        return df_data

    def outlier_value_processing(self, df_data):

        u = df_data.mean()  # 计算均值
        std = df_data.std()  # 计算标准差
        stats.kstest(df_data, 'norm', (u, std))  # kstest，数据分布检验模块，正态性检验或其他数据分布类型，仅适用于连续分布的检验
        # print('均值为：%.3f，标准差为：%.3f' % (u, std))
        # print('------\n')

        # 正态性检验
        # 筛选出异常值error、剔除异常值之后的数据df_data_c
        error = df_data[np.abs(df_data - u) > 3 * std]  # 大于3σ的异常值数据
        del_index_list = error.index

        return del_index_list

    def dummy_variable_processing(self, df_data):

        # 哑变量处理
        # 删除某些待定的 无用的列
        del_field_list = ['RCV_DATE']
        df_data = df_data.drop(del_field_list, axis=1)

        # 医院等级（中文->英文标记）映射（中文映射为英文）
        PROV_LEVEL_lever_to_symbol = {
            '一级': 'L0',
            '二级': 'L1',
            '三级': 'L2',
            '未评级': 'L3',
            '医保': 'L4',
            '非医保': 'L5',
            '卫生所': 'L6',
            '未知': 'L7'
        }
        df_data['PROV_LEVEL'] = df_data['PROV_LEVEL'].map(PROV_LEVEL_lever_to_symbol)

        # 哑变量处理
        '''
        pre_dummies_columns = ['BEN_HEAD_TYPE','INVOICE_RTN_IND','MBR_TYPE','POLICY_CNT','PROV_LEVEL','SCMA_OID_BEN_TYPE','SCMA_OID_CL_LINE_STATUS','SCMA_OID_CL_STATUS','SCMA_OID_COUNTRY_TREATMENT']
        dummies_columns_prefix = ['BEN_HEAD_TYPE_','INVOICE_RTN_IND_','MBR_TYPE_','POLICY_CNT_','PROV_LEVEL_','SCMA_OID_BEN_TYPE_','SCMA_OID_CL_LINE_STATUS_','SCMA_OID_CL_STATUS_','SCMA_OID_COUNTRY_TREATMENT_']
        '''
        pre_dummies_columns = ['BEN_HEAD_TYPE', 'INVOICE_RTN_IND', 'MBR_TYPE', 'POLICY_CNT', 'PROV_LEVEL',
                               'SCMA_OID_BEN_TYPE', 'SCMA_OID_CL_STATUS', 'SCMA_OID_COUNTRY_TREATMENT']
        dummies_columns_prefix = ['BEN_HEAD_TYPE_', 'INVOICE_RTN_IND_', 'MBR_TYPE_', 'POLICY_CNT_', 'PROV_LEVEL_',
                                  'SCMA_OID_BEN_TYPE_', 'SCMA_OID_CL_STATUS_', 'SCMA_OID_COUNTRY_TREATMENT_']

        for idx in range(len(pre_dummies_columns)):
            dummies_item = pd.get_dummies(df_data[pre_dummies_columns[idx]], prefix=dummies_columns_prefix[idx])
            df_data = pd.concat([df_data, dummies_item], axis=1)
            df_data.drop(pre_dummies_columns[idx], axis=1, inplace=True)
        df_data.isna().sum()

        # 非数值型相关字段分类后哑变量处理
        # print(df_data['CLSH_HOSP_CODE'].dtypes)
        # print(set(df_data['CLSH_HOSP_CODE'].values))
        # print(len(df_data['CLSH_HOSP_CODE'].value_counts()))
        # df_data['CLSH_HOSP_CODE'] = df_data['CLSH_HOSP_CODE'].astype(str)

        # 定义一个字典，将26个字母映射为数字
        province_code_dict = {
            'AH': 'AH',
            'BJ': 'BJ',
            'FJ': 'FJ',
            'GD': 'GD',
            'GX': 'GX',
            'GS': 'GS',
            'HB': 'HB',
            'HN': 'HN',
            'HLJ': 'HLJ',
            'JS': 'JS',
            'JX': 'JX',
            'JL': 'JL',
            'LN': 'LN',
            'NM': 'NM',
            'NX': 'NX',
            'QH': 'QH',
            'SD': 'SD',
            'SX': 'SX',
            'SC': 'SC',
            'TW': 'TW',
            'XZ': 'XZ',
            'XN': 'XN',
            'YN': 'YN',
            'ZJ': 'ZJ',
            'CQ': 'CQ',
            'SH': 'SH',
            'TJ': 'TJ',
            'XG': 'XG',
            'AM': 'AM'
        }
        # print(province_code_dict)

        # 定义一个函数，根据首字母返回对应的数字
        def get_alpha_num(alpha):
            if alpha[2:4] in province_code_dict:  # 按照第1个字符编码
                return province_code_dict[alpha[2:4]]
            else:
                return None

        df_data['CLSH_HOSP_CODE'] = df_data['CLSH_HOSP_CODE'].apply(get_alpha_num)

        # 删除空值所在行
        df_data = df_data.dropna(axis=0, subset=['CLSH_HOSP_CODE'])
        # print(df_data.isna().sum())
        df_data['CLSH_HOSP_CODE'].value_counts()

        # 哑变量处理
        df_data = pd.get_dummies(df_data, columns=['CLSH_HOSP_CODE'])

        # DIAG_CODE
        # print(df_data['DIAG_CODE'].dtypes)
        # print(set(df_data['DIAG_CODE'].values))
        # print(len(df_data['DIAG_CODE'].value_counts()))
        df_data['DIAG_CODE'] = df_data['DIAG_CODE'].astype(str)

        import string

        # 定义一个字典，将26个字母映射为数字
        # alpha_dict = {alpha: num for num, alpha in enumerate(string.ascii_uppercase)}
        alpha_dict = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I',
                      'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R',
                      'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
        # print(alpha_dict)

        # 定义一个函数，根据首字母返回对应的数字
        def get_alpha_num(alpha):
            if alpha[0] in alpha_dict:  # 按照第1个字符编码
                return alpha_dict[alpha[0]]
            else:
                return None

        df_data['DIAG_CODE'] = df_data['DIAG_CODE'].apply(get_alpha_num)

        df_data['DIAG_CODE'].value_counts()

        # 删除空值所在行
        df_data = df_data.dropna(axis=0, subset=['DIAG_CODE'])
        # print(df_data.isna().sum())
        df_data['DIAG_CODE'].value_counts()

        # 哑变量处理
        df_data = pd.get_dummies(df_data, columns=['DIAG_CODE'])

        return df_data

    def log_processing(self, df_data):

        # 数值变量数据log10X纠偏

        # 删除 CL_THIRD_PARTY_PAY_AMT (大部分数值都是0)

        df_data = df_data.drop(['CL_THIRD_PARTY_PAY_AMT'], axis=1)

        numeric_feats = df_data.dtypes[df_data.dtypes == 'float64'].index
        skewed_feats = df_data[numeric_feats].apply(lambda x: skew(x.dropna()))

        # 筛选出对所有的float64的数据
        log_features = list(df_data.select_dtypes(include=['float64', 'int64']).columns)
        unrequired_process_features = ['MBR_NO', 'POLICY_CNT', 'PROV_CODE']
        log_features = [item for idx, item in enumerate(log_features) if item not in unrequired_process_features]

        # 对这些偏度大的金额数据进行Log10()转换的纠偏处理

        for i in log_features:
            df_data[i] = df_data[i].map(lambda x: np.log10(x) if x > 0 else 0)

        # 查看用log10X进行纠偏后数据的偏度，因为数据严重右偏的得到纠偏后还是有些偏态的。但是相比之前的数据状态已经调整了很多。
        skewed_feats_afterlog = df_data[log_features].apply(lambda x: skew(x.dropna()))

        # 数据标准化
        # 对float64相关的数值变量进行区间缩放数据标准化处理(0-1)

        trans = MinMaxScaler()  # 归一化[0,1]

        df_data[log_features] = trans.fit_transform(df_data[log_features])

        return df_data

    def feature_selection(self, df_data):

        # 包装法特征选择
        pre_selection_columns = df_data.dtypes.index[0:-8]

        # 训练数据
        X = df_data[pre_selection_columns].drop('FRAUD', axis=1)

        # 标签列
        y = df_data['FRAUD']

        RFC_ = RFC(n_estimators=10, random_state=0)
        selector = RFE(RFC_, n_features_to_select=80, step=50).fit(X, y)

        X_wrapper = selector.transform(X)
        cross_val_score(RFC_, X_wrapper, y, cv=5).mean()  # score得分为0.93797619

        df_data_selected_features = X.iloc[:, selector.support_]

        # 对包装法画学习曲线,找到最优特征参数
        score = []
        for i in range(1, 751, 50):
            X_wrapper = RFE(RFC_, n_features_to_select=i, step=50).fit_transform(X, y)
            once = cross_val_score(RFC_, X_wrapper, y, cv=5).mean()
            score.append(once)
        plt.figure(figsize=[20, 5])
        plt.plot(range(1, 751, 50), score)
        plt.xticks(range(1, 751, 50))
        plt.show()

        # 拼起来

        concat_columns = df_data.dtypes.index[-8:]
        df_data = pd.concat(
            [df_data_selected_features, df_data[concat_columns], df_data['FRAUD']], axis=1)

        return df_data


if __name__ == '__main__':
    it = Processing()
    it.processing('test.xlsx')