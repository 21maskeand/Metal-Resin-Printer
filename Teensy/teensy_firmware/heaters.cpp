//heaters.cpp
#include "heaters.h"
#include "config.h"
#include <DS18B20.h>
#include <QuickPID.h>
#include <Arduino.h>

static DS18B20 probes[num_heaters] = 
{
  DS18B20(probe_pins[0]) , 
  DS18B20(probe_pins[1])
};

static float temps[num_heaters];
static float outputs[num_heaters];
static float setpoints[num_heaters] = {0 , 0};
static int window_start_times[num_heaters] = {0 , 0};

static QuickPID pids[num_heaters] = 
{
  QuickPID(&temps[0] , &outputs[0] , &setpoints[0] , kps[0] , kis[0] , kds[0] , QuickPID::pMode::pOnError , QuickPID::dMode::dOnMeas , QuickPID::iAwMode::iAwClamp , QuickPID::Action::direct) , 
  QuickPID(&temps[1] , &outputs[1] , &setpoints[1] , kps[1] , kis[1] , kds[1] , QuickPID::pMode::pOnError , QuickPID::dMode::dOnMeas , QuickPID::iAwMode::iAwClamp , QuickPID::Action::direct) 
};

void heaters_Init()
{
  for (int i = 0; i < num_heaters; i++)
  {
    pinMode(heater_pins[i] , OUTPUT);
    pids[i].SetOutputLimits(0.0 , 1.0);
    pids[i].SetSampleTimeUs(window_size*1000);
    pids[i].SetMode(QuickPID::Control::automatic);
  }
}

static void probes_Update()
{
  for (int i = 0; i< num_heaters; i++)
  {
    probes[i].selectNext();
    temps[i] = probes[i].getTempC();
  }
}

void pid_Update()
{
  unsigned long now_time = millis();
  probes_Update();

  for (int i = 0; i < num_heaters; i++)
  {
    if (pids[i].Compute())
    {
      window_start_times[i] = now_time;
    }

    if (outputs[i]*window_size > (now_time - window_start_times[i]))
    {
      digitalWrite(heater_pins[i] , HIGH);
      // Serial.println(outputs[0]);
      // Serial.println("on");
    }
    else
    {
      digitalWrite(heater_pins[i] , LOW);
      // Serial.println(outputs[0]);
      // Serial.println("off");
    }
  }
}

void set_Heater_Setpoint(int id , float setpoint)
{
  setpoints[id] = setpoint;
}

float return_Temp(int id)
{
  return temps[id];
}

float return_Setpoint(int id)
{
  return setpoints[id];
}














