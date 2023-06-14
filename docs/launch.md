# Launch files description

## For basic control (JoyStick)

| File name                                   | Purpose                          |
| ------------------------------------------- | -------------------------------- |
| [main.launch](../haruna/launch/main.launch) | Control the robot using joystick |

## For simulation

| File name                                   | Purpose                          |
| ------------------------------------------- | -------------------------------- |
| [gazebo.launch](../haruna_simulations/launch/gazebo.launch) | Simulate haruna on Gazebo |

## For manual mapping

| File name                                                              | Purpose                                          |
| ---------------------------------------------------------------------- | ------------------------------------------------ |
| [mapping.launch](../haruna_navigation/launch/mapping.launch)           | Manual mapping. Control the robot using JoyStick |
| [mapping_rviz.launch](../haruna_navigation/launch/mapping_rviz.launch) | Visualize created map in `RViz`                  |

## For navigation

| File name                                                                    | Purpose                                                         |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [navigation.launch](../haruna_navigation/launch/navigation.launch)           | Run the robot in Navigation mode                                |
| [navigation_rviz.launch](../haruna_navigation/launch/navigation_rviz.launch) | Visualize map, path, robot model or else and set goal in `RViz` |

## For auto mapping

| File name                                                                        | Purpose                                                                                     |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [mapping_auto.launch](../haruna_navigation/launch/mapping_auto.launch)           | Auto mapping and autonomous                                                                 |
| [mapping_auto_rviz.launch](../haruna_navigation/launch/mapping_auto_rviz.launch) | [navigation_rviz.launch](../haruna_navigation/launch/navigation_rviz.launch) + auto mapping |
