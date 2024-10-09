import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

class AdjustedTtestSelection:

    def __init__(self, fc_threshold=2.0, p_value_threshold=0.05, fdr_threshold=0.05, is_save_file=True):

        self.fc_threshold = fc_threshold
        self.pvalue_threshold = p_value_threshold
        self.fdr_threshold = fdr_threshold
        self.is_save_file =  is_save_file

    def feature_selection(self, ori_dataset, scaled_dataset=None):

        df_static = self.static_analysis_unpaired_ttest(ori_dataset, self.fc_threshold)
        df_selection = self.selection_key_features(df_static, self.fc_threshold, self.pvalue_threshold, self.fdr_threshold)

        if self.is_save_file:
            self.save_file(ori_dataset, scaled_dataset, df_static, df_selection)

        return df_static, df_selection

        
    def static_analysis_unpaired_ttest(self, dataset, fdr_threshold):

        results = {}

        group1_means = []
        group2_means = []
        fold_change = []

        shapiro_1 = []
        shapiro_2 = []

        ttest_pvalues = []

        features = [f for f in dataset.columns if f not in ['Name', 'Label']]
        labels = dataset.Label.unique()
        if len(labels) != 2:
            raise ValueError('Only the statical analysis of two group is possible.')

        for f in features:
            group1 = dataset[dataset.Label == labels[0]][f]
            group2 = dataset[dataset.Label == labels[1]][f]

            mean1 = group1.mean()
            mean2 = group2.mean()

            _, shapiro_1_pvalue = stats.shapiro(group1)
            _, shapiro_2_pvalue = stats.shapiro(group2)

            _, l = stats.levene(group1, group2)
            

            if l > 0.05:
                _, p = stats.ttest_ind(group1, group2, equal_var=True)
            else:
                _, p = stats.ttest_ind(group1, group2, equal_var=False)


            group1_means.append(mean1)
            group2_means.append(mean2)
            if mean2 != 0.0 :
                fold_change.append(mean1/mean2)
            else:
                fold_change.append(99999)
                print(f'The mean of {f} is zero in any one group...')

            shapiro_1.append(shapiro_1_pvalue)
            shapiro_2.append(shapiro_2_pvalue)

            ttest_pvalues.append(p)

        results['feature'] = features
        results[f'{labels[0]}_mean'] = group1_means
        results[f'{labels[1]}_mean'] = group2_means
        results[f'Fold_change'] = fold_change
        results[f'{labels[0]}_shaprio'] = shapiro_1
        results[f'{labels[1]}_shaprio'] = shapiro_2
        results['p_value'] = ttest_pvalues


        df = pd.DataFrame(results)
        df['p_value'] = df['p_value'].fillna(1.0)

        _, fdr, _, _ = multipletests(df['p_value'], alpha=fdr_threshold, method='fdr_bh')
        df['FDR_values'] = fdr
        return df


    def selection_key_features(self, df_static, fold_change, p_value, fdr_value):

        # fold change
        df_rev = df_static[(df_static['Fold_change'] >= fold_change) | ((df_static['Fold_change']) <= (1/fold_change))]

        # p_value
        df_rev = df_rev[(df_rev['p_value'] <= p_value)]

        # fdr_value
        df_rev = df_rev[(df_rev['FDR_values'] <= fdr_value)]

        return df_rev
    

    def save_file(self, df_ori, df_scaled, df_static, df_select, path='feature_selection.xlsx',):
        with pd.ExcelWriter(path) as writer:

            if type(df_ori) == pd.DataFrame:
                df_ori.to_excel(writer, 'original_dataset', index=False)

            if type(df_scaled) == pd.DataFrame:
                df_scaled.to_excel(writer, 'scaled_dataset', index=False)
            
            if type(df_static) == pd.DataFrame:
                df_static.to_excel(writer, 'static_analysis', index=False)

            if type(df_select) == pd.DataFrame:
                df_select.to_excel(writer, sheet_name='selected_features', index=False)

            else:
                raise ValueError('Invalid save file format')
            
            print('feature_selection.xlsx file is saved')



    def group_mean_intensity(self, dataset: pd.DataFrame, features: list):

        groups = list(dataset.Label.unique())

        results = {}

        for feat in features:

            group_intensity = []

            for group in groups:
                 mean_intensity = dataset[dataset['Label'] == group][feat].mean()
                 group_intensity.append(mean_intensity)

            results[feat] = group_intensity
        
        results = pd.DataFrame(results, index=groups).T

        return results        



class OneWayAnova:

    def __init__(self, is_save_file=False, p_value=0.05):

        self.is_save_file = is_save_file
        self.p_value = p_value
    
    def processing(self, dataset):

        one_way_f_test = self.one_way_test(dataset)
        post_hoc_test = self.post_hoc_test(dataset)

        df_static = pd.concat([one_way_f_test, post_hoc_test], axis=1)

        if self.is_save_file:

            self.save_file(dataset, df_static, self.p_value)

        return df_static



    def one_way_test(self, dataset):
        features = [feat for feat in dataset.columns if feat not in ['Name', 'Label']]
        groups = list(dataset.Label.unique())

        results = {}
        for feat in features:

            data = []
            for group in groups:

                data.append(dataset[dataset.Label == group][feat].values)

            f, p = stats.f_oneway(*data)

            results[feat] = p

        return pd.DataFrame(results, index=['one-way_pvalue']).T



    def post_hoc_test(self, dataset, post_hoc='bonferroni'):


        groups = list(dataset.Label.unique())
        num_groups = len(groups)
        features = [feat for feat in dataset.columns if feat not in ['Name', 'Label']]
        num_comparsion = num_groups * (num_groups -1) / 2

        results = {}

        for i in range(num_groups - 1):
            for j in range(i + 1, num_groups):

                df_i = dataset[dataset.Label == groups[i]]
                df_j = dataset[dataset.Label == groups[j]]
                adj_p_value  = []

                for feat in features:
                    t, p = stats.ttest_ind(df_i[feat].values, df_j[feat].values, )

                    # calcuate the adjusted p-value using bonferroni correlation
                    adj_p = p * num_comparsion
                    if adj_p > 1:
                        adj_p = 1
                    adj_p_value.append(adj_p)

                results[f'{groups[i]}_{groups[j]}'] = adj_p_value

        return pd.DataFrame(results, index=features)
    

    def save_file(self, dataset_ori, dataset_static, p_value=0.05):

        df_selection = dataset_static[dataset_static['one-way_pvalue'] <= p_value]
        df_selection['significant_sum'] = ((df_selection <= 0.05).sum(axis=1) - 1)


        with pd.ExcelWriter(path='oneway_analysis.xlsx') as writer:


            dataset_ori.to_excel(writer, 'original_dataset', index=False)
            dataset_static.to_excel(writer, 'total_oneway_analysis')
            df_selection.to_excel(writer, 'selection')
        print('oneway_analysis.xlsx file is saved')




