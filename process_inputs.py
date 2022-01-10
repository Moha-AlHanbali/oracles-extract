""" This module is based on analyze.ipynb and uses inputs from oracles_extract.py to run and return values"""

import pandas as pd
import json
import difflib
import warnings


from item_keys import item_keys


def process_inputs(ally_team : list, enemy_team: list, champion : str, ally_tolerance = 0.2, enemy_tolerance = 0.2):
    """
    process_inputs function recieves data from input_handler and runs analysis on match data to return results.

        Arguments:
            ally_team: User's team
            enemy_team: The enemy team
            champion: The User's champion
            ally_tolerance: Alleid team similarity threshold (0.0 - 1.0)
            ally_tolerance: Enemy team similarity threshold (0.0 - 1.0)

        Return:
            String: Analyzed item builds
    """
    try:

        warnings.simplefilter(action='ignore', category=FutureWarning)
        
        df = read_data()

        team1_columns = df.columns[1:12]
        team2_columns = df.columns[12:]
        teams_columns = team1_columns[1:].append(team2_columns[1:])

        df, winning_team1_df, winning_team2_df = shape_data(df, champion, team1_columns, team2_columns)

        most_common_bought, most_common_list, most_common_df = most_common_winning(df, champion, teams_columns)

        ally_comp, enemy_comp = filter_relevant(teams_columns, winning_team1_df, winning_team2_df)


        relevant_most_common_build, relevant_most_common_bought = filter_composition(ally_team, ally_comp, ally_tolerance, enemy_team, enemy_comp, enemy_tolerance, champion, most_common_list, most_common_df)

        most_common_bought, relevant_most_common_build, relevant_most_common_bought = convert_keys(most_common_bought, relevant_most_common_build, relevant_most_common_bought)
        return f'''\nMost common bought items in winning matches: {most_common_bought}
        \nMost common bought item builds in similar situations:{relevant_most_common_build}
        \nMost common bought items in winning matches {relevant_most_common_bought}'''

    except:
        return 'Not sufficient data, try other team compositions...'


def read_data():
    try:
        df = pd.read_csv('preseason12_match_data.csv')

    except:

        with open('preseason12_match_data.json') as json_file:
            data = json.load(json_file)

        pd.json_normalize(data).to_csv('preseason12_match_data.csv')
        df = pd.read_csv('preseason12_match_data.csv')

    return df


def shape_data(df, champion, team1_columns, team2_columns):

    team1_df = (df[team1_columns] == champion) 
    winning_team1_df = df.iloc[team1_df.loc[team1_df.sum(axis=1) == 1].index.tolist()]
    winning_team1_df = winning_team1_df[winning_team1_df['team1.win'] == True]
    filtered_teams_list = winning_team1_df.index.tolist()


    team2_df = (df[team2_columns] == champion) 
    winning_team2_df = df.iloc[team2_df.loc[team2_df.sum(axis=1) == 1].index.tolist()]
    winning_team2_df = winning_team2_df[winning_team2_df['team2.win'] == True]
    filtered_teams_list += winning_team2_df.index.tolist()

    filtered_teams_list = list(set(filtered_teams_list))
    df = df.iloc[filtered_teams_list]
    df = df.drop('Unnamed: 0', 1)

    return df, winning_team1_df, winning_team2_df

def most_common_winning(df, champion,  teams_columns):
    most_common_list = []

    for col in df[teams_columns]:
        for i, row_value in df[col].iteritems():
            if df[col][i] == champion:
                most_common_list.append(eval(df[col+'_items'][i]))

    
    most_common_df = pd.DataFrame(most_common_list, columns =['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Vision Item'], dtype= int) 
    most_common_bought = dict()
    for col in most_common_df.columns:
        if most_common_df[col].mode()[0] == 0:
            most_common_bought[f'Most common {col}'] = most_common_df[col].value_counts().index[1]
        else:
            most_common_bought[f'Most common {col}'] = most_common_df[col].mode()[0]   

    return most_common_bought, most_common_list, most_common_df



