//settings.cpp
#include "settings.h"
#include "config.h"

Settings settings = default_settings;

void set_Max_Speed(int id , float speed)
{
  if (id < 0 || id >= num_axes) return;
  settings.max_speeds[id] = speed;
}

void set_Acceleration(int id , float acc)
{
  if (id < 0 || id >= num_axes) return;
  settings.accelerations[id] = acc;
}

void set_Microstepping_Mode(int mode)
{
  if (mode < 0 || mode >= 5) return;
  settings.microstepping_mode = mode;
}

void set_Offset_Distance(int id , float dist)
{
  if (id < 0 || id >= num_axes) return;
  settings.homing_offset_dists[id] = dist;
}

void reset_Default_Settings()
{
  settings = default_settings;
}