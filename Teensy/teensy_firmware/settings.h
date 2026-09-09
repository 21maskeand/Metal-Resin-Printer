//settings.h
#pragma once

struct Settings
{
  float max_speeds[3];     // pitch units (mm) per Second
  float accelerations[3];  // pitch units (mm) per Second^2
  int   microstepping_mode;
  float homing_offset_dists[3];
};

constexpr Settings default_settings = 
{
  .max_speeds = {2.5 , 2.5 , 10} , 
  .accelerations = {5 , 5 , 5} , 
  .microstepping_mode = 5 , 
  .homing_offset_dists = {2.8 , 2.5 , 3}
};

extern Settings settings;