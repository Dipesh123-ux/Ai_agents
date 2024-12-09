import numpy as np
from time import process_time

# time taken by the list 

python_list = [i for i in range(1000)]


start_time = process_time()


python_list = [i+5 for i in python_list]

end_time = process_time()


print(end_time-start_time)


# time taken by numpy


np_array = np.array([i for i in range(1000)])

start_time = process_time()

np_array += 5

end_time = process_time()

print(end_time-start_time)


# creating a 2d array

np_array_2 = np.array([(1,2,3,4),(5,6,7,8)])

print(np_array_2)


#initialize the array with all zeros

a = np.zeros((4,5))

print(a)

# initialze all values with one

b = np.ones((4,5))

print(b)

# initialize all values with a specific value

c = np.full((4,5),3)

print(c)

# identity matrix

i = np.eye(4)

print(i)



# analysing numpy array



c = np.random.randint(10,90,(5,5))

print(c)

print(c.shape,c.ndim)

# mathematical operations

