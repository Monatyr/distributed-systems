import sys, Ice
import calculator_ice
import Devices
import re

with Ice.initialize(sys.argv) as communicator:
    # base = communicator.stringToProxy('calc/calc11:tcp -h 127.0.0.2 -p 10000')
    # base = communicator.stringToProxy('calc/calc11:default -p 10000')
    # calculator = Demo.CalcPrx.checkedCast(base)
    # print(calculator.add(1, 2))

    devices_manager_base_1 = communicator.stringToProxy('manager/dm:tcp -h 127.0.0.2 -p 10000')

    fridge_base_1 = communicator.stringToProxy('fridge/f1:tcp -h 127.0.0.2 -p 10000')
    fridge_base_2 = communicator.stringToProxy('fridge/f2:tcp -h 127.0.0.2 -p 10000')
    fridge_with_freezer_base = communicator.stringToProxy('fridge/fwf1:tcp -h 127.0.0.2 -p 10000')
    microwave_base = communicator.stringToProxy('microwave/m1:tcp -h 127.0.0.2 -p 10000')
    sensor_base = communicator.stringToProxy('sensor/s1:tcp -h 127.0.0.2 -p 10000')
    pressure_sensor_base_1 = communicator.stringToProxy('sensor/ps1:tcp -h 127.0.0.2 -p 10000')
    pressure_sensor_base_2 = communicator.stringToProxy('sensor/ps2:tcp -h 127.0.0.2 -p 10000')
    humidity_sensor_base_1 = communicator.stringToProxy('sensor/hs1:tcp -h 127.0.0.2 -p 10000')

    devices_manager_1 = Devices.DevicesManagerPrx.checkedCast(devices_manager_base_1)

    fridge_1 = Devices.FridgePrx.checkedCast(fridge_base_1)
    fridge_2 = Devices.FridgePrx.checkedCast(fridge_base_2)
    fridge_with_freezer_1 = Devices.FridgeWithFreezerPrx.checkedCast(fridge_with_freezer_base)
    microwave_1 = Devices.MicrowavePrx.checkedCast(microwave_base)
    sensor_1 = Devices.SensorPrx.checkedCast(sensor_base)
    pressure_sensor_1 = Devices.PressureSensorPrx.checkedCast(pressure_sensor_base_1)
    pressure_sensor_2 = Devices.PressureSensorPrx.checkedCast(pressure_sensor_base_2)
    humidity_sensor_1 = Devices.HumiditySensorPrx.checkedCast(humidity_sensor_base_1)

    print("\nTo send a command type: <device_name> <function_name> <args>\nIf you don't know devices' names type: 'names'\n")

    while True:
        command = input("> ").strip().lower()
        command = re.split(r",|\s|/", command)
        
        if(command[0] == "names" and len(command) == 1):
            names = devices_manager_1.getAllDevicesNames()
            print("[devices_names]: ", end='')
            for name in names:
                print(name, end=" ")
            print()
        elif(command[0] == "exit"):
            print("Exit")
            break
        elif(command[0] == "fridge"):
            if(command[1] == "f1"):
                pass
            elif(command[1] == "f2"):
                pass
            elif(command[1] == "fwf1"):
                pass

#     print(devices_manager_1.getAllDevicesNames())
#     print(humidity_sensor_1.getHumidity())
#     print(pressure_sensor_2.getAllMeasurements())
#     print(pressure_sensor_1.getPressure())
#     microwave_1.setTemp(12)


#     names = devices_manager_1.getAllDevicesNames()
#     for name in names:
#         print(name, end=" ")
#     print()


# def printDevicesNames():
#     type(devices_manager_1)
#     names = devices_manager_1.getAllDevicesNames()
#     for name in names:
#         print(name, end=" ")
#     print()

# printDevicesNames()