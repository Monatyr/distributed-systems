import sys, Ice
import calculator_ice
import Devices
import re, signal

def signal_handler(signal, frame):
    print("Exit")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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
        elif(command[0] == "fridge"): #LODÓWKI
            if(command[1] == "f1"): #Lodówka 1
                if(command[2] == "switchlight"):
                    fridge_1.switchLight(command[3] == 'true')
                elif(command[2] == "islighton"):
                    print(fridge_1.isLightOn())
                elif(command[2] == "setfridgetemp"):
                    fridge_1.setFridgeTemp(float(command[3]))
                elif(command[2] == "getfridgetemp"):
                    print(fridge_1.getFridgeTemp())
                else:
                    print("Invalid function")
            elif(command[1] == "f2"): #Lodówka 2
                if(command[2] == "switchlight"):
                    fridge_2.switchLight(command[3] == 'true')
                elif(command[2] == "islighton"):
                    print(fridge_2.isLightOn())
                elif(command[2] == "setfridgetemp"):
                    fridge_2.setFridgeTemp(float(command[3]))
                elif(command[2] == "getfridgetemp"):
                    print(fridge_2.getFridgeTemp())
                else:
                    print("Invalid function")
            elif(command[1] == "fwf1"): #Lodówka z zamrażarką
                if(command[2] == "switchlight"):
                    fridge_with_freezer_1.switchLight(command[3] == 'true')
                elif(command[2] == "islighton"):
                    print(fridge_with_freezer_1.isLightOn())
                elif(command[2] == "setfridgetemp"):
                    fridge_with_freezer_1.setFridgeTemp(float(command[3]))
                elif(command[2] == "getfridgetemp"):
                    print(fridge_with_freezer_1.getFridgeTemp())
                elif(command[2] == "setfreezertemp"):
                    fridge_with_freezer_1.setFreezerTemp(float(command[3]))
                elif(command[2] == "getfreezertemp"):
                    print(fridge_with_freezer_1.getFreezreTemp())
                else:
                    print("Invalid function")
        elif(command[0] == "microwave"): #MIKROFALE
            if(command[1] == "m1"):
                if(command[2] == "settemp"):
                    microwave_1.setTemp(float(command[3]))
                if(command[2] == "gettemp"):
                    print(microwave_1.getTemp())
                else:
                    print("Invalid function")
        elif(command[0] == "sensor"):
            if(command[1] == "s1"):
                if(command[2] == "gettemp"):
                    print(sensor_1.getTemp())
                elif(command[2] == "getluminousintensity"):
                    print(sensor_1.getLuminousIntensity())
                elif(command[2] == "makemeasurements"):
                    sensor_1.makeMeasurements()
                elif(command[2] == "gettimeofday"):
                    print(sensor_1.getTimeOfDay())
                elif(command[2] == "getallmeasurements"):
                    print(sensor_1.getAllMeasurements())
                else:
                    print("Invalid funciton")
            if(command[1] == "ps1"):
                if(command[2] == "gettemp"):
                    print(pressure_sensor_1.getTemp())
                elif(command[2] == "getluminousintensity"):
                    print(pressure_sensor_1.getLuminousIntensity())
                elif(command[2] == "makemeasurements"):
                    pressure_sensor_1.makeMeasurements()
                elif(command[2] == "gettimeofday"):
                    print(pressure_sensor_1.getTimeOfDay())
                elif(command[2] == "getallmeasurements"):
                    print(pressure_sensor_1.getAllMeasurements())
                elif(command[2] == "getpressure"):
                    print(pressure_sensor_1.getPressure())
                else:
                    print("Invalid funciton")
            if(command[1] == "ps2"):
                if(command[2] == "gettemp"):
                    print(pressure_sensor_2.getTemp())
                elif(command[2] == "getluminousintensity"):
                    print(pressure_sensor_2.getLuminousIntensity())
                elif(command[2] == "makemeasurements"):
                    pressure_sensor_2.makeMeasurements()
                elif(command[2] == "gettimeofday"):
                    print(pressure_sensor_2.getTimeOfDay())
                elif(command[2] == "getallmeasurements"):
                    print(pressure_sensor_2.getAllMeasurements())
                elif(command[2] == "getpressure"):
                    print(pressure_sensor_2.getPressure())
                else:
                    print("Invalid funciton")
            if(command[1] == "hs1"):
                if(command[2] == "gettemp"):
                    print(humidity_sensor_1.getTemp())
                elif(command[2] == "getluminousintensity"):
                    print(humidity_sensor_1.getLuminousIntensity())
                elif(command[2] == "makemeasurements"):
                    humidity_sensor_1.makeMeasurements()
                elif(command[2] == "gettimeofday"):
                    print(humidity_sensor_1.getTimeOfDay())
                elif(command[2] == "getallmeasurements"):
                    print(humidity_sensor_1.getAllMeasurements())
                elif(command[2] == "getpressure"):
                    print(humidity_sensor_1.getPressure())
                elif(command[2] == "gethumidity"):
                    print(humidity_sensor_1.getHumidity())
                else:
                    print("Invalid funciton")