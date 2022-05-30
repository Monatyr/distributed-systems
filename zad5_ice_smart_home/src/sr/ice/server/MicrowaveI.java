package sr.ice.server;

import Devices.RangeException;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class MicrowaveI implements Devices.Microwave {

//    private float temperature;
    private final Map<String, Float> temperatures = new HashMap<String, Float>();
    private final float minTemp = 0;
    private final float maxTemp = 100;

    @Override
    public void setTemp(float newTemp, Current current) throws RangeException {
        if (newTemp > maxTemp || newTemp < minTemp) {
            System.out.println(current.id.name + " - number out of range in setTemp call: " + newTemp);
            throw (new RangeException(newTemp, minTemp, maxTemp));
        }
        System.out.println(current.id.name + " - change microwave temperature to: " + newTemp);
        temperatures.put(current.id.name, newTemp);
//        temperature = newTemp;
    }

    @Override
    public float getTemp(Current current) {
        temperatures.putIfAbsent(current.id.name, (float) 0);
        System.out.println(current.id.name + " - get microwave temperature: " + temperatures.get(current.id.name));
        return temperatures.get(current.id.name);
//        System.out.println(current.id + " - get microwave temperature: " + temperature);
//        return temperature;
    }
}
