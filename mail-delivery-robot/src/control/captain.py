import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from src.control.action_translator import translate_action
from rclpy.action import ActionClient
from irobot_create_msgs.action import Dock, Undock
import subprocess

class Captain(Node):
    '''
    The Node responsible for listening to actions from the
    subsumption layers and sending commands to the robot.

    @Subscribers:
    - Listens to /actions for new actions

    @Publishers:
    - Publishes commands to the robot to /cmd_vel
    '''
    def __init__(self):
        '''
        The constructor for the node.
        Defines the necessary publishers and subscribers.
        '''
        super().__init__('captain')

        self.current_actions = {
            '0' : 'NONE',
            '1' : 'NONE',
            '2' : 'NONE',
            '3' : 'NONE'
        }

        self.actions_sub = self.create_subscription(String, 'actions', self.parse_action, 10)
        self.command_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        self.docking_client = ActionClient(self, Dock, 'dock')
        self.undocking_client = ActionClient(self, Undock, 'undock')
        self.dock_msg = Dock.Goal()
        self.undock_msg = Undock.Goal()

        self.timer = self.create_timer(0.2, self.send_command)

    def parse_action(self, data):
        prio, action = data.data.split(':')
        self.current_actions[prio] = action

    def send_command(self):
        for action in self.current_actions.values():
            if action != 'NONE' and action != 'DOCK' and action != 'UNDOCK':
                command = translate_action(action)
                self.command_publisher.publish(command)
                break
            elif action == 'DOCK':
                #subprocess.run(["ros2", "action", "send_goal", "/dock", "irobot_create_msgs/action/Dock", "{}"])
                self.docking_client.send_goal_async(self.dock_msg)
                break
            elif action == 'UNDOCK':
                #subprocess.run(["ros2", "action", "send_goal", "/undock", "irobot_create_msgs/action/Undock", "{}"])
                self.undocking_client.send_goal_async(self.undock_msg)
                break
        self.get_logger().info(str(self.current_actions))

def main():
    rclpy.init()
    captain = Captain()
    rclpy.spin(captain)

if __name__ == '__main__':
    main()