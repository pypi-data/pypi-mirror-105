import abc

from controller import Radar
from flockai.interfaces.drone import IDrone


class AutopilotControlledDrone(IDrone, abc.ABC):
    def __init__(self, devices):
        super().__init__(devices)
        self.target = [5, 5]
        self.prev_distance = self.get_distance_from_target()
        self.simulation_step = 0

    def set_flight_plan(self, plan):
        pass

    def update_flight_plan(self, plan):
        pass

    def abort_flight_plan(self):
        pass

    def get_flight_plan(self):
        pass

    def move(self, direction=1):
        """
        Return forward or backward disturbance for moving
        :param direction: 1 for forward, -1 for backward, 0 for stable
        :return:
        """
        pitch_disturbance = 2 * direction
        return pitch_disturbance

    def rotate(self, direction=1):
        """
        Return left or right disturbance for rotation
        :param direction: 1 for right, -1 for left, 0 for stable
        :return:
        """
        yaw_disturbance = 1.3 * direction

    def should_move_forward(self, target):
        pass

    def get_coordinates(self):
        gps = self.devices['gps']['device']
        return gps.getValues()

    def get_distance_from_target(self):
        coordinates = self.get_coordinates()
        distances = [abs(coordinates[0] - self.target[0]), abs(coordinates[2] - self.target[1])]
        return distances

    def target_has_reached(self):
        distance = [d // 1 for d in self.get_distance_from_target()]
        return not any(distance)

    def on_track(self):
        new_distance = self.get_distance_from_target()
        ok = all([self.prev_distance[0] > new_distance[0], self.prev_distance[1] > new_distance[1]])
        self.prev_distance = new_distance
        return ok

    def get_input(self):
        """
        Input is based on if we are getting closer to the target
        In case we are on the target no input is given
        :return:
        """
        # self.simulation_step += 1
        # if self.simulation_step % 5 == 0:
        #     if self.target_has_reached():
        #         return 0, 0, 0
        #
        #     if self.on_track():
        #         self.simulation_step -= 1
        #         return 0, 4, 0
        #
        #     return 0, 0, 2.3
        # return 0, 0, 0
        from os import system
        system('clear')

        radar: Radar = self.devices['radar']['device']
        total_targets = radar.getNumberOfTargets()
        targets = radar.getTargets()
        print('Currently seeing', total_targets, 'targets')
        for i in range(total_targets):
            print(f'--target {i}: distance = {targets[i].distance}')

        # # Transform the keyboard input to disturbances on the stabilization algorithm.
        roll_disturbance = 0
        pitch_disturbance = 0
        yaw_disturbance = 2.3

        return roll_disturbance, pitch_disturbance, yaw_disturbance
