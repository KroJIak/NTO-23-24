#include <vector>
#include <valarray>
#include <iostream>
#include <cmath>

#include <thread>
#include <chrono>

#include <opencv2/opencv.hpp>

#include "Task.hpp"

void solve()
{
    // Инициализация переменных
    cv::Mat scene, mapWithZones;
    Task sim;

    // Запуск симуляции
    sim.start();

    // Информации о роботе
    std::cout << "Robots number: " << sim.robotsSize() << std::endl;
    std::cout << "Robot 0" << std::endl;
    auto robot_state = sim.getRobotState(0);
    std::cout << "Left Motor angle: " << robot_state.leftMotorAngle << std::endl;
    std::cout << "Right Motor angle: " << robot_state.rightMotorAngle << std::endl;
    std::cout << "Left Motor speed: " << robot_state.leftMotorSpeed << std::endl;
    std::cout << "Right Motor speed: " << robot_state.rightMotorSpeed << std::endl;

    std::valarray<double> voltage = {0, 0};

    std::cout << std::endl << "Task: " << std::endl << sim.getTask() << std::endl;
    
    for(size_t i = 0; i < 10; i++) 
    {

        sim.sendMessage("p_1 OK");
        voltage[0] = 0;
        voltage[1] = 10;

        sim.setMotorVoltage(0, voltage);

        scene = sim.getTaskScene();

        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        std::cout << "cpp" << std::endl;
    }

    sim.stop(); // Остановка симуляции (прерывание теста)
}

int main()
{
    solve();
    return 0;
}
