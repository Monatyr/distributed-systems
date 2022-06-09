package sr.ice.server;

import Devices.DevicesManager;
import com.zeroc.Ice.Current;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class DevicesManagerI implements DevicesManager {

    List<String> devicesIds = new ArrayList<>();

    @Override
    public String[] getAllDevicesNames(Current current) {
        System.out.print("[DeviceManager] Get all devices' ids: ");
        devicesIds.forEach(n -> System.out.print(n + " "));
        System.out.println();
        String[] array = new String[devicesIds.size()];
        return devicesIds.toArray(array); // fill the array
    }

    @Override
    public void setDevicesNames(String[] names, Current current) {
        devicesIds.addAll(Arrays.stream(names).toList());
        System.out.print("[DeviceManager] Adding devices' names: ");
        for(int i = 0; i < names.length; i++){
            System.out.print(names[i] + " ");
        }
        System.out.println();
    }
}
