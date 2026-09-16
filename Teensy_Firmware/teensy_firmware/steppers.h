//steppers.h
#pragma once

void steppers_Init();
void steppers_Update();
void move_Stepper_Relative(int id , float move);
void move_Stepper_Absolute(int id , float move);
void home_Stepper(int id);
void move_To_Top(int id);
