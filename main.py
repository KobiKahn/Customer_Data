import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import statistics as stats

# FUNCTIONS
def mean(data):
    total = sum(data)
    m = total / len(data)
    return m
def median(data):
    data.sort()
    if len(data) % 2 == 0:
        m = (data[len(data) // 2] + data[len(data) // 2 - 1]) / 2
    else:
        m = data[len(data) // 2]
    return m
def variance(data):
    new_list = [(val - mean(data)) ** 2 for val in data]
    v = mean(new_list)
    return v
def stand_dev(data):
    v = variance(data)
    s = math.sqrt(v)
    return s

def calc_stats(dict):
    x_stats = {}
    y_stats = {}
    for key, item in dict.items():
        x_stats_list = []
        y_stats_list = []
        x_list = [val[0] for val in item]
        y_list = [val[1] for val in item]
        x_stats_list.append(mean(x_list)), x_stats_list.append(median(x_list)), x_stats_list.append(stand_dev(x_list)), x_stats_list.append(max(x_list)), x_stats_list.append(min(x_list))
        y_stats_list.append(mean(y_list)), y_stats_list.append(median(y_list)), y_stats_list.append(stand_dev(y_list)), y_stats_list.append(max(y_list)), y_stats_list.append(min(y_list))
        x_stats[key] = x_stats_list
        y_stats[key] = y_stats_list
    return(x_stats, y_stats)

def cal_corr(list1, list2, option=0):
    if len(list1) == len(list2):
        i = -1
        prod_list = []
        min_sqr1 = []
        min_sqr2 = []
        for val in list1:
            i += 1
            prod_list.append(list1[i] * list2[i])
            min_sqr1.append(list1[i] ** 2)
            min_sqr2.append(list2[i] ** 2)
        numerator = ((len(list1) * sum(prod_list)) - (sum(list1) * sum(list2)))
        denominator = (math.sqrt(len(list1) * sum(min_sqr1) - sum(list1) ** 2) * math.sqrt(len(list2) * sum(min_sqr2) - sum(list2) ** 2))
        denominator = denominator.real
        correlation = numerator / denominator
        if option == 0:
            return (correlation)
        elif option == 1:
            return (sum(list1), sum(list2), sum(prod_list), sum(min_sqr1), len(list1))
    else:
        print('ERROR LISTS ARE NOT THE SAME LENGTH CANT COMPUTE')
        return False

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
    return dict, centroids


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


print(cal_corr(male_income, male_age))
print(cal_corr(female_income, female_age))

print(cal_corr(male_age, male_score))
print(cal_corr(female_age, female_score))

# Male and Female Choices Respectively
# (25, 20), (25, 70), (55, 50), (85, 15), (85, 80)
# (25, 20), (25, 80), (55, 50), (90, 20), (90, 80)
def main(rep, gender):
    dictionary, centroid_list = [], []
    cluster_dict = assign_cluster(income_dict[gender], score_dict[gender], guess_centroid(income_dict[gender], score_dict[gender]))
    cent_coord = calc_centroid(cluster_dict)
    plot_centroids(cluster_dict, f'{gender} INCOME VS SCORE', cent_coord)
    for i in range(rep):
        cluster_dict = assign_cluster(income_dict[gender], score_dict[gender], cent_coord)
        cent_coord = calc_centroid(cluster_dict)
        dictionary, centroid_list = plot_centroids(cluster_dict, f'{gender} INCOME VS SCORE', cent_coord)
    x_stats, y_stats = calc_stats(dictionary)
    print(cal_corr(male_income, male_age))

# main(4, 'Male')
# main(4, 'Female')



