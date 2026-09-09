// limit_switch.cpp
#include "limit_switches.h"
#include "config.h"
#include <Arduino.h>

void switches_Init()
{
  pinMode(switch_pins[0] , INPUT);
  pinMode(switch_pins[1] , INPUT);
  pinMode(switch_pins[2] , INPUT);
}

bool switch_Pressed(int id)
{
  if (digitalRead(switch_pins[id]))
  {
    return normally_open[id];
  }
  else
  {
    return !normally_open[id];
  }
}