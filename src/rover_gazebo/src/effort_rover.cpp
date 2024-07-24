#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>

class TorqueCommandPublisher : public rclcpp::Node
{
public:
  TorqueCommandPublisher()
  : Node("torque_command_publisher")
  {
    publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>("/torque_controller/commands", 10);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&TorqueCommandPublisher::publish_torque_command, this));
  }

private:
  void publish_torque_command()
  {
    auto message = std_msgs::msg::Float64MultiArray();
    // Example torque values for each joint
    message.data = {0.5, 0.5, 0.5, -0.5, -0.5, -0.5};
    publisher_->publish(message);
  }

  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<TorqueCommandPublisher>());
  rclcpp::shutdown();
  return 0;
}
