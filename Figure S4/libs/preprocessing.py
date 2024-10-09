import os
import numpy as np
import pandas as pd
from libs.scaler import ParetoScaling
from libs.scaler import AutoScaling


class MetaboPreprocer:

    def __init__(self, step_blank_substrateion=False, step_filter_rsd=False, step_log_transformation=False, filter_ratio=0.3, qc_label='QC', scaling='pareto', file_save=True, criteria_ND_proportion=0.5):

        self.step_blank_substrateion = step_blank_substrateion
        self.criteria_ND_proportion = criteria_ND_proportion

        self.step_filter_rsd = step_filter_rsd
        self.filter_ratio = filter_ratio
        self.qc_label = qc_label

        self.step_log_transformation = step_log_transformation

        self.scaling = scaling
        self.file_save = file_save
        

    def preprocessing(self, dataset_path, sheet_name=None, label_list=['all']):

        
        if '.xlsx' == dataset_path[-5:]:
            dataset = pd.read_excel(dataset_path, sheet_name=sheet_name)

        elif '.csv' == dataset_path[-4:]:
            dataset = pd.read_csv(dataset_path)
        else:
            raise ValueError('Invalid file extension. only csv or xlsx files is allowed')
        
        # Column information 이 안맞으면... 경고문 추가 WARING 함수 써가지고
        
        missing_values = dataset.isnull().sum().sum()
        print('=========== Preprocessing ==========')
        print(f'Original dataset shape (n_samples, n_features + 2) = {(dataset.shape[0], dataset.shape[1])}')
        print(f'A total of {missing_values:d} missing values were detected')

        # Fill missing values and Delete all-zero columns 
        dataset = self.delete_all_zero_values_features(dataset)

        if self.step_blank_substrateion:
            sub_dataset = self.substrate_blank_intensity(dataset, self.criteria_ND_proportion).reset_index(drop=True)
        else:
            sub_dataset = dataset.copy().reset_index(drop=True)

          
        # Filtering the featuring [Criteria, RSD (filter_ratio)] basd on QC samples
        if self.step_filter_rsd:
            filtered_dataset = self.filter_rsd(sub_dataset, filter_ratio=self.filter_ratio, qc_label=self.qc_label)

        else:
            filtered_dataset = sub_dataset.copy()

        filtered_dataset = self.delete_all_zero_values_features(filtered_dataset)

        # log transfomation
        if self.step_log_transformation:
            filtered_dataset = self.log_transformation(filtered_dataset)


        # Group Editing... 
        filtered_dataset = self.label_selection(filtered_dataset, label_list)
        filtered_dataset = self.delete_all_zero_values_features(filtered_dataset)


        # Scaling the features 
        X = filtered_dataset.drop(columns=['Name', 'Label'], axis=1)

        X_scaled, scaler = self.data_scaler(X.values, self.scaling)
        self.scaler = scaler
        
        scaled_dataset = pd.DataFrame(X_scaled, X.index, X.columns)
        scaled_dataset = pd.concat([filtered_dataset[['Name', 'Label']], scaled_dataset], axis=1)

        print(f'Processed dataset shape (n_samples, n_features + 2) = {(scaled_dataset.shape[0], scaled_dataset.shape[1])}\n')


        # Save the non-scaled and scaled dataset
        if self.file_save:

            if not os.path.exists('./data'):
                os.mkdir('./data')

            filtered_dataset.to_csv('dataset_filtered.csv', index=False)
            scaled_dataset.to_csv('dataset_filtered_scaled.csv', index=False)

        return scaled_dataset, filtered_dataset
           
        
    def filter_rsd(self, dataset, filter_ratio=0.3, qc_label='QC'):

    
        dataset_ = dataset[dataset.Label == qc_label]
        rsd = dataset_.std(numeric_only=True) / dataset_.mean(numeric_only=True)

        # If mean is 0.. This features is removed
        # It is different from MetaboAnalyst.... 
        
        selected_features = rsd[rsd <= filter_ratio].index
        selected_features =  ['Name', 'Label'] + list(selected_features)

        filterd_dataset = dataset[selected_features]

        print('========== Filtering features based on RSD values ==========')
        print(f'Filtering features with above {filter_ratio* 100:.2f}% of RSD values in QC samples ')
        print(f'Note. {(dataset_.mean(numeric_only=True) == 0.0).sum()} Features with zero mean intensity in QC samples will be removed')
        print(f'Filtered dataset shape (n_samples, n_features + 2) = {(filterd_dataset.shape[0], filterd_dataset.shape[1])}')

        return filterd_dataset
    
      
    
    def data_scaler(self, X, kinds_of_sacler='auto',):

        if kinds_of_sacler == 'auto':
            scaler = AutoScaling()
            X_scaled = scaler.fit_transform(X)            
            return X_scaled, scaler
        
        elif kinds_of_sacler == 'pareto':
            scaler = ParetoScaling()
            X_scaled = scaler.fit_transform(X)
            return X_scaled, scaler
        
        elif kinds_of_sacler == 'None':
            return X, None
        
        else:
            raise ValueError('Invalid scaler... ["auto", "pareto", "None"]')
        
   
    # Fill the num values to zeores... Delete the all zero features

    def delete_all_zero_values_features(self, dataset):
        if dataset.isnull().sum().sum() != 0 :
            print('There is Num value (empty value) in dataset.Num value is replaced with 0')
            dataset = dataset.fillna(0)

        if (dataset.sum() == 0).sum() != 0 :
            print(f'{(dataset.sum() == 0).sum():d} features have all zero values. These featuers are removed')
            selected_featuers = (dataset.sum() != 0)
            selected_featuers = selected_featuers[selected_featuers].index

            dataset = dataset[selected_featuers]
        
        return dataset
    
    # Group Editing
    def label_selection(self, dataset, label_list):

        print('========== Label Selectioin ==========')
        print(f'{label_list} features are selected and scaled')

        if label_list == ['all']:
            label_list = list(dataset.Label.unique())

        target_features = [label in label_list for label in dataset.Label]
        
        dataset = dataset[target_features].reset_index(drop=True)
        return dataset
   

    def substrate_blank_intensity(self, dataset, criteria_ND_proportion=0.5):

        '''
        Substrate blank intensity.
        1. Substrate the blank values from the original intensities.
        2. Replace negative values, including 0, with "ND"
        3. Calcuate the proportion of "ND" values for each features within each group (eg, the propotion of negative values of A features.. treat group : 10%, non-treated group : 20%, QC : 5%)
           *Note, we do not consider the blank group
        4. if the proportion of ND values within each featuers is more then 50% in all groups, the remove that feature.

        hyperparameter
        critiera_ND_proportion : (default = 0.5 (50%))
        '''

        print('========== Substrate the blank intensity from raw(original) intensity ==========')
        print(f'Removal of featuers with more than {criteria_ND_proportion*100}% proportion of negative values in all groups')
        print(f'Before the substration process, dataset shape (n_samples, n_features + 2) = {(dataset.shape[0], dataset.shape[1])}.')

        # Substrate blank values from the original intensity 

        if (dataset.Label == 'blank').sum() == 0 :
            raise ValueError('blank group should be designated in dataset')

        df_featuers = dataset.drop(columns=['Name', 'Label'])
        blank_avg = dataset[dataset.Label == 'blank'].mean(numeric_only=True)
        df_sub = df_featuers - blank_avg

        # replace negative values with ND

        df_sub2 = df_sub.mask(df_sub <= 0, 'ND')

        df_ND = pd.concat([dataset[['Name', 'Label']], df_sub2], axis=1)
        df_ND = df_ND[df_ND.Label != 'blank']


        # Calcuate the proportion of "ND" values for each features within each group
        # ND criteria... criteria_ND_proportion(default = 0.5)

        df_new = pd.DataFrame(df_ND.columns, columns=['features']).reset_index(drop=True)
        labels = list(df_ND.Label.unique())
        labels.remove(self.qc_label)  # Except QC group


        for label in labels:
            df_temp = df_ND[df_ND.Label == label]
            df_count = pd.DataFrame((df_temp == 'ND').sum(), columns=[label]).reset_index(drop=True) / df_temp.shape[0]
            df_count = (df_count > criteria_ND_proportion) # Do not meet the ND ratio criteria
            df_new = pd.concat([df_new, df_count], axis=1)  


        # Featuer selection

        features = df_new.drop(columns='features', axis=1)
        criteria = (features.sum(axis=1) < len(features.columns)) # featuers.sum(axis=1) is the "number of groups" that do not meet the ND criteria 

        selected_features = df_new.features[criteria]
        df_final = df_ND[selected_features]
        df_final = df_final.mask(df_final == 'ND', 0.0)

        # Data Type...
        df_final_1 = df_final[['Name', 'Label']].reset_index(drop=True)
        df_final_2 = df_final.drop(columns=['Name', 'Label'], axis=1).astype(float).reset_index(drop=True)
        df_final_3 = pd.concat([df_final_1, df_final_2], axis=1)


        print(f'After the substration process, dataset shape (n_samples, n_features + 2) = {(df_final_3.shape[0], df_final_3.shape[1])}.')
        return df_final_3
    

    def log_transformation(self, dataset):

        for col in dataset.columns:
            if col not in ['Name', 'Label']:

                dataset[col] =dataset[col].replace(0, 1)
                dataset[col] = np.log10(dataset[col])
        
        return dataset