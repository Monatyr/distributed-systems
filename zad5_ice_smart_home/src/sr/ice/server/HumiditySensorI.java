package sr.ice.server;

import Devices.HumiditySensor;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class HumiditySensorI extends SensorI implements HumiditySensor {

//    private float humidity;
    private final Map<String, Float> humidities = new HashMap<String, Float>();

    @Override
    public float getHumidity(Current current) {
        makeMeasurements(current);
        System.out.println(current.id.name + " - get humidity: " + humidities.get(current.id.name) + "%");
        return humidities.get(current.id.name);
    }

    @Override
    public void makeMeasurements(Current current) {
        super.makeMeasurements(current);
        humidities.put(current.id.name, (float) ((Math.random() * 100)));
    }

    @Override
    public Map<String, Float> getAllMeasurements(Current current) {
        makeMeasurements(current);
        Map<String, Float> measurements = super.getAllMeasurements(current);
        measurements.put("humidity", humidities.get(current.id.name));
        System.out.print(" humidity: " + humidities.get(current.id.name) + "%");
        return measurements;
    }
}
