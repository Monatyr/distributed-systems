package sr.ice.server;

import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class PressureSensorI extends SensorI implements Devices.PressureSensor {

    private final Map<String, Float> pressures = new HashMap<String, Float>();

    @Override
    public float getPressure(Current current) {
        makeMeasurements(current);
        float currPressure = pressures.get(current.id.name);
        System.out.println(current.id.category + "/" + current.id.name + " - get pressure: " + currPressure);
        return currPressure;
    }

    @Override
    public void makeMeasurements(Current current) {
        super.makeMeasurements(current);
        float currPressure = (float) ((Math.random() * (1050 - 980)) + 980);
        pressures.put(current.id.name, currPressure);
    }

    @Override
    public Map<String, Float> getAllMeasurements(Current current) {
        makeMeasurements(current);
        Map<String, Float> measurements = super.getAllMeasurements(current);
        measurements.put("pressure [hPa]", pressures.get(current.id.name));
        System.out.println(" pressure [hPa]: " + pressures.get(current.id.name));
        return measurements;
    }
}
