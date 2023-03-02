# Launch files description

## For basic control (JoyStick)

| File name                                   | Purpose                          |
| ------------------------------------------- | -------------------------------- |
| [main.launch](../haruna/launch/main.launch) | Control the robot using joystick |

## For manual mapping

| File name                                                   | Purpose                                          |
| ----------------------------------------------------------- | ------------------------------------------------ |
| [mapping.launch](../haruna/launch/map.launch)               | Manual mapping. Control the robot using JoyStick |
| [mapping_host.launch](../haruna/launch/mapping_host.launch) | Visualize created map in `RViz`                  |

## For navigation

| File name                                                         | Purpose                                                         |
| ----------------------------------------------------------------- | --------------------------------------------------------------- |
| [navigation.launch](../haruna/launch/navigation.launch)           | Run the robot in Navigation mode                                |
| [navigation_host.launch](../haruna/launch/navigation_host.launch) | Vizualize map, path, robot model or else and set goal in `RViz` |

## For auto mapping

| File name                                                             | Purpose                                                                          |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [mapping_auto.launch](../haruna/launch/map_auto.launch)               | Auto mapping and autonomous                                                      |
| [mapping_auto_host.launch](../haruna/launch/auto_mapping_host.launch) | [navigation_host.launch](../haruna/launch/navigation_host.launch) + auto mapping |
