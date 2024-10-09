import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
class MultiVariateAnalysis:

    def __init__(self, n_components, is_save_file=False, dpi=600):

        self.n_components = n_components
        self.is_save_file = is_save_file
        self.dpi = dpi
      

    def pca_analysis(self, dataset, palette='Set3', plotting=True, figsize=(5.5, 5), marker_size=100, alpha=0.8, dpi=450, ):     
             

        X = dataset.drop(columns=['Name', 'Label'], axis=1)
        y = dataset[['Label']].reset_index(drop=True)

        pca = PCA(n_components=self.n_components)
        results = pca.fit_transform(X)

        pca_explain_value = pca.explained_variance_ratio_
        column_name = [f'PCA{i+1}' for i in range(self.n_components)]

        _df_pca_result = pd.DataFrame(results, columns=column_name)
        df_pca_result = pd.concat([_df_pca_result, y], axis=1)

        if plotting:
            self.pca_plot(df_pca_result, pca_explain_value, figsize, marker_size, alpha, palette=palette)

            if self.is_save_file:
                plt.tight_layout()
                plt.savefig('pca.png', dpi=dpi)
                print('pca.png files are saved')
            plt.show()


        return df_pca_result, pca_explain_value
    
    def pca_plot(self, df_pca_result, pca_explain_value, figsize=(5.5, 5), marker_size=100, alpha=0.8, palette='Set3', markers=['o', 's', 'D', '^', '>', '<']):

        plt.figure(figsize=figsize)
        sns.scatterplot(data=df_pca_result, x='PCA1', y='PCA2', hue='Label', style='Label',s=marker_size, markers=markers,alpha=alpha, palette=palette, edgecolor='k',)
        plt.xlim(-abs(df_pca_result.PCA1).max()*1.2, abs(df_pca_result.PCA1).max()*1.2)
        plt.ylim(-abs(df_pca_result.PCA2).max()*1.2, abs(df_pca_result.PCA2).max()*1.2)
        
        plt.hlines(0, xmin=-abs(df_pca_result.PCA1).max()*1.2, xmax=abs(df_pca_result.PCA1).max()*1.2, colors='k', linestyles='dashed',  linewidth=0.5)
        plt.vlines(0, ymin=-abs(df_pca_result.PCA2).max()*1.2, ymax=abs(df_pca_result.PCA2).max()*1.2, colors='k', linestyles='dashed',  linewidth=0.5)

        plt.title('PCA Analysis', fontsize=20)
        plt.xlabel(f'PCA1 components ({pca_explain_value[0]*100:.2f}%)', fontsize=18)
        plt.ylabel(f'PCA2 components ({pca_explain_value[1]*100:.2f}%)', fontsize=18)
        plt.xticks(fontsize=14, ticks=[-8000,  -4000, 0, 4000, 8000])       
        plt.yticks(fontsize=13, )
        plt.legend(loc='upper right', bbox_to_anchor=(1.01, 1.01), fontsize=16)


    # PLS-DA validation function...