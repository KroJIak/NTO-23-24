#pragma once

#include "Robot.hpp"

#include <opencv2/opencv.hpp>
#include <string>
#include <signal.h>

class Simulation;
class GrayRobotC;
class Checker;

void readTaskFile(std::string filePath, std::vector<uint> &start_point, std::string &task);

class Task
{
private:

    static std::vector<Task*> all_tasks_ptr;
    std::shared_ptr<Simulation> sim;
    GrayRobotC* grayRobot;
    Checker* checker;

    std::queue <std::string> userMessages;

    static void sigintCallback(int signum)
    {
        for (auto& task_ptr : all_tasks_ptr) { 
            task_ptr -> stop();
        }
        exit(0);
    }

public:
    Task();
    ~Task();

    void start();
    void stop();
    void complete();

    cv::Mat getTaskScene();
    cv::Mat getTaskMap();
    cv::Mat getTaskMapWithZones();

    size_t robotsSize();
    Robot::State getRobotState(size_t idx);
    void setMotorVoltage(size_t idx, std::valarray<double> ctrl);

    void sendMessage(std::string msg);
    std::string getTask();
};
