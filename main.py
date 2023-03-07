import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import statistics as stats

# FUNCTIONS
def guess_centroid(list1, list2):
    plt.scatter(list1, list2)
    plt.show()
    guess = input('Input Centroid Locations: ')
    guess = eval(guess)  # if written as coordinate points gives tuple or tuple of tuples
    return list(guess)

def calc_dist(p1, p2):
    return(abs(math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)))

def assign_cluster(x_list, y_list, centroid_list = None):
    if centroid_list is None:
        centroid_list = guess_centroid(x_list, y_list)
    # MAKE CLUSTER DICT FOR ANY LENGTH
    cluster_dict = {}
    for val in range(len(centroid_list)):
        cluster_dict[val] = []
    # FIND DISTANCE AND CALCULATE WHERE EACH CENTROID IS AND ASSIGN EVERY POINT TO KEY IN DICT
    for i in range(len(x_list)):
        point = (x_list[i], y_list[i])
        dist_list = []
        for centroid in centroid_list:
            dist_list.append(calc_dist(point, centroid))
        i2 = -1
        for entry in dist_list:
            i2 += 1
            if entry == min(dist_list):
                cluster_dict[i2].append([point[0], point[1]])
    return cluster_dict


def plot_centroids(dict, title, centroids = None):
    for key in dict:
        x_list = []
        y_list = []
        for val in dict[key]:
            x_list.append(val[0])
            y_list.append(val[1])
        plt.scatter(x_list, y_list)
    if centroids != None:
        for point in centroids:
            print(point)
            plt.plot([point[0]], [point[1]], 'k', marker='D')
    plt.title(title)
    plt.show()


def calc_centroid(dict):
    centroid_coord = []
    for key in dict:
        x_list = []
        y_list = []
        for val in dict[key]:
            x_list.append(val[0])
            y_list.append(val[1])
        centroid_coord.append([stats.mean(x_list), stats.mean(y_list)])
    return(centroid_coord)



#############################################################################
# Create and change column names in Dataframe
customer_df = pd.read_csv('customer_data.csv', delim_whitespace=False)
customer_df.columns = ['ID', 'Gender', 'Age', 'Income', 'Score']

# CREATE RAW LISTS FOR BOTH GENDERS
i = -1
age_dict = {}
income_dict = {}
score_dict = {}
male_age = []
male_income = []
male_score = []
female_age = []
female_income = []
female_score = []
for item in customer_df['Gender']:
    i += 1
    if item == 'Male':
        male_age.append(customer_df['Age'][i])
        male_income.append(customer_df['Income'][i])
        male_score.append(customer_df['Score'][i])
    else:
        female_age.append(customer_df['Age'][i])
        female_income.append(customer_df['Income'][i])
        female_score.append(customer_df['Score'][i])
age_dict['Male'], age_dict['Female'] = male_age, female_age
income_dict['Male'], income_dict['Female'] = male_income, female_income
score_dict['Male'], score_dict['Female'] = male_score, female_score



# Male and Female Choices Respectively
#(25, 20), (25, 70), (55, 50), (85, 15), (85, 80)
#(25, 20), (25, 80), (55, 50), (90, 20), (90, 80)
def main(rep, gender):
    cluster_dict = assign_cluster(income_dict[gender], score_dict[gender], guess_centroid(income_dict[gender], score_dict[gender]))
    cent_coord = calc_centroid(cluster_dict)
    plot_centroids(cluster_dict, f'{gender} INCOME VS SCORE', cent_coord)
    for i in range(rep):
        cluster_dict = assign_cluster(income_dict[gender], score_dict[gender], cent_coord)
        cent_coord = calc_centroid(cluster_dict)
        plot_centroids(cluster_dict, f'{gender} INCOME VS SCORE', cent_coord)

main(4, 'Male')
main(4, 'Female')










