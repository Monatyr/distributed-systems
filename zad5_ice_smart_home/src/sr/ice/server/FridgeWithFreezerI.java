package sr.ice.server;

import Devices.FridgeWithFreezer;
import Devices.RangeException;
import com.zeroc.Ice.Current;

import java.util.HashMap;
import java.util.Map;

public class FridgeWithFreezerI extends FridgeI implements FridgeWithFreezer {

    private final Map<String, Float> freezerTemps = new HashMap<String, Float>();
    private final float minFreezerTemp = -10;
    private final float maxFreezerTemp = 5;

    @Override
    public void setFreezerTemp(float newTemp, Current current) throws RangeException {
        if (newTemp > maxFreezerTemp || newTemp < minFreezerTemp) {
            System.out.println(current.id.category + "/" + current.id.name + " - number out of range in setFreezerTemp call: " + newTemp);
            throw (new RangeException(newTemp, minFreezerTemp, maxFreezerTemp));
        }
        System.out.println(current.id.category + "/" + current.id.name + " - change freezer temperature to: " + newTemp);
        freezerTemps.put(current.id.name, newTemp);
    }

    @Override
    public float getFreezerTemp(Current current) {
        if(!freezerTemps.containsKey(current.id.name)) { freezerTemps.put(current.id.name, (float) -5); }
        System.out.println(current.id.category + "/" + current.id.name + " - get freezer temperature: " + freezerTemps.get(current.id.name));
        return freezerTemps.get(current.id.name);
    }
}
