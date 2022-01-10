""" This Module Requests Input from user and uses analyze module to return result data to the user"""

from champion_list import champion_list, champion_list_lower
from process_inputs import process_inputs


def input_handler():
    """
    input_handler function asks the user to input 2 teams compositions and specify their champion to process the inputs and return the builds.

        ARGUMENTS:
            None
        
        Return:
            String: Analyzed item builds
    """

    champion = ""
    ally_team = []
    enemy_team = []
    composition = []

    while not len(ally_team) == 5:

        print("Enter your team composition, separated by commas in this order [Support,Adc,Mid,Jungle,Top]\n")

        user_response = input("> ")

        if len(user_response.split(',')) == 5:
            ally_team = user_response.split(',')

        for i in range(len(ally_team)):
            if not ally_team[i].lower().strip() in champion_list_lower:
                ally_team = []
                break

        if not len(ally_team) == 5:
            print("Please enter a valid composition.\n")

        else:
            while True:
                print("\nEnter your current champion name.\n")

                user_response = input("> ")

                if not user_response.lower().strip() in [name.lower() for name in ally_team] or not user_response.lower().strip() in champion_list_lower:

                    print("Enter your champion name correctly.")
                    continue

                else:
                    champion = user_response
                    break

            while not len(enemy_team) == 5:

                print("Enter the team composition, separated by commas in this order [Support,Adc,Mid,Jungle,Top]\n")

                user_response = input("> ")

                if len(user_response.split(',')) == 5:
                    enemy_team = user_response.split(',')

                for i in range(len(enemy_team)):
                    if enemy_team[i].lower().strip() in [name.lower() for name in ally_team]:
                        print("Please enter a valid composition. One champion cannot be on both teams.\n")
                        enemy_team = []
                        break

                    if not enemy_team[i].lower().strip() in champion_list_lower:
                        enemy_team = []
                        break

                if not len(enemy_team) == 5:
                    print("Please enter a valid composition.\n")
                    continue
                else:
                    composition.append(ally_team)
                    composition.append(enemy_team)
                    composition.append(champion)

                    for i in range(2):
                        for j in range(len(composition[i])):
                            composition[i][j] = composition[i][j].title(
                            )
                    composition[2] = composition[2].title()
                    return(process_inputs(composition[0], composition[1], composition[2]))

if __name__ == '__main__':            
    print(input_handler())

# Nami,Lucian,Syndra,Nidalee,Irelia
# Leona,Jhin,Orianna,JarvanIV,Camille