from math import *
import random

class robot:
    
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        self.measurement_noise = 0.0
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0
    
    
    # returns a positive, random float
    def rand(self):
        return random.random() * 2.0 - 1.0
    
    
    def move(self, dx, dy):
        
        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise
        
        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True


    def sense(self):
        ''' This function does not take in any parameters, instead it references internal variables
            (such as self.landamrks) to measure the distance between the robot and any landmarks
            that the robot can see (that are within its measurement range).
            This function returns a list of landmark indices, and the measured distances (dx, dy)
            between the robot's position and said landmarks.
            This function should account for measurement_noise and measurement_range.
            One item in the returned list should be in the form: [landmark_index, dx, dy].
            '''
           
        measurements = []
        
        dx, dy = 0, 0

        for landmark_index in range(self.num_landmarks):
            # Compute dx and dy
            dx, dy = self.landmarks[landmark_index][0] - self.x, self.landmarks[landmark_index][1] - self.y
            # Adding noise
            noise = self.rand() * self.measurement_noise
            dx, dy = dx + noise, dy + noise
            # Check if we can sense the landmark
            if dx > self.measurement_range or dy > self.measurement_range:
                continue
            else:
                # Keep track of landmark_index, dx, dy in measurements list
                measurements.append([landmark_index, dx, dy])        
        
        ## TODO: return the final, complete list of measurements
        return measurements


    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks


    def __repr__(self):
        return 'Robot: [x=%.5f y=%.5f]'  % (self.x, self.y)