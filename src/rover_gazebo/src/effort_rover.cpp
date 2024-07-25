#include <memory>
#include <string>
#include <vector>
#include <chrono>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<rclcpp::Node>("effort_test_node");

  auto publisher = node->create_publisher<std_msgs::msg::Float64MultiArray>(
    "/effort_controller/commands", 10);

  RCLCPP_INFO(node->get_logger(), "Node created");

  std_msgs::msg::Float64MultiArray commands;
  float t = 0.29;
  commands.data = {t, t, t, t, t, t};

  rclcpp::WallRate loop_rate(50);  // Loop rate in Hz

  while (rclcpp::ok()) {
    publisher->publish(commands);
    loop_rate.sleep();  // Sleep for the duration of the loop rate
  }

  rclcpp::shutdown();
  return 0;
}
