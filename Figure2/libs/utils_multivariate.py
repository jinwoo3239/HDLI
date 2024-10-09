import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cross_decomposition import PLSRegression


class MultiVariateAnalysis:

    def __init__(self, n_components, is_save_file=False, dpi=600):

        self.n_components = n_components
        self.is_save_file = is_save_file
        self.dpi = dpi
    
    def plsda_analysis(self, dataset, plotting=True, figsize=(5.5, 5), marker_size=100, alpha=0.8, dpi=450, palette='Set3', ):

        X = dataset.drop(columns=['Name', 'Label'], axis=1).reset_index(drop=True)
        y = dataset[['Label']].reset_index(drop=True)
        one_hot_y = pd.get_dummies(y)

        plsda = PLSRegression(n_components=self.n_components, scale=False)
        results = plsda.fit_transform(X, one_hot_y)
        x_scores = results[0]
        column_name = [f'Component{i+1}' for i in range(self.n_components)]


        _df_results = pd.DataFrame(x_scores, columns=column_name)
        df_results = pd.concat([_df_results, y], axis=1)

        if plotting:
            self.plsda_plot(df_results, figsize, marker_size, alpha, palette)
            if self.is_save_file:
                plt.tight_layout()

                plt.savefig('plsda.png', dpi=self.dpi)
                print('plsda.png files are saved')
            plt.show()

        return df_results
    
    def plsda_plot(self, df_results, figsize=(5.5, 5), marker_size=100, alpha=0.8, palette='Set3', markers=['o', 's', 'D', '^', '>', '<']):

        plt.figure(figsize=figsize)
       
        sns.scatterplot(data=df_results, x='Component1', y='Component2', hue='Label', style='Label', markers=markers, s=marker_size, alpha=alpha, palette=palette, edgecolor='k')
        plt.xlim(-abs(df_results.Component1).max()*1.2, abs(df_results.Component1).max()*1.2)
        plt.ylim(-abs(df_results.Component2).max()*1.2, abs(df_results.Component2).max()*1.2)
       
        plt.hlines(0, xmin=-abs(df_results.Component1).max()*1.2, xmax=abs(df_results.Component1).max()*1.2, colors='k', linestyles='dashed',  linewidth=0.5)
        plt.vlines(0, ymin=-abs(df_results.Component2).max()*1.2, ymax=abs(df_results.Component2).max()*1.2, colors='k', linestyles='dashed',  linewidth=0.5)


        plt.title('PLS-DA analysis', fontsize=20)
        plt.xlabel(f'Component 1', fontsize=18)
        plt.ylabel(f'Component 2', fontsize=18)
        plt.xticks(fontsize=14, ticks=[-8000,  -4000, 0, 4000, 8000])
        plt.yticks(fontsize=14)
        plt.legend(loc='upper right', bbox_to_anchor=(1.01, 1.01), fontsize=16)


    # PLS-DA validation function...