
import numpy as np
import cv2



class KalmanFilter(object):
    """A Kalman filter tracker"""

    def __init__(self, init_x, init_y, Q=0.1 * np.eye(4), R=0.1 * np.eye(2)):
        """Initializes the Kalman Filter

        Args:
            init_x (int or float): Initial x position.
            init_y (int or float): Initial y position.
            Q (numpy.array): Process noise array.
            R (numpy.array): Measurement noise array.
        """
        self.state = np.array([init_x, init_y, 0., 0.])  # state
        self.X = np.array([init_x, init_y, 0., 0.]).reshape(4,1)  # state
        #self.X = np.array([init_x, init_y, 0., 0.]).reshape(1,4)  # state
        #self.state = np.array([init_x, init_y, 0., 0.]).T  # state
        self.Q = Q          # process noise matrix
        self.R = R          # measurement noise matrix
        #self.D = 1.0 * np.eye(4)  # state transition matrix
        self.D = np.array([[1.,0.,1.,0.],[0.,1.,0.,1.],[0.,0.,1.,0.],[0.,0.,0.,1.]]).reshape(4,4)
        #self.M = np.zeros((2,4)) # measurement matrix
        self.M = np.array([[1,0,0,0],[0,1,0,0]])
        self.P = 0.1 * np.eye(4)  # covariance array
        #self.P = np.zeros((4,4))  # covariance array

        #print(self.Q)
        #print(self.R)
        #print(self.D)
        #print(self.M)
        #print(self.P)

    def predict(self):
        #self.state = np.dot(self.D,self.state)
        #self.X = np.dot(self.D,self.X) + self.Q
        self.X = np.dot(self.D,self.X)
        self.P = np.dot(np.dot(self.D,self.P),self.D.T)+ self.Q

    def correct(self, meas_x, meas_y):
        a = np.dot(self.P, self.M.T)
        b = np.dot(self.M,a)
        a_ = b + self.R
        k_t = np.dot(a,np.linalg.inv(a_))    # kalman gain
        z = np.array([meas_x,meas_y]).reshape(2,1)
        #z = np.array([meas_x,meas_y]).reshape(1,2)
        y = z - np.dot(self.M,self.X)
        self.X = self.X + np.dot(k_t,y)
        e = np.dot(k_t, self.M)

        I =  1.0 * np.eye(4)
        self.P = np.dot(I - e,self.P)

        #self.state = self.state.reshape(1,4)[0]
        #print(self.state)
        #print(self.state[0],self.state[1])





    def process(self, measurement_x, measurement_y):

        self.predict()
        self.correct(measurement_x, measurement_y)
        #print("measurement_x, measurement_y")
        #print(measurement_x, measurement_y)
        self.state = self.X.reshape(1,4)[0]
        #print(self.state[0],self.state[1])

        return self.state[0], self.state[1]


