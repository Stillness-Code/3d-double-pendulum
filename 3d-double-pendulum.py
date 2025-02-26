from manim import *
import numpy as np

class DoublePendulum(ThreeDScene):
    def construct(self):
        # set initial camera rotation angle
        self.rotation = -45

        # let's define our constants
        g = 9.8 # gravity
        L1, L2 = 2, 2 # rods length
        M1, M2 = 1, 2 # masses of the pendulums
        # Time step for simulation
        dt = .3
        
        # origin point for the pendulums
        origin = np.array([0, 0, 2])

        # set the initial angles for both pendulums (rads)
        theta1, theta2 = np.pi / 2, np.pi / 2
        # initial angular velocities (rad/s)
        omega1, omega2 = 0, 0

        # create rods
        rod1 = Line(origin, origin, color=BLUE)
        rod2 = Line(origin, origin, color=GREEN)

        # spherical masses
        mass1 = Sphere(radius=.25)
        mass1.set_color(RED)
        mass2 = Sphere(radius=.25)
        mass2.set_color(BLUE)

        # we'll group all pendulum elements together
        pendulum = VGroup(rod1, rod2, mass1, mass2)
        self.add(pendulum)
    
        # create and add 3d axes
        axes = ThreeDAxes()
        axes.set_color(GREY)
        # let's add labels
        lab_x = axes.get_x_axis_label(Tex("$x$"))
        lab_y = axes.get_y_axis_label(Tex("$y$"))
        lab_z = axes.get_z_axis_label(Tex("$z$"))
        self.add(axes, lab_x, lab_y, lab_z)

        def update(mob, dt=dt):
            nonlocal theta1, theta2, omega1, omega2

            # difference between angles
            delta = theta2 - theta1

            # denominators for the equations
            den1 = (2 * M1 + M2 - M2 * np.cos(2 * delta))
            den2 = (L2/L1) * den1

            # angular accel for the first pendulum
            a1 = (-g * (2*M1+M2) * np.sin(theta1) - M2 * g * np.sin(theta1 - 2*theta2) - 2*np.sin(delta) * M2 * (omega2**2 * L2 + omega1**2 * L1 * np.cos(delta))) / (L1 * den1)
            # accel for the second pendulum
            a2 = (2*np.sin(delta) * (omega1**2 * L1 * (M1+M2) + g * (M1+M2) * np.cos(theta1) + omega2**2 * L2 * M2 * np.cos(delta))) / (L1*den2)

            # set the angular vel using accel
            omega1 += a1 * dt
            omega2 += a2 * dt

            # update angles using new ang. vel.
            theta1 += omega1 * dt
            theta2 += omega2 * dt

            # set the positions
            pos1 = origin + L1 * np.array([0, np.sin(theta1), -np.cos(theta1)])
            pos2 = pos1 + L2 * np.array([0, np.sin(theta2), np.cos(theta2)])

            # update rods and masses
            rod1.put_start_and_end_on(origin, pos1)
            rod2.put_start_and_end_on(pos1, pos2)
            mass1.move_to(pos1)
            mass2.move_to(pos2)
            
            self.rotation += 1
            self.set_camera_orientation(phi=60*DEGREES, theta=self.rotation*DEGREES)

        pendulum.add_updater(update)
        self.wait(20)


DoublePendulum().render()