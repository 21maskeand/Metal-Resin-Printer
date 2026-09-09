//heater.h
#pragma once

void heaters_Init();
void pid_Update();
void set_Heater_Setpoint(int id , float setpoint);
float return_Temp(int id);
float return_Setpoint(int id);