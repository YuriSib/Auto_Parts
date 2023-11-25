import pickle

with open('data_list.pickle', 'rb') as file:
    data_list = pickle.load(file)

data_list = data_list[:1]
print(data_list)


with open('data_list.pickle', 'wb') as file:
    pickle.dump(data_list, file)