def filter_relevant(teams_columns, winning_team1_df, winning_team2_df):
    ally_list = []
    enemy_list = []

    for col in range(len(teams_columns)):
        if col < len(teams_columns)//2:
            ally_list.append(winning_team1_df[winning_team1_df[teams_columns].columns[col]].tolist())
        else:
            enemy_list.append(winning_team1_df[winning_team1_df[teams_columns].columns[col]].tolist())

    for col in range(len(teams_columns)):
        if col < len(teams_columns)//2:
            enemy_list.append(winning_team2_df[winning_team2_df[teams_columns].columns[col]].tolist())
        else:
            ally_list.append(winning_team2_df[winning_team2_df[teams_columns].columns[col]].tolist())

    
    ally_comp = []
    enemy_comp = []

    for value in range(len(enemy_list[0])):
        ally_comp.append([])
        enemy_comp.append([])

        for row in range(len(ally_list)//2):
            ally_comp[value].append(ally_list[row][value])
            enemy_comp[value].append(enemy_list[row][value])

    return ally_comp, enemy_comp

def filter_composition(ally_team, ally_comp, ally_tolerance, enemy_team, enemy_comp, enemy_tolerance, champion, most_common_list, most_common_df):
    relevant_comopsitions = []

    for comp in range(len(ally_comp)):
        ally_similarity = difflib.SequenceMatcher(None, ally_team, ally_comp[comp][::2]).ratio()
        enemy_similarity = difflib.SequenceMatcher(None, enemy_team, enemy_comp[comp][::2]).ratio()
        # print(ally_similarity, enemy_similarity)
        if ally_similarity < ally_tolerance or enemy_similarity < enemy_tolerance:
            continue
        
        relevant_comopsitions.append([])
        relevant_comopsitions[-1] = ally_comp[comp] + enemy_comp[comp]


    relevant_comopsitions_df = pd.DataFrame(relevant_comopsitions, columns =['Ally_1', 'Ally_1_Items', 'Ally_2', 'Ally_2_Items', 'Ally_3', 'Ally_3_Items', 'Ally_4', 'Ally_4_Items', 'Ally_5', 'Ally_5_Items', 'Enemy_1', 'Enemy_1_Items', 'Enemy_2', 'Enemy_2_Items', 'Enemy_3', 'Enemy_3_Items', 'Enemy_4', 'Enemy_4_Items', 'Enemy_5', 'Enemy_5_Items',]) 

    relevant_most_common_list = []

    for col in relevant_comopsitions_df.columns:
        for i, row_value in relevant_comopsitions_df[col].iteritems():
            if relevant_comopsitions_df[col][i] == champion:
                relevant_most_common_list.append(eval(relevant_comopsitions_df[col+'_Items'][i]))    

    relevant_most_common_build_list = []
    for build in relevant_most_common_list:
        relevant_most_common_build_list.append((str(build))
    )


    relevant_most_common_build_df = pd.DataFrame((relevant_most_common_build_list), columns = ['Items_Build'])
    relevant_most_common_build = relevant_most_common_build_df['Items_Build'].mode()[0]

    relevant_most_common_df = pd.DataFrame(most_common_list, columns =['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Vision Item'], dtype= int) 
    relevant_most_common_bought = dict()
    for col in most_common_df.columns:
        if relevant_most_common_df[col].mode()[0] == 0:
            relevant_most_common_bought[f'Most common {col}'] = relevant_most_common_df[col].value_counts().index[1]
        else:
            relevant_most_common_bought[f'Most common {col}'] = relevant_most_common_df[col].mode()[0]    
    return relevant_most_common_build, relevant_most_common_bought


def convert_keys(most_common_bought, relevant_most_common_build, relevant_most_common_bought):
    for key, item in most_common_bought.items():
        most_common_bought[key] = item_keys[str(item)]

    relevant_most_common_build = eval(relevant_most_common_build)
    for item in range(len(relevant_most_common_build)):
        if relevant_most_common_build[item] > 0:
            relevant_most_common_build[item] = (item_keys[str(relevant_most_common_build[item])])
        else:
            relevant_most_common_build[item] =  'None'

    for key, item in relevant_most_common_bought.items():
        relevant_most_common_bought[key] = item_keys[str(item)]

    return most_common_bought, relevant_most_common_build, relevant_most_common_bought