class ParticleFilter(object):
    """A particle filter tracker.

    Encapsulating state, initialization and update methods. Refer to
    the method run_particle_filter( ) in experiment.py to understand
    how this class and methods work.
    """

    def __init__(self, frame, template, **kwargs):
        """Initializes the particle filter object.

        The main components of your particle filter should at least be:
        - self.particles (numpy.array): Here you will store your particles.
                                        This should be a N x 2 array where
                                        N = self.num_particles. This component
                                        is used by the autograder so make sure
                                        you define it appropriately.
                                        Make sure you use (x, y)
        - self.weights (numpy.array): Array of N weights, one for each
                                      particle.
                                      Hint: initialize them with a uniform
                                      normalized distribution (equal weight for
                                      each one). Required by the autograder.
        - self.template (numpy.array): Cropped section of the first video
                                       frame that will be used as the template
                                       to track.
        - self.frame (numpy.array): Current image frame.

        Args:
            frame (numpy.array): color BGR uint8 image of initial video frame,
                                 values in [0, 255].
            template (numpy.array): color BGR uint8 image of patch to track,
                                    values in [0, 255].
            kwargs: keyword arguments needed by particle filter model:
                    - num_particles (int): number of particles.
                    - sigma_exp (float): sigma value used in the similarity
                                         measure.
                    - sigma_dyn (float): sigma value that can be used when
                                         adding gaussian noise to u and v.
                    - template_rect (dict): Template coordinates with x, y,
                                            width, and height values.
        """
        self.num_particles = kwargs.get('num_particles')  # required by the autograder
        self.sigma_exp = kwargs.get('sigma_exp')  # required by the autograder
        self.sigma_dyn = kwargs.get('sigma_dyn')  # required by the autograder
        self.template_rect = kwargs.get('template_coords')  # required by the autograder
        # If you want to add more parameters, make sure you set a default value so that
        # your test doesn't fail the autograder because of an unknown or None value.
        #
        # The way to do it is:
        # self.some_parameter_name = kwargs.get('parameter_name', default_value)

        #self.template = template
        self.template = cv2.cvtColor(template.astype('float32'),cv2.COLOR_BGR2GRAY)
        self.frame = frame
        N = self.num_particles
        #h,w = self.frame.shape[:2]
        #xy_min = [0.0,0.0]
        #xy_max = [w,h]
        x = self.template_rect['x']
        y = self.template_rect['y']
        w = self.template_rect['w']
        h = self.template_rect['h']
        xy_min = [x-w,y-h]
        xy_max = [x+w,y+h]
        self.particles = np.array([x+w/2.,y+h/2.]*N).reshape(N,2)
        #self.particles = np.array([x,y]*N).reshape(N,2)
        #self.particles = np.random.uniform(low=xy_min,high=xy_max,size=(N,2))  # Initialize your particles array. Read the docstring.
        self.weights = np.array([1/N] * N)  # Initialize your weights array. Read the docstring.
        # Initialize any other components you may need when designing your filter.
        self.n_eff = 0

    def get_particles(self):
        """Returns the current particles state.

        This method is used by the autograder. Do not modify this function.

        Returns:
            numpy.array: particles data structure.
        """
        return self.particles

    def get_weights(self):
        """Returns the current particle filter's weights.

        This method is used by the autograder. Do not modify this function.

        Returns:
            numpy.array: weights data structure.
        """
        return self.weights

    def get_error_metric(self, template, frame_cutout):
        """Returns the error metric used based on the similarity measure.

        Returns:
            float: similarity value.
        """
        #print(template.shape)
        #print(frame_cutout.shape)
        #template = cv2.cvtColor(template.astype('float32'),cv2.COLOR_BGR2GRAY)
        #image = cv2.cvtColor(frame_cutout.astype('float32'),cv2.COLOR_BGR2GRAY)
        x = self.template_rect['x']
        y = self.template_rect['y']
        w,h = template.shape[:2]
        #diff = template-image
        #diff_square = [[y**2 for y in x] for x in diff]
        #sqe = np.sum(diff_square)
        #cv2.imshow("temp", template)
        #cv2.imshow("image", image)
        #sqe = np.sum((template.astype("float")-frame_cutout.astype("float"))**2)
        if template.shape[0] > frame_cutout.shape[0]:
            self.template = template[:frame_cutout.shape[0],:]
        if template.shape[1] > frame_cutout.shape[1]:
            self.template = template[:,:frame_cutout.shape[1]]

        sqe = np.sum((template-frame_cutout)**2)
        #print("sqe")
        #print(sqe)
        mse = sqe/float(w*h)
        #print("mse")
        #print(mse)
        similarity = np.exp(-1 * mse/(2.0 * self.sigma_exp ** 2))
        #print("similarity")
        #print(similarity)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return similarity


    def resample_particles(self):
        """Returns a new set of particles

        This method does not alter self.particles.

        Use self.num_particles and self.weights to return an array of
        resampled particles based on their weights.

        See np.random.choice or np.random.multinomial.
        
        Returns:
            numpy.array: particles data structure.
        """
        w = self.get_weights()
        n = self.num_particles
        particle_indices = np.arange(n)
        indices = np.random.choice(a=particle_indices,size=n,p=w,replace=True)
        
        return self.particles[indices,:]

    def process(self, frame):
        """Processes a video frame (image) and updates the filter's state.

        Implement the particle filter in this method returning None
        (do not include a return call). This function should update the
        particles and weights data structures.

        Make sure your particle filter is able to cover the entire area of the
        image. This means you should address particles that are close to the
        image borders.

        Args:
            frame (numpy.array): color BGR uint8 image of current video frame,
                                 values in [0, 255].

        Returns:
            None.
        """
        n = self.num_particles
        u_weighted_mean = 0
        v_weighted_mean = 0
        for i in range(n):
            u_weighted_mean += self.particles[i, 0] * self.weights[i]
            v_weighted_mean += self.particles[i, 1] * self.weights[i]
        self.particles = np.array([u_weighted_mean,v_weighted_mean]* n).reshape(n,2)
        self.weights = np.array([1/n] * n)  # Initialize your weights array. Read the docstring.
        states = self.get_particles()
        frame = cv2.cvtColor(frame.astype('float32'),cv2.COLOR_BGR2GRAY)
        #print("states")
        #print(states)
        #weights = self.get_weights()
        w = self.template_rect['w']
        h = self.template_rect['h']
        gauss = np.random.normal(loc=0.0,scale=self.sigma_dyn,size=(self.num_particles,2))
        states += gauss 
        #print("states with gauss")
        #print(states)
        for state in states:
            if state[0] > self.frame.shape[1]:
                state[0] = self.frame.shape[1] - 1
            if state[1] > self.frame.shape[0]:
                state[1] = self.frame.shape[0] - 1
            if state[0] < 0:
                state[0] = 0
            if state[1] < 0:
                state[1] = 0
        #print("states with gauss after")
        #print(states)



        #pad frame
        top = int(0.6 * h)
        bottom = top
        left = int(0.6 * w)
        right = left
        #print("frame.shape")
        #print(frame.shape)
        frame = cv2.copyMakeBorder(frame,top,bottom,left,right,borderType=cv2.BORDER_CONSTANT)
        #self.weights = np.array([1/n] * n)  # Initialize your weights array. Read the docstring.

        #print("self.n_eff")
        #print(self.n_eff)
        #for j in range(4):
        for j in range(8):
            #print("self.n_eff")
            #print(self.n_eff)
            s = self.resample_particles()
            self.particles = s
            eta = 0
            weights = []
            for i in range(n):
                centre = self.particles[i]    # ith particle location: tuple (x,y)
                #print("centre")
                #print(centre)
                new_x = centre[0] + 0.6*w
                new_y = centre[1] + 0.6*h
                y = new_y - h/2. 
                x = new_x - w/2.
                if y < 0: y = 0
                if x < 0: x = 0
                H,W = frame.shape[:2]
                if int(x) + int(w) > W: x = W - int(w)
                if int(y) + int(h) > H: y = H - int(h)
                #print("x,y")
                #print(x,y)
                frame_cut = frame[int(y):int(y)+int(h),int(x):int(x)+int(w)]
                #print("------------")
                #print(frame_cut.shape)
                #print(self.template.shape)
                #print(frame.shape)
                wi = self.get_error_metric(self.template,frame_cut)
                weights.append(wi)

                eta += wi
            self.weights = weights/eta
            #self.n_eff = (1.0 / np.sum(self.weights ** 2)) / n
            
            #self.particles = s
            #print("self.particles")
            #print(self.particles)
        '''
        u_weighted_mean = 0
        v_weighted_mean = 0
        for i in range(n):
            u_weighted_mean += self.particles[i, 0] * self.weights[i]
            v_weighted_mean += self.particles[i, 1] * self.weights[i]
        '''
        








    def render(self, frame_in):
        """Visualizes current particle filter state.

        This method may not be called for all frames, so don't do any model
        updates here!

        These steps will calculate the weighted mean. The resulting values
        should represent the tracking window center point.

        In order to visualize the tracker's behavior you will need to overlay
        each successive frame with the following elements:

        - Every particle's (x, y) location in the distribution should be
          plotted by drawing a colored dot point on the image. Remember that
          this should be the center of the window, not the corner.
        - Draw the rectangle of the tracking window associated with the
          Bayesian estimate for the current location which is simply the
          weighted mean of the (x, y) of the particles.
        - Finally we need to get some sense of the standard deviation or
          spread of the distribution. First, find the distance of every
          particle to the weighted mean. Next, take the weighted sum of these
          distances and plot a circle centered at the weighted mean with this
          radius.

        This function should work for all particle filters in this problem set.

        Args:
            frame_in (numpy.array): copy of frame to render the state of the
                                    particle filter.
        """

        x_weighted_mean = 0
        y_weighted_mean = 0
        distance = np.array([0.0] * self.num_particles)
        for i in range(self.num_particles):
            x_weighted_mean += self.particles[i, 0] * self.weights[i]
            y_weighted_mean += self.particles[i, 1] * self.weights[i]

        # draw each particle location
        for i in range(self.num_particles):
            distance[i] = np.sqrt((self.particles[i,0]-x_weighted_mean)**2+(self.particles[i,1]-y_weighted_mean)**2)
            cv2.circle(frame_in,(int(self.particles[i,0]),int(self.particles[i,1])),1,(255,0,0),2)
        # draw rectangle 
        h = self.template_rect['h']
        w = self.template_rect['w']
        x1 = x_weighted_mean - w/2
        y1 = y_weighted_mean - h/2
        x2 = x_weighted_mean + w/2
        y2 = y_weighted_mean + h/2
        cv2.rectangle(frame_in,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0), 2)
        #print("distance") 
        #print(distance) 
        # draw circle
        weighted_sum = np.dot(distance, self.weights.T)
        #print("weighted_sum")
        #print(weighted_sum)
        cv2.circle(frame_in,(int(x_weighted_mean),int(y_weighted_mean)),int(weighted_sum),(255,0,255),2)
        



