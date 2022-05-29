
#ifndef DEVICES_ICE
#define DEVICES_ICE

module Devices
{
    exception RangeException
    {
        float number;
        float min;
        float max;
    };

    sequence<string> Names;

    interface DevicesManager
    {
        Names getAllDevicesNames();
        void setDevicesNames(Names names);
    };

    interface Microwave
    {
        void setTemp(float newTemp) throws RangeException;
        float getTemp();
    };
//////////////////////////
    interface Fridge
    {
        void switchLight(bool lightState);
        bool isLightOn();
        void setFridgeTemp(float newTemp) throws RangeException;
        float getFridgeTemp();
    };

    interface FridgeWithFreezer extends Fridge
    {
        void setFreezerTemp(float newTemp) throws RangeException;
        float getFreezerTemp();
    };

//////////////////////////
    dictionary<string, float> measurements;

    struct TimeOfDay
    {
        int hour;
        int minute;
        int second;
    };

    interface Sensor
    {
        float getTemp();
        float getLuminousIntensity();
        void makeMeasurements();
        TimeOfDay getTimeOfDay();
        measurements getAllMeasurements();
    };

    interface PressureSensor extends Sensor
    {
        float getPressure();
    };

    interface HumiditySensor extends Sensor
    {
        float getHumidity();
    };
/////////////////////////
};

#endif