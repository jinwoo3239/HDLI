import pandas as pd 
import numpy as np
import math
import itertools

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']



def main(df, x):
    """
        Do some more magic stuff
    """
    df = insert(data=df)

    dups = absorb(df=df)  # absorb before sweep
    if len(dups) > 0:
        df = df.drop(dups, axis=1)
    else:
        pass

    df = sweep(df)

    dups = absorb(df=df)  # absorb after sweep
    if len(dups) > 0:
        df = df.drop(dups, axis=1)
    else:
        pass

    return df


def insert(data):
    """
        Insert phase of algortihm.  Duplicate columns for significant differences and then swap boolean values around
    """
    unique = list(set(list(data['product_1'])))
    initial_col = [1] * len(unique)
    df = pd.DataFrame(initial_col, columns=['initial_col'])
    df['product'] = unique
    df = df.set_index('product')

    # get the significant differences.
    signifs = data[data['reject H0'] == True]

    if not any(data['reject H0']):  # case wheres theres no significant differences we end up with one group.
        groups = get_letters(1)
        df[groups[0]] = 1
        df = df.drop(labels='initial_col', axis=1)
        return df
    else:           # every other case
        #do the insert
        for i, signif in enumerate(signifs['product_1']):
            signif_1 = signif
            signif_2 = signifs['product_2'].iloc[i]

            # get the columns to duplicate from df by testing that signif_1 row and signif_2 row are both equal to 1
            test = df.loc[[signif_1, signif_2]]
            cols_to_dup = []
            for col in test.columns:
                if test[col].sum() == 2:
                    cols_to_dup.append(col)
                else:
                    continue

            # duplicate the dataframes
            df1 = df[cols_to_dup]
            df2 = df[cols_to_dup]
            df3 = df[df.columns].drop(labels=cols_to_dup, axis=1)

            #set the 1's and 0's
            df1.loc[signif_1] = 1
            df1.loc[signif_2] = 0

            df2.loc[signif_1] = 0
            df2.loc[signif_2] = 1


            #merge the duplicate dataframes back to the original with any unduped columns
            df = df1.merge(df2, left_index=True, right_index=True)
            df = df.merge(df3, left_index=True, right_index=True)
            letters = get_letters(n=len(df.columns))
            df.columns = letters
            new_cols = []  #  list of the new columns to check for duplication.

    return df.sort_index()


def absorb(df):
    """
        Check each new column against all old columns.  If its a duplicate we can drop it i.e. "absorb" it.
    """
    groups = df.columns.to_series().groupby(df.dtypes).groups
    dups = []
    for t, v in groups.items():
        dcols = df[v].to_dict(orient="list")

        vs = list(dcols.values())
        ks = list(dcols.keys())
        lvs = len(vs)

        for i in range(lvs):
            for j in range(i+1,lvs):
                if vs[i] == vs[j]: 
                    dups.append(ks[i])
                    break
    return dups  


def sweep(df):
    """
        Implement the 'sweep' method to reduce number of 1's
    """
    df = df.sort_index()
    cols = df.columns

    data = df.copy()

    locked = df.copy()
    locked[:] = 0

    for col in cols:
        col_to_sweep = data[col].loc[data[col] == 1]
        tmp = data.drop(labels=col, axis=1)

        index = list(col_to_sweep.index)

        # get the pairs to check for each positive record
        for i in index:
            pairs = [(i, x) for x in index if x != i]
            check = {}
            lock_index = {}  # Get the index we need to lock
            for pair in pairs:
                check[pair] = 0  # initialise with zeros
                lock_index[pair] = 0 # initialise so that we only have one key for each pair not multiple

            for tmp_col in tmp.columns:  # for each pair we need to loop through all columns to see if the pair exists elsewhere
                # if pair in a column are both ones then continue the loop else break
                for pair in pairs:

                    # check if the record is locked here, if it is move on to next iteration
                    if locked[tmp_col].loc[pair[0]] == 1:
                        break

                    if tmp[tmp_col].loc[pair[0]] == 1 &  tmp[tmp_col].loc[pair[1]] == 1:
                        check[pair] = 1
                        lock_index[pair] = [col, pair[1]]
                    elif check[pair] == 1:  # if its already been flagged dont overwrite it
                        pass
                    else:
                        check[pair] = 0
                        break

            if len(set(check.values())) == 1  & list(set(check.values()))[0] == 1: # if all pairs exists and are 1 our entry is redundant and should be deleted
                

                data[col].loc[list(check.keys())[0][0]] = 0  # turn the 1 to a zero

                # Lock the records it depends on
                for keys, values in lock_index.items():
                    column_to_lock = values[0]
                    index_to_lock = values[1]
                    locked[column_to_lock].loc[index_to_lock] = 1

    return data


def get_letters(n, letters=LETTERS, sep='.'):
    """
        Put a sensiible docstring here
    """
    complete = math.floor(n/len(letters))
    partial = n % len(letters)
    separ = ''
    lett = []

    if complete > 0:
        for i in range(0, complete):
            lett.extend([separ + letter for letter in letters])
            separ = separ + sep

    if partial > 0:
        lett.extend([separ + letter for letter in letters[0:partial]])

    return lett


if __name__ == "__main__":
    df = pd.read_csv('input.csv', index_col=0)

    df = main(df, 'reject H0')
    print(df)
