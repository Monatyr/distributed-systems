package sr.ice.server;

import Devices.TimeOfDay;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class SensorI implements Devices.Sensor {

    protected Map<String, Float> temperatures = new HashMap<>();
    protected Map<String, Float> luminousIntensities = new HashMap<>();
//    protected float temperature;
//    protected float luminousIntensity;

    @Override
    public float getTemp(Current current) {
        makeMeasurements(current);
        System.out.println(current.id.name + " - get temperature: " + temperatures.get(current.id.name));
        return temperatures.get(current.id.name);
    }

    @Override
    public float getLuminousIntensity(Current current) {
        makeMeasurements(current);
        System.out.println(current.id.name + " - get luminous intensity: " + luminousIntensities.get(current.id.name));
        return  luminousIntensities.get(current.id.name);
    }

    @Override
    public void makeMeasurements(Current current) {
        System.out.println(current.id.name + " - making measurements");
        temperatures.put(current.id.name, (float) ((Math.random() * (30 - 12)) + 12));
        luminousIntensities.put(current.id.name, (float) (Math.random() * 10000));
    }

    @Override
    public TimeOfDay getTimeOfDay(Current current) {
        int hours = (int) (Math.random() * 24);
        int minutes = (int) (Math.random() * 60);
        int seconds = (int) (Math.random() * 60);
        return new TimeOfDay(hours, minutes, seconds);
    }

    @Override
    public Map<String, Float> getAllMeasurements(Current current) {
        makeMeasurements(current);
        Map<String, Float> measurements = new HashMap<String, Float>();
        measurements.put("temperature", temperatures.get(current.id.name));
        measurements.put("luminousIntensity", luminousIntensities.get(current.id.name));
        System.out.print(current.id.name + " - sending measurements -");
        measurements.forEach((key, value) -> System.out.print(" " + key + ": " + value));
        return measurements;
    }
}
