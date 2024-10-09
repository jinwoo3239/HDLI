import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Figure
def get_group_figure(
        dataset: pd.DataFrame,
        dict_group: dict,
        dict_id: dict,
        group: str,
        order: list,
        kind='barplot', palette='Pastel1', figsize=(20, 18), top_alpha=1.0, is_save_file=False, dpi=600, x_label_rotation='45'
    ):

    '''
    dataset (pd.DataFrame)  : dataset containing metabolite intensity. The dataset should include Label column
    dict_group (dict)       : ID_groups:features # Key metabolties... (interesting features)
    dict_id (dict)          : features:ID # Get metabolties ID
    top_alpha               : hyperparameters of y-axis max value
    '''

    plt.figure(figsize=figsize)

    for i, feat in enumerate(dict_group[group]):

        plt.subplot(5, 6, i + 1)


        if kind == 'barplot':
            sns.barplot(data=dataset, x='Label', y=feat, order=order, palette=palette, errwidth=1.5, errcolor='k', edgecolor='blacK')           

        elif kind == 'stripplot':    
            sns.stripplot(data=dataset, x='Label', y=feat, order=order, jitter=True, palette=palette)
            

            sns.boxplot(data=dataset, x='Label', y=feat, order=order,
                        showmeans=True,
                        showbox=False,
                        medianprops={'visible' : False},
                        whiskerprops={'visible' : False},
                        showcaps=False,
                        meanline=True,
                        showfliers=False,
                        meanprops={'color' : 'k', 'lw': 1})
        
        elif kind == 'boxplot':
            sns.boxplot(data=dataset, x='Label', y=feat, order=order, palette=palette,)

        else:
            raise ValueError('Invalid kinds of plot. [barplot, stripplot, boxplot]')           


        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(fontsize=12)
        plt.title(f'{dict_id[feat]}\n{feat}', fontdict={'fontsize' : 15, 'fontweight' : 'bold'})
        plt.xticks(rotation=x_label_rotation, ha='right')
        bottom, top = plt.ylim()
        plt.ylim((bottom, top*top_alpha))
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.7)


    if is_save_file:
        plt.savefig('figure.png', dpi=dpi)
        print('figure.png file is saved')

    plt.show()

def get_group_figure_rev3(
        dataset: pd.DataFrame,
        dict_id: dict,
        order: list,
        feature_order: list,
        palette='Pastel1', figsize=(10, 14), top_alpha=1.2, is_save_file=False, dpi=600, x_label_rotation='45', ha='ha',
        save_name='a'
    ):

    plt.figure(figsize=figsize)

    for i, feat in enumerate(feature_order):

        plt.subplot(5, 5, i + 1)

        # relative 
        df_criteria = dataset[dataset['Label'] == 'D'].drop(['Name', 'Label'], axis=1)
        dataset_tmp = dataset.drop(['Name', 'Label'], axis=1)
        dataset_tmp /= np.mean(df_criteria, axis=0)
        dataset_rev = pd.concat([dataset[['Name', 'Label']], dataset_tmp], axis=1)
    

        sns.stripplot(data=dataset_rev, x='Label', y=feat, order=order, jitter=True, palette=palette, edgecolor="gray", linewidth=1,)      
        sns.barplot(data=dataset_rev, x='Label', y=feat, order=order, color='white', ci=95, edgecolor='k',palette=palette, alpha=0.5)           

        plt.xlabel('')
        plt.ylabel('')
        plt.yticks(fontsize=14)
        plt.title(f'{dict_id[feat]}\n{feat}', fontdict={'fontsize' : 15, 'fontweight' : 'bold'})
        plt.xticks(fontsize=15, )
        bottom, top = plt.ylim()
        plt.ylim(-0.1, top*top_alpha)

        # plt.yscale('log', base=10)
        # bottom, top = plt.ylim()
        # plt.ylim(0, 9*top_alpha)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=1.1)


    if is_save_file:
        plt.savefig(f'figure_{save_name}.png', dpi=dpi)
        print('figure.png file is saved')

    plt.show()