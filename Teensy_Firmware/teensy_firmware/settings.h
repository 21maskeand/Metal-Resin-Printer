//settings.h
#pragma once

void set_Max_Speed(int axis_id , float speed);
void set_Acceleration(int axis_id , float acc);
void set_Microstepping_Mode(int mode);
void set_Offset_Distance(int axis_id , float dist);
void reset_Default_Settings();

struct Settings
{
  float max_speeds[3];     // pitch units (mm) per Second
  float accelerations[3];  // pitch units (mm) per Second^2
  int   microstepping_mode;
  float homing_offset_dists[3];
};

constexpr Settings default_settings = 
{
  .max_speeds = {10 , 10 , 40} , 
  .accelerations = {5 , 5 , 5} , 
  .microstepping_mode = 5 , 
  .homing_offset_dists = {.3 , 2.5 , 3}
};

extern Settings settings;