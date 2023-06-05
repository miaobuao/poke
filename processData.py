def processData(originFilePath,processedFilePath):
    # %%
    # 导入库
    import os
    import time
    import warnings
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns   # 绘图库
    import numpy as np
    from matplotlib.gridspec import GridSpec  # 自定义子图的网格布局库
    from sklearn.impute import SimpleImputer

    warnings.filterwarnings('ignore')    # 忽略警告消息
    plt.rcParams['font.sans-serif'] = ['Simhei']   # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
    # plt.rcParams['figure.figsize'] = (12.0, 8.0)  # 调整大小,可根据自实际情况进行设置
    pd.set_option('display.max_columns', 999)    # 设置数据展示的最大列数和最大行数
    pd.set_option('display.max_rows', 500)
    np.set_printoptions(threshold=np.inf)

    # %% [markdown]
    # # 一、数据查看和分析

    # %% [markdown]
    # ## 1.1 加载并查看数据
    # - 查看数据大小，数据基本特征。
    # - 数据是否存在缺失值
    # - 查看数据列、数据类型，以便数据预处理
    # - 分别查看数值型数据和非数值型数据

    # %%
    # 加载数据，查看数据大小
    df_data = pd.read_excel(originFilePath,index_col=[0])


    # %%
    # datetime64[ns] 转换为 Object 对象
    df_data['INCUR_DATE_FROM'] = df_data['INCUR_DATE_FROM'].dt.strftime('%Y-%m-%d')
    df_data['INCUR_DATE_TO'] = df_data['INCUR_DATE_TO'].dt.strftime('%Y-%m-%d')
    df_data['RCV_DATE'] = df_data['RCV_DATE'].dt.strftime('%Y-%m-%d')

    # %% [markdown]
    # ## 1.2 查看字符类型数据

    # %%
    # 查看类别变量的取值，即非数值型，这里是object
    df_data.select_dtypes(include=['object']).columns.tolist()

    # %%
    # 福利项目
    df_data['BEN_HEAD'].value_counts()

    # %%
    # 福利项目类型
    df_data['BEN_HEAD_TYPE'].value_counts()

    # %%
    # 福利类型
    df_data['BEN_TYPE'].value_counts()

    # %%
    # 保险公司医院代码
    df_data['CLSH_HOSP_CODE'].value_counts()

    # 值很多

    # %%
    suspicious_status = ['CL_LINE_STATUS_PD','CL_LINE_STATUS_RJ','CL_LINE_STATUS_UE']
    nomal_status = ['CL_LINE_STATUS_AC']

    sum_suspicious = 0
    sum_nomal = 0
    for i in suspicious_status:
        sum_suspicious += len(df_data['CLSH_HOSP_CODE'][df_data['SCMA_OID_CL_LINE_STATUS'] == i ].value_counts())

    # 和欺诈相关的保险公司医院代码总数
    print("和欺诈相关的疾病编码的名称总数为：",sum_suspicious)
    # 和欺诈无关的保险公司医院代码总数
    print("和欺诈无关的疾病编码的名称总数为：",len(df_data['CLSH_HOSP_CODE'][df_data['SCMA_OID_CL_LINE_STATUS'] == 'CL_LINE_STATUS_AC'].value_counts()))

    # 保险公司医院代码总数目
    print("保险公司医院代码的总数目",len(df_data['CLSH_HOSP_CODE'].value_counts()))

    # %%
    # 创建者
    df_data['CRT_USER'].value_counts()

    # %%
    # 杂项- CSR备注
    df_data['CSR_REMARK'].value_counts()

    # 值很多；有标注1，无标注0

    # %%
    # 疾病代码
    df_data['DIAG_CODE'].value_counts()

    # 值很多

    # %%
    suspicious_status = ['CL_LINE_STATUS_PD','CL_LINE_STATUS_RJ','CL_LINE_STATUS_UE']
    nomal_status = ['CL_LINE_STATUS_AC']

    sum_suspicious = 0
    sum_nomal = 0
    for i in suspicious_status:
        sum_suspicious += len(df_data['DIAG_CODE'][df_data['SCMA_OID_CL_LINE_STATUS'] == i ].value_counts())

    # 和欺诈相关的病编码的名称总数
    print("和欺诈相关的疾病编码的名称总数为：",sum_suspicious)
    # 和欺诈无关的病编码的名称总数
    print("和欺诈无关的疾病编码的名称总数为：",len(df_data['DIAG_CODE'][df_data['SCMA_OID_CL_LINE_STATUS'] == 'CL_LINE_STATUS_AC'].value_counts()))

    #疾病编码的总数目
    print("疾病编码的总数目",len(df_data['DIAG_CODE'].value_counts()))

    # 值很多

    # %%
    # 出险开始日期
    df_data['INCUR_DATE_FROM'].value_counts()

    # %%
    # 出险结束日期
    df_data['INCUR_DATE_TO'].value_counts()

    # %%
    # 发票资料退回标志
    df_data['INVOICE_RTN_IND'].value_counts()

    # %%
    # 险种类型代码
    df_data['KIND_CODE'].value_counts()

    # %%
    # 被保险人类型
    df_data['MBR_TYPE'].value_counts()

    # %%
    # 被保险人备注
    df_data['MEMBER_EVENT'].value_counts()

    # %%
    # 核准金额（货币）
    df_data['ORG_PRES_AMT'].value_counts()

    # 值很多,分块,价格区间编码

    # %%
    # 投保人编号
    df_data['POHO_NO'].value_counts()

    # %%
    # 一级合作经纪人名
    df_data['PRI_CORR_BRKR_NAME'].value_counts()

    # %%
    # 医院科室
    df_data['PROV_DEPT'].value_counts()

    # %%
    # 医院等级
    df_data['PROV_LEVEL'].value_counts()

    # %%
    # 医疗机构名称
    df_data['PROV_NAME'].value_counts()

    # 值很多

    # %%
    # 理赔收单日
    df_data['RCV_DATE'].value_counts()

    # %%
    # 福利类型
    df_data['SCMA_OID_BEN_TYPE'].value_counts()

    # %%
    # 理赔条状态
    # ★此列为标签列
    df_data['SCMA_OID_CL_LINE_STATUS'].value_counts()

    # %%
    # 案件状态
    df_data['SCMA_OID_CL_STATUS'].value_counts()

    # %%
    # 理赔类型
    df_data['SCMA_OID_CL_TYPE'].value_counts()

    # %%
    # 治疗国家
    df_data['SCMA_OID_COUNTRY_TREATMENT'].value_counts()

    # %%
    # 产品类型
    df_data['SCMA_OID_PROD_TYPE'].value_counts()

    # %%
    # 单位
    df_data['WORKPLACE_NAME'].value_counts()

    # 值很多

    # %% [markdown]
    # ## 1.3 查看数值型数据

    # %%
    # 已使用日限额 
    df_data['AMT_DAY_USED'].value_counts().sort_index()

    # %%
    # 自费金额
    df_data['CL_OWNER_PAY_AMT'].value_counts()

    # %%
    # 分类自付金额 
    df_data['CL_SELF_CAT_PAY_AMT'].value_counts()

    # %%
    # 社保基金支付金额
    df_data['CL_SOCIAL_PAY_AMT'].value_counts()

    # %%
    # 第三方支付金额
    df_data['CL_THIRD_PARTY_PAY_AMT'].value_counts()

    print("缺失值占比：%f%%"%(df_data['CL_THIRD_PARTY_PAY_AMT'].value_counts()[0]/len(df_data['CL_THIRD_PARTY_PAY_AMT'])*100))
    # 绝大多数都是0，删除

    # %%
    # 自付比例
    df_data['COPAY_PCT'].value_counts()

    # 需要后续对变量COPAY_PCT（自负比例）进行字符编码处理

    # %%
    # 查看数据的分布情况
    df_data['COPAY_PCT'].hist()

    # 从数据的分布来看，并不离散

    # %%
    # 福利项目的日限额
    df_data['CWF_AMT_DAY'].value_counts()

    # %%
    # 查看数据的分布情况
    df_data['CWF_AMT_DAY'].hist()

    #从数据的分布可以看出"福利项目日限额"字段虽然是数值型变量，但是取值离散化，可以当成分类变量处理

    # 需要后续对变量CWF_AMT_DAY（福利项目的日限额）进行字符编码处理

    # %%
    # 汇率
    df_data['FX_RATE'].value_counts()

    # 计划删除，1汇率为人民币，非1汇率为美元；美元数据仅占 0.026%

    # %%
    # 被保险人编号
    df_data['MBR_NO'].value_counts()

    # 删除，无关字段

    # %%
    # 年数
    df_data['NO_OF_YR'].value_counts()

    # %%
    # 案件保单数
    df_data['POLICY_CNT'].value_counts()

    # %%
    # 医院代码
    df_data['PROV_CODE'].value_counts()

    # %%
    # 发票金额
    df_data['SUB_AMT'].value_counts()

    # %%
    # 发票总金额
    df_data['TOTAL_RECEIPT_AMT'].value_counts()

    # %% [markdown]
    # # 二、数据探索性分析

    # %% [markdown]
    # ## 2.1 处理标签列
    # - 为了更好地分析各字段和标签列的关系，先处理标签列

    # %%
    # 对标签列进行处理，删除标签为'CL_LINE_STATUS_PV'、'CL_LINE_STATUS_PD'的数据
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())
    # df_data_1 = df_data.drop(index=(df_data.loc[df_data['SCMA_OID_CL_LINE_STATUS']=='CL_LINE_STATUS_PV'].index),inplace=False)

    drop_value_list = ['CL_LINE_STATUS_PV', 'CL_LINE_STATUS_PD']
    drop_idx_list = [i for i, v in df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'].items() if v in drop_value_list]
    print(drop_idx_list)

    df_data = df_data.drop(axis=0, index=drop_idx_list, inplace=False)
    print("删除'CL_LINE_STATUS_PV'、'CL_LINE_STATUS_PD'后的:\n")
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())

    # %%
    # 对标签进行编码(LabelEncoder)
    from sklearn.preprocessing import LabelEncoder

    y = df_data.loc[:,'SCMA_OID_CL_LINE_STATUS'] # 获得标签列（保存一分后面用得到）

    # %%
    le = LabelEncoder() # 实例化，即创建对象
    le = le.fit(y)  # 导入数据
    label = le.transform(y) # tranform接口调取结果,也可以直接使用fit_transform接口一步到位

    le.classes_ # 属性.classes_查看标签中究竟有多少类别

    # %%
    # 查看获取的结果label
    label

    # %%
    # 把处理好的标签，赋值回原数据矩阵
    df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'] = label

    # 查看结果
    print("line SCMA_OID_CL_LINE_STATUS:")
    print(df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'].head(20))

    print("\nline SCMA_OID_CL_LINE_STATUS value statistic:")
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())

    # %%
    # 标签列改名为 FRAUD
    df_data.rename(columns={'SCMA_OID_CL_LINE_STATUS': 'FRAUD'}, inplace=True)


    # %% [markdown]
    # ## 2.2 数据相关性分析

    # %%
    import matplotlib.pyplot as plt
    import seaborn as sns

    #corr 相关系数函数，[-1,1]，-1反相关，+1正相关
    corrmat = df_data.corr()

    #print(corrmat)
    f,ax = plt.subplots(figsize=(18,14))
    sns.heatmap(corrmat, vmax=0.8, square=True,annot=True)

    # 相关度比较大的有 
    # CL_OWNER_PAY_AMT    CL_SOCIAL_PAY_AMT
    # CL_OWNER_PAY_AMT    SUB_AMT    
    # CL_OWNER_PAY_AMT    TOTAL_RECEIPT_AMT
    # CL_SOCIAL_PAY_AMT   SUB_AMT 
    # CL_OWNER_PAY_AMT    TOTAL_RECEIPT_AMT


    # %% [markdown]
    # ## 2.3 某些字段与结果的关系分析
    # ### 用violin图探索FRAUD和某些变量之间的关系
    # 
    # - 1）FRAUD 和 BEN_TYPE 福利类型之间的关系

    # %%
    # 福利类型
    df_data['BEN_TYPE'].unique()

    # 条形图
    # f,ax = plt.subplots(figsize=(12,9))
    sns.barplot(x='BEN_TYPE',y='FRAUD', data=df_data) 

    # %%
    # 查看和福利类型相关的欺诈占比
    # groupby 分组方法，by是分组字段，常用为列名，as_index，是否将分组列名作为输出的索引，默认为True，设置为False时相当于加了reset_index功能
    # agg 聚合方法，该函数传入的参数为字典，键为变量名，值为对应的聚合函数字符串，sum求和即欺诈的数量，count为总共的条数
    df_BEN_TYPE = df_data.groupby('BEN_TYPE', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_BEN_TYPE)

    # %% [markdown]
    # - 2）查看欺诈和MBR_TYPE被保险人类型的关系

    # %%
    # 查看所有被保险人类型
    df_data['MBR_TYPE'].unique()

    # %%
    # f,ax = plt.subplots(figsize=(12,9))   # 设置图形的大小，单位为英寸
    sns.barplot(x='MBR_TYPE',y='FRAUD', data=df_data)

    # %%
    # 查看和被保险人类型相关的欺诈占比
    # 分组，聚合
    df_MBR_TYPE = df_data.groupby('MBR_TYPE', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_MBR_TYPE)

    # %% [markdown]
    # - 3） FRAUD 和 COPAY_PCT 病人自付比例之间的关系

    # %%
    # 查看所有自付比例
    df_data['COPAY_PCT'].unique()

    # %%
    # f,ax = plt.subplots(figsize=(12,9))
    sns.barplot(x='COPAY_PCT',y='FRAUD', data=df_data)

    # %%
    # 查看和自付比例相关的欺诈占比
    df_COPAY_PCT = df_data.groupby('COPAY_PCT', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_COPAY_PCT)

    # %% [markdown]
    # - 4） FRAUD 和 NO_OF_YR 年数比例之间的关系
    # 

    # %%
    # 查看所有年数
    df_data['NO_OF_YR'].unique()

    # %%
    # f,ax = plt.subplots(figsize=(12,9))
    sns.barplot(y='FRAUD', x='NO_OF_YR', data=df_data)

    # %%
    # 查看和年数比例相关的欺诈占比
    df_NO_OF_YR = df_data.groupby('NO_OF_YR', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_NO_OF_YR)

    # %% [markdown]
    # - 5） FRAUD 和 BEN_HEAD 福利项目比例之间的关系
    # 

    # %%
    # 查看所有福利项目
    df_data['BEN_HEAD'].unique()

    # %%
    # f,ax = plt.subplots(figsize=(12,9))
    # sns.barplot(y='FRAUD', x='BEN_HEAD', data=df_data)

    # %%
    # 查看和福利项目比例相关的欺诈占比
    df_BEN_HEAD = df_data.groupby('BEN_HEAD', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_BEN_HEAD)

    # %% [markdown]
    # - 6） FRAUD 和 PROV_LEVEL 医院等级之间的关系
    # 

    # %%
    # 查看所有医院等级
    df_data['PROV_LEVEL'].unique()

    # %%
    # f,ax = plt.subplots(figsize=(12,9))
    sns.barplot(y='FRAUD', x='PROV_LEVEL', data=df_data)

    # %%
    # 查看和医院等级比例相关的欺诈占比
    df_PROV_LEVEL = df_data.groupby('PROV_LEVEL', as_index=False).agg({"FRAUD":['sum','mean','count']})
    print(df_PROV_LEVEL)

    # %% [markdown]
    # # 三、数据清洗和特征工程

    # %% [markdown]
    # ## 3.1 缺失值处理

    # %%
    # 查看缺失值统计
    df_data.isna().sum()

    # %%
    type(df_data.isna().sum())  # Series
    # df_data.isna().sum()[2]
    # 查看缺失值数据类型
    print("%-10s"%"存在缺失值字段","%-8s"%"字段数据类型","缺失值个数")
    for key,value in df_data.isna().sum().to_dict().items():
        if(value!=0):
            print("%-20s"%key,"%-15s"%df_data[key].dtypes,df_data[key].isna().sum())

    # %%
    # 空白缺失值的个数
    df_data.loc[:,'AMT_DAY_USED'].isna().sum()  # 定位行列：data.loc[行索引, 列名]，获得不是数值的个数，即空白缺失值的个数。

    # %%
    print("缺失值占比：%f%%"%(df_data.loc[:,'AMT_DAY_USED'].isna().sum()/len(df_data['AMT_DAY_USED'])*100))
    # 绝大多数都是0，删除

    # %%
    # 删除 AMT_DAY_USED 字段(缺失值太多)

    df_data = df_data.drop(['AMT_DAY_USED'],axis=1)

    # 用中位数填充已使用限额
    # df_data.loc[:,'AMT_DAY_USED'] = df_data.loc[:,'AMT_DAY_USED'].fillna(df_data.loc[:,'AMT_DAY_USED'].median())
    # df_data.isna().sum()

    # %%
    # 查看填充后的结果
    df_data.head()

    # %%
    '''
    AMT_DAY_USED         float64         75102   # 已使用日限额                   √
    BEN_HEAD_TYPE        object          26492   # 福利项目                       √
    CLSH_HOSP_CODE       object          9212    # 保险公司医院代码               √  ×
    CSR_REMARK           object          68410   # 杂项 - CSR备注                 √
    INVOICE_RTN_IND      object          77028   # 发票资料退回标志               √
    KIND_CODE            object          1748    # 险种类型代码                   √ 
    PROV_DEPT            object          47683   # 医院科室                       √
    PROV_LEVEL           object          649     # 医院等级                       √
    WORKPLACE_NAME       object          1742    # 单位                           √  ×


    CRT_USER             object          1       # 创建者                         √
    PROV_NAME            object          1       # 医疗机构名称                   √  ×
    PROV_CODE            float64         1       # 医院代码                       √  ×
    '''

    # %%
    print("缺失值占比：%f%%"%(df_data.loc[:,'CSR_REMARK'].isna().sum()/len(df_data['CSR_REMARK'])*100))
    # 绝大多数都是0，删除

    # %%
    # 删除 CSR_REMARK 列
    df_data = df_data.drop(['CSR_REMARK'],axis=1)

    # %%
    # 填充其他的缺失值数据（只有一条缺失值的删除整行数据）
    # df_data.loc[:,'BEN_HEAD_TYPE ] = df_data.loc[:,'BEN_HEAD_TYPE '].fillna(df_data.loc[:,'BEN_HEAD_TYPE '].median())

    print("df_data['BEN_HEAD_TYPE']的值统计：\n%s"%df_data['BEN_HEAD_TYPE'].value_counts())
    '''
    YPF    33618
    JCF    16368
    CWF       65
    (Unkonwn    26378) 
    '''
    fill_list = ['BEN_HEAD_TYPE','KIND_CODE','PROV_DEPT']
    for i in fill_list:
        df_data.loc[:,i] = df_data.loc[:,i].fillna('Unkonwn')  # Unkonwn    26378


    # df_data['INVOICE_RTN_IND'].unique()
    # df_data['INVOICE_RTN_IND'].value_counts()
    # 8 nan
    # 51 Y

    df_data.loc[:,'INVOICE_RTN_IND'] = df_data.loc[:,'INVOICE_RTN_IND'].fillna('N')
    df_data.loc[:,'INVOICE_RTN_IND'] = df_data.loc[:,'INVOICE_RTN_IND'].replace('nan','N')
    # df_data['INVOICE_RTN_IND'].unique()
    print("\n填充后 df_data['INVOICE_RTN_IND'] 的值统计:\n%s"%df_data['INVOICE_RTN_IND'].value_counts())


    # df_data.isna().sum()

    # %%
    # 以下字段缺失值数量少，直接删除有缺失值所在行
    del_field_null_list = ['CRT_USER','PROV_NAME','PROV_CODE','PROV_LEVEL','CLSH_HOSP_CODE']
    for i in del_field_null_list:
        df_data = df_data.dropna(axis=0, subset=[i])
    # df_data.isna().sum()


    # 删掉(值太多且关联性不大)

    del_field_list = ['PROV_NAME','WORKPLACE_NAME']
    df_data = df_data.drop(del_field_list,axis=1)
    df_data.isna().sum()

    # %%
    # 缺失值处理完毕，查看是否还有缺失值
    df_data.isna().sum()

    # %% [markdown]
    # ## 3.2 异常值处理

    # %% [markdown]
    # - 异常值分析 → 3σ原则 / 箱型图分析

    # %% [markdown]
    # ### 3.2.1 3σ原则分析异常值

    # %%
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats

    # %%
    # 异常值分析
    class ExceptionAnalysis_1:
        def __init__(self):
            pass

        def show_exception_analysis(self,series):
            data = series

            u = data.mean()  # 计算均值
            std = data.std()  # 计算标准差
            stats.kstest(data, 'norm', (u, std))  # kstest，数据分布检验模块，正态性检验或其他数据分布类型，仅适用于连续分布的检验
            print('均值为：%.3f，标准差为：%.3f' % (u, std))
            print('------\n')

            # 正态性检验
            # 绘制数据密度曲线
            fig = plt.figure(figsize=(10, 6))
            ax1 = fig.add_subplot(2, 1, 1)
            data.plot(kind='kde', grid=True, style='-k', title='密度曲线')
            plt.axvline(3 * std, color='r', linestyle="--", alpha=0.8)
            plt.axvline(-3 * std, color='r', linestyle="--", alpha=0.8)

            # 筛选出异常值error、剔除异常值之后的数据data_c
            ax2 = fig.add_subplot(2, 1, 2)
            error = data[np.abs(data - u) > 3 * std]  # 大于3σ的异常值数据
            data_c = data[np.abs(data - u) <= 3 * std]  # 小于等于3σ的正常值数据
            print('异常值共%i条\n' % len(error))
            print('异常数据：\n{}'.format(error.index))
            print(len(df_data))
            del_index_list = error.index
            

            # 图表表达
            plt.scatter(data_c.index, data_c, color='k', marker='.', alpha=0.3)
            plt.scatter(error.index, error, color='r', marker='.', alpha=0.5)
            plt.xlim([-100, 100])
            plt.grid()
            
            return del_index_list

    # %%
    # 可研究的数值型字段
    digital_features = list(df_data.select_dtypes(include=['float64','int64']).columns)
    unrequired_process_features  = ['MBR_NO','POLICY_CNT','PROV_CODE']
    digital_features = [item for idx,item in enumerate(digital_features) if item not in unrequired_process_features]
    digital_features

    # %%
    ea1 = ExceptionAnalysis_1()

    # %%
    # for i in digital_features:
    #     ea.show_exception_analysis(df_data[i])

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['CL_OWNER_PAY_AMT'])

    print(del_index_list)

    df_data.drop(index=del_index_list,inplace=True)
    print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['CL_SELF_CAT_PAY_AMT'])

    df_data.drop(index=del_index_list,inplace=True)
    print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['CL_SOCIAL_PAY_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['CL_THIRD_PARTY_PAY_AMT'])

    df_data.drop(index=del_index_list,inplace=True)
    print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['CWF_AMT_DAY'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['NO_OF_YR'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['SUB_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea1.show_exception_analysis(df_data['TOTAL_RECEIPT_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    print(len(df_data))

    # %% [markdown]
    # ### 3.2.2 箱线图分析异常值

    # %%
    class ExceptionAnalysis_2:
        def __init__(self):
            pass
        def show_exception_analysis(self,series):
            # 箱型图分析
            # 箱型图看数据分布情况
            # 以内限为界
            data = series
            fig = plt.figure(figsize=(10, 6))
            ax1 = fig.add_subplot(2, 1, 1)
            color = dict(boxes='DarkGreen', whiskers='DarkOrange', medians='DarkBlue', caps='Gray')
            data.plot.box(vert=False, grid=True, color=color, ax=ax1, label='样本数据')

            # 基本统计量
            s = data.describe()  # 提供了平均值mean,标准差std,最小值min,最大值max以及1/4,1/2,3/4分位数
            print(s)
            print('------')

            # 计算分位差
            q1 = s['25%']  # 1/4分位数
            q3 = s['75%']  # 3/4分位数
            iqr = q3 - q1
            mi = q1 - 1.5 * iqr  # 分位差下限
            ma = q3 + 1.5 * iqr  # 分位差上限
            print('分位差为：%.3f，下限为：%.3f，上限为：%.3f' % (iqr, mi, ma))
            print('------')

            # 筛选出异常值error、剔除异常值之后的数据data_c
            ax2 = fig.add_subplot(2, 1, 2)
            error = data[(data < mi) | (data > ma)]
            data_c = data[(data >= mi) & (data <= ma)]
            print('异常值共%i条' % len(error))
            print('异常数据：\n{}'.format(error.index))
            del_index_list = error.index
            # df_data.drop(index=del_index_list, inplace=True)

            # 图表表达
            plt.scatter(data_c.index, data_c, color='k', marker='.', alpha=0.3)
            plt.scatter(error.index, error, color='r', marker='.', alpha=0.5)
            plt.xlim([-100, 100])
            plt.grid()
            
            return del_index_list

    # %%
    ea2 = ExceptionAnalysis_2()

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['CL_OWNER_PAY_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['CL_SELF_CAT_PAY_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['CL_SOCIAL_PAY_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['CL_THIRD_PARTY_PAY_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['COPAY_PCT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['CWF_AMT_DAY'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['NO_OF_YR'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['SUB_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    del_index_list = ea2.show_exception_analysis(df_data['TOTAL_RECEIPT_AMT'])

    # df_data.drop(index=del_index_list,inplace=True)
    # print(len(df_data))

    # %%
    print(len(df_data))

    # %% [markdown]
    # ### 3.2.3 其他异常值

    # %%
    # 'POHO_NO'中出现异常值(出现了非数值数据)，删除
    df_data['POHO_NO'] = pd.to_numeric(df_data['POHO_NO'], errors='coerce')

    # 删除包含NaN值的行
    df_data = df_data.dropna()

    # 将col1列转换回Object类型
    df_data['POHO_NO'] = df_data['POHO_NO'].astype(str)
    df_data['POHO_NO'].value_counts()

    # %% [markdown]
    # ## 3.3 处理非数值型数据
    # - 删除一些无关
    # - 对相关变量进行哑变量处理

    # %% [markdown]
    # ### 3.3.1 删除无关列

    # %%
    # 删除以下字段（所有数据该列值都是同一个）
    del_field_list = ['MEMBER_EVENT', 'PRI_CORR_BRKR_NAME', 'SCMA_OID_CL_TYPE', 'SCMA_OID_PROD_TYPE', 'INCUR_DATE_FROM','INCUR_DATE_TO']
    df_data = df_data.drop(del_field_list, axis=1)
    # FX_RATE 字段也删除（所有数据该列值都是同一个）
    df_data = df_data.drop(['FX_RATE'], axis=1)
    df_data.isna().sum()

    # %% [markdown]
    # ### 3.3.2 哑变量处理
    # 

    # %%
    df_data_process = df_data
    # 删除某些待定的 无用的列
    del_field_list = ['RCV_DATE']
    df_data_process = df_data_process.drop(del_field_list,axis=1)





    # 医院等级（中文->英文标记）映射（中文映射为英文）
    PROV_LEVEL_lever_to_symbol = {
        '一级':'L0',
        '二级':'L1',
        '三级':'L2',
        '未评级':'L3',
        '医保':'L4',
        '非医保':'L5',
        '卫生所':'L6',
        '未知':'L7'
    }
    df_data_process['PROV_LEVEL'] = df_data_process['PROV_LEVEL'].map(PROV_LEVEL_lever_to_symbol)


    # 哑变量处理
    '''
    pre_dummies_columns = ['BEN_HEAD_TYPE','INVOICE_RTN_IND','MBR_TYPE','POLICY_CNT','PROV_LEVEL','SCMA_OID_BEN_TYPE','SCMA_OID_CL_LINE_STATUS','SCMA_OID_CL_STATUS','SCMA_OID_COUNTRY_TREATMENT']
    dummies_columns_prefix = ['BEN_HEAD_TYPE_','INVOICE_RTN_IND_','MBR_TYPE_','POLICY_CNT_','PROV_LEVEL_','SCMA_OID_BEN_TYPE_','SCMA_OID_CL_LINE_STATUS_','SCMA_OID_CL_STATUS_','SCMA_OID_COUNTRY_TREATMENT_']
    '''
    pre_dummies_columns = ['BEN_HEAD_TYPE','INVOICE_RTN_IND','MBR_TYPE','POLICY_CNT','PROV_LEVEL','SCMA_OID_BEN_TYPE','SCMA_OID_CL_STATUS','SCMA_OID_COUNTRY_TREATMENT']
    dummies_columns_prefix = ['BEN_HEAD_TYPE_','INVOICE_RTN_IND_','MBR_TYPE_','POLICY_CNT_','PROV_LEVEL_','SCMA_OID_BEN_TYPE_','SCMA_OID_CL_STATUS_','SCMA_OID_COUNTRY_TREATMENT_']


    for idx in range(len(pre_dummies_columns)):
        dummies_item = pd.get_dummies(df_data_process[pre_dummies_columns[idx]],prefix=dummies_columns_prefix[idx])
        df_data_process = pd.concat([df_data_process, dummies_item], axis=1)
        df_data_process.drop( pre_dummies_columns[idx],axis=1, inplace=True)
    df_data_process.isna().sum()


    # %% [markdown]
    # ### 3.3.3 非数值型相关字段分类后哑变量处理

    # %%
    print(df_data_process['CLSH_HOSP_CODE'].dtypes)
    print(set(df_data_process['CLSH_HOSP_CODE'].values))
    print(len(df_data_process['CLSH_HOSP_CODE'].value_counts()))
    # df_data_process['CLSH_HOSP_CODE'] = df_data_process['CLSH_HOSP_CODE'].astype(str)


    import string

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
    print(province_code_dict)


    # 定义一个函数，根据首字母返回对应的数字
    def get_alpha_num(alpha):
        if alpha[2:4] in province_code_dict:  # 按照第1个字符编码
            return province_code_dict[alpha[2:4]]
        else:
            return None

    df_data_process['CLSH_HOSP_CODE'] = df_data_process['CLSH_HOSP_CODE'].apply(get_alpha_num)

    # 删除空值所在行
    df_data_process = df_data_process.dropna(axis=0,subset=['CLSH_HOSP_CODE'])
    print(df_data_process.isna().sum())
    df_data_process['CLSH_HOSP_CODE'].value_counts()


    # 哑变量处理
    df_data_process = pd.get_dummies(df_data_process, columns=['CLSH_HOSP_CODE'])
    df_data_process

    # %%
    # DIAG_CODE

    print(df_data_process['DIAG_CODE'].dtypes)
    print(set(df_data_process['DIAG_CODE'].values))
    print(len(df_data_process['DIAG_CODE'].value_counts()))
    df_data_process['DIAG_CODE'] = df_data_process['DIAG_CODE'].astype(str)

    import string

    # 定义一个字典，将26个字母映射为数字
    # alpha_dict = {alpha: num for num, alpha in enumerate(string.ascii_uppercase)}
    alpha_dict = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}
    print(alpha_dict)


    # 定义一个函数，根据首字母返回对应的数字
    def get_alpha_num(alpha):
        if alpha[0] in alpha_dict:  # 按照第1个字符编码
            return alpha_dict[alpha[0]]
        else:
            return None


    df_data_process['DIAG_CODE'] = df_data_process['DIAG_CODE'].apply(get_alpha_num)

    df_data_process['DIAG_CODE'].value_counts()


    # 删除空值所在行
    df_data_process = df_data_process.dropna(axis=0,subset=['DIAG_CODE'])
    print(df_data_process.isna().sum())
    df_data_process['DIAG_CODE'].value_counts()


    # 哑变量处理
    df_data_process = pd.get_dummies(df_data_process, columns=['DIAG_CODE'])
    df_data_process

    # %% [markdown]
    # - 将未处理(保留)的字段放到数据表最后

    # %%
    # MBR_NO
    series_tmp = df_data_process['MBR_NO']
    df_data_process.drop(['MBR_NO'],axis=1, inplace=True)
    df_data_process['MBR_NO'] = series_tmp

    # %%
    # POHO_NO
    series_tmp = df_data_process['POHO_NO']
    df_data_process.drop(['POHO_NO'],axis=1, inplace=True)
    df_data_process['POHO_NO'] = series_tmp

    # %%
    # BEN_HEAD
    series_tmp = df_data_process['BEN_HEAD']
    df_data_process.drop(['BEN_HEAD'],axis=1, inplace=True)
    df_data_process['BEN_HEAD'] = series_tmp

    # %%
    # BEN_TYPE
    series_tmp = df_data_process['BEN_TYPE']
    df_data_process.drop(['BEN_TYPE'],axis=1, inplace=True)
    df_data_process['BEN_TYPE'] = series_tmp

    # %%
    # CRT_USER
    series_tmp = df_data_process['CRT_USER']
    df_data_process.drop(['CRT_USER'],axis=1, inplace=True)
    df_data_process['CRT_USER'] = series_tmp

    # %%
    # KIND_CODE
    series_tmp = df_data_process['KIND_CODE']
    df_data_process.drop(['KIND_CODE'],axis=1, inplace=True)
    df_data_process['KIND_CODE'] = series_tmp

    # %%
    # PROV_CODE
    series_tmp = df_data_process['PROV_CODE']
    df_data_process.drop(['PROV_CODE'],axis=1, inplace=True)
    df_data_process['PROV_CODE'] = series_tmp

    # %%
    # PROV_DEPT
    series_tmp = df_data_process['PROV_DEPT']
    df_data_process.drop(['PROV_DEPT'],axis=1, inplace=True)
    df_data_process['PROV_DEPT'] = series_tmp

    # %% [markdown]
    # ## 3.4 数值型数据处理
    # - 数值变量数据log10X纠偏
    # - log10X纠偏后标准化
    # - 区间分段编码

    # %% [markdown]
    # ### 3.4.1 数值变量数据log10X纠偏

    # %%
    # 删除 CL_THIRD_PARTY_PAY_AMT (大部分数值都是0)

    df_data_process = df_data_process.drop(['CL_THIRD_PARTY_PAY_AMT'],axis=1)

    # %% [markdown]
    # #### 查看CL_OWNER_PAY_AMT数据分布
    # 

    # %%
    df_data_process['CL_OWNER_PAY_AMT'].hist()   # 直方图

    # %%
    data1 = df_data_process['CL_OWNER_PAY_AMT'].where(df_data_process['CL_OWNER_PAY_AMT']<=600, other=601)
    data1.hist()

    # %%
    # SUB_AMT 数据偏态严重
    data2 = df_data_process['SUB_AMT'].where(df_data_process['SUB_AMT']<=2000, other=2001)
    data2.hist()

    # %%
    # 对所有的float64的数据进行数据纠偏操作
    # 找出df1中数值型的变量,查看数据的偏度，所有偏度都远大于零，说明数据右偏。
    from scipy.stats import skew

    numeric_feats = df_data_process.dtypes[df_data_process.dtypes == 'float64'].index
    skewed_feats = df_data_process[numeric_feats].apply(lambda x: skew(x.dropna()))
    skewed_feats

    # %%
    # 筛选出对所有的float64的数据
    # log_features = list(df_data_process.select_dtypes(include=['float64']).columns)
    # log_features

    # 筛选出对所有的float64的数据
    log_features = list(df_data_process.select_dtypes(include=['float64','int64']).columns)
    unrequired_process_features  = ['MBR_NO','POLICY_CNT','PROV_CODE']
    log_features = [item for idx,item in enumerate(log_features) if item not in unrequired_process_features]
    log_features

    # %%
    # 对这些偏度大的金额数据进行Log10()转换的纠偏处理

    for i in log_features:
        df_data_process[i] = df_data_process[i].map(lambda x: np.log10(x) if x>0 else 0)

    df_data_process[log_features].describe()

    # %%
    # 查看用log10X进行纠偏后数据的偏度，因为数据严重右偏的得到纠偏后还是有些偏态的。但是相比之前的数据状态已经调整了很多。
    skewed_feats_afterlog = df_data_process[log_features].apply(lambda x: skew(x.dropna()))
    skewed_feats_afterlog

    # %% [markdown]
    # ### 3.4.2 数据标准化
    # #### 对log纠偏的数值型变量float64，进行数据标准化操作：MinMaxScaler¶

    # %%
    # 对float64相关的数值变量进行区间缩放数据标准化处理(0-1)
    from sklearn.preprocessing import MinMaxScaler
    trans = MinMaxScaler()   # 归一化[0,1]

    df_data_process[log_features] = trans.fit_transform(df_data_process[log_features])
    df_data_process[log_features].describe()

    # %% [markdown]
    # ### 对 ORG_PRES_AMT 进行换算，变为数值

    # %%
    # ORG_PRES_AMT

    print(df_data['ORG_PRES_AMT'].value_counts(),"\n\n")
    print(df_data['ORG_PRES_AMT'].sort_values(),"\n")

    def replace_of_squares(x):
        if x.startswith("RMB "):
            x = x.lstrip("RMB ")
            
            return float(x)
        else:
            x = x.lstrip("USD ")
            return float(x)*7

    df_data_process['ORG_PRES_AMT'] = df_data_process['ORG_PRES_AMT'].apply(replace_of_squares)
    print(df_data_process['ORG_PRES_AMT'].sort_values())
    df_data_process = df_data_process.dropna(axis=0,subset=['ORG_PRES_AMT'])


    # 显示结果
    print(df_data_process.isna().sum())
    df_data_process['ORG_PRES_AMT'].value_counts()



    # 标准化处理(0-1)
    from sklearn.preprocessing import MinMaxScaler
    trans = MinMaxScaler()   # 归一化[0,1]

    df_data_process[['ORG_PRES_AMT']] = trans.fit_transform(df_data_process[['ORG_PRES_AMT']])
    df_data_process[['ORG_PRES_AMT']].describe()

    # %% [markdown]
    # ## 5.特征选择

    # %% [markdown]
    # ## 5.1 包装法特征选择（wrapper）

    # %%
    df_data_process.dtypes

    # %%
    pre_selection_columns = df_data_process.dtypes.index[0:-8]

    # %%
    # 训练数据
    X = df_data_process[pre_selection_columns].drop('FRAUD',axis=1)
    X

    # %%
    # 标签列
    y = df_data_process['FRAUD']

    # %%
    from sklearn.feature_selection import RFE
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestClassifier as RFC


    RFC_ = RFC(n_estimators =10,random_state=0)
    selector = RFE(RFC_, n_features_to_select=80, step=50).fit(X, y)

    print(selector.support_.sum()) #.support_：返回所有的特征的是否最后被选中的布尔矩阵
    print(selector.ranking_ )# .ranking_返回特征的按数次迭代中综合重要性的排名

    X_wrapper = selector.transform(X)
    cross_val_score(RFC_,X_wrapper,y,cv=5).mean() # score得分为0.93797619

    # %%
    df_data_selected_features = X.iloc[:, selector.support_]
    df_data_selected_features
    # X_wrapper

    # %%
    # 对包装法画学习曲线,找到最优特征参数
    score = []
    for i in range(1,751,50):
        X_wrapper = RFE(RFC_,n_features_to_select=i, step=50).fit_transform(X,y)
        once = cross_val_score(RFC_,X_wrapper,y,cv=5).mean()
        score.append(once)
    plt.figure(figsize=[20,5])
    plt.plot(range(1,751,50),score)
    plt.xticks(range(1,751,50))
    plt.show()

    # %%
    # 拼起来

    # %%
    df_data_selected_features.columns

    # %%
    concat_columns = df_data_process.dtypes.index[-8:]
    df_data_process = pd.concat([df_data_selected_features,df_data_process[concat_columns],df_data_process['FRAUD']],axis=1)

    # %%
    df_data_process

    # %%


    # %% [markdown]
    # ## 降维

    # %% [markdown]
    # - class sklearn.decomposition.PCA (n_components=None, copy=True, whiten=False, svd_solver=’auto’, tol=0.0,iterated_power=’auto’, random_state=None)
    # 
    # - n_components是我们降维后需要的维度，即降维后需要保留的特征数量。取太小，特征向量无法表达原数据的信息；如果取值大，起不到降维的效果。
    # 
    # - 可以先从我们的降维目标说起：如果我们希望可视化一组数据来观察数据分布，通常是把数据降到二维，即n_components的取值为2。
    # 

    # %%
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    from sklearn.decomposition import PCA

    # %%
    df_data_selected_features

    # %%
    # 提取数据
    X  = df_data_selected_features

    # %%
    print(X.shape)
    import pandas as pd
    pd.DataFrame(X).head()

    # %%
    # 调用PCA
    pca = PCA(n_components=20) # 实例化
    pca = pca.fit(X) #拟合模型

    X_dr = pca.transform(X) # 获取新 X_dr
    # X_dr = PCA(2).fit_transform(X)

    X_dr.shape

    # %%
    # X_dr

    # %% [markdown]
    # 

    # %%
    df_data_process.dtypes

    # %%
    df_data_premodel = df_data_process

    # %%
    df_data.shape

    # %%
    df_data_premodel.shape

    # %% [markdown]
    # # 四、数据保存为建模使用

    # %%
    df_data_premodel.to_csv(processedFilePath ,index=False)
    print("BHHHH")
    # %%
    df_data_premodel.shape

    # %%
    list(df_data_premodel.columns)

    # %%
    df_data_premodel.dtypes

    # %%
    df_data_premodel.isna().sum()

    # %% [markdown]
    # # 数据编码标准化

    # %%
    # 删除某些待定的 ########################################################################################################################
    # del_field_list = ['BEN_HEAD','BEN_TYPE','CRT_USER','DIAG_CODE','KIND_CODE','PROV_DEPT','RCV_DATE']
    # df_data_process = df_data_process.drop(del_field_list,axis=1)

    # %%


    # %%
    '''
    # 归一化，返回值为归一化后的数据
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_data_process)

    df_data_process = pd.DataFrame(df_scaled, columns=df_data_process.columns)
    df_data_process
    '''

    # %% [markdown]
    # 

    # %% [markdown]
    # ## 提出标签列

    # %%

    '''
    # 对标签列进行处理，删除标签为'CL_LINE_STATUS_PV'、'CL_LINE_STATUS_PD'的数据
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())
    # df_data_1 = df_data.drop(index=(df_data.loc[df_data['SCMA_OID_CL_LINE_STATUS']=='CL_LINE_STATUS_PV'].index),inplace=False)

    drop_value_list = ['CL_LINE_STATUS_PV', 'CL_LINE_STATUS_PD']
    drop_idx_list = [i for i, v in df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'].items() if v in drop_value_list]
    print(drop_idx_list)
    df_data = df_data.drop(axis=0, index=drop_idx_list, inplace=False)
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())
    '''

    # %%
    '''
    # LabelEncoder

    from sklearn.preprocessing import LabelEncoder

    y = df_data.loc[:,'SCMA_OID_CL_LINE_STATUS'] # 获得标签列
    '''

    # %%

    '''
    le = LabelEncoder() # 实例化，即创建对象
    le = le.fit(y)  # 导入数据
    label = le.transform(y) # tranform接口调取结果,也可以直接使用fit_transform接口一步到位

    le.classes_ # 属性.classes_查看标签中究竟有多少类别

    '''

    # %%
    # 查看获取的结果label
    # label


    # %%
    '''
    # 把处理好的标签，赋值回原数据矩阵
    df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'] = label

    # 查看结果
    print("line SCMA_OID_CL_LINE_STATUS:")
    print(df_data.loc[:, 'SCMA_OID_CL_LINE_STATUS'].head(20))

    print("\nline SCMA_OID_CL_LINE_STATUS value statistic:")
    print(df_data['SCMA_OID_CL_LINE_STATUS'].value_counts())
    '''
