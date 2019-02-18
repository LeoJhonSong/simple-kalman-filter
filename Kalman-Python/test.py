import simple_kalman_py as kal
import numpy as np
import matplotlib.pyplot as plt
import cv2


# initial the filter
motor = kal.myKalman(2, 2, 1, 1)

# set period = 4ms
t = 0.04

# set transition matrix and transform matrix
# the transition matrix and transform matrix for control vector is simply based on Newton's law
motor.setAH([[1, t], [0, 1]], 0)
motor.setB([[t * t / 2], [t]])

# set P, Q, R
P = 6e-2
Qa = 4.5e-1
Ra = 1e-5
Qv = 6e-3
Rv = 1e-6

motor.setP(P)
motor.setQ([Qa, Qv])
motor.setR([Ra, Rv])

velocity = 0
velocity_last = 0

# give a initial state (be careful the unit)
# motor.statePost = np.mat([[input[0, 0]], [input[0, 2]*2*np.pi]])  # better initial value

# use these two array to store the filtered data
angle = []
speed = []

input = np.loadtxt('./test_data2/with_cmd.txt')  # angle, control, velocity

for column in input:
    angleIn = column[0]
    controlIn = column[1]
    velocityIn = column[2]

    # transfer the units
    angle = angleIn
    velocity = velocityIn * 2 * np.pi
    control = (controlIn * 2 * np.pi - velocity)  # indicate acceleration by increment

    # filter the data
    motor.new(([angle], [velocity]), control)

    # store the filtered data
    angle.append(motor.statePost[0, 0])
    speed.append(motor.statePost[1, 0])

# smooth the data utilizing Gaussian Blur
# angle = np.array(angle)
# angle = cv2.GaussianBlur(angle, (1, 25), 0)

# save the filtered data
# for i in range(len(angle)):
#     with open('./dst/filtered.txt', 'a') as dst:
#             dst.write(str(angle[i, 0]))
#             dst.write('\n')

# plot them
time = np.linspace(0, input.shape[0], input.shape[0])

plt.subplot(211)
plt.plot(time, angle, color='green')  # filtered
plt.plot(time, input[:, 0], color='red', linestyle='--')  # unfiltered

plt.subplot(212)
plt.plot(time, speed, color='green')  # filtered
plt.plot(time, (input[:, 2]*2*np.pi/60), color='red', linestyle='--')  # unfiltered

plt.show()
