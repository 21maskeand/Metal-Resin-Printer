// config.h
#pragma once

// MICROSTEPPING PINS AND CONFIGURATION

constexpr int m0 = 9 , m1 = 10 , m2 = 11;
constexpr int microstepping_mode_to_pins[6][3] = 
{
  {0 , 0 , 0} , // Full Step , Mode 0
  {0 , 0 , 1} , // 1/2 Step  , Mode 1
  {0 , 1 , 0} , // 1/4 Step  , Mode 2
  {0 , 1 , 1} , // 1/8 Step  , Mode 3
  {1 , 0 , 0} , // 1/16 Step , Mode 4
  {1 , 1 , 1}   // 1/32 Step , Mode 5
};
constexpr int microstepping_mode_to_steps[6] = {1 , 2 , 4 , 8 , 16 , 32};


// STEPPER MOTOR PINS AND CONFIGURATION

// Reservoir: 0 , Build: 1 , Recoater: 2
constexpr int num_axes = 3;
constexpr int step_pins[3] = {19 , 17 , 15};
constexpr int dir_pins[3] = {18 , 16 , 14};
constexpr int leads[3] = {4 , 4 , 8};                     // mm/rot or whatever other unit per rotation
constexpr int steps_per_rotation[3] = {200 , 200 , 200};  // steps/rot (full steps)
constexpr int min_travel[3] = {-185 , -185 , -2};         // mm minimum from being zeroed
constexpr int max_travel[3] = {1 , 1 , 200};              // mm maximum from being zeroed
constexpr int min_pulse_width = 5;                        // us minimum pulse witdth that the teensy can send to the drv8825


// LIMIT SWITCH PINS

// Reservoir: 0 , Build: 1 , Recoater: 2
constexpr int switch_pins[3] = {22 , 21 , 20};
constexpr bool normally_open[3] = {false , false , true};
constexpr float homing_fast_speed_fracs[3] = {1 , 1 , -0.5};
constexpr float homing_slow_speed_fracs[3] = {.1 , .1 , -.1};
constexpr float backoff_dist[3] = {-4 , -4 , 4};


// TEMPERATURE PINS AND CONFIGURATION

// Chamber: 0 , Recoater: 1
constexpr int num_heaters = 2;
constexpr int probe_pins[2] = {4 , 5};
constexpr int heater_pins[2] = {3 , 2};
constexpr float kps[2] = {.1 , 1};
constexpr float kis[2] = {0 , 0};
constexpr float kds[2] = {1 , 2};
constexpr int window_size = 5000;
constexpr int resolution_modes[2] = {0 , 0}; // 0 --> 9 bits , 1 --> 10 bits , 2 --> 11 bits , 3 --> 12 bits
constexpr int resolution_mode_to_bits[4] = {9 , 10 , 11 , 12};
constexpr int resolution_mode_to_read_time[4] = {94 , 188 , 376 , 751}; // ms