class AppearanceModelPF(ParticleFilter):
    """A variation of particle filter tracker."""

    def __init__(self, frame, template, **kwargs):
        """Initializes the appearance model particle filter.

        The documentation for this class is the same as the ParticleFilter
        above. There is one element that is added called alpha which is
        explained in the problem set documentation. By calling super(...) all
        the elements used in ParticleFilter will be inherited so you do not
        have to declare them again.
        """

        super(AppearanceModelPF, self).__init__(frame, template, **kwargs)  # call base class constructor

        self.alpha = kwargs.get('alpha')  # required by the autograder
        # If you want to add more parameters, make sure you set a default value so that
        # your test doesn't fail the autograder because of an unknown or None value.
        #
        # The way to do it is:
        # self.some_parameter_name = kwargs.get('parameter_name', default_value)

    def process(self, frame):
        """Processes a video frame (image) and updates the filter's state.

        This process is also inherited from ParticleFilter. Depending on your
        implementation, you may comment out this function and use helper
        methods that implement the "Appearance Model" procedure.

        Args:
            frame (numpy.array): color BGR uint8 image of current video frame, values in [0, 255].

        Returns:
            None.
        """
        #print(self.template.shape)
        #print(frame.shape)
        super().process(frame)
        #print("self.particles")
        #print(self.particles[0])
        #print(self.particles[0,0])
        n = self.num_particles
        '''
        u_weighted_mean = 0
        v_weighted_mean = 0
        for i in range(n):
            u_weighted_mean += self.particles[i, 0] * self.weights[i]
            v_weighted_mean += self.particles[i, 1] * self.weights[i]
        '''
        x = self.particles[0,0] - self.template_rect['w']/2
        y = self.particles[0,1] - self.template_rect['h']/2
        h = self.template_rect['h']
        w = self.template_rect['w']
        if x < 0: x = 0
        if y < 0: y = 0
        H,W = frame.shape[:2]
        if int(x) + int(w) > W: x = W - int(w)
        if int(y) + int(h) > H: y = H - int(h)
        Best = frame[int(y):int(y)+int(h),int(x):int(x)+int(w)]
        #template = cv2.cvtColor(template.astype('float32'),cv2.COLOR_BGR2GRAY)
        Best = cv2.cvtColor(Best.astype('float32'),cv2.COLOR_BGR2GRAY) 
        self.template = self.alpha * Best + (1-self.alpha) * self.template

        


