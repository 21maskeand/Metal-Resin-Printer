//commands.cpp
#include "commands.h"
#include "steppers.h"
#include "heaters.h"
#include <Arduino.h>

static char buffer[32];
static int length = 0;

static void handle_Command(char *command)
{

  if ((command[0] == 'M') & (command[1] == 'R'))
  {
    int stepper_id = atoi(command + 2);
    char *space = strchr(command , ' ');
    if (space)
    {
      float move = atof(space + 1);
      move_Stepper_Relative(stepper_id , move);
    }
  }

  else if ((command[0] == 'M') & (command[1] == 'A'))
  {
    int stepper_id = atoi(command + 2);
    char *space = strchr(command , ' ');
    if (space)
    {
      float move = atof(space + 1);
      move_Stepper_Absolute(stepper_id , move);
    }
  }

  else if ((command[0] == 'M') & (command[1] == 'T'))
  {
    int stepper_id = atoi(command + 2);
    move_To_Top(stepper_id);
  }

  else if (command[0] == 'H')
  {
    int stepper_id = atoi(command + 1);
    home_Stepper(stepper_id);
    
  }

  else if ((command[0] == 'S') && (command[1] == 'H'))
  {
    int heater_id = atoi(command + 2);
    char *space = strchr(command , ' ');
    if (space)
    {
      float setpoint = atof(space + 1);
      set_Heater_Setpoint(heater_id , setpoint);
    }
  }

  else if ((command[0] == 'R') && (command[1] == 'T'))
  {
    int probe_id = atoi(command + 2);
    float temp = return_Temp(probe_id);
    Serial.print("RT"); Serial.print(probe_id); Serial.print(" "); Serial.println(temp);
  }

  else if (command[0] == 'E')
  {
    char *space = strchr(command , ' ');
    if (space)
    {
      Serial.println(space + 1);
    }
  }


}

void poll_For_Commands()
{
  while (Serial.available())
  {
      char c = Serial.read();
      if (c == '\n')
      {
        buffer[length] = 0;
        handle_Command(buffer);
        length = 0;
      }
      else if (length < (int)sizeof(buffer) - 1)
      {
        buffer[length++] = c;
      }
  }
}





